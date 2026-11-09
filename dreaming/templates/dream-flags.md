# Dream Flags in Sessions

Sometimes a dream finds something in the notes about the client that might no longer be right. Two sessions may seem to disagree, or there may be a proposed profile change waiting. The dream doesn't decide these on its own. It writes them to `dreams/flags.md`.

They're asked during dream review in maintainer mode. If the client has opted in, the assistant may also ask them gently during ordinary sessions. The startup script prints a "Dream flags" line naming the one flag that may be asked this session: the oldest open one. A flag that was already asked and set aside waits 30 days before it can be asked again.

*If the client hasn't opted in to in-session asking, delete this file and the CLAUDE.md bullet that points here. Flags are then only answered during review, or with "show my dream flags".*

## When the assistant may ask

All of these must hold:

- The session opened neutrally, and there's a natural lull. Never at the start of a heavy session. Never during crisis or acute grief, or while the client is in their body.
- The client hasn't brought something of their own that's still unfolding.
- No other housekeeping has been offered this session (a profile review, an open-thread offer, a standing-threads check, an arc review). One piece of housekeeping per session at most.
- The flag isn't about a boundary subject. Flags never are; the dream protocol forbids it.

**Ask at most one flag per session:** the one the startup script names.

## How to ask

- Ask about the notes, not about them: "I've got two different things written down about X — which is closer to how it is now?"
- Say it in plain words, once. Don't explain the dream system unless they ask.
- Offer an easy way out: "Or we can leave it — it's not important."
- Don't interpret their answer, and don't turn it into a conversation about why it changed unless they take it there.

## Recording the answer (at session end)

In `dreams/flags.md`, update the flag:

| The client's response | Record |
|---|---|
| Answered | `answered (YYYY-MM-DD)`, plus their answer in their own words and the session file |
| Set aside ("not now") | `asked (YYYY-MM-DD)`. Don't ask it again for at least 30 days. |
| Didn't want it ("leave it", "doesn't matter") | `dropped (YYYY-MM-DD)`. Never ask it again. |

Don't change any other file because of the answer. The next dream applies answered flags, with the session as evidence.
