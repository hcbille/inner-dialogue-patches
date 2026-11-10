#!/usr/bin/env python3
"""Pick the context files the next audit dream should check, and the session
notes to read for each (.therapy/protocols/dream-audit.md).

Install: copy to .therapy/scripts/audit_next.py. It imports the install's own
.therapy/scripts/startup.py and needs the dreaming patch's part 3 in it
(session_files() and last_dream() from startup-dream-additions.py), plus
context_entries() and parse_date() from the opus-5-5-rebaseline script.

Run from the install's root:
    python3 .therapy/scripts/audit_next.py            # the next run's plan
    python3 .therapy/scripts/audit_next.py --status   # coverage so far
    python3 .therapy/scripts/audit_next.py --file context/people/some-name.md

Read-only: it never edits a file. The audit dream records its progress in
dreams/audit.md, one line per file:
    - context/people/some-name.md · through 2026-11-09b · last 2026-11-10 · complete
"complete" means the audit has read every note on the file's list, up to the
last merged regular dream. Newer sessions are the regular dream's job, so an
audit never reads past that point.

Two modes, chosen per file:
  full   every note that mentions the file fits in one run's per-file budget,
         so the audit rereads all of them (accuracy and completeness).
  cited  too many notes mention it, so the audit reads the notes the file
         itself cites (its dated claims) and checks each claim against them
         (accuracy). Completeness for big files is left to regular dreams.

Order:
  1. Core/Active files whose summary is printed at startup
  2. Core/Active files read in full at startup
  3. other people, concept and place files
  4. event files
Within a tier: never audited first, then the oldest "last" date, then the
largest file. A file whose notes exceed the per-file budget is audited in
chunks, oldest notes first, across several runs ("partial").

A note "mentions" a file when it links it ([[stem]] or the stem.md path), or
names its H1 title or a frontmatter alias as a whole word (aliases of three
letters or fewer must match case too).
"""

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import startup  # noqa: E402

SUMMARY_RE = re.compile(r"<!-- summary -->\s*\n(.*?)\n\s*<!-- /summary -->", re.S)


def has_summary(rel):
    """True if the file has a summary block (the arc-review/startup-weight convention)."""
    try:
        return bool(SUMMARY_RE.search((startup.ROOT / rel).read_text(encoding="utf-8")))
    except OSError:
        return False

ROOT = startup.ROOT
FOLDERS = ["people", "concepts", "places", "events"]
FILES_PER_RUN = 5
FILE_BUDGET = 150_000      # session-note bytes read for one file in one run
RUN_BUDGET = 450_000       # session-note bytes read in one run, all files
AUDIT_LINE_RE = re.compile(
    r"^- (context/\S+\.md) · through (\S+) · last (\d{4}-\d{2}-\d{2}) · (complete|partial)(?: · (full|cited))?")
CITE_RE = re.compile(r"(?<![\d-])(?:(20\d{2})-)?(\d{2})-(\d{2})([a-z]?)(?!\d)")


def coverage():
    """{path: (through stem, last date, state)} from dreams/audit.md."""
    out = {}
    f = ROOT / "dreams/audit.md"
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            m = AUDIT_LINE_RE.match(line)
            if m:
                out[m.group(1)] = (m.group(2), startup.parse_date(m.group(3)), m.group(4), m.group(5))
    return out


def terms_for(path):
    """Regexes that count as a mention of this context file."""
    text = (ROOT / path).read_text(encoding="utf-8")
    stem = Path(path).stem
    pats = [re.compile(r"\[\[" + re.escape(stem) + r"(\||\]|#)", re.I),
            re.compile(re.escape(stem) + r"\.md", re.I)]
    names = []
    fm = re.match(r"^---\n(.*?)\n---", text, re.S)
    if fm:
        block = re.search(r"^aliases:\s*\n((?:\s+- .*\n?)+)", fm.group(1) + "\n", re.M)
        if block:
            names += [a.strip().strip('"\'') for a in re.findall(r"- (.*)", block.group(1))]
    h1 = re.search(r"^# (.+)$", text, re.M)
    if h1 and Path(path).parent.name != "events":
        names.append(h1.group(1).strip())
    for n in names:
        if not n or len(n) > 60:
            continue
        flags = 0 if len(n) <= 3 else re.I
        pats.append(re.compile(r"(?<!\w)" + re.escape(n) + r"(?!\w)", flags))
    return pats


def notes_mentioning(path, after, upto):
    """Session notes (stem order) after `after` and up to `upto` that mention the file."""
    pats = terms_for(path)
    found = []
    for _, name in startup.session_files():
        stem = name[:-3]
        if (after and stem <= after) or stem > upto:
            continue
        text = (ROOT / "sessions" / name).read_text(encoding="utf-8")
        if any(p.search(text) for p in pats):
            found.append((stem, len(text.encode())))
    return found


