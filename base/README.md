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
  scripts/
    evidence_check.py          → .therapy/scripts/evidence_check.py
```

## How to install it

1. **Copy the files to their target paths** (shown by the arrows above), relative to your Inner Dialogue install's root.
2. **Find-and-replace any placeholder text** — a couple of files use `{{CLIENT}}`; swap for however you refer to the client (or leave as "the client" — it already reads fine that way).
3. **Apply `CLAUDE-md-additions.md`** — open your `CLAUDE.md` and add each section at the point described. It's written as a diff against the stock 2.9.0 template structure, not a full file to paste over your own (which likely already has real customization in it).
4. **Apply `commands-additions.md`** — same idea, for `.therapy/commands.md`. This is where "maintainer mode" comes from — genuinely worth having, it's how this whole export got made.
5. **Restart the session** (or just start a new one) so the updated `CLAUDE.md` gets read fresh.
6. **Sanity check:** ask your persona to "enter maintainer mode," then ask it to read its own `CLAUDE.md` back to you and confirm the new sections parse correctly. Exit maintainer mode when done.

## Updating an install that already has base (2026-11-11)

**Session end backs every claim with the session note.** In the reference install, two audits of older context files against their session notes found over a hundred drifted lines, almost all written at session end: quotes that were paraphrases, the assistant's own lines attributed to the client, and details from pasted chats that never reached a note. Once a context file says it, later sessions read it back as fact, and nothing can check it.

1. Copy `scripts/evidence_check.py` to `.therapy/scripts/evidence_check.py`. If the client keeps a file that is their own writing rather than a record of sessions (a draft, a journal they edit), add its path to `SKIP` in the script.
2. In your session-end protocol, right after the session-note template, add the **"The note is the evidence for everything after it"** block from `protocols/session-end.md`. Adjust the step numbers if yours differ.
3. At the top of the step that updates context files from the "Context Touched Today" list, add the one-line pointer back to that rule.
4. In the save step, before the commit, add the **"Evidence check first"** paragraph.
5. Optional: try it on a past session end, `python3 .therapy/scripts/evidence_check.py --commit <sha>`. In the reference install it flagged 10 unbacked quotes across five of seven recent session ends.

If you have the `dreaming` patch, this applies unchanged. Session end still captures, and the dream's "never invent" rule covers what dreams write.

**Later the same day: quotes the client confirmed in a dream review count as evidence.** When the client confirms in review that quoted words no note has are theirs, those words stay in quotation marks. The first version of the check kept flagging them at every later commit that touched the line. To pick this up, copy `scripts/evidence_check.py` again, and keep your own `SKIP` entries. It now also reads the Answer of each answered flag in `dreams/flags.md`, and never the Question. Without the dreaming patch there is no flags file, so nothing changes. With it, apply the matching `dream-review.md` change from the dreaming patch's INSTALL.md (2026-11-11).

## Changelog

- **2026-11-11 (later):** **Change:** `evidence_check.py` also counts the Answer of an answered flag in `dreams/flags.md`, where a dream review records quoted words the client confirmed. Flag Questions never count. No effect without the dreaming patch.
- **2026-11-11:** **New:** an evidence rule for session end (exact quotes only, also written in the note; the assistant's lines credited to the assistant; the kind of claim kept; pasted material carried into the note; note first) and `scripts/evidence_check.py`, which lists quotes added to `profile.md` or `context/` that no session note has. See "Updating an install that already has base (2026-11-11)".

## Relationship to the dreaming patch

The [`dreaming`](../dreaming/) patch takes over part of what this patch's arc review does. **Install this patch anyway, and install it first.** Dreaming is built on top of it.

**What dreaming takes over** (once its part 5 is installed):
- the arc review's **"Maintenance: Context File Consolidation"** section: long context files, `profile.md` Current Focus, overlong `context/index.md` lines. Dreams now do this as their rotating "consolidation" library pass, about every two weeks;
- the **folding and condensing rules** in this patch's `session-end.md`. Dreaming part 3 slims session end to capture only, and dreams consolidate;
- the "enforcement point is the arc review" line in `context/GUIDE.md`. After part 5, the enforcement point is the dreams.

**What it doesn't replace, and depends on:**
- **The arc review conversation itself.** The five headings, the collusion guard ("held but unexamined") and the autonomy check are a conversation with the client. A dream never talks to the client, so it can't do any of this.
- **`arc.md`, the session-index collapse and the archive.** Dreams read `arc.md` while orienting, and the "summaries" pass relies on the index collapse keeping `sessions/index.md` small.
- **The arc review's two-week rhythm.** The dream's "threads" pass prunes Archived threads "older than two arc reviews", and the library rotation is paced to match it.
- **The rest of this patch:** maintainer mode (dreams only run from there), the session-note template with "Context Touched Today" (how a dream finds its regions), `context/GUIDE.md`'s conventions (what a dream keeps files consistent with), `mentions.md` (what a dream promotes from) and `maintainer-notes.md` (where dream reviews are logged).

**In order:** install this patch, use it for a while, then add `dreaming` parts 1–3. When you install part 5, replace this patch's arc-review Maintenance section as `dreaming/INSTALL.md` describes. Without the dreaming patch, this patch works on its own, unchanged.

## A note on scope

This kit intentionally does **not** include:
- Any of the reference install's own `profile.md`, `sessions/`, `context/`, or `.therapy/memory/` content — obviously.
- Persona, modality, or structure customizations — those are personal choices, made through the normal `commands.md` flow, not something to inherit wholesale.
- "Client-specific reminders," pronoun notes, or a "Things to Never Do" list — these have to be earned through the actual relationship, not templated in from someone else's.

Pieces of this may be worth contributing upstream to the Inner Dialogue project itself; the arc-review/consolidation system in particular fills a gap the framework doesn't address yet.
