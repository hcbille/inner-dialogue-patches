# INSTALL — Scheduled Dreams Patch

This guide moves an install with dreams one step further: session end writes only the session note, and dreams write every other file. It has three parts, and only the last one needs a server:

1. **Session end writes only the note.** The note ends in a **For the next session** block that the startup script reads. Longform dreams, still run by hand, write everything else.
2. **Ingests.** A small, frequent dream that does a note's mechanical work and lands with no review once a gate script passes it. You run it by hand in maintainer mode. No server is needed.
3. **Scheduled on a server.** A Linux machine that's always on (a home server, a VM, a container) runs ingests by itself after two quiet hours, plus longform dreams when they're due. It pushes longform dreams as branches for review.

Do the parts in order. **Parts 1 and 2 are self-contained:** they run on the client's own machine, like the rest of Inner Dialogue. Stop after part 1 or 2 if the client doesn't want their notes on a second machine.

The guide is written for files that have **diverged** from the reference setup, so every change is anchored on a *concept* to find, not a line number. If you're an assistant reading this in maintainer mode: work through it against *this* setup's actual files. Adapt names and pronouns, and don't assume the reference structure matches yours.

---

## Terminology mapping (do this first)

The templates say "the assistant" and "the client" (they/them). Replace "the client" with whatever this setup calls the person, in their real pronouns, and "the assistant" with the assistant's name where it reads better. The paths are the same as in the `dreaming` patch's INSTALL.md. New ones:

- `.therapy/protocols/file-conventions.md` (part 1): how the standing files are written, moved out of session end.
- `.therapy/protocols/dream-ingest.md`, `.therapy/scripts/scheduled/` and `dreams/ingests/` (part 2).

## Prerequisites (check, don't assume)

- **The `dreaming` patch, parts 1–3**, with at least one longform dream merged (`dreams/index.md` has a line with outcome `merged`). Before the first merged dream, the startup script has no starting point for "notes no dream has covered", so it would keep none of them on the list. Part 3 of `dreaming` ("session end captures") is what part 1 here replaces.
- **The `base` patch's `evidence_check.py`** (`.therapy/scripts/evidence_check.py`, 2026-11-11 or later, with `--commit`). Since dreams now write every quote, the dream and the gate both run it.
- **The startup script** from `opus-5-5-rebaseline` with the `dreaming` additions (`startup-dream-additions.py`), or one shaped like it.
- **A git repo working on `main`.** For part 3, also a remote both machines can reach (GitHub or similar).
- **Optional patches** this one touches if they're installed: `thread-registry`, `no-topic-greeting-offer`, `near-term-event-surfacing`, `context-loader`, and the stock profile review (`.therapy/profile-protocol.md`). Each step says what to skip when one is missing.

## Decisions to make with the client first

Record the answers in the log entry.

