# startup-ingest-additions.py — paste into .therapy/scripts/startup.py
#
# For a startup script that already has the dreaming patch's additions
# (dreaming/templates/startup-dream-additions.py) on top of the
# opus-5-5-rebaseline script, or one shaped like it. It relies on names those
# already have: `re`, `dt`, `ROOT`, `parse_date()`, `DATE_RE`,
# `ENTRY_PATH_RE`, `STATUS_RE`, `EVENT_AHEAD_DAYS`, `ACTIVE_DAYS`,
# `FIXED_HEAD`, `CONTEXT_TRIO`, `OPTIONAL`, `THREADS`, `threads_excerpt()`,
# `session_files()`, `last_dream()`, `DREAM_LINE_RE`, `DREAM_DATE_RE` and
# `FLAG_REASK_DAYS`. INSTALL.md, parts 1 and 2, says which block goes in when.
#
# What it does:
#   Part 1 (session end writes only the note):
#   - reads the "## For the next session" block of every note no dream has
#     covered (blocks()): its events count as near-term events, its threads
#     are printed as surfaced, a flag answered in it isn't offered again, a
#     file it names stays loaded for ACTIVE_DAYS, and its handling-rule
#     changes are printed;
#   - keeps every such note on the reading list (no UNDREAMED_MAX cap: until a
#     dream covers it, the note is the only record).
#   Part 2 (ingests):
#   - reads dreams/ingests/index.md; a note is "unprocessed" until an ingest
#     or a longform dream has covered it, and only unprocessed notes stay on
#     the list;
#   - a new due rule for longform dreams (dream_state()), and an "Ingest:"
#     line for maintainer mode;
#   - reading_list(), so scheduled/status.py can measure the startup bytes.
#
# Paste the part 1 blocks for part 1. For part 2, paste the part 2 blocks
# too: they REPLACE some part 1 functions (marked). The finished functions are
# the same either way; part 1 alone just counts from the last longform dream.


# ============================================================================
# PART 1
# ============================================================================

# ---- BLOCK 1A: constants (next to the dreaming constants) ----
# DELETE UNDREAMED_MAX: every undreamed note now stays on the list.

DREAM_OVERDUE_SESSIONS = 5  # undreamed notes are the only record, so warn early
BLOCK_RE = re.compile(r"^## For the next session\s*$(.*?)(?=^## |\Z)", re.M | re.S)
BLOCK_FIELD_RE = re.compile(r"^- ([A-Za-z -]+):\s*(.*)$")
NONE_RE = re.compile(r"^\(?none\)?\.?$", re.I)


# ---- BLOCK 1B: functions ----
# context_entries(), near_events(), recent_sessions(), dream_status() and
# askable_flag() REPLACE the script's own. pending_notes() is new: part 1
# points it at undreamed_sessions(), part 2 at unprocessed_sessions().

def pending_notes():
    """Notes whose block the script reads and keeps on the list."""
    return undreamed_sessions()


def context_entries(today, touched=None):
    """Return (load, expired) lists of context paths from context/index.md.

    touched maps a context path to the newest pending note date naming it in
    its block; such a file stays loaded for ACTIVE_DAYS from that date, since
    only a dream refreshes Active dates now."""
    load, expired = [], []
    touched = touched or {}
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
        seen = touched.get(rel)
        kept = seen and (today - seen).days <= ACTIVE_DAYS
        if kind == "Active" and stamp and (today - parse_date(stamp)).days > ACTIVE_DAYS and not kept:
            expired.append(f"{rel} (Active {stamp})")
        elif rel not in load:
            load.append(rel)
    return load, expired


def near_events(today, block_events=()):
    """Event files dated yesterday through today+2, plus undated pending ones,
    plus events named in pending notes' blocks (date, label, path or None,
    note), which no dream has turned into files yet."""
    near, pending = [], []
    events = ROOT / "context/events"
    if events.is_dir():
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
    listed = {path for path, _ in near}
    for day, label, path, note in block_events:
        delta = (day - today).days
        if not -1 <= delta <= EVENT_AHEAD_DAYS:
            continue
        when = {-1: "yesterday", 0: "today", 1: "tomorrow"}.get(delta, f"in {delta} days")
        target = path if path and (ROOT / path).exists() else note
        if target in listed:
            continue
        listed.add(target)
        near.append((target, f"{when} ({label}, from {note}'s block)" if target == note else when))
    return near, pending


