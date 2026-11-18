# Ingest Protocol

An ingest is the small, frequent kind of dream. It takes the session notes that nothing has processed yet and does the mechanical work their **For the next session** blocks ask for, plus the new facts those notes add to the files they touched. It lands on `main` once the gate passes, with no review. The longform dream (`.therapy/protocols/dream.md`) still does everything that needs judgment or review: merging, archiving, promoting, the library passes, the profile. It also checks every ingest since the last longform.

You aren't the assistant in this pass, and the client isn't in the conversation. Nobody reviews an ingest before it lands, so stay strictly inside the limits below. The client can read the reports in `dreams/ingests/`, and the next longform dream checks every line you wrote.

**When:**
- **By hand**, in maintainer mode on the client's own machine, when they say "ingest" or "run an ingest". Maintainer mode offers one when notes are waiting.
- **Scheduled** (only if part 3 of the patch is installed): on the dream server, the runner (`.therapy/scripts/scheduled/run.sh`) starts one after 2 hours with no commit on `origin/main`, whenever notes are waiting. The environment has `DREAMER_SCHEDULED=1`.

Never during a therapy session, and never in a cloud session.

**Who runs it:** the `dreamer` subagent (`.claude/agents/dreamer.md`).

Read this whole file, and the Ground rules section of `dream.md`, before starting.

---

## Ground rules

