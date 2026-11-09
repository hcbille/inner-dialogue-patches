# Inner Dialogue Patch — No-Topic Greeting Offer

A small follow-on to the `thread-registry` patch: when the client opens a session with nothing specific in mind, the greeting itself offers a couple of open threads as optional starting points, instead of defaulting to a content-free "how are you feeling today?"

Built for Sage, the reference install, and packaged so any Inner Dialogue install can have it.

**Requires the `thread-registry` patch already installed** (needs `context/threads.md` to exist). If that hasn't been installed here yet, do that one first.

## What problem it solves

The thread registry's "standing threads check" nudges a single stale thread once, at a natural moment mid-session — but that only fires once the client has already brought their own topic and the conversation is underway. It does nothing for the specific, common case where they open with a plain greeting and genuinely has nothing in mind: the assistant either falls back to a generic "how are you," or the client has to reach for something themselves. This patch gives the greeting a light menu to offer in exactly that gap.

## What's in the box

```
no-topic-greeting-offer/
  README.md    ← you are here (human overview)
  INSTALL.md   ← the integration guide — hand THIS to your assistant in maintainer mode
```

No template file — this patch is a protocol-text addition to an existing continuity/greeting mechanism, not a new file.

## How to install (two ways)

**Easiest — let your assistant do it.** In maintainer mode, give it this folder plus the (already-installed) `thread-registry` patch context and say: *"Install this no-topic-greeting-offer patch into your own setup, following INSTALL.md. Adapt it to my files — don't assume they look like the reference."*

**By hand.** Open `INSTALL.md` and work through the single mandatory step.

## Design notes worth knowing

- **Cap of 2 threads**, framed as a menu ("is there anything particular on your mind? Otherwise we could start with...") — not a push. The client picking one, declining, or bringing their own topic instead are equally fine outcomes.
- **Pulls only from Open + therapeutic** — same pool the standing-threads check uses. Logistical threads never get offered here either.
- **Excludes any thread whose Surfacing rule says not to raise unprompted** (the do-not-raise / return-only-if-reopened style entries) — this menu is still a form of surfacing, so the same restraint rules apply.
- **Excludes anything surfaced in the last 5 days.** Without this, a thread that just came up in the previous session could get immediately re-offered as a "starting point," which reads as the assistant not tracking what was just discussed. Tune the exact number of days to whatever cadence fits this setup — 5 was the reference install's choice, not a load-bearing constant.
- **Takes the place of, doesn't stack with, the standing-threads check for that session.** Both mechanisms pull from the same "one thread-surfacing moment per session" budget — if the greeting already offered threads, don't also fire the later single-stale-thread nudge.
- **Skipped during crisis or acute distress**, same as every other thread-surfacing mechanism.