def recent_sessions(today):
    """Sessions dated today or yesterday (if fewer than two, the two newest),
    plus every pending note (until a dream covers it, the note is the only
    record, so none may fall off quietly)."""
    files = session_files()
    recent = [name for day, name in files if (today - parse_date(day)).days <= 1]
    if len(recent) < 2:
        recent = [name for _, name in files[-2:]]
    for name in pending_notes():
        if name not in recent:
            recent.append(name)
    recent.sort()
    return ["sessions/" + name for name in recent]


def dream_status(today, startup_bytes):
    """One status line on whether a dream is due. (Part 2 replaces this.)"""
    dream = last_dream()
    if dream is None:
        return "Dream: no merged dream yet; offer one in maintainer mode"
    pending = len(undreamed_sessions())
    age = (today - dream[0]).days
    reasons = []
    if pending >= DREAM_DUE_SESSIONS and age >= DREAM_DUE_DAYS:
        reasons.append(f"{pending} undreamed sessions")
    if startup_bytes > DREAM_DUE_BYTES:
        reasons.append(f"startup list {startup_bytes:,} bytes")
    head = f"last {dream[0].isoformat()}, covered through {dream[1]}, {pending} undreamed"
    if pending >= DREAM_OVERDUE_SESSIONS:
        return (f"Dream: overdue ({pending} undreamed sessions; {head}). Their notes are the "
                "only record until a dream runs. Offer it only in maintainer mode.")
    if reasons:
        return f"Dream: due ({', '.join(reasons)}; {head}). Offer it only in maintainer mode."
    return f"Dream: not due ({head})"


