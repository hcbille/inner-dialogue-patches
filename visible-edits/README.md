# Inner Dialogue Patch — Visible Edits

A rule that every change to the install's files goes through the assistant's Edit tool, and new files through its Write tool, never through a python, sed, perl or heredoc script run in the shell. That way the client can see exactly what changed in every file.

Built for Sage, the reference install, and packaged so any Inner Dialogue install can have it.

**No prerequisite patch required.** It works best alongside `base` (maintainer mode) and `dreaming` (the dream subagent), since those are the places that write the most.

## What problem it solves

Session end, dreams and maintainer work touch many files at once: the session note, the index, the thread registry, the profile, people files. When several of those updates get batched into one shell script, the client sees a single opaque command instead of the individual changes. That makes it hard to notice a wrong sentence, a dropped line or an edit to a file that shouldn't have been touched, which matters in a system whose files are someone's memory of their own therapy.

In the reference install, a session end did seven files' worth of updates in one python script. The client asked for every edit to go through the Edit tool from then on, so each change shows up as its own reviewable diff.

## What's in the box

```
visible-edits/
  README.md    ← you are here (human overview)
  INSTALL.md   ← the integration guide — hand THIS to your assistant in maintainer mode
```

No template files. The patch adds one memory/feedback file and one line to the dream agent, if there is one.

## How to install (two ways)

**Easiest — let your assistant do it.** In maintainer mode, give it this folder and say: *"Install this visible-edits patch into your own setup, following INSTALL.md. Adapt it to my files — don't assume they look like the reference."*

**By hand.** Open `INSTALL.md` and work through the steps.

## Design notes worth knowing

- **Where the rule lives.** A memory/feedback file, read at every session start, covers the assistant itself. Subagents start cold and don't read that file unless told to, so a dream agent needs the rule in its own definition as well.
- **What the shell is still for.** Reading, searching, running the scripts the protocols name (like a startup script), git, and scratch work outside the install. The rule is about *writing to the install's files*, not about avoiding the shell altogether.
- **Appends count.** "Append a line to the index" is still an edit: Edit at the end of the file, not `cat >>`.
- **Big merges count too.** Pasting long generated notes into a log file goes through Write or Edit, not a script that splices them in.
- **An escape hatch, with consent.** If a change really can't be done with Edit (a large mechanical rewrite across many files), the assistant says so and asks first, rather than quietly scripting it.
- **Honest about the limit.** This is an instruction, not a hard block. Nothing stops the assistant from running a script. If the client wants it enforced, a `PreToolUse` hook that rejects shell commands writing into the install (redirects, `sed -i`, python `open(...,'w')`) is possible, but brittle; this patch doesn't ship one.
