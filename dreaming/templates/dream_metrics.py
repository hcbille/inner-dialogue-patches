#!/usr/bin/env python3
"""Print the numbers a dream report records (dream.md, Phase 5), measured the
same way every time.

Install at .therapy/scripts/dream_metrics.py, next to startup.py, and run from
the install root before and after a dream:
    python3 .therapy/scripts/dream_metrics.py

Read-only: it never edits a file. It imports startup.py and reuses its own
logic, so "startup list bytes" is exactly what the next session would read.
Needs the part 3.2 dream additions in startup.py (DREAM_LINE_RE, last_dream(),
undreamed_sessions()). Everything else is optional and skipped when this
install doesn't have it.

Definitions:
- startup list bytes: total size of every file on startup.py's reading list,
  plus the thread-registry sections it prints instead of the whole file
  (opus-5-5-rebaseline, 2026-11-10), if it does.
- projected after merge: when dreams/index.md has a dream with outcome
  "pending", the startup list bytes as if it were already merged. That's the
  "after" figure a dream report should use, since the in-range notes only
  leave the list at merge.
- summary output bytes: what startup.py prints from SUMMARY_MARKER to the end
  of its output, if this install's startup prints summary blocks.
- file sizes: each file in SIZED_FILES that exists.
- mentions entries: lines starting "- " in context/mentions.md, below its
  first "---".
- open threads: entries under the "## Open" sections of context/threads.md;
  "not surfaced in 30+ days" counts the ones whose *Last surfaced* date is
  more than STALE_DAYS old (do-not-raise and logistical ones included).
- expired Active tags: from startup.py's context_entries(), if it has one.
- undreamed sessions: session notes newer than the last merged dream.
- next library pass (part 5): the pass after the one named ("· pass <name>")
  on the last merged dream line that names one, in the order threads →
  summaries → consolidation. "threads" if none has run yet.
- memory misses in range: undreamed session notes whose "## Memory Misses"
  section (part 1.4) says something other than "None".

ADAPT: SIZED_FILES and SUMMARY_MARKER to this install's files and output.
"""

import contextlib
import datetime as dt
import io
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import startup  # noqa: E402

ROOT = startup.ROOT
STALE_DAYS = 30
LIBRARY_PASSES = ["threads", "summaries", "consolidation"]
SIZED_FILES = ["profile.md", "context/index.md", "context/threads.md", "context/mentions.md"]
# The line startup.py prints before any summary blocks. Leave it if this
# install has none; the line is then left out of the output.
SUMMARY_MARKER = "\nSummaries of "
MERGED = ("merged", "merged with edits")

REQUIRED = ("DREAM_LINE_RE", "last_dream", "undreamed_sessions", "parse_date", "main")
missing = [name for name in REQUIRED if not hasattr(startup, name)]
if missing:
    sys.exit("dream_metrics: startup.py is missing " + ", ".join(missing)
             + " (install the part 3.2 dream additions first)")


def size(rel):
    p = ROOT / rel
    return p.stat().st_size if p.exists() else 0