def askable_flag(today, answered=()):
    """(open count, title of the oldest flag the assistant may ask this session, or None).

    A flag answered in a pending note's block is skipped (the dream records
    it). Statuses other than open/asked, such as "waiting for dream review
    (ingest ...)", are never asked in a session."""
    flags = ROOT / "dreams/flags.md"
    if not flags.exists():
        return 0, None
    text = flags.read_text(encoding="utf-8")
    m = re.search(r"^## Open\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    if not m:
        return 0, None
    count, oldest = 0, None
    for block in re.split(r"^### ", m.group(1), flags=re.M)[1:]:
        title = block.splitlines()[0].strip()
        if any(a and (a in title or title in a) for a in answered):
            continue
        status = re.search(r"\*\*Status:\*\*\s*(.+)", block)
        status = status.group(1).strip() if status else ""
        if status.startswith("open"):
            ok = True
        elif status.startswith("asked"):
            d = DREAM_DATE_RE.search(status)
            ok = bool(d) and (today - parse_date(d.group(1))).days >= FLAG_REASK_DAYS
        else:
            continue
        count += 1
        if ok and oldest is None:
            oldest = title
    return count, oldest


def _items(value):
    """Split a block field into its ;-separated items, dropping "(none)"."""
    if NONE_RE.match(value.strip()):
        return []
    return [v.strip() for v in value.split(";") if v.strip() and not NONE_RE.match(v.strip())]


def blocks():
    """Parse the "## For the next session" block of every pending note.

    Returns a dict: events [(date, label, path, note)], threads [(note, item)],
    touched {context path: newest note date}, answered [flag title fragments],
    declines [dates], rules [(note, item)], missing [notes with no block]."""
    out = {"events": [], "threads": [], "touched": {}, "answered": [],
           "declines": [], "rules": [], "missing": []}
    for name in pending_notes():
        note = "sessions/" + name
        day = parse_date(name[:10])
        try:
            m = BLOCK_RE.search((ROOT / note).read_text(encoding="utf-8"))
        except OSError:
            continue
        if not m:
            out["missing"].append(note)
            continue
        for line in m.group(1).splitlines():
            f = BLOCK_FIELD_RE.match(line.strip())
            if not f:
                continue
            key, value = f.group(1).strip().lower(), f.group(2)
            if key == "events":
                for item in _items(value):
                    d = DATE_RE.search(item)
                    if not d:
                        continue
                    path = ENTRY_PATH_RE.search(item)
                    path = path.group(1) if path else None
                    if path and not path.startswith("context/"):
                        path = "context/" + path
                    label = re.sub(r"\s*\(`.*$", "", item.split("·", 1)[-1]).strip()
                    out["events"].append((parse_date(d.group(1)), label, path, note))
            elif key == "threads":
                out["threads"] += [(note, i) for i in _items(value)]
            elif key in ("files touched", "new stubs"):
                for item in re.split(r"[;,]", value):
                    rel = item.strip().strip("`")
                    if not rel.endswith(".md") or NONE_RE.match(rel):
                        continue
                    rel = rel if rel.startswith("context/") else "context/" + rel
                    if day > out["touched"].get(rel, dt.date.min):
                        out["touched"][rel] = day
            elif key == "flag answers":
                out["answered"] += re.findall(r'"([^"]+)"', value)
            elif key == "profile":
                if re.search(r"review (offered and )?declined", value, re.I):
                    out["declines"].append(day)
            elif key == "handling-rule changes":
                out["rules"] += [(note, i) for i in _items(value)]
    return out


def reading_list(today):
    """Everything main() prints, resolved: a dict with blk (blocks()), reads,
    threads (excerpt or None), near, pending, expired, and startup_bytes (the
    reads plus the printed threads excerpt)."""
    blk = blocks()
    load, expired = context_entries(today, blk["touched"])
    near, pending = near_events(today, blk["events"])
    memory = sorted(str(p.relative_to(ROOT)) for p in (ROOT / ".therapy/memory").glob("*.md"))
    threads = threads_excerpt()
    context = CONTEXT_TRIO + ([] if threads else [THREADS])
    reads = [r for r in FIXED_HEAD + memory + context if r not in OPTIONAL or (ROOT / r).exists()]
    reads += [r for r in load if r not in reads]
    reads += [path for path, _ in near if path not in reads]
    # a note named as a near-term event (from its block) is already listed
    reads += [p for p in ["sessions/index.md"] + recent_sessions(today) if p not in reads]
    startup_bytes = sum((ROOT / r).stat().st_size for r in reads if (ROOT / r).exists())
    startup_bytes += len(threads.encode()) if threads else 0
    return {"blk": blk, "reads": reads, "threads": threads, "near": near,
            "pending": pending, "expired": expired, "startup_bytes": startup_bytes}


# ---- BLOCK 1C: main() ----
# Replace the start of main(), up to the first print, with the lines below,
# and use these names in the rest of it (reads, threads, near, pending,
# expired). If this install's main() builds more (summaries, a profile-review
# line), move that into reading_list() and return it in the dict.
#
#     today = dt.date.today()
#     r = reading_list(today)
#     blk, reads, threads = r["blk"], r["reads"], r["threads"]
#     near, pending, expired = r["near"], r["pending"], r["expired"]
#     missing = [p for p in reads if not (ROOT / p).exists()]
#
# Change the expired-Active line's wording from "drop the tag at session end"
# to "the next dream drops the tag".
#
# Replace the dreaming patch's BLOCK C (the startup_bytes sum, the dream line,
# the flags lines and the "Undreamed sessions" line) with:
#
#     print(dream_status(today, r["startup_bytes"]))
#     count, oldest = askable_flag(today, blk["answered"])
#     if oldest:
#         print(f"Dream flags: {count} open; may ask this session, at most one, per "
#               f".therapy/protocols/dream-flags.md: \"{oldest}\" (dreams/flags.md)")
#     elif count:
#         print(f"Dream flags: {count} open, none askable this session")
#     if blk["threads"]:
#         print("Threads in undreamed notes (newer than threads.md; count each as surfaced "
#               "on its note's date, and honour shelved/closed): "
#               + "; ".join(f"{i} [{n[9:-3]}]" for n, i in blk["threads"]))
#     if blk["rules"]:
#         print("Handling-rule changes in undreamed notes (these outrank older file wording): "
#               + "; ".join(f"{i} [{n[9:-3]}]" for n, i in blk["rules"]))
#     if blk["missing"]:
#         print("Undreamed notes without a For-the-next-session block (read them for events, "
#               "threads and flag answers): " + ", ".join(blk["missing"]))
#
# If this install has a profile-review status line (the stock
# profile-protocol.md's staleness check), add blk["declines"] to the
# declines it reads from profile.md, so a review declined in a note counts
# at once.
#
# In the thread-registry printout at the end, change "read at session end, or
# when one of its threads comes up" to "read when one of its threads comes up".


# ============================================================================
# PART 2
# ============================================================================

# ---- BLOCK 2A: constants ----
# REPLACE DREAM_DUE_SESSIONS, DREAM_DUE_DAYS and DREAM_OVERDUE_SESSIONS with
# these (keep DREAM_DUE_BYTES as tuned). Counts and ages are since the last
# merged longform dream.

DREAM_DUE_SESSIONS = 5      # due at this many sessions...
DREAM_DUE_DAYS = 5          # ...once the last longform is at least this old
DREAM_MAX_DAYS = 10         # or at this age with at least one session
DREAM_OVERDUE_SESSIONS = 10 # "overdue" from this many sessions
INGEST_INDEX = "dreams/ingests/index.md"
INGEST_LINE_RE = re.compile(
    r"^- (\d{4}-\d{2}-\d{2}(?:-\d+)?) · covered (\d{4}-\d{2}-\d{2}[a-z]?) → (\d{4}-\d{2}-\d{2}[a-z]?)"
    r".*outcome: ([a-z ]+?)\s*(?:·|$)")


# ---- BLOCK 2B: functions ----
# pending_notes() and dream_status() REPLACE the part 1 ones; the rest is new.

def _ingest_key(ingest_id):
    """Sort key for an ingest id: 2026-01-15 < 2026-01-15-2 < 2026-01-15-10."""
    n = ingest_id[11:]
    return (ingest_id[:10], int(n) if n.isdigit() else 1)


def last_ingest():
    """(ingest id, covered-through session stem) of the newest merged ingest in
    dreams/ingests/index.md, or None if the file is missing or has no entries.

    Only merged ingests land on main, so every line there should say merged;
    a line with another outcome is skipped all the same."""
    index = ROOT / INGEST_INDEX
    if not index.exists():
        return None
    found = None
    for line in index.read_text(encoding="utf-8").splitlines():
        m = INGEST_LINE_RE.match(line)
        if not m or not m.group(4).strip().startswith("merged"):
            continue
        if found is None or _ingest_key(m.group(1)) >= _ingest_key(found[0]):
            found = (m.group(1), m.group(3))
    return found


def covered_through():
    """The later covered-through stem of the last merged longform dream and the
    last ingest, or None when neither has run."""
    stems = [x[1] for x in (last_dream(), last_ingest()) if x]
    return max(stems) if stems else None


def unprocessed_sessions():
    """Session files after covered_through(): no ingest or longform has covered
    them, so their note is the only record. Empty before the first merged
    dream (the install runs one by hand first)."""
    through = covered_through()
    if through is None:
        return []
    return [name for _, name in session_files() if name[:-3] > through]


def pending_notes():
    """Notes whose block the script reads and keeps on the list: the ones no
    ingest or longform has covered."""
    return unprocessed_sessions()


def dream_state(today, startup_bytes):
    """Whether a longform dream is due: (state, reasons, last dream or None,
    sessions since it). state is "none" (no merged longform yet), "overdue",
    "due" or "not due"."""
    dream = last_dream()
    if dream is None:
        return "none", [], None, 0
    since = len(undreamed_sessions())
    age = (today - dream[0]).days
    reasons = []
    if since >= DREAM_DUE_SESSIONS and age >= DREAM_DUE_DAYS:
        reasons.append(f"{since} sessions in {age} days")
    if age >= DREAM_MAX_DAYS and since >= 1:
        reasons.append(f"{age} days since the last")
    if startup_bytes > DREAM_DUE_BYTES:
        reasons.append(f"startup list {startup_bytes:,} bytes")
    if since >= DREAM_OVERDUE_SESSIONS:
        return "overdue", reasons, dream, since
    return ("due" if reasons else "not due"), reasons, dream, since


def dream_status(today, startup_bytes):
    """One status line on whether a longform dream is due."""
    state, reasons, dream, since = dream_state(today, startup_bytes)
    if state == "none":
        return "Dream: no merged dream yet; offer one in maintainer mode"
    head = f"last {dream[0].isoformat()}, covered through {dream[1]}, {since} sessions since"
    if state == "overdue":
        return (f"Dream: overdue ({since} sessions since the last longform; {head}). "
                "Offer it only in maintainer mode.")
    if state == "due":
        return f"Dream: due ({', '.join(reasons)}; {head}). Offer it only in maintainer mode."
    return f"Dream: not due ({head})"


def ingest_status():
    """The Ingest: line, or None when every note has been ingested or dreamed."""
    waiting = unprocessed_sessions()
    if not waiting:
        return None
    return (f"Ingest: {len(waiting)} notes not yet ingested (newest {waiting[-1][:-3]}). "
            "Maintainer mode only; never mention in a session.")


# ---- BLOCK 2C: main() ----
# Right after the dream_status line, add:
#
#     ingest = ingest_status()
#     if ingest:
#         print(ingest)
#
# and in the three block lines from 1C, change "undreamed notes" to "notes
# not yet ingested".