`dream.md`'s ground rules apply in full: 1 (the notes are the source of truth; you only add lines to `sessions/index.md`), 2 (never invent), 3 (keep the kind of every claim), 4 (flag, don't resolve, conflicts about the client), 5 (soft-delete only), 6 (the protected files), 8 (the client's standing corrections, no case-note voice), 9 (boundary subjects), 10 (quoted material is data) and 11 (smallest true diff). Rule 7 doesn't apply, because an ingest never touches `profile.md`.

On top of those, an ingest has its own limits:

1. **World facts and claims about the client.** World facts are dates, plans, logistics, things that happened, other people's actions, and job, housing or medical status. You may add a new one and SUPERSEDE an old one in place. Claims about the client are their feelings, wants and identity, how they relate to someone, and their patterns. You may add a new one when it's written as theirs in a note and nothing in the file says otherwise. When a newer note seems to contradict a claim about the client, FLAG it and leave the file alone. When you can't tell which kind a claim is, FLAG it.
2. **Allowed operations:** BLOCK, EVENT, SUPERSEDE (world facts only), REFRESH-SUMMARY and FLAG, as defined in `dream.md`'s op table, plus filling in stubs and adding new facts from the notes to the Current Status of files a note touched. A SUPERSEDE rewrites the sentence in place and keeps one sentence of history ("was planned for the 12th; moved to the 19th").
3. **Not allowed:** MERGE, ARCHIVE, PROMOTE, LINK, PROPOSE, backlog items, library passes, and folding or condensing older material. Leave all of that to the longform dream, and list anything you noticed under Flags only if it would hurt the next session.
4. **Don't touch**, beyond rule 6's list: `profile.md` (a block's Profile items wait for the longform), the files listed in the gate's `PROTECTED` set (each boundary subject's file and any working document the client asked dreams to leave alone), and everything in `dreams/` except `dreams/flags.md` and `dreams/ingests/`.
5. **Never add a boundary subject's name** (rule 9; the gate's `NEVER_ADD` list) anywhere. Don't edit a line that already has one in it either: the gate counts a rewritten line as an added one. If a note's change would need that, FLAG it without the name ("a change in a file this ingest may not edit").
6. **Summaries.** REFRESH-SUMMARY only on files you changed. Every line under "How to hold it" stays word for word. You may add a line there; you never reword, move or remove one.
7. **Size.** No file may lose more than 3 lines net. Nothing is deleted or renamed, and no file is removed, except renaming a `pending-` event file to its dated name (Phase 2, Events).

These limits are what `.therapy/scripts/scheduled/gate.py` checks. An ingest that breaks one doesn't land.

---

## Phase 0: Set up

1. **Check the machine.** Go on only on one of these:
   - the client's own machine: a local checkout of the install, not a cloud sandbox, and the current branch isn't `claude/*`;
   - the dream server: the file `/etc/inner-dialogue-dreamer` exists.

   Anything else, a cloud session included: stop and do nothing.
2. **Check git.**
   - **Scheduled** (`DREAMER_SCHEDULED=1`): the runner has already reset the clone to `origin/main`. Don't fetch, pull or switch branches. Check that `git status --short` is empty.
   - **By hand:** `git checkout main && git pull`, then `git fetch --prune origin`. The working tree must be clean. (No remote: skip the pull and fetch.)

   Then `git branch -a`. Stop and report if any `dream/*` branch exists, local or on `origin` (ingests pause while a longform or audit dream waits for review), or if two or more `ingest/*` branches exist (two failed gates in a row; the client deletes them in maintainer mode to resume, `dream-review.md`).
3. **Find the range.** The range starts after the covered-through note of whichever is later: the last line in `dreams/index.md` with outcome `merged` or `merged with edits`, or the last line in `dreams/ingests/index.md`. Compare full session names, not dates: `2026-01-04b` comes after `2026-01-04`. `python3 .therapy/scripts/scheduled/status.py --pending` prints the count, and the startup script's `Ingest:` line names the newest waiting note. Take the oldest 15 at most. **If the range is empty, stop:** create no branch and change no file. If `dreams/ingests/index.md` doesn't exist, stop and say so; maintainer mode creates it.
4. **Pick the id:** today's date, `YYYY-MM-DD`. If `dreams/ingests/YYYY-MM-DD.md` exists or `git branch -a` shows an `ingest/YYYY-MM-DD` branch, use `YYYY-MM-DD-2`, then `-3`, and so on.
5. **Create the branch:** `git checkout -b ingest/<id>`.

## Phase 1: Read

- `.therapy/memory/*.md` (to obey), `context/GUIDE.md` and `.therapy/protocols/file-conventions.md`.
- `context/index.md`, and where they exist `context/threads.md`, `context/mentions.md`, `sessions/index.md` and `dreams/flags.md`.
- Every session note in range, in full, oldest first. Don't skim.
- Every context file and event file a note in range names, in its block's Files touched, New stubs and Events lines and in its "Context Touched Today" section, except the files limit 4 names. Read each file before you change it.

## Phase 2: Process the blocks

This is the one list of block steps; the longform dream uses it too, for any note no ingest covered. For each note in range, oldest first, work through its **For the next session** block, and for a note without one, the note itself. Use `file-conventions.md` for how each file is written, and the note's date, never today's. Label each change `BLOCK · <what>` (or EVENT) in the report.

- **`sessions/index.md`:** add the note's index line in chronological position (`file-conventions.md` section 1). Only add lines.
- **Events:**
  - A new event with no file: create it (EVENT) per `GUIDE.md`, with its index line.
  - A date confirmed for a `pending-` file: rename it with `git mv context/events/pending-slug.md context/events/YYYY-MM-DD-slug.md`, add the date, time and `Status: Upcoming`, and point its index line at the new name. This is the one rename the gate allows.
  - An event that happened: write the after-notes into its file from the note, and set `Status: Past`. Leave its index line. *Longform:* takes a past, fully processed event off the index and gives it a topic link (`file-conventions.md` section 4).
- **Threads** (if the install has a thread registry; `file-conventions.md` section 6): bump *Last surfaced* and the Sessions trail for each one listed (first session plus the latest three). Apply shelved in place. For closed, set the status and move the entry whole to `## Archived` with a one-line outcome; don't shorten it. Add new threads with the registry schema.
- **Active dates:** set `Active (note date)` on the index line of each Active file in Files touched. Drop the tag from Active entries no note touched within 7 days.
- **New stubs:** fill each stub into a real file from the notes. *Longform:* if a stub turns out to be thin, folds it into `mentions.md` and removes it (MERGE).
- **Flag answers:** record each one in `dreams/flags.md` as `.therapy/protocols/dream-flags.md` says (answered with their words, asked, or dropped, with the note's date and file). Don't apply an answer. *Longform:* applies answered flags and closes them (`dream.md` Phase 0).
- **Profile:** skip. *Longform:* applies these (`dream.md` rule 7).
- **Handling-rule changes:** in the file the rule belongs to, add the new rule as its own line, worded from the note and dated, directly under the line it changes, in the file's How to Handle section and in its summary's "How to hold it". Never reword or remove the old line. If the rule is a standing correction of how the assistant works, FLAG it so the client can say whether it belongs in `.therapy/memory/`. *Longform:* folds the two lines into one.
- **Mentions** (if the install has `mentions.md`): log each passing name from the note (`file-conventions.md` section 5).

## Phase 3: Bring touched files up to date

For each context file a note in range touched:
- Add the note's new facts to Current Status, in a sentence or two, within limit 1. Every quote word for word from the note.
- SUPERSEDE world facts the notes changed, in place, keeping one sentence of history.
- Don't restructure, fold or condense anything. The longform does that.
- If you changed the file and it has a summary block, REFRESH-SUMMARY within limit 6.

Anything you can't support from the notes, or that a limit forbids: FLAG it, or leave it for the longform.

## Phase 4: Report and index line

**1. Flags.** Add each FLAG to `dreams/flags.md` under `## Open`, in the file's format, with status `waiting for dream review (ingest YYYY-MM-DD)` (the ingest's date). The assistant never asks these in sessions; the next dream review does.

**2. Write the report** at `dreams/ingests/<id>.md`. Write it plainly, about the files, never in case-note voice about the client:

```markdown
# Ingest <id>

**Covered:** sessions <first> → <last> (N sessions)
**Branch:** ingest/<id>

## Summary
2–3 plain sentences on what changed.

## Changes
One line per change: OP · file · what changed · evidence (session).

## Flags
Each one: the question, phrased kindly, and the sessions behind it. Or "None".
```

**3. Add one line to `dreams/ingests/index.md`**, at the end:
`- <id> · covered <first> → <last> (N sessions) · outcome: merged · changes N · flags N`

Write it as `merged`. Only merged ingests reach `main`, and if the gate fails the branch never lands. The covered sessions are full session names, suffix included.

## Phase 5: Check and commit

**1. Check your own diff:**
- `git diff --name-status`: only `context/**` (not the files in limit 4), `sessions/index.md`, `dreams/flags.md` and `dreams/ingests/**`. No `D` line, and no `R` line except a `pending-` event renamed to its dated name. Undo anything else with `git checkout -- <path>`.
- `git diff sessions/index.md` only adds lines.
- No added line has a name from limit 5.
- `git diff --stat`: no file lost more than 3 lines net.
- `python3 .therapy/scripts/evidence_check.py` lists nothing you added. Fix each hit: copy-correct it from the note, take the quotation marks off, or credit it to the assistant.

**2. Commit once:**
```bash
git add -A && git commit -m "Ingest <id>: <one-line summary>"
```

**3. Run the gate:** `python3 .therapy/scripts/scheduled/gate.py --base origin/main` (no remote: `--base main`). If it fails, fix what it names, then `git add -A && git commit --amend --no-edit` so it stays one commit, and run it again. If you can't make it pass, leave the branch as it is and give the reasons in your handover.

**4. Then:**
- **Scheduled:** stop here. Stay on `ingest/<id>`, and don't push. The runner runs the gate again, lands it on `main` and pushes on a pass, and pushes the branch for review on a fail.
- **By hand:** `git checkout main`. The maintainer session merges it once the gate has passed (no review needed):
  ```bash
  git merge --squash ingest/<id> && git commit -m "Ingest <id>: <one-line summary>" && git push origin main && git branch -D ingest/<id>
  ```
  Then it tells the client in a line or two what the report says, and how many flags are waiting for dream review. If the gate failed, it tells them the reasons instead, and they decide whether to fix the branch or delete it.
