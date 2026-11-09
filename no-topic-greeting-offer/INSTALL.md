# INSTALL — No-Topic Greeting Offer Patch

Integration guide for a small addition to the `thread-registry` patch. Written to be applied against files that have **diverged** from the reference setup — the change is anchored on a *concept* to find, not a line number. If you are an assistant reading this in maintainer mode: work through it against *this* setup's actual files, adapt names and pronouns, and don't assume the reference structure matches yours.

**Prerequisite check first:** confirm `context/threads.md` (or wherever this setup's open-thread registry lives) already exists and is read at session start. If it doesn't, stop and install the `thread-registry` patch first — this patch has nothing to draw from without it.

---

## Terminology mapping (do this first)

The reference setup calls the assistant **Sage**; this guide calls the person "the client". Before applying anything:

- Replace "the client" with whatever this setup calls the person, in their real pronouns.
- The reference registry's schema uses `Status`, `Type`, `Last surfaced`, and a per-entry `Surfacing` rule. If this setup's registry uses different field names for the same concepts, map accordingly — the logic below only depends on those four concepts existing in some form.

---

## MANDATORY

### 1. Add the no-topic greeting offer

Find this setup's continuity/greeting protocol — wherever it lists "at session start" behaviors (the reference has this in `CLAUDE.md`'s Session Continuity Protocol, right where it says "Reference previous content naturally: ..."). Add a new rule near the top of that list, before any "check homework" / "standing threads check" style bullet:

> **No-topic greeting offer:** If the client's opening message is a plain greeting/check-in with no specific topic to respond to, the greeting itself may offer open threads as optional starting points, e.g.: "Hi [name], is there anything particular on your mind? Otherwise we could start with one of these threads we've talked about before." Draw only from the **Open + therapeutic** set in the thread registry, excluding any entry whose **Surfacing** note says not to raise unprompted (do-not-raise, return-only-if-reopened threads) and any entry whose *Last surfaced* is **5 days or less** old. Offer up to 2, framed as a menu, not a push — the client choosing one, declining, or bringing their own topic instead are equally fine outcomes. Skip entirely during crisis or acute distress. Offering a thread this way counts as surfacing it (update its *Last surfaced* date) and takes the place of the standing-threads check for that session — don't also run the single-stale-thread nudge later once this has fired.

Adjust the "5 days" threshold to whatever fits this setup's actual session cadence — the point is only that a thread surfaced very recently (e.g. last session) shouldn't be immediately re-offered as if it were a fresh starting point. If sessions here run daily, 5 days is probably right as-is; if they run weekly, consider shortening it so the pool isn't perpetually empty.

### 2. Confirm it doesn't double-fire with the standing-threads check

Whatever mechanism this setup uses for the later single-stale-thread nudge (installed by the `thread-registry` patch), make sure the "at most one standing thread per session" rule it already states actually covers this new bullet too — i.e. if the greeting fires this offer, the later nudge should not also fire in the same session. If that global one-per-session cap already exists (it should, from the `thread-registry` patch), no rewrite is needed here — just don't introduce contradictory wording.

---

## VERIFY

- Simulate an opening message that's a plain greeting with nothing else in it (e.g. "hey" / "hi, how's it going"). Confirm the assistant's response would pick ≤2 qualifying threads (Open, therapeutic, no do-not-raise flag, *Last surfaced* older than the threshold) and offer them as a menu rather than asserting one as the topic.
- Simulate an opening message that *does* bring a topic. Confirm this new rule stays silent and the standing-threads check (if its own 7+ day condition is met) is still the only thread-surfacing path available later in that session.
- Check the registry after a simulated no-topic-offer run: whichever thread(s) were offered should have their *Last surfaced* date bumped to today, same as any other surfacing.

That's the whole patch — one new rule in the greeting/continuity protocol, reusing the registry and surfacing conventions the `thread-registry` patch already established.
