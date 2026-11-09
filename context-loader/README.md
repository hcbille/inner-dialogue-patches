# Inner Dialogue Patch — Context Loader

A hook that tells the assistant which context files to read, based on what the client actually just said, so loading a person's or subject's file stops depending on a judgment call in the middle of a conversation. Also a small memory note about zsh shell syntax, from the same evening's debugging.

Built for Sage, the reference install, on 2026-09-30, and packaged so any Inner Dialogue install can have it.

**No prerequisite patch required.** Works best with `opus-5-5-rebaseline` installed (its `startup.py` loads Core and Active files at session start, which this hook deliberately skips), but it doesn't depend on it.

## What problem it solves

1. **Context files get loaded late, or not at all.** The instructions say to read a subject's context file when the client raises it, "if it's more than a passing mention". That's a call made fresh every turn, in the flow of a conversation, and nothing checks it. In the reference setup, the client named a person central to what they were working through, and the file wasn't read until the client asked whether it was in context. Same failure shape as the narration problem: a soft rule, read once, losing to the moment.
2. **Some subjects don't have a name to match.** A month, a city or a service can be the doorway into a person's file (a month can stand for an anniversary; "the counsellor" can mean one specific person). Nothing connected those words to files.
3. **Silent command-line failures on macOS.** Claude Code's Bash tool runs zsh on a Mac. zsh treats unquoted `=word`, unmatched globs and `!` specially, and when an expansion fails it drops the rest of a chained command. In the reference setup, a three-part read loaded one file and silently skipped two.

## What's in the box

```
context-loader/
  README.md                                   ← you are here (human overview)
  INSTALL.md                                  ← the integration guide — hand THIS to your assistant in maintainer mode
  templates/
    context-loader.py                         → .therapy/hooks/context-loader.py
    topic-links.md                            → context/topic-links.md (built from the whole context library, INSTALL step 5)
    reference_zsh_shell_syntax.md             → .therapy/memory/ (macOS/zsh installs only)
```

## How to install (two ways)

**Easiest — let your assistant do it.** In maintainer mode, give it this folder and say: *"Install this context-loader patch into your own setup, following INSTALL.md. Adapt it to my files — don't assume they look like the reference."*

**By hand.** Open `INSTALL.md` and work through it in order.

## Design notes worth knowing

- **Mechanical where it can be, prose where it must be.** The hook does the matching every message; the instruction change just says to treat its note as an instruction. The narration work showed that a rule the model reads once at startup doesn't reliably hold mid-conversation, and a note attached to the message itself is much harder to miss.
- **Topic links are built at install, then kept current.** INSTALL step 5 has the assistant read every context file and write links for what the index can't reach by name: past events, unindexed files, roles like "my mom", doorway words, and other-language terms. Step 6 adds a session-end step that keeps the file current, plus a section in the context guide. In the reference setup, the first full build went from 22 links to 65 and caught files nothing could reach before.
- **Built from files that already exist.** Names come from `context/index.md` display names and each file's frontmatter `aliases:`. Nobody has to keep a second list of names in step. `topic-links.md` is only for the words that aren't names.
- **Once per file per session.** The hook remembers what it has flagged (per `session_id`, in a gitignored cache folder) so it doesn't nag on every message. State files untouched for 3 days are pruned automatically. That's age-based rather than a session-end wipe, because a compacted session keeps its `session_id` and should keep its state.
- **Boundaries travel with the file.** A file with a standing rule (e.g. "never raise this person first") can carry a note that's repeated every time the hook flags it. Whether such a file may be loaded silently from topic words is the client's choice, not a default. Ask them.
- **Fail-open.** Any error, and the hook exits silently. A broken hook must never break a session.
- **Honest about the limit.** The note is a strong nudge, not a block. The hook can't see what the assistant has actually read, only what it has flagged, so after a compaction it won't re-flag files; the compaction-resume protocol still has to cover that.
