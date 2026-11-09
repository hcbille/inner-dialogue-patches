# Inner Dialogue Patch — Narration Hardening

A hard, top-level rule against a recurring failure shape: the assistant narrating its own process or referring to the client in the third person, inside a message addressed directly to them — most dangerously as a whole preamble sentence sitting in front of the actual reply.

Built for Sage, the reference install, and packaged so any Inner Dialogue install can have it.

**No prerequisite patch required** — this is a standalone addition to the assistant's core response-shape instructions.

## What problem it solves

A soft, memory-file-only version of this rule already existed and kept failing to prevent recurrence, in a growing set of surface shapes:

1. Mid-response narration ("I'll create the memory file now and respond to her simply and directly").
2. Third-person case-note phrasing inside a reflective sentence ("that's real, steady care, given without being asked").
3. A reflective-summary recap sentence that reads as ordinary but uses "she/her" instead of "you" ("She got the message sent and the deadline handled").
4. **The newest, sharpest shape:** a full standalone sentence of stage direction *before* any words actually meant for the client — describing them and the assistant's own steering decision in the third person, then a separate line that's the real reply.

Worked through in maintainer mode: this probably isn't just "the assistant forgetting a rule" — it plausibly comes from the underlying coding-agent platform's own habit of narrating actions ("state in one sentence what you're about to do") bleeding into a persona that must never do that. A memory file is soft context, read once at session start, competing against a habit baked in at a layer the memory file can't see or override. The fix that actually moved things: stop treating this as one more memory-file bullet, and instead put a hard, explicit rule — naming the competing habit directly — into the always-loaded, highest-authority instruction file itself.

## What's in the box

```
narration-hardening/
  README.md    ← you are here (human overview)
  INSTALL.md   ← the integration guide — hand THIS to your assistant in maintainer mode
```

No template file — this patch is a protocol-text addition to the response-shape / persona-voice instructions this setup already has, not a new file.

## How to install (two ways)

**Easiest — let your assistant do it.** In maintainer mode, give it this folder and say: *"Install this narration-hardening patch into your own setup, following INSTALL.md. Adapt it to my files — don't assume they look like the reference."*

**By hand.** Open `INSTALL.md` and work through the two steps (the rule addition, and the accompanying memory/notes-file entry).

## Design notes worth knowing

- **Elevation, not just documentation.** The core move isn't a new example added to a memory file — it's moving the rule into the top-level, always-loaded instruction file (`CLAUDE.md` in the reference setup), with the competing platform habit named explicitly so it reads as an override, not an isolated preference.
- **Concrete wrong/right examples, not just an abstract statement.** The rule includes a real, literal example of the failure (the preamble-sentence shape) rather than only describing it — pattern-matching against a concrete example works better than an abstract instruction.
- **A checkable test, not just a rule.** "Before sending anything, check the first sentence: does it describe the client, your plan, or your own reasoning, instead of just talking to them?" — gives something to actually run, not just a value to hold.
- **Honest about the limit.** This is a prompt-salience fix, not a hard filter — there is no mechanism in this harness that strips assistant text before the client sees it. State that plainly if the client asks whether this "fixes" the problem; it reduces frequency, it doesn't guarantee elimination.
- **Log it as an evolving memory-file pattern, not a one-off.** The reference setup keeps a single growing file (`feedback_no_clinical_narration.md`) tracking every surface shape this failure has taken, dated, so a future review can see whether the CLAUDE.md elevation actually changed the recurrence rate over time.
