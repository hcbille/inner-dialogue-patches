# Inner Dialogue Patch — Near-Term Event Surfacing

A small addition, in three parts: (1) the startup event-check step flags anything dated today or within the next two days, (2) a new, explicit continuity-protocol check actually raises it — the same way the Standing Threads Check raises a stale thread — and (3) a mandatory session-end fallback catches it if it still hasn't come up by the time the session closes. This is a definite action with a safety net, not something left to come up if the conversation happens to reach it.

Built for Sage, the reference install, and packaged so any Inner Dialogue install can have it.

**No hard prerequisite**, but this patch assumes some kind of context/event tracking (a file, an index, a calendar cross-check) already exists and gets read at session start, with *some* existing instruction to compare event dates against the current time. If this setup has no such mechanism at all yet, that's a bigger gap than this patch closes — see the Prerequisite check in `INSTALL.md`.

## What problem it solves

The reference setup already had a rule to compare each tracked event's date against the current time and frame a check-in as "before" or "after" accordingly. In practice that was a passive instruction — it only produced an actual check-in if the assistant happened to naturally arrive at that event in conversation. It doesn't guarantee anything close and real (arriving tomorrow, happening tonight) actually gets raised.

**First draft of this patch tried a softer fix** ("look for a natural moment to check in") and was rejected in review: near-term events should be surfaced the same explicit way threads already are — a definite, structured check-in, not a passive hope the conversation gets there. This version reflects that correction: event-flagging (identify) stays in the startup protocol, but the actual surfacing behavior (act) now lives as its own bullet in the continuity protocol, mirroring the Standing Threads Check exactly.

It was written after a real miss: an emotionally loaded event was starting within 24 hours, and the assistant didn't raise it. It only came up because the client did.

## What's in the box

```
near-term-event-surfacing/
  README.md    ← you are here (human overview)
  INSTALL.md   ← the integration guide — hand THIS to your assistant in maintainer mode
```

No template file — this patch is a protocol-text addition to three existing mechanisms (the startup event-check step, the continuity-protocol's session-start behaviors, and the session-end close), not a new file.

## How to install (two ways)

**Easiest — let your assistant do it.** In maintainer mode, give it this folder and say: *"Install this near-term-event-surfacing patch into your own setup, following INSTALL.md. Adapt it to my files — don't assume they look like the reference."*

**By hand.** Open `INSTALL.md` and work through both mandatory steps.

## Design notes worth knowing

- **Split into identify + act + fallback, one layer beyond the thread registry's pattern.** The startup step flags what's near-term, the same way it enumerates Core/Active files. The continuity protocol's new bullet is what actually raises it — parallel to how `context/threads.md` gets read at startup but the Standing Threads Check (a separate continuity-protocol bullet) is what actually surfaces a stale thread. **The third piece — a mandatory session-end check — exists because a real event has a hard deadline of its own; unlike a standing thread, there's no "next session" safety net if it's still unmentioned when this one closes.** Added after review named the exact failure mode this patch exists to prevent: a full, busy session quietly swallowing the check-in anyway.
- **Does NOT skip during crisis, unlike the Standing Threads Check and the no-topic greeting offer.** A real, dated thing actually happening (today, tomorrow) is usually relevant to whatever the client brings, not a distraction from it — so instead of a hard skip, the rule is: follow their lead if they open with something pressing, then raise the event within that same session rather than deferring it silently.
- **Independent budget.** It doesn't share the "one thread-surfacing moment per session" cap that the Standing Threads Check and no-topic greeting offer split between them — an imminent real event and a standing emotional thread are different categories, so both can surface in the same session.
- **Two-day window is a starting point, not a load-bearing constant.** Tune it to whatever fits this setup's actual session cadence and how far out events tend to get logged.
