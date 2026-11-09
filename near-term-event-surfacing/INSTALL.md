# INSTALL — Near-Term Event Surfacing Patch

Integration guide for a small, two-part addition: one clause in the startup event-check step, one new bullet in the continuity/greeting protocol. Written to be applied against files that have **diverged** from the reference setup — the change is anchored on a *concept* to find, not a line number. If you are an assistant reading this in maintainer mode: work through it against *this* setup's actual files, adapt names and pronouns, and don't assume the reference structure matches yours.

**Prerequisite check first:** confirm this setup already has, somewhere in its session-start reading, (a) some form of event tracking — a context file, an index section, a calendar cross-check — and (b) an existing instruction to compare each event's date/time against the current moment for framing purposes (e.g. deciding whether to ask "how are you feeling about it" vs. "how did it go"). If neither exists at all, stop — this patch has nothing to attach to, and building that base mechanism is a separate, larger piece of work outside this patch's scope.

---

## Terminology mapping (do this first)

The reference setup calls the assistant **Sage**; this guide calls the person "the client". Before applying anything:

- Replace "the client" with whatever this setup calls the person, in their real pronouns.
- The reference keeps events in `context/index.md` under an "Events" section, with individual files in `context/events/`. If this setup tracks events differently (a single log, a calendar integration, inline notes), adapt the mechanics below to wherever the date/time actually lives.
- The reference's continuity/greeting protocol also has a **Standing Threads Check** (raises a stale open thread once per session) and a **no-topic greeting offer** (offers open threads when the client's opener has no topic of its own) — this patch's new bullet is written to sit alongside those and explicitly not share their budget. If this setup doesn't have an equivalent standing-threads mechanism, that's fine; just add the new bullet as its own thing.

---

## MANDATORY

### 1. Flag near-term events in the startup step

Find this setup's startup instruction that already handles events (look for language like "compare each event's date... to determine whether to check in before or after"). Add a clause directly after it:

> **Explicitly flag anything dated today or within the next two days** — internally note it the same way you enumerate Core/Active files (for your own tracking, not shown to the client); it drives the Near-term event check in the continuity protocol.

### 2. Add the actual check-in as its own continuity-protocol bullet

Find this setup's continuity/greeting protocol — wherever it lists "at session start" behaviors (the reference has this in `CLAUDE.md`'s Session Continuity Protocol, alongside "Check homework" and the Standing Threads Check). Add a new bullet:

> **Near-term event check:** If a tracked event is dated today or within the next two days (flagged in the startup step above), raise it directly — don't wait for it to come up on its own. "I saw [event] is [today/tomorrow] — how are you feeling about it?" for something ahead; "How did [event] go?" for something just past. If the client opens with something else pressing, follow their lead first, then bring the event up within that same session rather than deferring it silently — this doesn't get skipped the way the Standing Threads Check does during crisis, since a real, dated thing that's actually happening is usually relevant to whatever they bring, not a distraction from it. Independent of the Standing Threads Check and the no-topic greeting offer — it doesn't share their one-per-session budget.

Adjust "the next two days" to whatever window actually fits this setup — the point is only that something genuinely imminent (today, tomorrow) gets treated as a guaranteed check-in, not left to chance.

**Important — do not use the softer "look for a natural moment" phrasing.** An earlier draft of this patch used that wording and was rejected: it left the check-in optional in practice, the same problem as leaving it purely implicit. The bullet above is a commitment to actually raise it, not a hope that the conversation gets there.

### 3. Add the session-end fallback

Find this setup's session-end/close-out procedure (the reference has this in `.therapy/protocols/session-end.md`, at the very start of its "close warmly" step). Add a mandatory check right before the actual goodbye:

> **First, check the near-term event flag from session start.** If an event was flagged as today or within the next two days and never actually got raised or discussed anywhere in this session, surface it now, briefly, before the goodbye — e.g., "Before we go — I never got to ask, how are you feeling about [event] [today/tomorrow]?" This is a mandatory fallback, not a judgment call: the whole reason to flag it at session start is so a packed or heavy session can't cause it to quietly fall through unmentioned. This is the one exception to any "no new threads at close" rule this setup has — it's not opening something new, it's closing a loop that was already open going in.

If this setup's session-end procedure doesn't have an explicit "no new threads" rule at close, just add the check as its own mandatory line — the exception framing only matters if there's something to make an exception to.

---

## VERIFY

- Simulate a session start where a tracked event is dated for today or tomorrow. Confirm the assistant actually raises it early in the session — not silence, and not a client having to bring it up first.
- Simulate the same, but with the client opening on something else heavy or pressing. Confirm the assistant follows their lead first, then still raises the event later in that same session rather than dropping it.
- Simulate a session start where the nearest tracked event is a week or more out. Confirm nothing forces an unprompted mention — the flag only applies inside the window.
- Confirm this check-in can co-occur in the same session as a Standing Threads Check or no-topic greeting offer firing — it should not be blocked by either having already used its one-per-session slot.
- Simulate a full, busy session where the flagged event genuinely never comes up (the client leads the whole conversation somewhere else). Confirm the session-end fallback catches it right before the goodbye, rather than letting the session close with the event never mentioned at all.

That's the whole patch — one clause in the startup event-check step, one new bullet in the continuity protocol, one mandatory check in the session-end close, no new files, no changes to how events get tracked in the first place.