1. **How far to go.** Part 1 only, parts 1–2, or all three. Part 3 puts a full copy of the notes on a second machine and gives that machine push access to the repo. Some clients won't want that, and parts 1–2 work fine without it.
2. **Boundary subjects** (part 2). Ingests land unreviewed, so the gate refuses any change to certain files and any added line with certain names. List the subjects the client has asked the assistant never to raise first (`dreaming`'s rule 9), their files, and any working document the client asked dreams to leave alone. These go in `gate.py`'s `PROTECTED` and `NEVER_ADD`.
3. **Where the server runs** (part 3). A machine the client controls, always on, on a network they trust. Not a cloud sandbox that keeps transcripts. Decide whether it's backed up. The reference deliberately leaves it out of backups: the repo is the backup, and every backup is another copy of the notes.

---

## Part 1 — Session end writes only the note

Session end used to write the note and then update the index, profile, context files, mentions and threads, late at night, in the session's own context. Audits in the reference install found that this is where most drift came from. After this part, session end writes the note, a seven-line block at its end, and at most a stub for a genuinely new subject. The dream does the rest from the notes.

The block keeps the next greeting right in the meantime. The startup script reads the block of every note no dream has covered:
- its events count as near-term events;
- its threads count as surfaced;
- a flag answered in it isn't offered again;
- a file it names stays loaded for 7 days;
- its handling-rule changes are printed, and they outrank older wording.

### 1.1 Move the file rules out of session end

1. Copy `templates/file-conventions.md` to `.therapy/protocols/file-conventions.md`.
2. Open this install's session-end protocol and find the steps that write files other than the note: the sessions index, the profile update, the "Context Touched Today" walk-through, new context files and events, brief mentions, and the thread registry. Carry anything those steps say that the template doesn't (install-specific conventions, extra rules) into the matching section of `file-conventions.md`. Readdress it to the dream: "the session the note is from" instead of "today".

### 1.2 Rewrite the session-end protocol

`templates/session-end.md` is the reference version. If this install's protocol is still close to the `base` template, replace it with the template and carry over anything install-specific: trigger phrases in the client's language, a linking convention, extra note sections. Otherwise, change it concept by concept:

1. **Add the "Session end writes only the note" paragraph** and the one after it (what the startup script reads from the block) near the top.
2. **The note template:** add `## Memory Misses` if it's missing, then `## For the next session` as the last section, with its seven lines. Add the paragraph after the template that explains each line. For an install without a thread registry or dream flags, those lines are simply always `(none)`.
3. **The evidence paragraph:** reword it so the note is the evidence for everything *the dream* will write.
4. **Remove the steps 1.1 moved out.** In their place comes Step 3, "Create a stub for a genuinely new subject", from the template.
5. **The save step:** add "Check what you changed" and "Check the block" from the template. Add `git pull --rebase --quiet origin main` before the push (only needed for part 3, harmless before it). The evidence check moves to the dream, so remove it here.
6. **Near-term events** (`near-term-event-surfacing`): keep Step 1's event check as it is.

### 1.3 The startup script

`templates/startup-ingest-additions.py` has part 1 blocks and part 2 blocks. For now, paste the part 1 blocks only:

- **Block 1A (constants):** next to the dreaming constants. Delete `UNDREAMED_MAX`: every undreamed note now stays on the list, because until a dream it's the only record.
- **Block 1B (functions):** `context_entries()`, `near_events()`, `recent_sessions()`, `dream_status()` and `askable_flag()` **replace** the script's own. `pending_notes()`, `_items()`, `blocks()` and `reading_list()` are new. If the script's versions have install-specific additions (summaries, extra checks), keep those and add only the new parameters and lines.
- **Block 1C (main):** follow its comments. Build everything through `reading_list()`, replace the dreaming patch's BLOCK C with the new lines, and change two wordings. If `main()` builds more than the template (summary blocks, a profile-review line), move that into `reading_list()`. If there's a profile-review status line, pass it `blk["declines"]`.

Test:

```bash
python3 .therapy/scripts/startup.py; echo "exit $?"
```

- The reading list matches what it was before, plus every undreamed note.
- In a scratch copy (or a throwaway note you delete afterwards), give an undreamed note a block with an event dated tomorrow, a thread, a handling-rule change and a Files touched line naming an expired Active file. Startup should show the event under Near-term events, print the thread and rule lines, and load the file. A note without a block is listed as such.
- `python3 .therapy/scripts/dream_metrics.py` still runs.

### 1.4 The longform dream (`dream.md`)

The dream now does everything session end used to, from the blocks. Find each concept in `.therapy/protocols/dream.md`:

1. **The intro paragraph** that says session end only captures. Replace it with:

   > **Session end writes only the note.** Each note ends with a **For the next session** block (events, threads, files touched, new stubs, flag answers, profile confirmations, handling-rule changes), and session end creates at most a stub file and its index line for a genuinely new subject. Everything else is this protocol's job: the `sessions/index.md` line, event files, thread bumps, Active dates, flag answers, profile stamps, and every change to an existing context file. Expect context files to lag their notes; that's the design, not a failure. Until a dream covers them, the startup script keeps every undreamed note on the startup list and reads its block. How each file is written: `.therapy/protocols/file-conventions.md`.

2. **Rule 1** (session notes are the source of truth): "Nothing in `sessions/` changes **except `sessions/index.md`, where you add each note's index line** (Process the blocks)."
3. **Rule 6** (don't touch): the `sessions/` item becomes "`sessions/`, except adding lines to `sessions/index.md`". After the profile stamps item, add "(…a note's block recording one is that confirmation, rule 7)".
4. **Rule 7** (profile is propose-only). Replace with:

   > **`profile.md` is propose-only, with one exception.** Write each proposed change in the report under "Profile proposals", with the exact current text, the proposed text and the evidence, and don't edit the file. The exception: an item a note's block lists under **Profile** as confirmed or revised by the client live. Apply that one, using the client's words from the note, with the note's date as its stamp, label it `BLOCK · PROFILE` in the report, and touch nothing else in the bullet. A never-do section is never edited this way; a change there is always a proposal. A block's "review offered and declined" becomes the `<!-- profile review offered and declined: YYYY-MM-DD -->` marker, with the note's date.

5. **Rule 11** (smallest true diff): point "Edit, don't append" at `file-conventions.md` instead of `session-end.md`, and add "Growth from processing the blocks (index lines, new threads, event files) is expected."
6. **Phase 0, applying answered flags:** before it, add "First record every **Flag answers** item from the blocks of the notes in range in `dreams/flags.md`, as `.therapy/protocols/dream-flags.md` says (answered, asked or dropped, with the note's date and file)."
7. **Phase 1 reading:** read `.therapy/protocols/file-conventions.md` instead of the session-end steps. The regions come from the notes' "Context Touched Today" sections **and their blocks' Files touched and New stubs lines**.
8. **The op table:** add a row:

   > | **BLOCK** | The mechanical items from a note's block (Process the blocks, below): an index line in `sessions/index.md`, a thread bump, an Active date, a flag answer, a profile confirmation (rule 7), a stub filled in. Label it `BLOCK · <what>` in the report. |

   Make the EVENT row's trigger "a dated, upcoming event in range that has no file yet (from a block's Events line, or a note that mentions one the block missed)".
