#!/usr/bin/env python3
"""context-loader.py — UserPromptSubmit hook: point the assistant at context files.

The instructions ask the assistant to read a subject's context file the
first time the client raises it. That is a judgment call made
mid-conversation, and it slips: in the reference setup, a person the client
named wasn't read until the client asked about it. This hook makes the
check mechanical: it matches the client's message against the names
and aliases of every context file, plus the hand-kept topic links in
`context/topic-links.md`, and injects a short note naming the files to read.

What it matches:
  - every `context/index.md` entry's display name, including both halves
    of [[target|label]] links, "A / B" splits, and "(Parenthetical)" names;
  - a person's first name when the display name is "First Last";
  - `aliases:` in each context file's frontmatter;
  - the keywords in `context/topic-links.md`.
Matching is case-insensitive on whole words, and accepts a trailing
possessive ("Annas", "Anna's").

What it skips:
  - Core and unexpired Active files (startup.py already loads them);
  - files it has already flagged in this session (state kept per
    session_id under .therapy/.cache/, gitignored), so each file is named
    once, not on every message. State files untouched for
    STATE_MAX_AGE_DAYS are pruned whenever the hook writes, so they
    don't pile up;
  - aliases in GENERIC_ALIASES, which are everyday phrases.

Fail-open: on any error, exit 0 with no output. A broken hook must never
break a session.
"""

import datetime as dt
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTEXT = ROOT / "context"
CACHE = ROOT / ".therapy/.cache/context-loader"
ACTIVE_DAYS = 7  # keep in step with startup.py
STATE_MAX_AGE_DAYS = 3  # state files older than this belong to finished sessions
MIN_ALIAS_LEN = 3

# Aliases that are everyday phrases, not names. Matching them would flag a
# file every time the client says the words in their ordinary sense.
# Fill in from this install's aliases (INSTALL step 1.4); these are examples.
GENERIC_ALIASES = {
    "index", "the office", "the plan",
}

# Files with a standing rule about how they're used once loaded. The note is
# appended to the file's line in the injected reminder. Example:
#   "context/people/some-name.md": (
#       "Boundary: read it silently so you're prepared, "
#       "but never name them first. Wait for the client to."
#   ),
FILE_NOTES = {}

ENTRY_RE = re.compile(r"^- (.+?)\s*\(`([^`]+\.md)`\)")
STATUS_RE = re.compile(r"\*\*(Core|Active)(?: \((\d{4}-\d{2}-\d{2})\))?\*\*")
LINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")
PAREN_RE = re.compile(r"\(([^)]+)\)")
TOPIC_RE = re.compile(r"^- (.+?)\s*(?:→|->)\s*(.+)$")


def clean(name):
    return re.sub(r"\s+", " ", name.replace("*", "").replace("`", "")).strip()


def names_from_display(display, is_person):
    names = set()
    for target, label in LINK_RE.findall(display):
        names.add(target)
        if label:
            names.add(label)
    plain = LINK_RE.sub(lambda m: m.group(2) or m.group(1), display)
    for inner in PAREN_RE.findall(plain):
        # "(Kim)", "(Grandma)" are names; "(friend group)", "(ex)" are descriptors.
        if inner[:1].isupper():
            names.add(inner)
    plain = PAREN_RE.sub("", plain)
    for part in plain.split(" / "):
        names.add(part)
    names = {clean(n) for n in names if clean(n)}
    if is_person:
        for n in list(names):
            words = n.split()
            if len(words) == 2 and all(w[:1].isupper() for w in words) and "'" not in n:
                names.add(words[0])
    return names


def frontmatter_aliases(path):
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return set()
    if not text.startswith("---"):
        return set()
    end = text.find("\n---", 3)
    if end == -1:
        return set()
    aliases, in_aliases = set(), False
    for line in text[3:end].splitlines():
        if re.match(r"^aliases:\s*$", line):
            in_aliases = True
            continue
        if in_aliases:
            m = re.match(r"^\s*-\s*(.+)$", line)
            if not m:
                break
            aliases.add(clean(m.group(1).strip().strip("'\"")))
    return aliases


