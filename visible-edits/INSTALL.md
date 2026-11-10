# INSTALL — Visible Edits Patch

Integration guide for a rule that all changes to this install's files go through the Edit tool (Write for new files), so the client can see each change. Written to be applied against files that have **diverged** from the reference setup — each change is anchored on a *concept* to find, not a line number. If you are an assistant reading this in maintainer mode: work through it against *this* setup's actual files, adapt names and pronouns, and don't assume the reference structure matches yours.

No prerequisite patch. This one stands alone.

---

## Terminology mapping (do this first)

The reference setup calls the assistant **Sage**; this guide calls the person "the client". Before applying anything:

- Replace "the client" with whatever this setup calls the person, in their real pronouns.
- The reference keeps client-given behavioural corrections as one file each in `.therapy/memory/`, indexed by `.therapy/memory/MEMORY.md`, and read at every session start. Map that to wherever this setup keeps (a) its standing feedback/corrections and (b) the index or list that gets them loaded every session.
- The reference runs dreams through a subagent defined in `.claude/agents/dreamer.md`. Map that to any subagent definition this setup has that writes to the install. If there is none, skip step 3.

---

## MANDATORY

### 1. Add the feedback file

In this setup's standing-feedback location, create a file (the reference calls it `feedback_use_edit_tool.md`) with this content, adapted:

> ---
> name: feedback_use_edit_tool
> description: Change the install's files with the Edit tool (Write for new files), never with python, sed, perl or heredocs, so the client can see each change
> metadata:
>   type: feedback
> ---
>
> Make every change to an existing file in the install with the Edit tool, one visible edit at a time. Create new files with Write. Use the shell only for reading, searching, scripts the protocols name, git, and scratch work outside the install.
>
> **Why:** a session end once did several files' updates in a single shell script, so the client couldn't see what changed. They asked for edits through the Edit tool instead.
>
> **How to apply:** in therapy sessions, at session end, in dreams and in maintainer mode. Appends count: Edit at the end of the file instead of `cat >>`. Merging long notes into a file also goes through Edit or Write. If a change truly can't be done with Edit (a huge mechanical rewrite), say so and ask first.

Replace the generic **Why:** with the client's own words and date if they asked for this themselves. A real, dated reason holds up better in later sessions than a borrowed one.

### 2. Make sure it loads every session

Add a one-line pointer to the index or list that loads standing feedback at session start (the reference: a line in `MEMORY.md`, e.g. `- [Use the Edit tool](feedback_use_edit_tool.md) — change files with Edit (Write for new files), never scripts, so the client can see each change.`). If this setup's startup reading is built by a script, confirm the new file is picked up.

### 3. Tell any writing subagent

Subagents start without the session's context and won't read the feedback file unless told to. In each subagent definition that writes to the install (the reference's dream agent), add a line near its other tool or shell notes:

> - Change the install's files with Edit and create them with Write, never with python, sed, perl or heredocs. Use the shell for reading, searching, the protocol's scripts and git.

### 4. Log it

Record the change wherever this setup logs maintainer work (the reference: a dated entry in `.therapy/maintainer-notes.md`): what was added, why, and which files.

---

## VERIFY

- Confirm the feedback file is in the set that loads at every session start, not one that's only read on demand.
- Confirm each writing subagent's definition carries the line.
- At the next session end, check that every file update shows up as its own Edit or Write, with no shell command writing into the install.
- State the limit plainly if the client asks: this is an instruction, not an enforced block.
