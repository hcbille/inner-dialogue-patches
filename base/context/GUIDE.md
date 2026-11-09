# Context Library Guide

The `context/` folder is a subject-level reference library — deeper, more stable notes on the specific people, places, and recurring concepts in the client's life. Unlike session notes (chronological) or `profile.md` (about the client themselves), these files are about the things that orbit them.

---

## Folder Structure

```
context/
  index.md          ← always read at session start
  GUIDE.md           ← this file; read when maintaining context files
  people/
    [name].md
  places/
    [place].md
  concepts/
    [concept].md
  events/
    YYYY-MM-DD-[slug].md
```

---

## `context/index.md` — Status Levels

Each entry is one line: subject name, what it is, load status.

- **`Core`** — Always loaded at session start. No date, no expiry. For permanent fixtures: foundational concepts, ongoing structural threads.
- **`Active (YYYY-MM-DD)`** — Loaded at session start. Date-stamped when status was last confirmed relevant. Expires after 7 days if not refreshed.
- *(no status)* — Load only when the client raises the topic.

**At session start:** check every Active date. If more than 7 days before today, remove the Active status before proceeding.

**At session end:** for Active entries directly relevant today, update the date to today. For Active entries more than 7 days old and not relevant today, remove the Active status.

Example entry format:
```markdown
- **[Name]** (`people/name.md`) — one-line synthesis. **Active (2026-06-09)**
- **[Sensitive subject]** (`people/name.md`) — one-line synthesis. Load only if the client raises it first.
- **[Core concept]** (`concepts/name.md`) — one-line synthesis. **Core**
```

---

## Subject File Format

No rigid template — write what would actually help you understand this subject. Useful things to include:

- Who/what it is and its significance to the client
- History and background
- A single **Current Status** section — updated in place, never layered
- Patterns observed across sessions
- Things to handle carefully (sensitivities, boundaries)
- Key moments worth preserving (named sections, not dated status blocks)

**Core principle: reference document, not changelog.**
Context files are portraits, not logs. When something changes, update the existing Current Status section in place. Fold resolved history into the narrative. Preserve significant moments as named subsections (e.g. "The Final Goodbye"), not as "Status as of YYYY-MM-DD" layers. The test: could a new reader understand this person from the file without knowing session dates?

**How to update:** Read the current file first. Update existing sections in place — do not append new "as of" sections. If current status changed, overwrite it. If a significant event happened, add a named subsection. If something previously current is now history, fold it in or remove it. The file should get cleaner over time, not longer.

**Enforcement:** this is easy to state and hard to maintain session-to-session — appending a new dated block is always the path of least resistance. The actual enforcement point is the periodic arc review (`.therapy/protocols/arc-review.md`, "Maintenance: Context File Consolidation"), which checks file length and folds resolved history back into narrative. Don't rely on remembering to do this at every session-end; that's not where it's designed to happen.

---

## When to Create a New Subject File

Create one when a subject has appeared across **at least two sessions** and you find yourself wanting to know more than the session notes capture. When in doubt, create it — a sparse file that grows is better than missing context.

Signals:
- A person mentioned in 2+ sessions with meaningful texture
- A concept the client has named themselves
- A place with recurring significance
- An upcoming event with real emotional weight

Before creating the file, check `context/mentions.md` — if the subject already has prior session pointers logged there, pull that history in and seed the new file with a "Prior mentions" section, then remove the entry from `mentions.md`. Add every new file to `context/index.md` immediately with the correct status.

---

## `context/mentions.md` — Tracking What Hasn't Graduated Yet

A lightweight cross-reference for subjects that have come up in session notes but don't yet have enough depth for their own file. **Not loaded at session start** — it would just be noise at that stage. Only touched at session-end (`.therapy/protocols/session-end.md`, Steps 6–7).

- A passing mention gets a line: `- Name — sessions/YYYY-MM-DD.md`. Repeat mentions append a pointer to the same line rather than creating duplicates.
- A name accumulating multiple pointers without graduating to its own file is itself a signal — worth a periodic glance to see who's ready to be promoted.
- Once a subject is promoted to a real context file, remove its entry from `mentions.md` — this file is a holding area, not a permanent log.

---

## Events

One file per event, named `events/YYYY-MM-DD-[slug].md` once it has a confirmed date. Create one whenever the client mentions something at a specific date and time — appointments, difficult conversations, social events, anything with emotional weight.

**No confirmed date yet? Create it anyway.** Don't wait for a date to lock in — if the client mentions they've been invited to something, is expecting something to be scheduled, or names an event that's real but not yet dated ("training and brunch dates pending," "we're planning a trip sometime this fall"), create the file immediately as `events/pending-[slug].md` (no date prefix) with `**Date:** TBD` and `**Status:** Pending`. This is what catches things like a volunteer brunch whose date gets confirmed two sessions later — without a pending file, that gap between "mentioned" and "dated" is exactly where an event falls through and never gets a file at all.

**Once the date is confirmed:** rename the file from `events/pending-[slug].md` to `events/YYYY-MM-DD-[slug].md`, fill in the real Date/Time, and update Status to Upcoming. Update its `context/index.md` line to match (add the date/time once known).

**Event file format:**
```markdown
# [Event name]

**Date:** YYYY-MM-DD (or TBD)
**Time:** HH:MM (timezone) (or TBD)
**Status:** Pending / Upcoming / Past

## What it is
[Brief description and why it matters]

## Before
[How the client was feeling going in, if discussed]

## After
[How it went, if discussed]

## Threads
[Anything to follow up on]
```

**Index entry format** — include date and time so the therapist persona can reason about timing; for a Pending event, note what's still unknown instead:
```
- **[Event name]** (`events/2026-06-04-example.md`) — 2026-06-04 at 13:00 [timezone]. Active.
- **[Event name]** (`events/pending-example.md`) — date not yet set. Pending.
```

**At session start:** compare event date/time to current time from the hook, if one is configured.
- More than 2 hours before → ask how the client is feeling going in (if it fits naturally)
- Within 2 hours after → ask how it went
- Event passed without being discussed → carry it forward as an unasked question

**At session end:** update the event file with before/after notes. Mark Status as Past once passed. Once an event is Past and fully processed, delete its line from `context/index.md` entirely — the file stays in `context/events/`, which serves as the archive. Past events therefore aren't listed in the index at all; when a past event resurfaces in conversation, list the `context/events/` folder to find its file.

---

## Relationship to `profile.md`

`profile.md` is about the client — their patterns, their history, their growth. Context files are about the world around them. They complement rather than duplicate. If you find yourself writing the same person's name repeatedly in `profile.md`, that's a signal to promote them to their own context file.
