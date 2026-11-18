# File Conventions

How the standing files are written: `sessions/index.md`, `profile.md`, the context files, `mentions.md` and `context/threads.md`. These used to be session-end steps. Now session end writes only the note and its block, and **a dream** writes these files from the notes: an ingest, inside its limits (`.therapy/protocols/dream-ingest.md`, Phase 2, "Process the blocks"), then a longform dream for the rest (`.therapy/protocols/dream.md`). Read "today" below as "the session the note is from", and "this note" as the session note the change comes from. Every rule here is still bound by the dream's ground rules: in particular `profile.md` stays propose-only, except for the live confirmations a note's block records (`dream.md`, rule 7).

> **Installing:** this template is the reference install's version, written generically. If this install's old session-end steps had rules of their own (a linking convention, extra sections, a different index format), carry them over into the matching section below rather than dropping them. Skip the sections for files the install doesn't have.

**Edit, don't append.** The session note is the only log. Every other file here is read at the start of later sessions, in full or through its summary, so every sentence added costs every future session. Hold to these rules:

- **Replace, don't stack.** When something changed, find the sentence it supersedes and rewrite that sentence. Never add a bolded `**YYYY-MM-DD: …**` update after the old text, and never add a dated paragraph that restates a still-true claim with a new date.
- **Current state outside the session note.** "What's true now" goes in `profile.md`, `context/index.md`, `context/threads.md` and summary blocks. The blow-by-blow stays in the session note, which is always one link away.
- **Earn the line.** A new sentence needs something that didn't exist before: a new fact, a changed status, a new handling rule, or a moment significant enough to name. "It came up again" belongs in the session note, plus a *Last surfaced* bump.
- **Size check before the commit** (`dream.md`, Phase 5; `dream-ingest.md`, Phase 5).

---

## 1. `sessions/index.md`

2–3 lines max (about 400 characters): what the session was about, what emerged or shifted, pointers to context files where relevant. A table of contents, not a summary of the note. Quotes and detail stay in the note.

**Insert the entry in chronological position by session start time, never blindly append.** Same-day sessions sort by start time, and a past-midnight session files under its start date.

---

## 2. `profile.md`

`profile.md` is a reference document about who the client is: their patterns, history, and how they work. It is **not** a session log. Only the longform dream writes it, and only as rule 7 allows: proposals for review, plus confirmations the client gave live and a note's block records.

**Date every write to current-state content** per `.therapy/profile-protocol.md` (if installed): a trailing italic `*(YYYY-MM-DD)*` on new or materially revised current-state entries. In a dream, a stamp comes only from the client's live confirmation, which is the date of the note whose block records it (or of the dream review where they confirmed it), never the dream's own date, and never bulk-refreshed. Background and formative history stay undated.

**What belongs:** core beliefs and schemas (when meaningfully revised), foundational history that explains current functioning, newly identified triggers or coping mechanisms, an accurate **Current Focus**, progress markers, and any "Things to Never Do" section, always preserved intact.

**What does not:** session-specific incidents, specific messages or exchanges, dated "last updated" bullets or bolded dated updates, and content that lives in a context file (keep a pointer, not a copy).

**How to update:** read the current file first and match its style. Change only what the note's block records; rewrite that one bullet in place with its stamp. Don't restructure, trim or tidy other bullets; the longform dream proposes those changes and the client confirms them in review.

---

## 3. Context files touched (the note's "Context Touched Today" list)

Everything written here follows the evidence rule (`session-end.md`, Step 2): only what the note holds, quotes word for word.

For each item on the list:
- If it has a context file and its **status** changed (something happened, a decision was made, a date moved): update the Current Status in place, in one or two sentences. An ingest doesn't restructure, condense or fold older material; the longform dream does that. A passing mention changes nothing in the file, because the session note already records it.
- If that file has a summary block (`<!-- summary -->`) and the note changed a **handling rule** (a boundary, a never-say, a safety note, how to hold the subject), update the summary in the same dream.
- Update `context/index.md`: each entry stays one line (name, who or what, current status, ≤ ~400 characters). When the status changes, replace the status clause; never append a dated update to the line.

**Active date maintenance:**
- For any `Active (YYYY-MM-DD)` entry a note touched → set the date to that note's date.
- For any `Active (YYYY-MM-DD)` entry more than 7 days old that no note touched → remove the Active status (keep the entry, drop the tag).
- For any **event** entry that is Past, with its after-notes written and threads closed → the longform dream deletes the line from the index (section 4).

For context-file formats and creation signals, see `context/GUIDE.md`.

---

## 4. New context files and events

Session end only creates stubs. The dream fills each stub into a real file from the notes, and creates a file for a subject that has now appeared across several notes with real depth. Before creating one, check `context/mentions.md` for prior pointers: seed the new file with a "Prior pointer" section linking back to those sessions, and remove the entry from `mentions.md` (longform only; an ingest doesn't promote).

**Events have a lower bar, and no date required.** Any real, upcoming event in a note gets a file: `context/events/YYYY-MM-DD-[slug].md` when dated, `context/events/pending-[slug].md` with `Status: Pending` and `Date: TBD` when not. When a pending event's date is confirmed, rename the file to the dated form (`git mv`), fill in Date/Time, set Status to Upcoming, and fix its index line. After it happens, write the after-notes and set Status to Past.

**Past events come off the index** (longform only): once an event is Past and fully processed, delete its index line. The file stays in `context/events/`, which is the archive. If the install has topic links (`context/topic-links.md`), give it a link in the same dream using the words the client used for it, since otherwise nothing can reach that file. An ingest does neither; it leaves past events on the index.

---

## 5. Brief mentions (`context/mentions.md`)

For any person, place, or concept that came up *without* enough depth for its own file (a passing reference), log it: `- Name — sessions/YYYY-MM-DD.md`. If the name already has an entry, add this note's pointer rather than duplicating the line. This is what lets a name that keeps recurring get caught and promoted later.

---

## 6. The thread registry (`context/threads.md`)

The registry is the home for standing threads to revisit (see its own header). An ingest reconciles it from each new note; the longform dream checks it.

1. **Bump what was touched.** For any entry a note lists, set **Last surfaced** to the note's date and add the note to its **Sessions** list, keeping the first session and the latest three. If where the thread stands changed, replace the one sentence it supersedes, with the date in parentheses inside the sentence. Don't append a dated line under the description, and don't rewrite the whole description; the longform dream does fuller rewrites from the Sessions trail.
2. **Add genuinely new standing threads** from the block's `New:` items, using the schema in the registry header: Type, Opened and Last surfaced (the note's date), Subjects, Sessions, a 1–3 line description, and a Surfacing rule.
3. **Close what resolved.** Set **Status: Closed (date)** and move the entry whole to `## Archived` with a one-line outcome.
4. **Shelve what the client set down.** Set **Status: Shelved (date)** and adjust its Surfacing rule so only a rare "does this still feel rightly shelved?" is allowed.
5. **Promotion is the longform dream's job** (`dream.md`, PROMOTE).
