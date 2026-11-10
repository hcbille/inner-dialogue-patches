# INSTALL — Dreaming Patch

This guide adds "dreams" to an Inner Dialogue install. A dream is offline consolidation of the memory files: it runs in maintainer mode, works on its own git branch, and is reviewed with the client before it lands.

The guide is written for files that have **diverged** from the reference setup, so every change is anchored on a *concept* to find, not a line number. If you're an assistant reading this in maintainer mode: work through it against *this* setup's actual files. Adapt names and pronouns, and don't assume the reference structure matches yours.

There are five parts. **Do them in order, and don't do part 3 until at least one dream has been run and reviewed** (two or three is better). Part 3 changes how session end works, so it should only happen once dreams have proven themselves.

---

## Terminology mapping (do this first)

The reference setup calls the assistant **Sage**. The templates say "the assistant" and "the client" (they/them). Before applying anything:

- Replace "the client" with whatever this setup calls the person, in their real pronouns. Replace "the assistant" with the assistant's name where it reads better.
- Map each reference path to this setup's equivalent:
  - `CLAUDE.md`: always-loaded instructions
  - `.therapy/commands.md`: maintainer mode and the commands
  - `.therapy/protocols/session-end.md`
  - `.therapy/scripts/startup.py`: from the `opus-5-5-rebaseline` patch
  - `.therapy/memory/`: the client's standing corrections
  - `profile.md`, with its never-do list
  - `context/index.md`, `context/GUIDE.md`, and, if installed, `context/threads.md` (`thread-registry` patch), `context/mentions.md` (`base` patch) and `context/topic-links.md` (`context-loader` patch)
  - `.therapy/maintainer-notes.md`

  Where one doesn't exist, skip the steps that depend on it and say so in the log entry.

## Prerequisites (check, don't assume)

- **The install is a git repo with a remote, working on `main`.** Dreams are git branches; review and undo are git operations. Check with `git remote -v` and `git branch --show-current`. If there's no remote, dreams still work locally; drop the `git push` lines.
- **Maintainer mode exists** (`base` patch, `commands-additions.md`). Dreams only run from there.
- **Session notes have a "Context Touched Today" list** (`base` patch, `session-end.md`). The dream uses it to know which files to look at.
- **For part 3 only:** the `.therapy/scripts/startup.py` script from `opus-5-5-rebaseline`.
- **Auto-merge workflows.** Check `.github/workflows/` for anything that auto-merges branches by name (the reference auto-merges `claude/**`). Dream branches are named `dream/YYYY-MM-DD`. Confirm that no workflow matches that pattern. If one does, pick a different prefix everywhere in the templates.

---

## Decisions to make with the client first

Ask these in maintainer mode, and record the answers in the log entry. They change what gets installed.