def startup_numbers():
    """(reading-list bytes, summary bytes, whole output bytes)."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        startup.main()
    out = buf.getvalue()
    lines = out.splitlines()
    try:
        start = next(i for i, l in enumerate(lines) if l.startswith("Read all "))
    except StopIteration:
        return 0, 0, len(out.encode())
    reads = []
    for l in lines[start + 1:]:
        if not l.strip():
            break
        reads.append(l.strip())
    list_bytes = sum(size(r) for r in reads)
    threads_rel = getattr(startup, "THREADS", None)
    excerpt = getattr(startup, "threads_excerpt", None)
    if threads_rel and excerpt and threads_rel not in reads:
        list_bytes += len((excerpt() or "").encode())
    i = out.find(SUMMARY_MARKER)
    summary_bytes = len(out[i + 1:].encode()) if i >= 0 else 0
    return list_bytes, summary_bytes, len(out.encode())


def dream_lines():
    index = ROOT / "dreams/index.md"
    if not index.exists():
        return []
    out = []
    for line in index.read_text(encoding="utf-8").splitlines():
        m = startup.DREAM_LINE_RE.match(line)
        if m:
            out.append((m, line))
    return out


def pending_dream():
    """(dream date, covered-through stem) of the newest pending dream, or None."""
    found = None
    for m, _ in dream_lines():
        if m.group(4).strip() == "pending":
            found = (startup.parse_date(m.group(1)), m.group(3))
    return found


def projected_list_bytes():
    """Startup list bytes with the pending dream counted as merged, or None."""
    pend = pending_dream()
    if pend is None:
        return None
    real = startup.last_dream
    startup.last_dream = lambda: pend
    try:
        return startup_numbers()[0]
    finally:
        startup.last_dream = real


def next_library_pass():
    """(next pass, last pass or None, date of the dream that did it or None)."""
    last = None
    for m, line in dream_lines():
        p = re.search(r"· pass (\w+)", line)
        if p and m.group(4).strip() in MERGED and p.group(1) in LIBRARY_PASSES:
            last = (p.group(1), m.group(1))
    if last is None:
        return LIBRARY_PASSES[0], None, None
    nxt = LIBRARY_PASSES[(LIBRARY_PASSES.index(last[0]) + 1) % len(LIBRARY_PASSES)]
    return nxt, last[0], last[1]


def threads(today):
    """(open count, stale count), or None without a thread registry."""
    path = ROOT / "context/threads.md"
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    open_count, stale = 0, 0
    for sec in re.finditer(r"^## Open[^\n]*\n(.*?)(?=^## |\Z)", text, re.M | re.S):
        for block in re.split(r"^### ", sec.group(1), flags=re.M)[1:]:
            open_count += 1
            m = re.search(r"\*\*Last surfaced:\*\*\s*(\d{4}-\d{2}-\d{2})", block)
            if m and (today - startup.parse_date(m.group(1))).days > STALE_DAYS:
                stale += 1
    return open_count, stale


def mentions():
    path = ROOT / "context/mentions.md"
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    body = text.split("\n---", 1)[1] if "\n---" in text else text
    return sum(1 for l in body.splitlines() if l.startswith("- "))


def memory_misses():
    misses = []
    for name in startup.undreamed_sessions():
        text = (ROOT / "sessions" / name).read_text(encoding="utf-8")
        m = re.search(r"^## Memory Misses\s*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
        if m and m.group(1).strip() and not m.group(1).strip().lower().startswith("none"):
            misses.append(name)
    return misses


def main():
    today = dt.date.today()
    list_bytes, summary_bytes, whole = startup_numbers()
    undreamed = startup.undreamed_sessions()
    misses = memory_misses()

    print(f"Dream metrics, {today.isoformat()}")
    projected = projected_list_bytes()
    print(f"- Startup list bytes: {list_bytes:,}"
          + (f"; projected after merge: {projected:,}" if projected is not None else ""))
    if summary_bytes:
        print(f"- Summary output bytes: {summary_bytes:,} (whole startup output {whole:,})")
    else:
        print(f"- Whole startup output bytes: {whole:,}")
    for rel in SIZED_FILES:
        if (ROOT / rel).exists():
            print(f"- {rel}: {size(rel):,} bytes")
    count = mentions()
    if count is not None:
        print(f"- Mentions entries: {count}")
    t = threads(today)
    if t is not None:
        # counts only: thread titles can name subjects a dream report must leave out
        print(f"- Open threads: {t[0]}; not surfaced in {STALE_DAYS}+ days: {t[1]}")
    if hasattr(startup, "context_entries"):
        _, expired = startup.context_entries(today)
        print(f"- Expired Active tags: {len(expired)}")
    print(f"- Undreamed sessions: {len(undreamed)}"
          + (f" ({undreamed[0][:-3]} → {undreamed[-1][:-3]})" if undreamed else ""))
    nxt, prev, when = next_library_pass()
    print(f"- Next library pass: {nxt}" + (f" (last: {prev}, dream {when})" if prev else " (none run yet)"))
    print(f"- Memory misses in range: {len(misses)}"
          + (f" ({', '.join(m[:-3] for m in misses)})" if misses else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
