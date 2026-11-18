#!/usr/bin/env python3
"""Ingest and dream status, for the scheduled runner and for maintainer mode.

Run from anywhere (paths resolve from this file):
    python3 .therapy/scripts/scheduled/status.py --pending       # prints N
    python3 .therapy/scripts/scheduled/status.py --longform-due  # exit 0 = due
    python3 .therapy/scripts/scheduled/status.py [--fetch]       # health lines

--pending prints how many session notes no ingest or longform dream has
covered (startup.unprocessed_sessions()). The ingest itself caps its range.
--longform-due exits 0 when startup.dream_state() says due or overdue, 1
otherwise (also when there is no merged longform yet: the first one is run by
hand), and prints the Dream: line.
With no flag it prints maintainer-mode health lines: the last ingest, notes
waiting and how long, failed ingest branches and open dream branches on
origin. It reads `git branch -r` as it is; --fetch runs `git fetch --prune
origin` first. Read-only otherwise: it never edits a file, and it prints
stems, dates and branch names, never note content.

Works without a server too: with ingests run by hand, the health lines still
say how many notes wait and whether a failed ingest branch is open. Set
SCHEDULED = False below so the "over 24 h" warning talks about a by-hand
ingest instead of a server that may be down.
"""

import argparse
import datetime as dt
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import startup  # noqa: E402

ROOT = startup.ROOT
SCHEDULED = True           # False when ingests only run by hand (INSTALL.md, part 2)
WAIT_WARN_HOURS = 24
INGEST_STOP_BRANCHES = 2


def git(*args):
    """stdout of a git command in the install, or None if it failed."""
    try:
        p = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return None
    return p.stdout if p.returncode == 0 else None


def remote_branches(prefix):
    """Names under origin/<prefix> from `git branch -r`, without "origin/"."""
    out = git("branch", "-r", "--format=%(refname:short)") or ""
    names = [l.strip() for l in out.splitlines()]
    return sorted(n[len("origin/"):] for n in names if n.startswith(f"origin/{prefix}"))


def hours_ago(ts):
    return (time.time() - ts) / 3600


def fmt_age(hours):
    if hours < 1:
        return f"{int(hours * 60)} min ago"
    if hours < 48:
        return f"{hours:.0f} h ago"
    return f"{hours / 24:.0f} days ago"


def last_ingest_time():
    """Commit time of the newest "Ingest ..." commit on HEAD or origin/main, or None."""
    refs = ["HEAD"] + (["origin/main"] if git("rev-parse", "--verify", "-q", "origin/main") else [])
    out = git("log", "-1", "--format=%ct", "--grep=^Ingest ", *refs)
    return int(out.strip()) if out and out.strip() else None


def note_time(name):
    """When a note arrived: the commit that added it, else its mtime."""
    out = git("log", "--diff-filter=A", "-1", "--format=%ct", "--", f"sessions/{name}")
    if out and out.strip():
        return int(out.strip())
    try:
        return int((ROOT / "sessions" / name).stat().st_mtime)
    except OSError:
        return None


def health():
    lines = []
    ingest = startup.last_ingest()
    if ingest:
        ts = last_ingest_time()
        when = fmt_age(hours_ago(ts)) if ts else f"dated {ingest[0][:10]}, commit not found"
        lines.append(f"Last ingest: {ingest[0]} ({when}), covered through {ingest[1]}")
    else:
        lines.append("Last ingest: none yet")

    waiting = startup.unprocessed_sessions()
    if waiting:
        ts = note_time(waiting[0])
        age = hours_ago(ts) if ts else None
        lines.append(f"Notes waiting for an ingest: {len(waiting)} ({waiting[0][:-3]} → {waiting[-1][:-3]}); "
                     f"oldest arrived {fmt_age(age) if age is not None else 'at an unknown time'}")
        if age is not None and age > WAIT_WARN_HOURS:
            why = ("the dream server is likely down, or its timer is off" if SCHEDULED
                   else "offer an ingest")
            lines.append(f"WARNING: {waiting[0][:-3]} has waited over {WAIT_WARN_HOURS} h; {why}")
    else:
        lines.append("Notes waiting for an ingest: none")

    failed = remote_branches("ingest/")
    if failed:
        stopped = len(failed) >= INGEST_STOP_BRANCHES
        lines.append(f"Failed ingest branches on origin: {len(failed)} ({', '.join(failed)})"
                     + ("; ingest STOPPED until they're reviewed and deleted" if stopped else ""))
    else:
        lines.append("Failed ingest branches on origin: none")

    dreams = remote_branches("dream/")
    if dreams:
        lines.append(f"Open dream branches on origin: {', '.join(dreams)} "
                     "(longform/audit waiting for review; ingest paused)")
    else:
        lines.append("Open dream branches on origin: none")
    return lines


def main(argv=None):
    ap = argparse.ArgumentParser(description="Ingest and dream status (read-only).")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--pending", action="store_true", help="print the number of notes not yet ingested")
    mode.add_argument("--longform-due", action="store_true", help="exit 0 if a longform dream is due")
    ap.add_argument("--fetch", action="store_true", help="git fetch --prune origin first")
    args = ap.parse_args(argv)

    if args.fetch and git("fetch", "--prune", "--quiet", "origin") is None:
        print("status.py: git fetch failed; using the remote branches as last fetched", file=sys.stderr)

    if args.pending:
        print(len(startup.unprocessed_sessions()))
        return 0
    if args.longform_due:
        today = dt.date.today()
        bytes_ = startup.reading_list(today)["startup_bytes"]
        print(startup.dream_status(today, bytes_))
        return 0 if startup.dream_state(today, bytes_)[0] in ("due", "overdue") else 1
    for line in health():
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