1. **Who reviews a dream?** The diff is always reviewed in maintainer mode. Optionally, the assistant may also ask flagged questions gently in normal sessions: one per session, at a lull, never in a heavy session. *If no:* skip `dream-flags.md`, the CLAUDE.md flags bullet, and the "Dream flags" lines in the startup script.
2. **Should dream reports be visible?** The reference keeps them in a visible `dreams/` folder at the repo root. The alternative is `.therapy/dreams/`, which is hidden in Obsidian. If the client wants them hidden, change every `dreams/` path in the templates and in the startup additions.
3. **Profile edits.** The reference rule is that dreams only ever *propose* changes to `profile.md`, and the client confirms them in review. Keep this unless the client explicitly wants otherwise. It's the strongest guard against a dream rewriting how the client is described.
4. **Where dreams run.** The reference refuses to run a dream in a cloud session (only the client's own machine). Keep this if the install is used from cloud or mobile sessions too.

---

## Part 1 — Manual dreams and review (MANDATORY)

### 1.1 Copy the templates

| Template | Goes to |
|---|---|
| `templates/dream.md` | `.therapy/protocols/dream.md` |
| `templates/dream-review.md` | `.therapy/protocols/dream-review.md` |
| `templates/dream-flags.md` | `.therapy/protocols/dream-flags.md` (only if decision 1 is yes) |
| `templates/dreams-index.md` | `dreams/index.md` |
| `templates/dreams-flags.md` | `dreams/flags.md` |

### 1.2 Adapt `dream.md` to this install

- **Rule 6 (don't touch):** list this install's real paths for the safety protocol, persona, protocols, scripts and the profile's never-do section.
- **Rule 9 (boundary subjects):** read the profile's never-do list, `.therapy/memory/`, and any index line saying "load only if the client raises it". Name the boundary subjects *by file path* in rule 9, so the dream knows which files they are. Don't write about their content in the rule.
- **Rule 8:** if the install has a memory file about narration or case-note voice, point to it here.
- **Phase 1 and the region checklist:** delete the lines for files this install doesn't have (threads, mentions, topic links, wikilinks, summary blocks).
- **Phase 4** runs the startup script. If there isn't one yet, replace it with "read the files CLAUDE.md's session startup lists, as the next session would".
- **Phase 0, step 1:** if the install is only ever used on one machine, you can name its path explicitly (the reference checks the vault path).
- If the client chose hidden reports (decision 2), change the paths.

### 1.3 Add the commands

In `.therapy/commands.md`, add a section near maintainer mode:

```markdown
## Dreams (maintainer mode only)

A dream is offline consolidation of the memory files, reviewed before it lands.

- **"dream"** / "run a dream": follow `.therapy/protocols/dream.md`. Only in maintainer mode, only on the client's own machine, never during a therapy session.
- **"review the dream"**: follow `.therapy/protocols/dream-review.md`.
- **"undo the last dream"**: the "Undoing a merged dream later" section of `dream-review.md`.
- **"show my dream flags"**: read `dreams/flags.md` and go through the open ones with the client, recording answers as in `dream-review.md` §4.
```

### 1.4 Add Memory Misses to the session note

In the session-end protocol's session-note template, add a section after "Context Touched Today":

```markdown
## Memory Misses
- [Each time the client had to remind the assistant of something it should already have known: one line saying what it was and where it should have come from (a file, a summary, a topic link). Write "None" if there were none. The next dream uses these to fix what wasn't reachable.]
```

If decision 1 is yes, add this line after the template:

> **Dream flags:** if a dream flag from `dreams/flags.md` was asked this session (`.therapy/protocols/dream-flags.md`), record the client's response there now, as that file says.

### 1.5 Run the first dream with the client

In maintainer mode, say "dream". The first dream covers the last 10 sessions. Then follow `dream-review.md` together with the client, region by region. Expect the first dream to be mostly tightening: index lines, thread descriptions, duplicate mentions, and context files that fell behind.

---

## Part 2 — The dreamer subagent (recommended)

A dream reads a lot: every session note in range, plus every file it changes. Running it in its own context window keeps the maintainer session clean for the review.

1. Copy `templates/dreamer.md` to `.claude/agents/dreamer.md`. It needs Claude Code with subagent support. `model: opus` uses the strongest model, since nobody is waiting on it.
2. In `dream.md`, the "Who runs it" paragraph already describes the subagent and the fallback. Nothing to change.
3. In `.therapy/commands.md`, change the "dream" line to:

   ```markdown
   - **"dream"** / "run a dream": launch the `dreamer` subagent (Agent tool, `subagent_type: dreamer`) with the prompt "Run a dream per .therapy/protocols/dream.md." It follows `.therapy/protocols/dream.md` in its own context and returns a short handover. Then tell the client the handover in plain words and offer the review (`dream-review.md`). If the subagent isn't available, run `dream.md` here instead. Only in maintainer mode, only on the client's own machine, never during a therapy session.
   ```

4. **Agents load when a session starts.** The session that creates the file can't call it. Test it in the next maintainer session. With no new sessions since the last dream, Phase 0 should stop cleanly and report an empty range. That's a cheap wiring test.

---

## Part 3 — Session end captures, dreams consolidate (after 1–3 good dreams)

This is the part that actually lightens session end. Session end keeps only *capture*: the note, the index line, and time-critical updates. Everything else moves to the dream. To make sure nothing is lost in between, the startup script keeps undreamed session notes on the reading list.

### 3.1 Slim the session-end protocol

Find each concept below in this install's session-end protocol and change it.

1. **Add this block** near the top, after any "edit, don't append" rules:

   > **Capture now, consolidate later.** Session end *captures*: the note, the index line, and only the small, time-critical updates the next session can't do without. *Consolidation* belongs to the dream, which runs separately in maintainer mode (`.therapy/protocols/dream.md`). That covers rewriting and condensing context files, refreshing summaries, tidying the profile, promoting mentions and threads, topic links, and folding history. Until a dream covers this session, the startup script keeps the session note on the startup list, so nothing captured here is lost in between. When unsure whether something belongs here, ask: would the next session greet the client wrongly without it? If yes, write it now. If no, leave it to the dream.

2. **Profile step.** Replace the "how to update" guidance with:

   > Change only what today actually changed: a status the client reported, something they confirmed, a new trigger or insight they named. Rewrite that one bullet in place, with today's stamp. Don't restructure, trim or tidy other bullets; the dream proposes those, and the client confirms them in review. Most sessions change a sentence or two, or nothing.

3. **Context step** (the "Context Touched Today" walk-through). Replace the per-file update rule with:

   > If it has a context file and its **status** changed today (something happened, a decision was made, a date moved), update the Current Status in place, in one or two sentences. Don't restructure, condense or fold older material; the dream does that from the session notes. A passing mention changes nothing in the file.

   If summary blocks exist:

   > Update a summary block now only if today changed a **handling rule** (a boundary, a never-say, a safety note, how to hold the subject). A wrong greeting rule can't wait for a dream. Other summary refreshes are the dream's job.

   Keep creating new context files and event files at session end. That's cheap, and the context-loader hook needs the files to exist. Keep the Active-date maintenance.

4. **Topic links**, if the `context-loader` patch is installed. Replace the topic-link paragraph with:

   > **Topic links are the dream's job.** If the hook missed a file today (the client called a subject by a word it didn't know), say so in the note's Memory Misses section, naming the word and the file. The next dream adds the link. The exception: if you just deleted a past event's line from the index, add its topic link now, since otherwise nothing can reach that file.

5. **Thread registry**, if installed:
   - In "bump what was touched", replace "rewrite its description" with: "replace the one sentence it supersedes; the dream does fuller rewrites."
   - Replace the "promote what outgrew the file" step with: "Promotion is the dream's job. Don't promote here."

6. **Remove any "fold as you go" rule.** Folding is consolidation.

### 3.2 Add the dream lines to the startup script

Open `templates/startup-dream-additions.py`. It has three blocks:

- **Block A (constants):** paste next to the script's other constants. Check that the script already imports `re` and defines `ROOT`, `parse_date()` and `SESSION_RE`. The `opus-5-5-rebaseline` script does.
- **Block B (functions):** **replace** the existing `recent_sessions()` with the whole block. The new `recent_sessions()` behaves the same as before, plus the undreamed sessions.
- **Block C:** in `main()`, after the last status line (expired Active entries) and before the reading list. Remove the leading `#` and one space from each line, keeping the 4-space indentation. Leave out the four "Dream flags" lines if decision 1 was no.

Copy `templates/dream_metrics.py` to `.therapy/scripts/dream_metrics.py`, next to `startup.py`. It imports the startup script and prints every number a dream report records, measured the same way each time. Adapt `SIZED_FILES` (the files whose size the report tracks) to this install. Lines for things this install doesn't have (a thread registry, `mentions.md`, summary blocks) are left out on their own.

Tune `DREAM_DUE_BYTES` to this install. Run `python3 .therapy/scripts/dream_metrics.py` and read its "Startup list bytes" line. Set the threshold about 10% above today's number, so it only fires on real growth.

Test it (all must pass):

```bash
python3 .therapy/scripts/startup.py; echo "exit $?"
```

- With no merged dream, it prints `Dream: no merged dream yet…`.
- After the first merged dream with no newer sessions, it prints `Dream: not due (… 0 undreamed)`.
- If `dreams/flags.md` has an open flag, it prints a "Dream flags" line naming it.
- The reading list is unchanged apart from undreamed session notes being added.
- `python3 .therapy/scripts/dream_metrics.py` exits 0 and prints a "Startup list bytes" line. If it says startup.py is missing something, a block above wasn't pasted in.

### 3.3 CLAUDE.md

Find each concept and add the matching wording:

1. **The session-startup step that runs the script.** Add to its description: "…whether a dream is due, and whether a dream flag can be asked."
2. **The line about recent session notes on the reading list.** Add:

   > The list also includes every session note no dream has covered yet (up to six). Session end only captures, so until a dream consolidates them, those notes are where the newest facts live. They outrank older wording in `context/` and `profile.md`.

3. **Session continuity** (only if decision 1 is yes). Add a bullet:

   > **Dream flags.** If the startup script names a dream flag that may be asked, you may ask that one flag, once, gently, at a neutral lull. Never in a heavy session, never if the client brought something of their own that's still unfolding, and never in a session where another piece of housekeeping (open-thread offer, standing-threads check, profile review, arc review) was offered. Follow `.therapy/protocols/dream-flags.md`. A "Dream: due" line is for maintainer mode only; never mention dreams in a therapy session.

4. **Session end.** Add:

   > Session end captures (the note, the index line, time-critical updates). Consolidation of the files happens separately in a dream (`.therapy/protocols/dream.md`), run from maintainer mode.

5. **The other-protocols list.** Add a pointer: "**Dreams** (maintainer mode only): `.therapy/protocols/dream.md`, reviewed with `.therapy/protocols/dream-review.md`. The reports live in `dreams/`."

### 3.4 Maintainer mode offers a due dream

In `.therapy/commands.md`'s maintainer-mode steps, after the confirmation line, add:

> Check the dream status: run `python3 .therapy/scripts/startup.py | grep "^Dream"`. If it says due, mention it in one line after the confirmation ("Also: a dream is due — N sessions since the last one. Want to run it?"). Don't run it unasked.

### 3.5 Update the references to where consolidation happens

- In `dream.md`, nothing to change. It already assumes session end only captures.
- **Arc review** (if installed): anywhere it says session end keeps summaries current, or promotes threads, change it to say dreams do that.
- **Context guide** (`context/GUIDE.md`): the same, for summaries, topic-link maintenance and folding. Point at `dream.md`.
- In `dream-flags.md`, nothing to change if it's installed.

---

## Part 4 — Audit dreams (optional, after part 3)

A regular dream only reads sessions since the last dream. An established install has months of older notes that no dream has read, and context files that were built from them one session end at a time and never checked since. An **audit dream** goes back over them: a few context files per run, checked claim by claim against the session notes they came from. It uses the same rules, branch, report and review as a regular dream. It checks accuracy: unsupported claims, drifted quotes, stale statuses. Completeness for big files stays with the regular dreams.

It needs part 3: the picker script imports the startup script's `session_files()` and `last_dream()`.

### 4.1 Copy the files

| Template | Goes to |
|---|---|
| `templates/dream-audit.md` | `.therapy/protocols/dream-audit.md` |
| `templates/audit_next.py` | `.therapy/scripts/audit_next.py` |
| `templates/dreams-audit.md` | `dreams/audit.md` |

Part 1's `dream-review.md` and part 2's `dreamer.md` templates already know about audits (the unsupported-claims walk, the `-audit` branch). If this install copied them before 2026-11-09, re-apply the "Audit dreams" paragraph in `dream-review.md` §3, the rejected-audit sentence in §6, and the audit lines in `dreamer.md`.

### 4.2 Adapt

- **`dream-audit.md`:** map the paths, as in part 1. Its rules lean on `dream.md`'s ground rules by name (the boundary-subjects rule, the protected files), so check that those names match this install's `dream.md`.
- **`audit_next.py`:** check `FOLDERS` against this install's `context/` subfolders. The budgets (`FILE_BUDGET` 150 KB of notes per file per run, `RUN_BUDGET` 450 KB per run) suit Opus. Lower them if the dreamer runs on a smaller model.
- If the install has no summary blocks or no Core/Active statuses, the tiers still work. Everything just lands in tiers 3 and 4.

### 4.3 Add the commands

In `.therapy/commands.md`'s dreams section:

```markdown
- **"audit dream"** / "run an audit": launch the `dreamer` subagent with the prompt "Run an audit dream per .therapy/protocols/dream-audit.md." Only when no regular dream is due; if one is, offer that first. It checks a few older context files against their session notes and leaves a `dream/YYYY-MM-DD-audit` branch for review. "how far is the audit?": run `python3 .therapy/scripts/audit_next.py --status`.
```

In `dream.md`, add a line near "When": "**Older notes:** this protocol only covers sessions since the last dream. Checking older context files against the notes they came from is the audit dream, `.therapy/protocols/dream-audit.md`."

### 4.4 Test

```bash
python3 .therapy/scripts/audit_next.py --status
python3 .therapy/scripts/audit_next.py
```

- `--status` counts every context file as "never".
- The plan lists up to 5 files, each with a mode (`full` or `cited`), the session notes to read, and a `record:` line. No note on it is newer than the last merged regular dream.
- With no merged regular dream yet, it says to run one first.

Then run one audit with the client and review it. In the reference install, a full pass over ~130 context files is about 17 runs. The first five or six cover everything the startup reading shows, which is where drift costs most.

---

## Part 5 — Arc-review maintenance moves to dreams (after part 3)

The arc review ends with backend housekeeping passes (the `base` patch has "Maintenance: Context File Consolidation"; an install may have added others: startup weight, thread registry, link cleanup). They sit badly there. The arc review is a conversation with the client, often late at night, and in the reference install the passes were often left undone. Part 5 moves them into dreams. Not all at once: three whole-library passes take turns, one per dream (threads → summaries → consolidation), so each comes round about every two weeks at a dream every few sessions. That's the same rhythm as the arc review, and each dream stays small enough to review.

### 5.1 The dream template

`templates/dream.md` already has the "One library pass" section (after the region checklist), the `## Library pass` report heading, the `· pass` field in the index line, and rule 11's allowance for a summary the pass added. If this install copied `dream.md` before 2026-11-09, add those four pieces from the template. In `dreams/index.md`, add the `· pass` field to the format line (`templates/dreams-index.md`).

Adapt the passes to what the install has:
- no thread registry → the threads pass is skipped automatically (the section says so);
- no summary blocks → the summaries pass is just the Core-set and startup-list check;
- if the install's arc review had a pass that isn't covered (for example a link-cleanup script), add it to the region checklist, so it runs in every dream.

### 5.2 Slim the arc review

In `.therapy/protocols/arc-review.md`, find every `## Maintenance: …` section and replace them all with:

```markdown
## Maintenance (moved to dreams)

The arc review used to end with backend passes (context-file consolidation, and any others this install had). They're now done by dreams (`.therapy/protocols/dream.md`): three "library passes" (threads → summaries → consolidation) take turns, one per dream, about every two weeks. So the arc review is the conversation and its write-up: the `arc.md` entry, and whatever else this install's "After the Conversation" section does. It needs no backend pass.
```

Keep everything above the Maintenance sections: the conversation, the five headings, "After the Conversation" (the `arc.md` entry and the session-index collapse). Part 5 only removes the backend passes. The arc review itself stays, and the dreams depend on it (README, "How it relates to the arc review").

The pieces to look for in a typical install:
- the `base` patch's **"Maintenance: Context File Consolidation"**, which the consolidation pass replaces;
- the **thread-registry** patch's "consolidation pass" bullet (its INSTALL step 6), which the threads pass replaces. Keep that step's other bullet, the "held but unexamined" audit of the registry: that's conversation, not housekeeping;
- the `base` patch's `context/GUIDE.md` **"Enforcement"** paragraph, which names the arc review. Point it at the dreams instead.

Before deleting, check whether anything in those sections is a format or convention that other files point to (the reference install had the summary-block format there). Move any such text to `context/GUIDE.md` and update the pointers. Then search the install for "Maintenance:" and "arc review" in `context/GUIDE.md`, the session-end protocol and the scripts, and point anything about consolidation at `dream.md` instead.

### 5.3 Test

- The next dream's report has a `## Library pass` section naming **threads**, unless the install has no registry.
- Its index line ends `· pass threads`, and the startup script's "Dream:" line still reads correctly (the extra field doesn't affect it).
- After merge, the dream after that does **summaries**.
- The next arc review ends with the write-up and no backend pass.

