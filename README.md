# Inner Dialogue Patches

Add-ons for [Inner Dialogue](https://github.com/ataglianetti/inner-dialogue), the private, file-based AI therapist that runs in Claude Code.

Each patch fixes a problem that came up in real use of a long-running install called **Sage**, the reference install. Sage's own files are private, so nothing here comes from its sessions. These are the generic mechanisms, written so any install can adopt them.

**This is not part of the Inner Dialogue project**, and its maintainers don't review it. Inner Dialogue is an AI support tool, not a licensed therapist, and these patches don't change that. Keep the safety protocol intact.

## How the patches work

Every install's files drift away from the stock template as they're customized, so the patches don't ship diffs. Each folder has:

- `README.md`: the human overview (what it fixes, design notes, limits).
- `INSTALL.md`: the integration guide. Each change is anchored on a *concept* to find ("wherever your session-start protocol reads `mentions.md`"), not a line number.
- `templates/` (some patches): files to copy in.

The easiest way to install one is to let your assistant do it. In maintainer mode (from the `base` patch), give it the folder and say:

> Install this patch into your own setup, following INSTALL.md. Adapt it to my files — don't assume they look like the reference.

Or work through `INSTALL.md` by hand.

## The patches

| Patch | What it does | Needs |
|---|---|---|
| [`base`](base/) | Maintainer mode, a richer session-end protocol, arc reviews (a zoom-out every ~2 weeks), a context-library guide, `mentions.md`. | — |
| [`opus-5-5-rebaseline`](opus-5-5-rebaseline/) | **Crisis resources for the client's own country** (the stock list is US-only), a startup script that builds the reading list, and a re-tune for Claude Opus 5.5. | — |
| [`narration-hardening`](narration-hardening/) | A top-level rule against narrating process or describing the client in the third person in messages meant for them. | — |
| [`momentum-protection`](momentum-protection/) | Offer a stop-or-continue check only when the person shows a real sign of wanting to stop, not whenever the subject gets heavy. | — |
| [`thread-registry`](thread-registry/) | One canonical file for threads to revisit, gently surfaced when they go stale. | — |
| [`no-topic-greeting-offer`](no-topic-greeting-offer/) | When the client opens with a plain hello, offer up to two open threads as optional starting points. | `thread-registry` |
| [`near-term-event-surfacing`](near-term-event-surfacing/) | Raise events dated today or in the next two days, with a session-end fallback if they never came up. | some event tracking |
| [`context-loader`](context-loader/) | A hook that tells the assistant which context files to read, based on what the client just said. | — |
| [`dreaming`](dreaming/) | Offline memory consolidation between sessions, reviewed before it lands and undoable in one commit. Includes audit dreams and a research synthesis. | `base`, a git repo; `opus-5-5-rebaseline` for part 3 |

If you're outside the US, start with part 1 of `opus-5-5-rebaseline`.

## Suggested order

1. `base`
2. `opus-5-5-rebaseline` (part 1 at least)
3. `narration-hardening`, `momentum-protection`
4. `thread-registry`, then `no-topic-greeting-offer`
5. `near-term-event-surfacing`, `context-loader`
6. `dreaming`, in its five parts, after a few weeks of sessions

## Privacy

The patches ship empty templates on purpose. Seed registries, topic links and memory files from your own install, never from anyone else's. Every patch was scanned for personal content before publishing. If you find something that looks personal, please open an issue.

## License

MIT, same as Inner Dialogue. See [LICENSE](LICENSE).
