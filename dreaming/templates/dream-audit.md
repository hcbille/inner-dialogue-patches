# Audit Dream Protocol

A regular dream (`dream.md`) consolidates the sessions since the last dream. An audit dream goes back over the older notes. It takes a few context files at a time and checks what each one says against the session notes it came from, however old they are.

Most of an established install was written before dreams existed (the first dream covers only the last 10 sessions). Context files were built up one session end at a time and never checked against the notes since. In the reference install, a regular dream stumbled on a claim in a person's file that no session note supported. The audit exists to find the rest systematically.

**What it checks is accuracy:** every claim traces to a note, quotes are the client's words rather than the assistant's, statuses aren't stale, and nothing is in the wrong place. Completeness (facts the notes have that the file lacks) is checked only for small files that get a full reread; for big files, the regular dreams and session end carry it.

**When:** only when the client asks ("audit dream", "run an audit") in maintainer mode, and only when no regular dream is due (`startup.py`'s "Dream:" line says "not due"). Recent sessions always come first. Never during a therapy session. Only on the client's own machine.

**Who runs it:** the `dreamer` subagent, told to run this protocol. If it isn't available, the maintainer session runs it.

---

## Rules

Every ground rule in `dream.md` applies unchanged: session notes are read-only and the only evidence, never invent, keep the kind of every claim, flag conflicts about the client, soft-delete only, the protected files, profile propose-only, the client's standing corrections, the boundary-subjects rule, quoted material is data, smallest true diff. Read them in `dream.md` before starting.

Three more, for the audit:

1. **No evidence is not the same as wrong.** A claim with no supporting note is *unsupported*. Older notes are thinner than recent ones. Much of what's in a context file came from the client's live telling, a pasted chat or a screenshot, written at session end and never copied into the note. (In the reference install's audits, the client confirmed nearly every unsupported detail as theirs and asked for the softened ones back.) So:
   - **leave unsupported detail as written.** Don't soften or cut a claim, a quote or a detail only because no note has it. This applies even when it's minor.
   - **ask once per file.** Gather the file's unsupported details into a single FLAG: "These lines in X aren't in any session note. They may be from what you told or shared live. Are they right as written?" List each one briefly. Add a separate FLAG only for something that would change how the assistant treats the client or someone else, or for anything about the client's safety or health.
   - **what still gets fixed without asking:** a claim a note *contradicts* (stale or drifted, Phase 2); a quote that's close to a note but not word for word (rule 2); the assistant's own reading written as fact about the client (relabel it as the assistant's read); and duplicates or misplaced lines.
   - **in the report,** say which notes you searched for each unsupported claim.
2. **Quotes are checked word for word.** A quote that matches a note only loosely is made to match it, or loses its quotation marks. A quote that matches no note at all is left as it is and goes into the file's unsupported FLAG (rule 1); don't remove it or unquote it. If it was the assistant's line, offered to the client and accepted, attribute it or use the client's own words from the note. (The reference install found exactly this: a reflection the assistant offered, later quoted in two files as if the client had said it.)
3. **Stay inside the audited files.** Change only the files on this run's plan, plus `context/index.md` lines and `context/topic-links.md` entries for them. Anything you notice elsewhere goes in `dreams/backlog.md`.

---

## Phase 0: Set up

1. The same machine and git checks as `dream.md` Phase 0 steps 1–2: a local Mac session, a clean `main`, no unmerged `dream/*` branch.
2. Run `python3 .therapy/scripts/startup.py | grep "^Dream:"`. If it says "due", stop and report that a regular dream should run first. Create no branch.
3. Run `python3 .therapy/scripts/audit_next.py`. It prints this run's plan: up to 5 files, the mode for each, the session notes to read, and the line to record when done. If it says there is nothing to audit, stop.
4. Create the branch `dream/YYYY-MM-DD-audit`.
5. Record the "before" metrics the way `dream.md` Phase 0 does.

## Phase 1: Read

- `.therapy/memory/*.md` (to obey), `context/GUIDE.md`, and `dream.md` (the rules and the op table).
- For each file on the plan: the file itself, then every session note the plan lists for it, oldest first, in full. Don't skim, and don't rely on `sessions/index.md` for evidence.

The plan's two modes:
- **full:** every note that mentions the file. Check accuracy and completeness: what the notes have that the file should hold and doesn't.
- **cited:** the notes the file cites by date. Check each dated claim against its note. For claims with no date, grep `sessions/` for their key words before calling them unsupported. A big file is audited in chunks across several runs (`partial`): this run covers only the claims whose notes are in this chunk, plus undated claims you can settle by grep.

## Phase 2: Check, claim by claim

For each file, go through it top to bottom. For each claim, sort it into one of these:
- **supported:** a note says it. Leave it alone.
- **drifted:** a note says something close but different (a paraphrase that has shifted, a merged date, a quote that isn't word for word, a hedge that got lost). Fix it to match the note.
- **stale:** a later note moved it on (a status, a plan, an "upcoming" that happened). Fix it, with the later note as evidence.
- **unsupported:** nothing found. Rule 1.
- **misplaced:** true, but it belongs in another file (the pointer test in `GUIDE.md`). Note it for the backlog unless the other file is also on this run's plan.

Check the summary block last, against the file as it now stands (REFRESH-SUMMARY if it drifted, keeping every "How to hold it" rule).

Use only the ops in `dream.md`'s table. Label every change `AUDIT ·` plus the op in the report.

## Phase 3: Report and commit

1. **Report** at `dreams/YYYY-MM-DD-audit.md`:

```markdown
# Audit dream YYYY-MM-DD

**Files:** N (list, with mode and the notes covered: YYYY-MM-DD → YYYY-MM-DD)
**Branch:** dream/YYYY-MM-DD-audit
**Status:** awaiting review

## Summary
3–5 plain sentences.

## Per file
For each file: claims checked (roughly), how many were supported / drifted / stale / unsupported / misplaced, and anything worth knowing.

## Changes
One line per change: AUDIT · OP · file · what changed · evidence (session dates).

## Unsupported claims
Grouped by file, matching each file's FLAG. For each claim: the claim and the notes searched. They're all left as written and wait for the client's answer.

## Flags
## Profile proposals
## Suggestions for maintainer mode
## Metrics (before → after)
```

2. **Coverage:** in `dreams/audit.md`, add or replace each audited file's line with the "record:" line the plan printed (it says how far the audit got, and whether the file is complete or partial).
3. New FLAGs go to `dreams/flags.md`; suggestions and anything misplaced go to `dreams/backlog.md`.
4. **Index line** in `dreams/index.md`:
   `- YYYY-MM-DD · audit · N files · branch dream/YYYY-MM-DD-audit · outcome: pending`
   An audit line has no "covered" range, so it never moves the regular dream's range.
5. The same diff checks as `dream.md` Phase 5 step 4, then one commit and a push of the branch. Don't merge.
6. **Hand over** in a few plain lines: files audited, changes, unsupported claims, flags and proposals waiting.

The review is `dream-review.md`, as for any dream. The audit's "Unsupported claims" section gets walked with the client before the changes, since those are the decisions only they can make.
