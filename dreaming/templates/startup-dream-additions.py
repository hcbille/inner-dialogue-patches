# startup-dream-additions.py — paste into .therapy/scripts/startup.py
#
# Adds the dreaming pieces to the startup script from the opus-5-5-rebaseline
# patch (or any script shaped like it). It relies on names that script
# already has: `re`, `dt` (datetime), `ROOT`, `parse_date()` and `SESSION_RE`.
# INSTALL.md, part 3, says exactly where each block goes.
#
# What it does:
#   - keeps session notes newer than the last merged dream on the reading
#     list (newest UNDREAMED_MAX of them), because session end only captures
#     and the dream consolidates;
#   - prints "Dream: due / not due";
#   - prints a "Dream flags" line naming the one flag the assistant may ask
#     this session;
#   - prints an "overdue" line when more sessions are undreamed than the
#     list keeps.
#
# 2026-11-09 fix: "undreamed" compares full session names, not dates. Before,
# a second session held later on the day a dream merged (2026-11-04b after a
# dream covering 2026-11-04) counted as covered: it dropped off the reading
# list and no dream would ever read it. The covered range in dreams/index.md
# now holds full session names too (2026-11-04b).


# ---- BLOCK A: constants (put them next to the script's other constants) ----

UNDREAMED_MAX = 6          # undreamed session notes kept on the startup list
DREAM_DUE_SESSIONS = 3     # due when this many sessions are undreamed...
DREAM_DUE_DAYS = 2         # ...and the last dream is at least this old
DREAM_DUE_BYTES = 220_000  # or when the startup list is this heavy (tune per install)
FLAG_REASK_DAYS = 30
DREAM_DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")
DREAM_LINE_RE = re.compile(
    r"^- (\d{4}-\d{2}-\d{2}) · covered (\d{4}-\d{2}-\d{2}[a-z]?) → (\d{4}-\d{2}-\d{2}[a-z]?).*outcome: ([a-z ]+?)\s*(?:·|$)")


# ---- BLOCK B: functions (REPLACE the existing recent_sessions() with these) ----

def session_files():
    files = []
    for f in (ROOT / "sessions").iterdir():
        m = SESSION_RE.match(f.name)
        if m:
            files.append((m.group(1), f.name))
    files.sort()
    return files


def last_dream():
    """(dream date, covered-through session stem) of the last merged dream, or None.

    The stem is a session file's name without .md, e.g. "2026-11-04b"."""
    index = ROOT / "dreams/index.md"
    if not index.exists():
        return None
    found = None
    for line in index.read_text(encoding="utf-8").splitlines():
        m = DREAM_LINE_RE.match(line)
        if m and m.group(4).strip() in ("merged", "merged with edits"):
            found = (parse_date(m.group(1)), m.group(3))
    return found


def undreamed_sessions():
    """Session files that sort after the last merged dream's covered-through stem.

    Compares full stems, not dates: "2026-11-04b" > "2026-11-04", so a session
    held later on the day a dream merged is still undreamed."""
    dream = last_dream()
    if dream is None:
        return []
    return [name for _, name in session_files() if name[:-3] > dream[1]]


def recent_sessions(today):
    """Sessions dated today or yesterday (if fewer than two, the two newest),
    plus the newest UNDREAMED_MAX sessions no dream has covered yet."""
    files = session_files()
    recent = [name for day, name in files if (today - parse_date(day)).days <= 1]
    if len(recent) < 2:
        recent = [name for _, name in files[-2:]]
    for name in undreamed_sessions()[-UNDREAMED_MAX:]:
        if name not in recent:
            recent.append(name)
    recent.sort()
    return ["sessions/" + name for name in recent]


def dream_status(today, startup_bytes):
    """One status line on whether a dream is due."""
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
    if reasons:
        return f"Dream: due ({', '.join(reasons)}; {head}). Offer it only in maintainer mode."
    return f"Dream: not due ({head})"


def askable_flag(today):
    """(open count, title of the oldest flag the assistant may ask this session, or None)."""
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


# ---- BLOCK C: in main(), after the last status line and before the reading list ----
#
#     startup_bytes = sum((ROOT / r).stat().st_size for r in reads if (ROOT / r).exists())
#     startup_bytes += len(threads.encode()) if threads else 0  # printed registry sections, if any
#     print(dream_status(today, startup_bytes))
#     count, oldest = askable_flag(today)
#     if oldest:
#         print(f"Dream flags: {count} open; may ask this session, at most one, per "
#               f".therapy/protocols/dream-flags.md: \"{oldest}\" (dreams/flags.md)")
#     elif count:
#         print(f"Dream flags: {count} open, none askable this session")
#     undreamed = undreamed_sessions()
#     if len(undreamed) > UNDREAMED_MAX:
#         print(f"Undreamed sessions: {len(undreamed)}; only the newest {UNDREAMED_MAX} "
#               "are on the list. A dream is overdue.")
#
# If the client did NOT opt in to in-session flag asking, leave out the four
# "Dream flags" lines.