9. **Before the region checklist**, add:

   > **Process the blocks first.** For each note in range, oldest first, work through its **For the next session** block (for a note without one, the note itself), using `file-conventions.md` and the note's date, never today's:
   > - **`sessions/index.md`:** add the note's index line, in chronological position.
   > - **Events:** create the file for each new one (EVENT), set a confirmed date (rename `pending-` to the dated name and fix its index line), and write after-notes into the event file. Past, fully processed events come off the index, with a topic link if the install has them.
   > - **Threads:** bump *Last surfaced* and the Sessions trail for each one listed; apply shelved and closed; add the new ones with the registry schema.
   > - **Active dates:** set `Active (note date)` on the index line of each Active file in Files touched; drop the tag from Active entries no note in range touched within 7 days.
   > - **New stubs:** fill each stub into a real file from the notes, or, if it turns out to be thin, fold it into `mentions.md` and remove the stub and its line (MERGE).
   > - **Flag answers:** recorded in Phase 0; apply them like any answered flag.
   > - **Profile:** apply the confirmations and revisions (rule 7).
   > - **Handling-rule changes:** update the file the rule belongs to and its summary block. If the rule is a standing correction of how the assistant works, FLAG it so the client can say whether it belongs in `.therapy/memory/`, which you never edit.
   > - **Mentions:** log each passing name from the note in `mentions.md`.
   >
   > Then the region checklist.

10. **Phase 5, checking the diff:** allow `sessions/index.md` (added lines only), count BLOCK items as a reason a file grew, and add:

    > Run `python3 .therapy/scripts/evidence_check.py`. Every quote you added must be word for word in a note; the dream now writes every quote, so this check moved here from session end. Fix each one it lists: copy-correct it from the note, take the quotation marks off, or credit it to the assistant.

### 1.5 The other files

