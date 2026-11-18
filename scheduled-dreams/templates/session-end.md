# Session End Protocol

Run every step, in order, when the session ends. No need to ask permission. After the goodbye the client has gone, so work through to the push in one go: don't stop partway to summarize what you've written or to announce the next step. Nobody is there to answer, and a stop leaves the notes half-written.

**Triggers** (any phrasing, any language the client uses — when in doubt, run it): "end session", "goodbye", "bye", "talk later", "talk soon", "I'm going to sleep", "going to bed", "I need to sleep", "that's all for today", "that's enough for today", "I'm done for today". Skipping this loses the session's information for good, so err toward running it. Add the client's own language's equivalents once you notice which ones they actually use.

**Session end writes only the note.** Session end writes the session note, ending in a short **For the next session** block, plus a stub file for a genuinely new subject, then commits. It doesn't touch `profile.md`, `context/index.md` beyond a stub's line, any existing context file, `context/threads.md`, `context/mentions.md`, `context/topic-links.md`, `dreams/flags.md` or `sessions/index.md`. All of that is a dream's job: an ingest (`.therapy/protocols/dream-ingest.md`), then a longform dream (`.therapy/protocols/dream.md`), which rebuild those files from the notes with nothing else going on. Late-night writing in the session's own context is where most of the drift that audits find comes from. How each of those files is written: `.therapy/protocols/file-conventions.md`.

Until a dream covers the note, the startup script keeps it on the startup list and reads its block: the events in it count as near-term events, its threads count as surfaced, its flag answers stop the flag being asked again, the files it names stay loaded, and its handling-rule changes are printed. So the block is what keeps the next greeting right. Write it carefully and keep it mechanical.

Corrections, boundaries and preferences the client gives mid-session still go straight to `.therapy/memory/` the moment they land. That isn't session end, and it doesn't wait.

---

## Step 1 — Close the session warmly

**First, the near-term events the startup script flagged** (if the install raises them). If one never came up this session, raise it briefly before the goodbye: "Before we go — I never got to ask, how are you feeling about [event] tomorrow?" It's the one exception to "no new threads" below, because it closes a loop that was already open.

Then the actual goodbye: one or two sentences. No new threads beyond the event check. Make it feel like a real goodbye.

---

## Step 2 — Write session notes to `sessions/YYYY-MM-DD.md`

**Date rule:** Use the date the session *started*, not the date it ended. If a session begins in the evening and runs past midnight, file it under the start date. Check the first message timestamp.

**End-time rule:** The end time in the header (`[HH:MM]–[HH:MM]`) is the timestamp of the *last message that actually pertains to the session's content* — not the timestamp of whenever the end-session trigger phrase happens to be said. If that time isn't obvious from context, ask rather than guessing.

If multiple sessions occur on the same date, append a letter suffix: `2026-05-31.md`, `2026-05-31b.md`, etc. Check existing files in `sessions/` before writing to avoid overwriting.

```markdown
# Session: [Date], [HH:MM]–[HH:MM]

## Key Themes
- [Main topics discussed]

## Emotional State
- [Observations about affect, mood, energy]

## Moments of Aliveness
- [What brought light, laughter, warmth, or genuine engagement — however small. If the session genuinely had none, write that honestly.]

## Patterns Noted
- [Relevant behaviors or thought patterns observed]

## Exercises/Homework Assigned
- [Specific tasks given]

## Progress on Previous Homework
- [What was assigned, what happened]

## Threads to Revisit
- [Unfinished topics from this session only. Standing threads live in `context/threads.md`, which the dreams keep.]

## Safety Notes
- [Any crisis indicators, safety concerns, or follow-up needed]

## Observations
- [Your observations, hypotheses, what's working]

## Context Touched Today
- [Every person, place, concept, or event from `context/` that came up directly in this session. One line each. The dream works from this list, and it feeds the block's Files touched line — do not skip it.]

## Memory Misses
- [Each time the client had to remind you of something you should already have known: what it was and where it should have come from. "None" if there were none.]

## For the next session
- Events: [YYYY-MM-DD HH:MM · what (`events/file.md`, new stub | date set | after-notes in this note); … — or (none)]
- Threads: [registry title (surfaced | shelved | closed); New: "short title" (therapeutic | logistical); … — or (none)]
- Files touched: [people/x.md, concepts/y.md — or (none)]
- New stubs: [people/z.md — or (none)]
- Flag answers: ["flag title" — answered: their words | asked | dropped — or (none)]
- Profile: [item — confirmed | revised: what changed | review offered and declined — or (none)]
- Handling-rule changes: [file — the rule, in a sentence — or (none)]
```

