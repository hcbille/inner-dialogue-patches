# Session End Protocol

Run this in full when the session ends. Do not skip steps. Do not defer. Do not ask permission.

**Triggers** (any phrasing, any language the client uses — when in doubt, run it): "end session", "goodbye", "bye", "talk later", "talk soon", "I'm going to sleep", "going to bed", "I need to sleep", "that's all for today", "that's enough for today", "I'm done for today". Skipping this loses information permanently — err toward running it. Add the client's own language's equivalents once you notice which ones they actually use.

---

## Step 1 — Close the session warmly

One or two sentences. No new threads. Make it feel like a real goodbye.

---

## Step 2 — Write session notes to `sessions/YYYY-MM-DD.md`

**Date rule:** Use the date the session *started*, not the date it ended. If a session begins in the evening and runs past midnight, file it under the start date. Check the first message timestamp.

**End-time rule:** The end time in the header (`[HH:MM]–[HH:MM]`) is the timestamp of the *last message that actually pertains to the session's content* — not the timestamp of whenever the end-session trigger phrase happens to be said. If the client ends a session live, those are usually the same moment. But if the end-session command is invoked later (a different day, after other sessions have already happened in between), use the real last-relevant-message time, not the command's timestamp. If that time isn't obvious from context, ask rather than guessing.

If multiple sessions occur on the same date, append a letter suffix: `2026-05-31.md`, `2026-05-31b.md`, etc. Check existing files in `sessions/` before writing to avoid overwriting.

```markdown
# Session: [Date], [HH:MM]–[HH:MM]

## Key Themes
- [Main topics discussed]

## Emotional State
- [Observations about affect, mood, energy]

## Moments of Aliveness
- [What brought light, laughter, warmth, or genuine engagement — however small. This is data about what a good life looks like for them, not decoration. If the session genuinely had none, write that honestly.]

## Patterns Noted
- [Relevant behaviors or thought patterns observed]

## Exercises/Homework Assigned
- [Specific tasks given]

## Progress on Previous Homework
- [What was assigned, what happened]

## Threads to Revisit
- [Unfinished topics, questions to return to]

## Safety Notes
- [Any crisis indicators, safety concerns, or follow-up needed]

## Observations
- [Your observations, hypotheses, what's working]

## Context Touched Today
- [List every person, place, concept, or event from `context/` that came up directly in this session. One line each. This list drives steps 5–6 below — do not skip it.]
```

---

## Step 3 — Add to `sessions/index.md`

2–3 lines max: what the session was about, what emerged or shifted, pointers to context files where relevant. Keep it scannable.

**Insert the entry in chronological position by session start time — never blindly append.** Same-day sessions sort by start time, and a past-midnight session files under its start date and slots in accordingly. (The index can drift out of order over time; placing the entry correctly is part of the write.)

---

## Step 4 — Update `profile.md` if new insights emerge

`profile.md` is a quality reference document about who the client is — their patterns, history, and how they work. It is **not** a session log.

**Date every write to current-state content** per `.therapy/profile-protocol.md` — a trailing italic `*(YYYY-MM-DD)*` on new or materially revised current-state entries, refreshed only when the client re-confirms it live, never bulk-refreshed. `Background` and formative history stay undated by design. A dated profile is what lets a stale inference get caught and checked instead of read back as timeless truth. If `.therapy/profile-protocol.md` doesn't exist, skip this — a pre-feature install.

**What belongs:**
- Core beliefs and schemas (updated when meaningfully revised, not just restated)
- Foundational history that explains current functioning
- Newly identified triggers or coping mechanisms
- Updated **Current Focus** — keep this accurate; remove resolved threads, add new ones
- Progress markers and what's working therapeutically
- A "Things to Never Do" section, if one exists — always preserve intact

**What does NOT belong:**
- Session-specific incidents — those go in session notes
- Specific messages or exchanges — those go in session notes or context files
- Dated "last updated" bullets
- Duplicate content that lives in a context file — keep profile.md as a pointer, not a copy

