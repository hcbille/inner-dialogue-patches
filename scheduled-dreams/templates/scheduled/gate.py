#!/usr/bin/env python3
"""Gate for an ingest: decide whether HEAD may land on main unreviewed.

The scheduled runner (run.sh, next to this file) runs it on the ingest/<id>
branch the dreamer agent committed, before landing it on main
(.therapy/protocols/dream-ingest.md). An ingest run by hand in maintainer
mode runs it too, and it can be run on a failed ingest branch to see why it
didn't land.

Run from anywhere inside the install:
    python3 .therapy/scripts/scheduled/gate.py --base origin/main

Read-only. Compares HEAD with --base and checks:
  1. exactly one non-merge commit on top of base, subject "Ingest <id>: ...";
  2. changed paths only context/** (minus PROTECTED), sessions/index.md
     (added lines only), dreams/ingests/**, dreams/flags.md; no file deleted,
     and no rename except context/events/pending-<slug>.md ->
     context/events/YYYY-MM-DD-<slug>.md (an ingest setting a confirmed date);
  3. no added line contains a name in NEVER_ADD (any case), in any file;
  4. per file, lines removed minus lines added is at most 3 (a renamed
     file against its old path);
  5. every line under "How to hold it" in a summary block in base still
     appears verbatim in HEAD's version of that file;
  6. evidence_check.py --commit HEAD passes (base patch);
  7. a report dreams/ingests/<id>.md is added and dreams/ingests/index.md
     gains exactly one entry line, for that same <id>, saying merged.

Output names files and line numbers only, never the text of a line, so it can
go into a log. Exit 0 pass, 1 fail, 2 usage error (bad ref, not an install).
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

# ---- Set these for this install (INSTALL.md, part 2) ------------------------
# Files an ingest may never change: the file of each boundary subject
# (dream.md rule 9) and any working document the client has asked dreams to
# leave alone. Paths relative to the install root.
PROTECTED = set()
# Names an ingest may never add, lowercase: the boundary subjects' names and
# the aliases the client uses for them. Leave empty if there are none.
NEVER_ADD = []
# ------------------------------------------------------------------------------

MAX_NET_REMOVED = 3
ID_RE = r"\d{4}-\d{2}-\d{2}(?:-\d+)?"
REPORT_RE = re.compile(rf"^dreams/ingests/({ID_RE})\.md$")
INDEX = "dreams/ingests/index.md"
# Same shape the startup script's INGEST_LINE_RE reads.
ENTRY_RE = re.compile(
    rf"^- ({ID_RE}) · covered (\d{{4}}-\d{{2}}-\d{{2}}[a-z]?) → (\d{{4}}-\d{{2}}-\d{{2}}[a-z]?)"
    r".*outcome: ([a-z ]+?)\s*(?:·|$)")
SUBJECT_RE = re.compile(rf"^Ingest ({ID_RE}): \S")
PENDING_EVENT_RE = re.compile(r"^context/events/pending-[^/]+\.md$")
DATED_EVENT_RE = re.compile(r"^context/events/\d{4}-\d{2}-\d{2}-[^/]+\.md$")
HOLD_RE = re.compile(r"^\s*[-*]?\s*\**how to hold it\b", re.I)
TOP_ITEM_RE = re.compile(r"^(?:[-*] |\*\*|#)")


class UsageError(Exception):
    pass


def git(*args, check=True):
    r = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True)
    if check and r.returncode != 0:
        raise UsageError(f"git {' '.join(args)} failed: {r.stderr.strip()}")
    return r.stdout


def allowed_path(path):
    if path in PROTECTED:
        return False
    return (path.startswith("context/") or path == "sessions/index.md"
            or path.startswith("dreams/ingests/") or path == "dreams/flags.md")


def file_at(rev, path):
    r = subprocess.run(["git", "-C", str(ROOT), "show", f"{rev}:{path}"],
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def hold_lines(text):
    """(line number, line) for every line under "How to hold it" inside a
    summary block: the line itself and its continuation lines, up to the
    next top-level item or the end of the block."""
    out, in_block, holding = [], False, False
    for n, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if s == "<!-- summary -->":
            in_block, holding = True, False
            continue
        if s == "<!-- /summary -->":
            in_block = holding = False
            continue
        if not in_block:
            continue
        if HOLD_RE.match(line):
            holding = True
        elif holding and (TOP_ITEM_RE.match(line) or not s):
            holding = False
        if holding and s:
            out.append((n, line.rstrip()))
    return out


def allowed_rename(old, new):
    """An ingest setting a confirmed date: events/pending-<slug>.md ->
    events/YYYY-MM-DD-<anything>.md, staying inside context/events/."""
    return bool(PENDING_EVENT_RE.match(old) and DATED_EVENT_RE.match(new))


def added_removed(base, head, path, old=None):
    """Added and removed lines of one file's diff, without context. For a
    rename, the diff is between the old path in base and the new one in head."""
    if old:
        out = git("diff", "-U0", f"{base}:{old}", f"{head}:{path}")
    else:
        out = git("diff", "--no-renames", "-U0", base, head, "--", path)
    added, removed = [], []
    for line in out.splitlines():
        if line.startswith(("+++", "---")):
            continue
        if line.startswith("+"):
            added.append(line[1:])
        elif line.startswith("-"):
            removed.append(line[1:])
    return added, removed


def check(base):
    fails = []
    try:
        base_sha = git("rev-parse", "--verify", f"{base}^{{commit}}").strip()
        head_sha = git("rev-parse", "--verify", "HEAD^{commit}").strip()
    except UsageError as e:
        raise UsageError(f"can't resolve --base or HEAD ({e})")

    # 1. One commit on top of base.
    if subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor",
                       base_sha, head_sha]).returncode != 0:
        fails.append(f"HEAD is not on top of {base}: base isn't an ancestor of HEAD")
    count = int(git("rev-list", "--count", f"{base_sha}..{head_sha}").strip() or 0)
    if count != 1:
        fails.append(f"{count} commits on top of {base}; exactly one expected")
    parents = git("rev-list", "--parents", "-n", "1", head_sha).split()[1:]
    if len(parents) != 1:
        fails.append(f"HEAD has {len(parents)} parents; a single non-merge commit expected")
    elif count == 1 and parents[0] != base_sha:
        fails.append(f"HEAD's parent is not {base}")
    subject = git("log", "-1", "--format=%s", head_sha).strip()
    m = SUBJECT_RE.match(subject)
    subject_id = m.group(1) if m else None
    if not subject_id:
        fails.append('commit subject is not "Ingest <id>: <summary>"')

    if git("status", "--porcelain", "--untracked-files=no").strip():
        fails.append("working tree has uncommitted changes to tracked files; "
                     "the evidence check reads the working tree, so commit or discard them first")

    # 2. Paths.
    # (status, path, old path for a rename). Renames are detected so the one
    # allowed kind (pending event -> dated event) can pass; any other rename,
    # and any delete, fails. Copies are treated as plain additions.
    changes = []
    for line in git("diff", "-M", "--name-status", base_sha, head_sha).splitlines():
        fields = line.split("\t")
        status = fields[0][:1]
        if status == "R":
            changes.append(("R", fields[2], fields[1]))
        elif status == "C":
            changes.append(("A", fields[2], None))
        else:
            changes.append((status, fields[1], None))
    if not changes:
        fails.append("the commit changes no files")
    for status, path, old in changes:
        if status == "D":
            fails.append(f"{path}: deleted")
        elif status == "R" and not allowed_rename(old, path):
            fails.append(f"{old} -> {path}: renamed; only context/events/pending-<slug>.md -> "
                         "context/events/YYYY-MM-DD-<slug>.md is allowed")
        elif not allowed_path(path):
            why = "protected file" if path in PROTECTED else "outside the paths an ingest may change"
            fails.append(f"{path}: {why}")

    # 3, 4, and sessions/index.md added-only. A rename is measured against its old path.
    for status, path, old in changes:
        if status == "D":
            continue
        if old:
            stat = git("diff", "--numstat", f"{base_sha}:{old}", f"{head_sha}:{path}")
        else:
            stat = git("diff", "--no-renames", "--numstat", base_sha, head_sha, "--", path)
        if stat.startswith("-\t-\t"):
            fails.append(f"{path}: binary change")
            continue
        added, removed = added_removed(base_sha, head_sha, path, old)
        for i, text in enumerate(added, 1):
            low = text.lower()
            if any(name and name in low for name in NEVER_ADD):
                fails.append(f"{path}: added line {i} of the diff contains a name ingests may never add")
        if path == "sessions/index.md" and removed:
            fails.append(f"{path}: {len(removed)} line(s) removed or changed; only added lines are allowed")
        net = len(removed) - len(added)
        if net > MAX_NET_REMOVED:
            fails.append(f"{path}: net {net} lines removed (limit {MAX_NET_REMOVED})")

    # 5. How to hold it lines survive (a renamed file is compared with its old path).
    for status, path, old in changes:
        if status not in ("M", "R") or not path.endswith(".md"):
            continue
        before = file_at(base_sha, old or path)
        after = file_at(head_sha, path)
        if before is None or after is None:
            continue
        after_lines = {l.rstrip() for l in after.splitlines()}
        for n, line in hold_lines(before):
            if line not in after_lines:
                fails.append(f"{path}: \"How to hold it\" line {n} of the base version "
                             "is no longer there word for word")

    # 6. Evidence check (base patch). Skipped with a failure if it's missing,
    # since an ingest writes quotes nobody reviews.
    checker = ROOT / ".therapy/scripts/evidence_check.py"
    if not checker.exists():
        fails.append(".therapy/scripts/evidence_check.py is missing (base patch); "
                     "ingests can't land without it")
    else:
        ev = subprocess.run([sys.executable, str(checker), "--commit", head_sha],
                            cwd=str(ROOT), capture_output=True, text=True)
        if ev.returncode != 0:
            n = sum(1 for l in ev.stdout.splitlines() if l.startswith("- "))
            fails.append(f"evidence_check.py failed: {n} added quote(s) not found in any session note "
                         "(run it with --commit HEAD to see them)")

    # 7. Report and index line.
    reports = [REPORT_RE.match(p).group(1) for s, p, _ in changes if s == "A" and REPORT_RE.match(p)]
    index_status = next((s for s, p, _ in changes if p == INDEX), None)
    entry_id = None
    if index_status is None:
        fails.append(f"{INDEX}: no line added")
    else:
        added, removed = added_removed(base_sha, head_sha, INDEX)
        entries = [l for l in added if l.startswith("- ")]
        others = [l for l in added if not l.startswith("- ") and l.strip()]
        if len(entries) != 1:
            fails.append(f"{INDEX}: {len(entries)} entry lines added; exactly one expected")
        if index_status != "A" and (others or len(added) != 1):
            fails.append(f"{INDEX}: {len(added)} lines added; exactly one expected")
        if removed:
            fails.append(f"{INDEX}: {len(removed)} existing line(s) removed or changed")
        if len(entries) == 1:
            em = ENTRY_RE.match(entries[0])
            if not em:
                fails.append(f"{INDEX}: the added line doesn't match "
                             "\"- <id> · covered <first> → <last> (N sessions) · outcome: merged · ...\"")
            else:
                entry_id = em.group(1)
                if not em.group(4).strip().startswith("merged"):
                    fails.append(f"{INDEX}: the added line's outcome is not merged")
    if entry_id:
        if entry_id not in reports:
            fails.append(f"dreams/ingests/{entry_id}.md: report not added in this commit")
        if subject_id and subject_id != entry_id:
            fails.append(f"commit subject names ingest {subject_id} but the index line names {entry_id}")
    elif not reports:
        fails.append("no report dreams/ingests/<id>.md added")
    extra = [r for r in reports if r != entry_id]
    if entry_id and extra:
        fails.append(f"{len(extra)} extra report(s) added besides dreams/ingests/{entry_id}.md")

    return fails, entry_id


def main():
    ap = argparse.ArgumentParser(description="Gate an ingest commit.")
    ap.add_argument("--base", required=True, help="ref the ingest commit should sit on, e.g. origin/main")
    args = ap.parse_args()
    if not (ROOT / ".therapy").is_dir():
        print(f"Gate: error: {ROOT} doesn't look like the install root", file=sys.stderr)
        return 2
    try:
        fails, entry_id = check(args.base)
    except UsageError as e:
        print(f"Gate: error: {e}", file=sys.stderr)
        return 2
    if not fails:
        print(f"Gate: pass (ingest {entry_id})")
        return 0
    print(f"Gate: fail, {len(fails)} reason(s):")
    for f in fails:
        print(f"- {f}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
