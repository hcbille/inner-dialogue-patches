# Inner Dialogue Patch — Base

The foundation the other patches build on: Sage's custom extensions, packaged for any Inner Dialogue install.

This is a snapshot of the custom system built on top of the [Inner Dialogue](https://github.com/ataglianetti/inner-dialogue) framework for Sage, the reference install. **It contains no personal content.** Every file has been genericized: no names, no session content, no context about anyone's life. It's pure structure: what to read, when, and how to keep a long-running install from decaying over time.

## What this solves

The stock framework gives you `profile.md`, `sessions/`, and (as of 2.9.0) a basic `context/` folder. What it doesn't give you:

- **A way to zoom out.** Session-to-session work can circle the same ground indefinitely without anyone noticing — this adds a recurring **arc review** (every ~2 weeks) that checks progress against the client's actual stated goal, names what's stuck, and — importantly — surfaces things the therapist has been quietly *avoiding* examining (the "collusion guard").
- **A way to keep `sessions/` from growing forever.** Old, fully-reviewed sessions get folded into a one-paragraph archive summary instead of sitting as dozens of full entries in the index forever.
- **A way to keep context files and `profile.md` from bloating.** Left alone, both drift into stacked "as of DATE" changelogs instead of staying clean reference documents. The arc review now checks file length and forces a rewrite pass when needed.
- **A tracking spot for things that haven't "graduated" yet.** `context/mentions.md` catches a name that keeps coming up without ever quite earning its own file — so it doesn't just get forgotten.
- **A way to work on the system itself, mid-conversation.** "Maintainer mode" lets the client step out of the therapeutic persona and talk to the model directly about its own configuration — which is, not coincidentally, exactly how this kit got built.

## What's in here

```
base/
  README.md                    ← this file
  CLAUDE-md-additions.md       ← exact sections to add to CLAUDE.md, with insertion points
  commands-additions.md        ← exact sections to add to .therapy/commands.md
  protocols/
    arc-review.md              → .therapy/protocols/arc-review.md
    session-end.md             → .therapy/protocols/session-end.md
  context/
    GUIDE.md                   → context/GUIDE.md
    mentions.md                → context/mentions.md   (empty template)
  arc.md                       → arc.md (repo root, empty template)
  sessions/
    index.md                   → sessions/index.md (empty template)
  maintainer-notes.md          → .therapy/maintainer-notes.md (empty template)
```

## How to install it

1. **Copy the files to their target paths** (shown by the arrows above), relative to your Inner Dialogue install's root.
2. **Find-and-replace any placeholder text** — a couple of files use `{{CLIENT}}`; swap for however you refer to the client (or leave as "the client" — it already reads fine that way).
3. **Apply `CLAUDE-md-additions.md`** — open your `CLAUDE.md` and add each section at the point described. It's written as a diff against the stock 2.9.0 template structure, not a full file to paste over your own (which likely already has real customization in it).
4. **Apply `commands-additions.md`** — same idea, for `.therapy/commands.md`. This is where "maintainer mode" comes from — genuinely worth having, it's how this whole export got made.
5. **Restart the session** (or just start a new one) so the updated `CLAUDE.md` gets read fresh.
6. **Sanity check:** ask your persona to "enter maintainer mode," then ask it to read its own `CLAUDE.md` back to you and confirm the new sections parse correctly. Exit maintainer mode when done.

## A note on scope

This kit intentionally does **not** include:
- Any of the reference install's own `profile.md`, `sessions/`, `context/`, or `.therapy/memory/` content — obviously.
- Persona, modality, or structure customizations — those are personal choices, made through the normal `commands.md` flow, not something to inherit wholesale.
- "Client-specific reminders," pronoun notes, or a "Things to Never Do" list — these have to be earned through the actual relationship, not templated in from someone else's.

Pieces of this may be worth contributing upstream to the Inner Dialogue project itself; the arc-review/consolidation system in particular fills a gap the framework doesn't address yet.