def startup_loaded(line, today):
    status = STATUS_RE.search(line)
    if not status:
        return False
    kind, stamp = status.groups()
    if kind == "Core":
        return True
    return not stamp or (today - dt.date.fromisoformat(stamp)).days <= ACTIVE_DAYS


def build_map(today):
    """Return {alias_lower: set(rel_paths)} for files not loaded at startup."""
    amap = {}

    def add(alias, rel):
        key = alias.lower()
        if len(key) >= MIN_ALIAS_LEN and key not in GENERIC_ALIASES:
            amap.setdefault(key, set()).add(rel)

    skip = set()
    for line in (CONTEXT / "index.md").read_text(encoding="utf-8").splitlines():
        m = ENTRY_RE.match(line)
        if not m:
            continue
        display, rel_in_context = m.groups()
        rel = "context/" + rel_in_context
        if startup_loaded(line, today):
            skip.add(rel)
            continue
        for name in names_from_display(display, rel_in_context.startswith("people/")):
            add(name, rel)
        for alias in frontmatter_aliases(ROOT / rel):
            add(alias, rel)

    topics = CONTEXT / "topic-links.md"
    if topics.exists():
        for line in topics.read_text(encoding="utf-8").splitlines():
            m = TOPIC_RE.match(line)
            if not m:
                continue
            keywords = [clean(k) for k in m.group(1).split(",")]
            paths = [clean(p) for p in m.group(2).split(",")]
            for kw in keywords:
                for p in paths:
                    rel = p if p.startswith("context/") else "context/" + p
                    if rel not in skip and (ROOT / rel).exists():
                        amap.setdefault(kw.lower(), set()).add(rel)
    return amap


def matches(prompt, amap):
    text = prompt.lower().replace("’", "'")
    hits = {}
    for alias, rels in amap.items():
        pattern = r"(?<!\w)" + re.escape(alias) + r"(?:'?s|s')?(?!\w)"
        if re.search(pattern, text):
            for rel in rels:
                hits.setdefault(rel, alias)
    return hits


def prune_state():
    """Delete state files from finished sessions. A live session touches its
    file on every flag, so anything untouched for days is safe to remove."""
    import time
    cutoff = time.time() - STATE_MAX_AGE_DAYS * 86400
    for f in CACHE.glob("*.json"):
        try:
            if f.stat().st_mtime < cutoff:
                f.unlink()
        except OSError:
            pass


def load_state(session_id):
    path = CACHE / (re.sub(r"[^A-Za-z0-9_-]", "_", session_id) + ".json")
    try:
        return path, set(json.loads(path.read_text(encoding="utf-8")))
    except (OSError, ValueError):
        return path, set()


def main():
    payload = json.loads(sys.stdin.read() or "{}")
    prompt = payload.get("prompt")
    if not isinstance(prompt, str) or not prompt.strip():
        return
    session_id = str(payload.get("session_id") or "no-session")

    hits = matches(prompt, build_map(dt.date.today()))
    if not hits:
        return
    state_path, flagged = load_state(session_id)
    new = {rel: alias for rel, alias in hits.items() if rel not in flagged}
    if not new:
        return

    lines = [
        "Context files for subjects in the client's message (per CLAUDE.md, read each "
        "one before replying on that subject, silently, unless you've already "
        "read it this session):"
    ]
    for rel in sorted(new):
        line = f"- {rel} (matched \"{new[rel]}\")"
        if rel in FILE_NOTES:
            line += f" | {FILE_NOTES[rel]}"
        lines.append(line)

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": "\n".join(lines),
        }
    }))
    sys.stdout.flush()

    try:
        CACHE.mkdir(parents=True, exist_ok=True)
        prune_state()
        state_path.write_text(json.dumps(sorted(flagged | set(new))), encoding="utf-8")
    except OSError:
        pass


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
