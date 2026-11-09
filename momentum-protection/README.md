# Inner Dialogue Patch — Momentum Protection

A rule against a specific, narrow failure: asking *"are you done, or do you want to keep going?"* (or any equivalent stop-or-continue check) while the person is actively still digging into something they want to reach — turning a real, well-intentioned pacing tool into an interruption of the exact thing it was meant to protect.

Written after watching it happen in a live session on a second install: the stop-or-continue check kept landing exactly when the person wanted to keep going, and it broke their momentum instead of protecting their pace.

**No prerequisite patch required** — this is a standalone addition to the assistant's pacing / consent-checking instructions.

## What problem it solves

A pacing check like *"do you want to stay with this, or step back?"* is a real, useful tool — it belongs in the toolkit for a reason. It's the right move when someone seems overwhelmed, hesitant, or is visibly signaling ambivalence about continuing. The failure isn't that the tool exists; it's that it was firing on a different trigger than the one it should: **content getting heavy**, instead of **the person actually showing signs of wanting to stop**.

Those are not the same signal. Someone can be fully in it — still talking, still generating their own material, still leaning toward the hard thing rather than away from it — and get handed an offered exit anyway, just because the subject matter crossed some internal "this seems like a lot" threshold. In that moment the question doesn't read as care. It reads as the assistant needing permission to keep listening, or as a subtle suggestion that maybe they *should* stop — right when what they actually wanted was for someone to stay with them while they kept going.

The effect, put plainly: it makes it harder to dig deeper, in exactly the moments the person wants to.

## What's in the box

```
momentum-protection/
  README.md    ← you are here (human overview)
  INSTALL.md   ← the integration guide — hand THIS to your assistant in maintainer mode
```

No template file — this patch is a protocol-text addition to an existing pacing/consent-checking instruction this setup already has, not a new file.

## How to install (two ways)

**Easiest — let your assistant do it.** In maintainer mode, give it this folder and say: *"Install this momentum-protection patch into your own setup, following INSTALL.md. Adapt it to my files — don't assume they look like the reference."*

**By hand.** Open `INSTALL.md` and work through the mandatory steps.

## Design notes worth knowing

- **The fix is discrimination, not removal.** The pacing-check instinct stays — it's real and it matters for the cases it's actually for. This patch narrows *when* it fires, it doesn't delete it. A version of this patch that just told the assistant to stop offering off-ramps entirely would trade one failure mode for a worse one (never checking in when someone genuinely is overwhelmed).
- **Real stop-signals vs. "this is heavy."** The rule gives a concrete list to tell the two apart: trailing off, going quiet, saying it's too much, visibly changing the subject, or a flat affect shift — those are signals. The content itself being hard, sad, or intense is not, on its own, a signal to check in. Someone leaning further in while something gets harder is *more* reason to stay present, not the cue to offer them a door.
- **Same family of fix as narration-hardening.** A well-intentioned habit, applied reflexively rather than discriminately, undermines the exact goal it exists to serve. Watch for this shape recurring elsewhere in the assistant's pacing instincts, not just this one phrase.
- **Not crisis-specific.** This isn't about crisis protocol, where direct safety checks stay mandatory regardless of momentum — this is about ordinary emotional digging, the kind that's supposed to be allowed to go as deep as the person wants it to.