- **`dream-review.md`:** in the rule check, `sessions/index.md` may be listed (added lines only). Under profile proposals, add: "The `BLOCK · PROFILE` changes in the report are the client's already, confirmed live in the session the note is from (`dream.md` rule 7). Show them first so they can check the wording, then go through the proposals." Count BLOCK items among the reasons a file grew.
- **`dream-flags.md`** (if installed): answers go on the block's **Flag answers** line (the flag's title, then `answered:` and their words, `asked` or `dropped`), not into `dreams/flags.md`. The dream records them there.
- **`.therapy/profile-protocol.md`** (if it has a review): the client's answers and a declined offer go on the block's **Profile** line. The dream applies them with the note's date; the startup script counts a declined review at once.
- **`context/GUIDE.md`:** wherever it says session end updates Active dates, event files, topic links or summaries, say the dream does it from the notes (`file-conventions.md`), and session end only creates stubs.
- **CLAUDE.md:**
  - The reading-list description: "The list also includes every session note no dream has covered yet. Session end writes only the note, so until a dream consolidates them, those notes are where the newest facts live, and they outrank older wording in `context/` and `profile.md`. The script reads each note's **For the next session** block and prints what it says: events, threads surfaced, handling-rule changes."
  - Thread registry (if installed): the greeting offer's "update the offered threads' *Last surfaced* date" becomes "list the offered threads in the note's block at session end, which is what counts as surfacing them". The standing-threads check's "mark it Shelved" becomes "record it as shelved in the note's block".
  - The session-end line: "Session end writes only the session note, ending in its For the next session block, plus a stub for a genuinely new subject. Every other file is written by a dream."
- **Arc review** (if installed): anywhere it relies on session end keeping files current, point it at the dream.

### 1.6 Run it

Run one or two real sessions. After each, check that `git status` before the commit showed only the note (and any stub), and that the next startup printed the block's events and threads. Then run a longform dream and review it as usual. Its report should open with `BLOCK ·` changes. Watch whether "Dream: overdue" starts appearing: from five undreamed notes on, the next sessions read a lot of notes. If it appears often, part 2 is the fix.

---

## Part 2 — Ingests (still no server)

After part 1, the context files lag their notes until someone runs a longform dream. An ingest closes that gap cheaply. It does each note's block items, adds the notes' new facts to the files they touched, and lands without review once `gate.py` passes it. The longform dream checks every ingest afterwards. In part 2 the client runs ingests by hand in maintainer mode, for example once after each evening session, or whenever maintainer mode says notes are waiting.

### 2.1 Copy the files

| Template | Goes to |
|---|---|
| `templates/dream-ingest.md` | `.therapy/protocols/dream-ingest.md` |
| `templates/scheduled/gate.py` | `.therapy/scripts/scheduled/gate.py` |
| `templates/scheduled/status.py` | `.therapy/scripts/scheduled/status.py` |
| `templates/dreams-ingests-index.md` | `dreams/ingests/index.md` |

In `status.py`, set `SCHEDULED = False` until part 3.

### 2.2 Configure the gate

In `gate.py`, fill in decision 2: `PROTECTED` with the boundary subjects' files and any working document dreams must leave alone, and `NEVER_ADD` with the boundary names and aliases, lowercase. Mirror them in `dream-ingest.md`'s limits 4 and 5 if this install describes them by name anywhere. Both may stay empty if the client has no boundary subjects.

If the install has more files an ingest must never change (a second profile-like file, say), add them to `PROTECTED` too.

### 2.3 The startup script

Paste the part 2 blocks of `templates/startup-ingest-additions.py`:

- **Block 2A:** replace `DREAM_DUE_SESSIONS`, `DREAM_DUE_DAYS` and `DREAM_OVERDUE_SESSIONS` with the new values, and add the ingest constants. Keep `DREAM_DUE_BYTES` as tuned. With ingests doing the daily work, a longform dream is due every five sessions or ten days.
- **Block 2B:** `pending_notes()` and `dream_status()` **replace** the part 1 versions. The rest is new.
- **Block 2C:** the `Ingest:` line in `main()`, and the wording change.

Test:
- `python3 .therapy/scripts/startup.py`: with notes waiting, an `Ingest: N notes not yet ingested` line.
- `python3 .therapy/scripts/scheduled/status.py`: four health lines. `--pending` prints a number.

### 2.4 The longform dream (`dream.md`)

1. **The intro paragraph from 1.4.** After its first sentence, replace "Everything else is this protocol's job…" with:

   > Everything else is a dream's job, and there are two kinds:
   > - **Ingest** (`.therapy/protocols/dream-ingest.md`): it does the block items and adds the notes' new facts to the files they touched, within strict limits, and lands on `main` once its gate passes.
   > - **Longform** (this file): every few days, it checks the ingests since the last longform, does what an ingest may not (merging, archiving, promoting, profile confirmations, the backlog and library passes), and lands only through review.