**How to update:** Read the current file first. Match the existing prose style. Default to updating existing sections rather than appending. Consolidate rather than fragment.

**Principles:**
- Quality over accumulation. Don't append session incidents.
- Keep Current Focus accurate — this section decays fastest.
- **Pointer test:** before writing more than ~2 sentences about a subject that has (or warrants) a context file, stop — the depth goes in the context file, profile gets a brief pointer to it instead. Applies to every section, including new ones.
- Preserve any "Things to Never Do" section exactly. Never trim or rephrase without explicit instruction.
- Match existing prose style and section structure.
- Create a new H2 only when a coherent theme recurs across multiple sessions and no existing section fits.

---

## Step 5 — Work through the "Context Touched Today" list

For each item on the list:
- If it has a context file: read it, then update if anything significant shifted.
- If it doesn't have a context file but has enough depth: create it and add to `context/index.md`.
- Update `context/index.md`: refresh the Active date for items directly relevant today; add entries for new files.

Do not proceed to step 6 until every item has been checked.

**Active date maintenance:**
- For any `Active (YYYY-MM-DD)` entry directly relevant today → update the date to today.
- For any `Active (YYYY-MM-DD)` entry more than 7 days old and *not* relevant today → remove the Active status entirely (keep the entry, drop the tag).
- For any **event** entry that is Past, with its after-notes written and threads closed → delete the line from the index entirely. The event file stays in `context/events/` — the folder is the archive; list it if a past event ever resurfaces.

For context file conventions, formats, and creation signals, see `context/GUIDE.md`.

---

## Step 6 — Review for additional new context files

Beyond the "Context Touched Today" list, scan the full session for subjects that have appeared across multiple sessions without their own file and now have enough depth. **When in doubt, create the file.** A sparse file that grows is better than context that gets lost.

Signals: a person mentioned in 2+ sessions with meaningful texture, a concept the client has named themselves, a place with recurring significance, an upcoming event with real emotional weight. Before creating the file, check `context/mentions.md` for prior pointers to this subject — if found, seed the new file with a "Prior pointer" section linking back to those sessions, then remove the entry from `mentions.md`. Add each new file to `context/index.md` immediately.

**Events get their own check, with a lower bar than people/concepts — and no date required.** Any real, upcoming event that came up today — an appointment, a social plan, a training, a party — gets a file immediately, per `context/GUIDE.md`'s Events section, even from a single mention and **even before a date is confirmed.** If the date is known, create `context/events/YYYY-MM-DD-[slug].md`. If it isn't yet, create `context/events/pending-[slug].md` with `Status: Pending` and `Date: TBD` rather than waiting. Add it to `context/index.md` either way.

Also check two things each time: (1) whether a Pending event's date got confirmed today — if so, rename the file to the dated format, fill in Date/Time, update Status to Upcoming, and fix its index line; (2) whether an event confirmed in an *earlier* session still doesn't have a file at all. Catch both gaps here rather than letting them linger.

---

## Step 7 — Log brief mentions

For any person, place, or concept that came up today *without* enough depth to warrant Step 5 or Step 6 (a passing reference, not yet substantive) — log it to `context/mentions.md`: `- Name — sessions/YYYY-MM-DD.md`. If the name already has an entry, append today's session pointer rather than duplicating the line.

This is what lets a name that keeps recurring without ever quite being "enough" get caught and promoted later, instead of being lost to memory.

---

## Step 8 — Save to GitHub (only if this vault is a git repo)

```bash
git add -A && git commit -m "Session notes $(date +%Y-%m-%d)" && git push origin HEAD
```

Push to the current branch. Skip if there is genuinely nothing new to commit, or if this vault isn't version-controlled at all — that's a valid setup too, just skip this step silently.

---

## First session only

After closing, add this hint:
> One more thing — if you ever want to adjust how we work together, just ask. I can change my communication style, add therapeutic approaches, or adjust session structure. I can also check for updates to keep my knowledge current.