---

## Updating an install that already has dreams (2026-11-09)

Two changes. Apply the first even if you skip part 4.

1. **Same-day sessions after a dream (bug fix).** Before this, "undreamed" compared dates only. A session held later on the day a dream merged (`2026-10-02b` after a dream covering `2026-10-02`) counted as covered: it dropped off the startup reading list, and no dream would ever read it. Fix:
   - In `.therapy/scripts/startup.py`, replace `DREAM_LINE_RE`, `last_dream()`, `undreamed_sessions()` and the `head = …` line in `dream_status()` with the versions in `templates/startup-dream-additions.py` (search for "2026-11-09 fix").
   - In `.therapy/protocols/dream.md`, Phase 0 "Find the range" and the Phase 5 index-line format: copy the new wording from `templates/dream.md` (full session names, suffix included).
   - In `dreams/index.md`, the format line: `covered <first session> → <last session>`.
   - **Check for a missed session:** list `sessions/` and compare with the last merged dream's covered end. Any note on the same date with a later suffix (or a later note the old rule skipped) is undreamed. After the fix, the startup script's "Dream:" line counts it, and the next dream covers it.
   - Test: `python3 -c "import sys; sys.path.insert(0,'.therapy/scripts'); import startup; print(startup.last_dream(), startup.undreamed_sessions())"` prints the covered end as a string (`'2026-10-02'`), and any same-day later session is in the list.
