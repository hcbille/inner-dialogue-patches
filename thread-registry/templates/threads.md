# Threads to Revisit

The canonical registry of open threads — the standing topics, questions, and loose ends that are meant to **outlive the session they were named in**. This is the single source of truth for "things to come back to": the per-session "Threads to Revisit" notes are just daily snapshots, and (if this setup has a periodic/arc review) its "held but unexamined"-style list is a periodic audit *of this file*, not a separate list.

**Read at every session start** so the open set is in context before the greeting, and reconciled at session end. Like `context/mentions.md`, this is a protocol-referenced tracking file — not a Core subject, not listed in `context/index.md`.

> Adapt "the client" throughout to whatever this setup calls the person, and use their actual pronouns. Keep everything else.

---

## How it works

**Entry schema:**

```markdown
### <thread handle>
- **Status:** Open | Shelved (YYYY-MM-DD) | Closed (YYYY-MM-DD) | Promoted (YYYY-MM-DD)
- **Type:** therapeutic | logistical
- **Opened:** YYYY-MM-DD · **Last surfaced:** YYYY-MM-DD
- **Subjects:** <the people/concepts this thread involves>
- **Sessions:** sessions/YYYY-MM-DD.md, sessions/YYYY-MM-DD.md
- <1–3 line description of what the thread is and where it stands>
- **Surfacing:** <how/whether to raise it — the rule for this specific thread>
```

> **Subjects field:** reference the relevant people/concepts using whatever cross-reference convention this setup already uses — plain names, or however it links context files. (The reference build used Obsidian `[[double-bracket]]` links; if this setup isn't on that, just use plain names or its own linking style.)

**The bar for entry:** a thread only belongs here if it's expected to outlive the session it was named in. A loose end that opens and closes inside one session stays in that session note only.

**Status lifecycle:**
- **Open** — live. The standing-threads check (if this setup has one) draws from the **Open + therapeutic** set, picks the stalest item whose *Last surfaced* is more than 7 days old, and gently offers it — at most one per session, never during crisis or acute distress.
- **Shelved** — consciously set down by the client ("let it rest"). Stays in the file, excluded from the active-surfacing set; only a rare, light "does this still feel rightly shelved?" check is allowed, never a push to act. This is the durable home for the rule "if they decline, stop carrying it as active."
- **Closed** — examined/resolved. Move the entry to `## Archived` with a one-line outcome. Pruned at the next periodic review.
- **Promoted** — the thread outgrew the registry (see below). Move to `## Archived` as a one-line pointer to the file it became.

**Type:**
- **therapeutic** — emotional/standing-work threads. These are the only ones the standing-threads check surfaces in-session.
- **logistical** — real follow-ups (an outcome to check, a task pending). Tracked here so they stop leaking into session-note copy-paste, but **never surfaced as if they were emotional work**. Raise only if naturally relevant or if the client asks.

**Promotion — when a thread outgrows the file:** if a thread accumulates real texture across multiple sessions and becomes a substantive worked arc rather than a reminder, promote it to its own context file — usually a `concept`, occasionally a person/place/event. Seed the new file with a "Prior thread" section pulling this entry's description and full **Sessions** trail (the same pattern as promoting a `mentions.md` entry), add it to `context/index.md`, then mark this entry **Promoted** with a pointer. **If it doesn't clearly land as a person/place/event/concept, it isn't ripe — leave it here.** "Not classifiable yet" is the definition of still being a thread, not a signal for a new file type.

---

## Open — Therapeutic

*(none yet — seed from the client's current open threads)*

## Open — Logistical

*(none yet)*

## Shelved

*(none yet)*

## Archived (Closed / Promoted)

*Closed and promoted threads land here with a one-line outcome or pointer, then get pruned at the next periodic review.*