2. **When / due.** Add: "**Due:** at least 5 sessions after the last merged longform's covered-through note and at least 5 days since that longform; or at least 10 days since it with at least 1 new session; or the startup list over the byte threshold. The startup script's `Dream:` line applies this rule."
3. **Phase 0, check git:** a failed ingest branch waiting for review (`git branch -a --list '*ingest/*'`) doesn't stop a longform; mention it in the handover.
4. **Phase 0, find the range.** Add: "Ingests don't move this point: their lines are in `dreams/ingests/index.md`. Sort the notes in range into two sets. A note is **ingested** when it falls inside the Covered range of a line in `dreams/ingests/index.md`; its block items are already done, and Phase 3 checks them. Every other note is **un-ingested** (normally none), and Phase 3 processes its block."
5. **Phase 0, flags.** Record block flag answers only for the un-ingested notes (ingests recorded the rest). Apply answered flags, including ones an ingest recorded. Then add: "Flags an ingest raised have status `waiting for dream review (ingest YYYY-MM-DD)`. Check each against the notes. If the notes settle a world fact it asks about, apply it, mark it `closed` with the evidence, and list it in the report. Otherwise leave its status and list it under the report's Flags, so the review asks the client."
6. **Phase 1 reading:** add "The report of every ingest since the last longform (`dreams/ingests/`), and its commit."
7. **The op table:** add a row:

   > | **INGEST-FIX** | A line an ingest wrote is wrong, missing or outside its limits. Fix it, and label it `INGEST-FIX · file · what · evidence` in the report. |

8. **Replace "Process the blocks first"** (from 1.4) with:

   > **First, check the ingests.** Check every ingest since the last merged longform against the notes it covered. Find them in `dreams/ingests/index.md` and with `git log --oneline --grep "^Ingest "` since the last longform's commit. For each one, read `git show <sha>` and check every line it added or changed:
   > - it traces to a note it covered, quotes word for word, with the kind of claim kept (rules 1–3);
   > - it stays inside the ingest's limits (`dream-ingest.md`, Ground rules): a world fact superseded, never a claim about the client; every "How to hold it" line intact;
   > - the block items for each note it covered are all done and right.
   >
   > Fix what's wrong or missing, and list each fix under the report's `## Ingest fixes`. A clean ingest gets one line there saying so.
   >
   > **Then process the blocks.** For each un-ingested note in range, oldest first, follow `.therapy/protocols/dream-ingest.md`, Phase 2 (Process the blocks), with the longform additions marked there, and without the ingest's limits: your own ground rules apply. For the ingested notes, do the parts an ingest leaves to you:
   > - **Profile:** apply each block's confirmations and revisions (rule 7).
   > - **Flag answers:** apply the answers the ingests recorded (Phase 0).
   > - **Events:** take past, fully processed events off the index, with a topic link if the install has them.
   > - **New stubs:** fold a stub that turned out thin into `mentions.md` and remove it (MERGE).
   > - **Handling-rule changes:** where an ingest added a new rule beside the line it changes, fold the two into one, in the file and its summary.

9. **The report template:** add `## Ingest fixes` (one line per fix, or one line per clean ingest) before `## Changes`.

### 2.5 Review, the dreamer, commands

