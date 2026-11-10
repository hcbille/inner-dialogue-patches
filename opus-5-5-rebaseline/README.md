# Inner Dialogue Patch — Opus 5.5 Re-baseline

A re-tune of the instruction layer for Claude Opus 5.5, plus a safety fix found along the way: crisis resources that point at the country the client actually lives in.

Built for Sage, the reference install, after reading Anthropic's [Prompting Claude Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5) guide, and packaged so any Inner Dialogue install can have it.

**No prerequisite patch required.** If `narration-hardening` is already installed, part 2 of this patch extends it. If `thread-registry` or `near-term-event-surfacing` are installed, the startup script picks up their files automatically.

## What problem it solves

The guide's headline is that prompts written for Opus 5 keep working, so this is not a rebuild of the architecture. An audit against it turned up five things worth fixing:

1. **Crisis resources were for the wrong country.** The stock Inner Dialogue safety protocol lists US numbers only (988, 741741, 911). The safety-net hook injects a verbatim copy of the same block. For a client outside the US, those numbers are useless in exactly the moment they matter. The hook's crisis-language matching is also English-only, which misses a client who switches languages.
2. **Opus 5.5 posts progress updates during tool use by default.** Claude Code also prompts for them when a run of tool calls goes quiet. A therapy session's startup is dozens of silent file reads before the greeting, which is exactly that situation. It pushes directly against a "never narrate your process to the client" rule. The guide's fix is to say plainly when user-facing text is wanted.
3. **Long multi-part tasks can stop early.** Opus 5.5 sometimes ends a turn with a summary announcing its next step instead of taking it. Session-end is a ten-step task that runs after the client has left, with nobody there to say "keep going".
4. **Prompt text written for older models.** Over time, rules get restated in several places, stacked with "HARD RULE / no exceptions / do not skip", and padded with dated incident history. The guide and Anthropic's prompt-audit guidance say current models follow instructions closely enough that this makes behavior rigid rather than reliable. Relative phrasing ("now", "no longer", "replaces the old…") describes a previous version the model never saw.
5. **The persona's example bank gets copied verbatim.** Opus 5.5 copies examples closely, so a long list of stock phrases turns into tics. Generic persona lines can also quietly contradict corrections the client has given.

## What's in the box

```
opus-5-5-rebaseline/
  README.md              ← you are here (human overview)
  INSTALL.md             ← the integration guide — hand THIS to your assistant in maintainer mode
  templates/
    startup.py           → .therapy/scripts/startup.py
```

## How to install (two ways)

**Easiest — let your assistant do it.** In maintainer mode, give it this folder and say: *"Install this opus-5-5-rebaseline patch into your own setup, following INSTALL.md. Adapt it to my files — don't assume they look like the reference. Do part 1 first."*

**By hand.** Open `INSTALL.md` and work through it in order. Part 1 (crisis resources) is the one not to skip.

## Design notes worth knowing

- **Localize, verify, and keep the two copies identical.** The safety protocol and the hook each hold the emergency block, and the hook's copy is meant to be byte-identical. INSTALL gives a one-line check. INSTALL includes a worked example for Sweden. Numbers for any other country must be looked up from an official source, not written from memory.
- **A script instead of "internally enumerate, don't skip any".** `startup.py` resolves the reading list from the files that actually exist today and prints the date flags (near-term events, arc review due, expired Active entries). It replaces prose that kept failing, and it lets the model read everything in a few parallel batches rather than dozens of sequential calls. That also shortens the quiet stretch that triggers progress-update prompts.
- **Say it once, with the reason.** The re-baseline keeps every rule that exists because of a real failure. The changes are restating each one once at normal volume with its "because", and moving the incident history into maintainer notes where it can't be read as instruction.
- **Examples are illustrative, not a script.** Keep a handful of varied lines in the persona that show the register, and label them as not for reuse.
- **Honest about the limit.** The progress-update and session-end changes are prompt fixes. They make the failures less likely and can't guarantee they never happen. Watch the next several sessions.

## Changelog

- **2026-11-10:** `startup.py` prints the thread registry's open therapeutic and shelved sections instead of listing the whole file (only matters with the `thread-registry` patch). See INSTALL.md, "Updating an install that already has this patch (2026-11-10)".