def notes_cited(path, after, upto):
    """Session notes the file cites by date (2026-10-19, 10-19, 10-07b), in stem order.

    A short date with no year is read as the install's year. A date with a suffix
    (07-02d) means that note. A bare date (07-02), or a suffix with no note of
    its own, means every note from that day (07-02, 07-02b, 07-02c, 07-02d):
    files often cite the day when the evidence is in a lettered note."""
    text = (ROOT / path).read_text(encoding="utf-8")
    sizes = {name[:-3]: (ROOT / "sessions" / name).stat().st_size for _, name in startup.session_files()}
    by_day = {}
    for st in sizes:
        by_day.setdefault(st[:10], []).append(st)
    year = min(sizes)[:4] if sizes else "2026"
    found = set()
    for m in CITE_RE.finditer(text):
        day = f"{m.group(1) or year}-{m.group(2)}-{m.group(3)}"
        stem = day + m.group(4)
        if m.group(4) and stem in sizes:
            found.add(stem)
        else:
            found.update(by_day.get(day, []))
    return [(st, sizes[st]) for st in sorted(found)
            if not (after and st <= after) and st <= upto]


def reading_list(path, after, upto, mode, file_budget):
    """(mode, notes) for this file. A file keeps the mode its audit started in."""
    if mode == "cited":
        return "cited", notes_cited(path, after, upto)
    mentions = notes_mentioning(path, after, upto)
    if mode == "full" or (mentions and after is None and sum(b for _, b in mentions) <= file_budget):
        return "full", mentions
    # too many mentions, or none found by name (then the file's own dates are the only trail)
    return "cited", notes_cited(path, after, upto)


def candidates(today):
    load, _ = startup.context_entries(today)
    out = []
    for folder in FOLDERS:
        for f in sorted((ROOT / "context" / folder).glob("*.md")):
            rel = str(f.relative_to(ROOT))
            if folder == "events":
                tier = 4
            elif rel in load:
                tier = 1 if has_summary(rel) else 2
            else:
                tier = 3
            out.append((tier, rel, f.stat().st_size))
    return out


def plan(today, files_per_run, file_budget, run_budget, only=None):
    dream = startup.last_dream()
    if dream is None:
        return None, "No merged regular dream yet; run a regular dream first."
    upto = dream[1]
    cov = coverage()
    rows = []
    for tier, rel, size in candidates(today):
        if only and rel != only:
            continue
        through, last, state, mode = cov.get(rel, (None, None, None, None))
        if state == "complete" and not only:
            continue
        rows.append((tier, last is not None, last or dt.date.min, -size, rel, size, through, mode))
    rows.sort()
    picked, total = [], 0
    for tier, _, _, _, rel, size, through, mode in rows:
        mode, notes = reading_list(rel, through, upto, mode, file_budget)
        chunk, used = [], 0
        for stem, b in notes:
            if chunk and used + b > file_budget:
                break
            chunk.append(stem)
            used += b
        if picked and total + used > run_budget:
            continue  # doesn't fit this run; a smaller file might
        finishes = len(chunk) == len(notes)
        picked.append({"path": rel, "tier": tier, "size": size, "from": through, "mode": mode,
                       "notes": chunk, "bytes": used, "left": len(notes) - len(chunk),
                       "through": chunk[-1] if chunk else upto, "finishes": finishes})
        total += used
        if len(picked) >= files_per_run:
            break
    return {"upto": upto, "files": picked, "total": total}, None


def print_status(today):
    cov = coverage()
    cands = candidates(today)
    by_tier = {}
    for tier, rel, _ in cands:
        state = cov.get(rel, (None, None, "never", None))[2]
        by_tier.setdefault(tier, {}).setdefault(state, 0)
        by_tier[tier][state] += 1
    names = {1: "startup summaries", 2: "startup, read in full", 3: "people/concepts/places", 4: "events"}
    print(f"Audit coverage, {today.isoformat()} ({len(cands)} context files)")
    for tier in sorted(by_tier):
        parts = ", ".join(f"{n} {s}" for s, n in sorted(by_tier[tier].items()))
        print(f"- Tier {tier} ({names[tier]}): {parts}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--file")
    ap.add_argument("--files", type=int, default=FILES_PER_RUN)
    args = ap.parse_args()
    today = dt.date.today()
    if args.status:
        print_status(today)
        return 0
    result, err = plan(today, args.files, FILE_BUDGET, RUN_BUDGET, only=args.file)
    if err:
        print(err)
        return 1
    if not result["files"]:
        print(f"Nothing to audit: every file is complete through {result['upto']}.")
        return 0
    print(f"Audit plan: {len(result['files'])} files, {result['total']:,} bytes of session notes "
          f"(notes up to {result['upto']}, the last merged regular dream)")
    for f in result["files"]:
        start = f"after {f['from']}" if f["from"] else "from the start"
        end = "finishes it" if f["finishes"] else f"{f['left']} more notes in later runs"
        print(f"\n== {f['path']} (tier {f['tier']}, {f['size']:,} bytes; mode {f['mode']}; "
              f"{len(f['notes'])} notes {start}, {f['bytes']:,} bytes; {end})")
        print(f"   record: - {f['path']} · through {f['through']} · last {today.isoformat()} · "
              f"{'complete' if f['finishes'] else 'partial'} · {f['mode']}")
        for stem in f["notes"]:
            print(f"   sessions/{stem}.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