- **`dream-review.md`:**
  - It now covers longform and audit dreams. Ingests land by themselves when the gate passes.
  - In the walk-through, show the report's `## Ingest fixes` first. Each one corrects a line that's already on `main` and in the startup reading. If one ingest needed many fixes, say so: it may be worth undoing, or tightening `dream-ingest.md`.
  - Under flags, also go through every flag with status `waiting for dream review (ingest …)`. Ingests raise these, and the assistant never asks them in sessions.
  - Add two sections at the end:

  > ## Undoing an ingest
  >
  > When an ingest that landed on `main` is wrong enough that fixing it line by line isn't worth it: find its commit (`git log --oneline --grep "^Ingest <id>"`), then `git revert <sha> && git push origin main`. The revert also removes the ingest's report and its line in `dreams/ingests/index.md`. Add a line to `.therapy/maintainer-notes.md` saying which ingest and why. If it was the newest ingest, its notes count as unprocessed again and the next ingest redoes them. If later ingests have landed since, the next longform dream processes their blocks instead, so offer one soon.
  >
  > ## Failed ingests
  >
  > An ingest whose gate failed stays on an `ingest/<id>` branch (pushed to `origin` when the server ran it). After two, ingests stop until the client clears them; `status.py` says so in maintainer mode.
  >
  > 1. List them: `git fetch --prune origin && git branch -a --list "*ingest/*"`. Look at the oldest first.
  > 2. See why it failed: `git checkout ingest/<id> && python3 .therapy/scripts/scheduled/gate.py --base "$(git merge-base main HEAD)"`. The report on the branch, `dreams/ingests/<id>.md`, shows what it tried to change.
  > 3. Tell the client in a few plain lines what it tried and why the gate stopped it. Then, their call:
  >    - **Fix it:** make the change that satisfies the gate on the branch, `git add -A && git commit --amend --no-edit`, re-run the gate, squash-merge it onto `main` as `dream-ingest.md` Phase 5 says, and delete the branch (and its remote copy).
  >    - **Delete it:** `git checkout main && git branch -D ingest/<id>` (and `git push origin --delete ingest/<id>` if it's on the remote). Its notes are still unprocessed, so the next ingest tries them again.
  >
  > If the same notes fail twice for the same reason, the problem is probably in `dream-ingest.md` or the gate; note it in `.therapy/maintainer-notes.md`.

- **`.claude/agents/dreamer.md`** (`dreaming` part 2): the description names three kinds (ingest, longform, audit). The prompt decides the instruction set: "Run an ingest…" → `dream-ingest.md` (which relies on `dream.md`'s ground rules and op table, so read those too). It commits once on `ingest/<id>` or `dream/YYYY-MM-DD` and never merges or pushes `main`. An ingest branch isn't pushed; the maintainer session merges it after the gate. For an ingest, the handover says whether the gate passed, and its reasons if not.
- **`.therapy/commands.md`**, under the dream commands:

  > - **"ingest"** / "run an ingest": launch the `dreamer` subagent with the prompt "Run an ingest per .therapy/protocols/dream-ingest.md." It leaves a local `ingest/<id>` branch and runs the gate. If the gate passed, squash-merge it as `dream-ingest.md` Phase 5 says (no review needed), and tell the client in a line or two what its report says. If it failed, tell them the reasons and let them choose to fix or delete the branch. Never during a therapy session.

  And for "undo the last dream", add: "For an ingest, 'Undoing an ingest'; for a failed ingest branch, 'Failed ingests'."
- **Maintainer mode's status step:** after the `Dream` line, also run `python3 .therapy/scripts/scheduled/status.py` and mention, in the same line, notes waiting for an ingest (offer one), failed ingest branches, and dream branches waiting for review.
- **`dream_metrics.py`:** after the "Undreamed sessions" line, add one more:

  ```python
      waiting = startup.unprocessed_sessions()
      ingest = startup.last_ingest()
      print(f"- Not yet ingested: {len(waiting)}"
            + (f" ({waiting[0][:-3]} → {waiting[-1][:-3]})" if waiting else "")
            + (f"; last ingest {ingest[0]}, covered through {ingest[1]}" if ingest else "; no ingest yet"))
  ```

- **CLAUDE.md:**
  - Session end: "Every other file is written by an ingest (`.therapy/protocols/dream-ingest.md`) or a longform dream (`.therapy/protocols/dream.md`)."
  - Dream flags: "The 'Dream: due' and 'Ingest:' lines are for maintainer mode only; never mention dreams or ingests in a therapy session."
  - The other-protocols list: "**Dreams** (maintainer mode only): ingests, `.therapy/protocols/dream-ingest.md`; longform dreams, `.therapy/protocols/dream.md`, reviewed with `.therapy/protocols/dream-review.md`."
- **`context/GUIDE.md`:** the ingest keeps Active dates and event after-notes. The longform dream takes past events off the index, adds topic links and folds files; ingests never fold.

### 2.6 Run the first ingest with the client

After a session, in maintainer mode, say "ingest". Read the report together, and the diff if they want. Then check:
- `python3 .therapy/scripts/scheduled/gate.py --base main` passed before the merge;
- after the merge, `startup.py` no longer lists that note as waiting, and the files it touched read right.

Try one failing case on a scratch branch too: an ingest commit that deletes a file should fail the gate with a reason naming the file.

---

## Part 3 — Scheduled on a server (optional)

This part needs a Linux machine that's always on, with systemd, and that the client controls. A small VM or container on a home server is enough: the runner is a shell script, two Python scripts and Claude Code. Every 15 minutes, a timer:
1. fetches the repo into a disposable clone and resets it to `origin/main`;
2. waits for a quiet window: 2 hours with no commit on `main`;
3. pauses while a `dream/*` branch waits for review, and stops at two failed `ingest/*` branches;
4. runs an ingest when notes are waiting, gates it, and either lands it on `main` or pushes the branch for review;
5. then runs a longform dream if one is due, and pushes its `dream/*` branch for review.

The agent runs with an allow-list of tools: local git only, no push, fetch or reset, no reading credentials, and no edits to `.git`, `.claude` or the scripts. Only the runner pushes, and a pre-push hook in the clone refuses any other push. The log records times, kinds, ranges and counts, never note content. A successful run's transcript is deleted at once, and a failed one's after 7 days.

### 3.1 Set up the machine (as root)

1. **A system with systemd**, and `git`, `python3`, `flock` and `timeout` (`util-linux` and `coreutils` on Debian and Ubuntu), plus `curl`. Keep security updates on (`unattended-upgrades` or similar).
2. **A firewall** that drops incoming traffic except SSH from the local network. The runner only makes outgoing connections, to the git remote and to the Claude API.
3. **An unprivileged user** to run the dreams, e.g. `dreamer`, with lingering on so its timer runs while nobody is logged in: `loginctl enable-linger dreamer`.
4. **The marker file** the protocols' machine check looks for: `echo "Scheduled dreams for this install" > /etc/inner-dialogue-dreamer`.
5. **Backups:** decide per decision 3. If the machine is backed up, every backup holds a copy of the notes.

### 3.2 As the dream user

1. **Claude Code:** install it for this user (the native installer, or npm into `~/.local`), and put `~/.local/bin` on `PATH`.
2. **A token:** on any machine where the client is signed in, `claude setup-token` prints a long-lived token. Put it on the server as one line `CLAUDE_CODE_OAUTH_TOKEN=…` in `~/.config/dreamer/env`, and `chmod 600` it (the directory 700). The client pastes it in; the assistant shouldn't see or print it. Check the file by shape only (one line, mode 600). The runs count against the client's own Claude usage.
3. **A deploy key** for the repo: `ssh-keygen -t ed25519 -f ~/.ssh/dreamer_deploy -N ''`, then an `~/.ssh/config` entry for the git host using it. The client adds the public key to the repo's deploy keys **with write access** (the runner pushes `main` and review branches). Use a deploy key rather than the client's own key, so access is limited to this one repo and can be revoked on its own.
4. **Clone** the repo to `~/vault` (or set `DREAMER_REPO` everywhere).
5. **Install the runner files in the repo** first (3.3), then run `bash ~/vault/.therapy/scripts/scheduled/install.sh`. It installs the push guard and the systemd units and checks the rest. It doesn't enable anything.
6. **One test tick:** `systemctl --user daemon-reload && systemctl --user start dreamer.service`, then `tail ~/dreamer.log`. Expect `tick · skip · not quiet` or `quiet; nothing to ingest`.
7. **Turn it on:** `systemctl --user enable --now dreamer.timer`.

### 3.3 Files in the repo

On the client's machine, copy into `.therapy/scripts/scheduled/`: `run.sh`, `pre-push`, `dreamer.service`, `dreamer.timer` and `install.sh` (next to `gate.py` and `status.py` from part 2). Set `SCHEDULED = True` in `status.py`. Commit and push, then pull on the server.

Check `run.sh`'s settings against this install: the clone path, the quiet window (`DREAMER_QUIET_SECS`, default 2 hours) and the agent timeout. The allow-list (`ALLOWED_TOOLS`) covers the protocols' own commands. If this install's protocols run other scripts, add them there. Don't widen it to `Bash(*)`.

Check `.github/workflows/` (or the host's equivalent) for anything that auto-merges branches by name. `ingest/*` and `dream/*` must not match.

### 3.4 The client's machine

1. **Pull at session start.** Copy `templates/session-pull.sh` to `.claude/session-pull.sh` and register it as a SessionStart hook in `.claude/settings.json`:

   ```json
   "SessionStart": [
     { "hooks": [ { "type": "command", "command": "bash \"$CLAUDE_PROJECT_DIR/.claude/session-pull.sh\"" } ] }
   ]
   ```

   It fast-forwards `main` silently, so the session reads what the server's ingests landed. On any problem it does nothing, and the startup script reads the waiting notes' blocks as before. In CLAUDE.md's startup step, add: "(A SessionStart hook has already pulled `main`, so anything an ingest landed is in.)"
2. **Session end** already pulls with rebase before pushing (1.2, step 5). That's what keeps a session's push from colliding with an ingest that landed during the session.
3. **`dream-ingest.md` and `dream.md`:** in their "When" sections, mention the scheduled runner (`DREAMER_SCHEDULED=1` in the environment). The template `dream-ingest.md` already has it. In `dream.md`:
   - Phase 0's machine check accepts the server (`/etc/inner-dialogue-dreamer` exists).
   - In scheduled mode the clone is already reset, so it doesn't fetch, pull or switch branches.
   - At the commit step: "**Scheduled mode:** commit only. Don't push, and don't switch branches; the runner pushes the `dream/` branch." The handover is the report itself.
   - Use `"${TMPDIR:-/tmp}"` for the metrics file, since `$TMPDIR` isn't always set on Linux.
4. **`dreamer.md`:** in scheduled mode, commit and stop on the branch: no push, no switching branches. The server's shell is bash, so commands must work in both zsh and bash (quote patterns and revisions like `"HEAD^"`).
5. **`dream-review.md`:** a dream the server ran exists only on `origin`, so start the review with `git fetch --prune origin`, then `git checkout dream/YYYY-MM-DD`. Failed ingests are on `origin` too; the runner's log is `~/dreamer.log` on the server.
6. **`commands.md`:**
   - Maintainer mode's status step also mentions `status.py`'s warning when a note has waited over 24 hours, which usually means the server is down or its timer is off.
   - Add a command:

   > **"turn scheduled dreams off"** / "on": the runner is a systemd user timer on the dream server. Off: `ssh <server> 'systemctl --user disable --now dreamer.timer'`. On: `ssh <server> 'systemctl --user enable --now dreamer.timer'`. Run it only when the client asks, and log it. While it's off, notes wait for a by-hand ingest.

7. **CLAUDE.md:** the session-end line can now say ingests run "by themselves after two quiet hours".

### 3.5 Watch the first week

- After the first session, `status.py` in maintainer mode should show the note ingested about 2 hours later, and `~/dreamer.log` should show `ingest · merged`.
- Read the first few ingest reports with the client.
- When the first scheduled longform dream appears as a `dream/*` branch, review it as usual. Its `## Ingest fixes` section is the best measure of whether ingests can be trusted.

---

## Updating an install that already has dreams

Nothing to update. This patch is new as of 2026-11-18, and the `dreaming` patch itself didn't change. An install with `dreaming` parts 1–3 can start at part 1 here.

## Verify

- Part 1: a session's commit holds only the note (and any stub); the next startup prints its block; the next longform dream reports `BLOCK ·` changes and passes `evidence_check.py`.
- Part 2: an ingest passes the gate and lands; `startup.py` stops listing its notes; a deliberately bad ingest commit fails the gate with reasons naming files, never content.
- Part 3: `~/dreamer.log` shows ticks; a plain `git push` from the server's clone is refused by the pre-push hook; an ingest lands on `main` about 2 hours after a session.

## Log entry

Add a dated entry to `.therapy/maintainer-notes.md`: which parts were installed, the decisions (how far, the boundary lists by file, where the server runs and whether it's backed up), and anything skipped because a file didn't exist.

## Known limits

- The gate checks shape (paths, deletions, sizes, boundary names, "How to hold it" lines, quotes). It can't check that a sentence is true. The longform dream's ingest check is what catches that, so keep longform dreams going.
- Ingests are prompt-bound like every dream. The reference ran them on Claude Opus; a smaller model is more likely to cross a limit, and the gate then stops it.
- The runner is written for Linux with systemd. It hasn't been tried with launchd or Windows Task Scheduler.
- Between a session and its ingest, a second session reads the first note in full (it's on the list). With part 3 that window is a few hours; with part 2, it lasts until someone runs an ingest.
