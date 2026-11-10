#!/usr/bin/env python3
"""Print the session-start reading list and the date-driven flags.

Install at .therapy/scripts/startup.py and run from the install root:
    python3 .therapy/scripts/startup.py

The reading list is what CLAUDE.md's session startup asks for, resolved
against today's files, so nothing depends on enumerating it by hand:
fixed framework files, every memory file, the context index files, every
Core or unexpired Active context file, near-term event files, the
sessions index, and the recent session notes. The thread registry's open
therapeutic and shelved sections are printed after the list instead of
the whole file being listed (THREAD_SECTIONS). Files marked optional are
skipped quietly when this install doesn't have them. Read-only: it never
edits a file.

ADAPT: edit the lists below to match this install's actual files.
"""

import datetime as dt
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ACTIVE_DAYS = 7
EVENT_AHEAD_DAYS = 2
ARC_DUE_DAYS = 14

# Read in this order. Required files are reported as MISSING if absent.
FIXED_HEAD = [
    ".therapy/safety-protocol.md",
    ".therapy/persona.md",
    "profile.md",
    "arc.md",
    ".therapy/profile-protocol.md",
    ".therapy/modalities-index.md",
    ".therapy/session-structure.md",
]
CONTEXT_TRIO = ["context/index.md", "context/mentions.md"]
# Skipped silently when absent (not every install has every extension).
OPTIONAL = {
    "arc.md",
    ".therapy/profile-protocol.md",
    ".therapy/modalities-index.md",
    "context/mentions.md",
    "context/threads.md",
}
# The thread registry (thread-registry patch) isn't read in full at startup:
# only these sections are printed, because the greeting and the standing-
# threads check use only them. The schema, logistical and archived entries
# are read at session end. If a section is missing, the whole file is listed.
THREADS = "context/threads.md"
THREAD_SECTIONS = ("Open — Therapeutic", "Shelved")

DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")
ENTRY_PATH_RE = re.compile(r"`([^`]+\.md)`")
STATUS_RE = re.compile(r"\*\*(Core|Active)(?: \((\d{4}-\d{2}-\d{2})\))?\*\*")
SESSION_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})[a-z]?\.md$")


def parse_date(s):
    return dt.date.fromisoformat(s)


def context_entries(today):
    """Return (load, expired) lists of context paths from context/index.md."""
    load, expired = [], []
    index = ROOT / "context/index.md"
    if not index.exists():
        return load, expired
    for line in index.read_text(encoding="utf-8").splitlines():
        if not line.startswith("- "):
            continue
        status = STATUS_RE.search(line)
        path = ENTRY_PATH_RE.search(line)
        if not status or not path:
            continue
        rel = "context/" + path.group(1)
        kind, stamp = status.groups()
        if kind == "Active" and stamp and (today - parse_date(stamp)).days > ACTIVE_DAYS:
            expired.append(f"{rel} (Active {stamp})")
        elif rel not in load:
            load.append(rel)
    return load, expired


def near_events(today):
    """Event files dated yesterday through today+2, plus undated pending ones."""
    near, pending = [], []
    events = ROOT / "context/events"
    if not events.is_dir():
        return near, pending
    for f in sorted(events.glob("*.md")):
        if f.name.startswith("pending-"):
            pending.append(f"context/events/{f.name}")
            continue
        m = re.match(r"(\d{4}-\d{2}-\d{2})-", f.name)
        if not m:
            continue
        delta = (parse_date(m.group(1)) - today).days
        if -1 <= delta <= EVENT_AHEAD_DAYS:
            when = {-1: "yesterday", 0: "today", 1: "tomorrow"}.get(delta, f"in {delta} days")
            near.append((f"context/events/{f.name}", when))
    return near, pending


def recent_sessions(today):
    """Sessions dated today or yesterday; if fewer than two, the two newest."""
    files = []
    for f in (ROOT / "sessions").iterdir():
        m = SESSION_RE.match(f.name)
        if m:
            files.append((m.group(1), f.name))
    files.sort()
    recent = [name for day, name in files if (today - parse_date(day)).days <= 1]
    if len(recent) < 2:
        recent = [name for _, name in files[-2:]]
    return ["sessions/" + name for name in recent]


def threads_excerpt():
    """The THREAD_SECTIONS of the registry, joined, or None if the file or a
    section is missing (then the whole file goes on the reading list)."""
    try:
        text = (ROOT / THREADS).read_text(encoding="utf-8")
    except OSError:
        return None
    parts = []
    for name in THREAD_SECTIONS:
        m = re.search(rf"^## {re.escape(name)}[^\n]*\n.*?(?=^## |\Z)", text, re.M | re.S)
        if not m:
            return None
        parts.append(m.group(0).strip())
    return "\n\n".join(parts)


def last_arc_date():
    arc = ROOT / "arc.md"
    if not arc.exists():
        return None
    for line in arc.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            m = DATE_RE.search(line)
            if m:
                return parse_date(m.group(1))
    return None


def main():
    today = dt.date.today()
    load, expired = context_entries(today)
    near, pending = near_events(today)
    memory = sorted(str(p.relative_to(ROOT)) for p in (ROOT / ".therapy/memory").glob("*.md"))

    threads = threads_excerpt()
    context = CONTEXT_TRIO + ([] if threads else [THREADS])
    reads = [r for r in FIXED_HEAD + memory + context if r not in OPTIONAL or (ROOT / r).exists()]
    reads += load
    reads += [path for path, _ in near if path not in reads]
    reads += ["sessions/index.md"] + recent_sessions(today)

    missing = [r for r in reads if not (ROOT / r).exists()]

    print(f"Today: {today.isoformat()}")
    arc = last_arc_date()
    if not (ROOT / "arc.md").exists():
        pass
    elif arc is None:
        print("Arc review: no entries yet - offer one if the moment allows")
    else:
        age = (today - arc).days
        due = "due - offer if the moment allows" if age > ARC_DUE_DAYS else "not due"
        print(f"Arc review: last {arc.isoformat()} ({age} days ago), {due}")
    if near:
        print("Near-term events (raise these this session):")
        for path, when in near:
            print(f"  - {when}: {path}")
    else:
        print("Near-term events: none")
    if pending:
        print("Pending events without a date: " + ", ".join(pending))
    if expired:
        print("Expired Active entries (not loaded; drop the tag at session end): " + ", ".join(expired))
    if missing:
        print("MISSING (listed but not on disk): " + ", ".join(missing))

    print(f"\nRead all {len(reads)} files:")
    for r in reads:
        print(r)
    if threads:
        print(f"\nOpen therapeutic and shelved threads from {THREADS}. These count as read "
              "for the greeting; the rest of the file (schema, logistical, archived) is "
              "read at session end, or when one of its threads comes up.")
        print(f"\n===== {THREADS} ({', '.join(THREAD_SECTIONS)})\n{threads}")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