2. **Audit dreams:** part 4 above.
3. **Arc-review maintenance moves to dreams:** part 5 above.

Log both in `.therapy/maintainer-notes.md`.

## Updating an install that already has dreams (2026-11-10)

**Length limits for thread entries** (needs part 5 and the `thread-registry` patch). The threads pass folded dated add-ons into each description, which keeps the length instead of cutting it. In the reference install the registry nearly doubled in two months: most open descriptions ran past 400 characters, Sessions trails reached 18 entries, and Surfacing notes picked up history. The startup reading carries the whole file every session.

1. In `.therapy/protocols/dream.md`, the threads library pass: add the "Length limits" bullet from `templates/dream.md`, after "Fold dated add-ons".
2. In `context/threads.md`, the entry schema in the header: the Sessions, description and Surfacing lines from the `thread-registry` patch's `templates/threads.md`.
3. In the session-end thread reconcile step ("Bump what was touched"): when appending today's session to **Sessions**, keep the first session and the latest three.
4. Nothing is trimmed until the next threads pass comes round in the rotation. Review its `LIBRARY · ARCHIVE` lines like any other change: check that no do-not-raise rule or boundary was lost.

**Printed registry sections count toward the startup size.** If you apply the same-day `opus-5-5-rebaseline` update (startup prints only the registry's open therapeutic and shelved sections), add the BLOCK C line `startup_bytes += len(threads.encode()) if threads else 0` from `templates/startup-dream-additions.py`. Without it, the dream threshold stops seeing those sections. The startup size drops by the part no longer read, so re-check `DREAM_DUE_BYTES`.

**A metrics script** (needs part 3). Copy `templates/dream_metrics.py` to `.therapy/scripts/` and adapt `SIZED_FILES`. In `.therapy/protocols/dream.md`, copy from `templates/dream.md`: Phase 0 step 6 (record the "before" metrics with the script), the "From `dream_metrics.py`" line under the report's Metrics heading, and the last bullet of Phase 5 step 4 (run it again, and use "projected after merge" as the "after" startup figure). Test: it exits 0 and prints a "Startup list bytes" line.

Log it in `.therapy/maintainer-notes.md`.

## Verify

- `dreams/index.md` and `dreams/flags.md` exist, and keep the `## Log`, `## Open` and `## Closed` headings.
- In maintainer mode, "dream" with nothing new to cover stops cleanly: no branch, no changes.
- After the first real dream:
  - `git branch -a --list '*dream/*'` shows exactly one branch;
  - `git diff main...dream/<date> --name-only` lists nothing in `sessions/` or `.therapy/memory/`;
  - the report has every section.
- After review and merge, `main` has one "Dream … (reviewed)" commit, and the dream branch is gone locally and on the remote.
- After part 3, the next therapy session's greeting is still accurate. Check that the startup list included the undreamed notes.

## Log entry

Add an entry to `.therapy/maintainer-notes.md` covering:
- which parts were installed;
- the client's four decisions;
- the paths mapped or skipped;
- `DREAM_DUE_BYTES`;
- how the first dream and its review went.

## Known limits

- **A dream is only as good as the session notes.** It can't recover something session end never wrote down. The Memory Misses section is how gaps surface.
- **The prompt rules make inventing facts, rewriting the profile or touching the notes unlikely, but can't make them impossible.** The review and the diff check are the real guard. Watch for any change in the report without evidence.
- **More dreaming isn't better.** Research on dream cycles found rare details eroding after many consecutive passes over the same material. Dream every few sessions, not nightly.
- **Lag between dreams.** After part 3, context files lag their notes until the next dream. The startup script bridges up to six undreamed sessions; after that it prints "overdue", and older undreamed notes drop off the reading list.
