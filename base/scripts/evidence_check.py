#!/usr/bin/env python3
"""Check that quotes written to context files are backed by a session note.

Session end (.therapy/protocols/session-end.md, the save step) runs this before
the commit. Audits of a long-running install kept finding quotation marks around
words no session note has: a paraphrase, the assistant's own line, or a detail
from a pasted chat. Every quote added to profile.md or context/ must appear word
for word in sessions/ (or in a text file under attachments/, if the install keeps
one), so a later review can trace it.

Run from the install root:
    python3 .therapy/scripts/evidence_check.py               # uncommitted changes
    python3 .therapy/scripts/evidence_check.py --commit SHA  # one past commit

Read-only. It reads the added lines of the git diff, pulls out every
double-quoted passage of three words or more, and looks for it in the evidence.
A quote cut with "..." or "…" counts as found when each piece of three words or
more is found. Matching ignores case, punctuation, markdown emphasis and
[[link]] syntax. Exit code 1 when anything is missing.

Not checked: sessions/ itself and context/mentions.md. Add any file the client
keeps as their own writing (not a record of sessions) to SKIP. Facts written
without quotation marks can't be checked this way; the session note's evidence
rule covers them.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKIP = {"context/mentions.md"}
QUOTE_RE = re.compile(r'"([^"\n]{3,}?)"|“([^”\n]{3,}?)”')
PIECE_RE = re.compile(r"\.\.\.|…")
MIN_WORDS = 3


def norm(text):
    text = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", text)  # [[a|b]] -> b
    text = text.replace("’", "'").replace("‘", "'")
    text = re.sub(r"[*_`]", "", text)
    text = re.sub(r"[^\w']+", " ", text.lower())
    return " " + text.strip() + " "


def evidence():
    parts = []
    for folder, pattern in (("sessions", "*.md"), ("attachments", "**/*.md"), ("attachments", "**/*.txt")):
        for f in (ROOT / folder).glob(pattern):
            parts.append(norm(f.read_text(encoding="utf-8", errors="ignore")))
    return "".join(parts)


def git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True)


def added_lines(commit):
    args = ["show", "--format=", "-U0", commit] if commit else ["diff", "HEAD", "-U0"]
    out = git(*args, "--", "profile.md", "context").stdout
    path = None
    for line in out.splitlines():
        if line.startswith("+++ "):
            path = line[6:] if line.startswith("+++ b/") else None
        elif line.startswith("+") and path and path not in SKIP:
            yield path, line[1:]
    if not commit:  # new files git diff doesn't show until they're added
        new = git("ls-files", "--others", "--exclude-standard", "--", "profile.md", "context").stdout
        for path in new.split():
            if path not in SKIP:
                for line in (ROOT / path).read_text(encoding="utf-8").splitlines():
                    yield path, line


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--commit")
    args = ap.parse_args()
    if git("rev-parse", "--git-dir").returncode != 0:
        print("Evidence check: not a git repo, so nothing to compare. Check your diff by hand.")
        return 0
    ev = evidence()
    missing, checked = [], 0
    for path, line in added_lines(args.commit):
        for m in QUOTE_RE.finditer(line):
            quote = m.group(1) or m.group(2)
            pieces = [p for p in PIECE_RE.split(quote) if len(norm(p).split()) >= MIN_WORDS]
            if not pieces:
                continue
            checked += 1
            if not all(norm(p) in ev for p in pieces):
                missing.append((path, quote))
    if not missing:
        print(f"Evidence check: {checked} quotes added, all found in sessions/.")
        return 0
    print(f"Evidence check: {len(missing)} of {checked} added quotes aren't in any session note.")
    print("For each: copy the exact words into today's note, take the quotation marks off and")
    print("paraphrase, or credit them to the assistant if they were its own (session-end.md, Step 2).")
    for path, quote in missing:
        print(f'- {path}: "{quote}"')
    return 1


if __name__ == "__main__":
    sys.exit(main())