**The block** is the last section of the note, and the startup script parses it, so keep its shape exactly: the seven lines, in this order, items separated by `;`, `(none)` for an empty line. It records only what happened; the detail stays in the note above it. Leave out a line's content (write `(none)`) for anything this install doesn't have, such as a thread registry or dream flags.
- **Events:** every real event that came up with a date or a changed date, or that happened and now has after-notes, and every new undated plan (`pending`). Upcoming ones are what startup raises as near-term events, so get the date right.
- **Threads:** registry entries that came up (by their exact title), any the client set down or resolved, any they were offered at the greeting, and anything new expected to outlive this session. Startup treats each as surfaced on this note's date, so it isn't re-offered tomorrow.
- **Files touched:** the context files from "Context Touched Today". Startup keeps an Active file loaded for 7 days from this note.
- **New stubs:** the files created in Step 3.
- **Flag answers:** a dream flag asked this session (`.therapy/protocols/dream-flags.md`): its title as in `dreams/flags.md`, and what the client said. Startup won't offer it again; the dream records it.
- **Profile:** profile items the client confirmed or changed live, including in a profile review, and a declined review offer. The longform dream applies them with this note's date as the stamp.
- **Handling-rule changes:** a new or changed boundary, never-say, safety note or way to hold a subject that isn't already in `.therapy/memory/`. Startup prints these, and they outrank older file wording until a dream updates the file.

**The note is the evidence for everything the dream will write.** Every fact, quote, date and attribution that later goes into `profile.md` or `context/` must be findable here, because the dream writes from this note alone. Anything missing from it is lost. So:
- **Quotes are exact.** Quotation marks only for words someone actually said or wrote, copied from the conversation. A paraphrase goes without quotation marks.
- **Say whose words they are.** A line the assistant offered stays the assistant's, even when the client agreed with it. If the client took it up, quote their own reply.
- **Keep the kind of claim.** The assistant's reads are written as reads ("seems to", "the read is"), never as facts about the client. Jokes, hopes and plans stay marked as what they are.
- **Pasted material counts too.** If the client pasted a chat, letter, email or screenshot and a detail from it matters, put that detail in this note, quoted as pasted.
- **Write down what a dream will need.** A status that changed, a date, a decision, a new person's texture: if it's only in the conversation, the dream can't know it.

---

## Step 3 — Create a stub for a genuinely new subject

Only for a subject with **no context file yet** that has to be findable before the next dream: a new person with real texture, a concept the client named themselves, or a real event (dated or not). That's what lets the context-loader hook (if installed) and startup find it the same night. Everything else waits for the dream: an existing file never changes here, however much happened.

Check `context/index.md`, `context/mentions.md` and `context/events/` first; if a file exists, it's not new. A passing mention isn't a stub either: the dream logs it in `mentions.md`.

A stub is short and mechanical:
- **The file**, per `context/GUIDE.md`: the H1, an `aliases:` frontmatter list if the client uses more than one name for it, and one or two lines saying what or who it is, with a pointer to this session note. For an event: `context/events/YYYY-MM-DD-slug.md`, or `pending-slug.md` with `Status: Pending` and `Date: TBD`, plus Date, Time and Status lines. No Current Status write-up and no summary block; the dream builds the file from the note.
- **Its index line** in `context/index.md`, one line in the usual format. Mark it `Active (today)` only if it will matter in the next few days.
- **The block:** list it under New stubs, and an event under Events too.

Most sessions create no stub.

---

## Step 4 — Save (only if this install is a git repo)

**Check what you changed.** Run `git status --short`. It should list the new session note and, at most, the stubs and their index lines from Step 3 (plus any memory file written during the session). If it lists any other file under `context/`, `profile.md`, `dreams/` or `sessions/index.md`, you wrote something a dream owns: undo that change with `git checkout -- <path>`, and make sure the note carries it instead.

**Check the block.** Run `python3 .therapy/scripts/startup.py | head -20`. Any upcoming event in the block should show under Near-term events if it's within two days, and the threads and handling-rule lines should list what you wrote. If the script says the note has no block, fix the block's heading.

```bash
git add -A && git commit -m "Session notes $(date +%Y-%m-%d)" && git pull --rebase --quiet origin main && git push origin HEAD
```

Push to the current branch. The pull picks up anything an ingest landed on `main` while the session ran; the note and stubs are new files, so the rebase goes through cleanly. If it ever stops on a conflict, run `git rebase --abort` and push anyway (`git push origin HEAD`); a rejected push leaves the commit safe locally, and the next session end's pull and push carry it. Without a remote, commit only. Skip if there is genuinely nothing new to commit.

---

## First session only

After closing, add this hint:
> One more thing — if you ever want to adjust how we work together, just ask. I can change my communication style, add therapeutic approaches, or adjust session structure. I can also check for updates to keep my knowledge current.
