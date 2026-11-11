# Inner Dialogue Patch — Dreaming

Offline memory consolidation for an Inner Dialogue install. It runs between sessions, is reviewed before it lands, and can be undone in one step.

Built for Sage, the reference install, on 2026-10-30, after researching how "dreaming" works for AI agents. Anthropic, Letta and several research papers use the idea in some form; `background/research-synthesis.md` has the research. It's packaged here so any Inner Dialogue install can have it. **It contains no personal content**: everything is genericized to "the client" and "the assistant".

**Prerequisites:**
- the `base` patch, including its arc review (see "How it relates to the arc review" below);
- maintainer mode (`base` patch);
- session notes with a "Context Touched Today" list (`base` patch, `session-end.md`);
- a git repo;
- for part 3, the startup script from `opus-5-5-rebaseline`.

`thread-registry`, `context-loader` and the `base` patch's `mentions.md` are optional. The dream tidies whichever of them exist.

## What problem it solves

Over time, a long-running install's memory files drift:
- index lines and thread descriptions pick up dated bold updates;
- context files fall behind what the sessions say;
- duplicate entries pile up;
- the startup reading gets heavier every month.

Session end was doing all the tidying itself. That means a long, careful rewrite at the end of every session, often late at night, by the same context that just held the therapy conversation. It's the step most likely to be skipped, rushed, or done halfway.

Research on agent memory has converged on a fix: **separate capture from consolidation.** Capture in the moment; consolidate later, offline, with a view across several sessions. That's a "dream".

## How it works

- **Session end captures.** The note, its index line, and only what the next greeting can't do without: new files, events, status changes, handling-rule changes.
- **A dream consolidates.** In maintainer mode the client says "dream". A helper agent reads every session note since the last dream and brings the standing files up to date, one region at a time. It uses a closed set of operations (SUPERSEDE, MERGE, ARCHIVE, PROMOTE, LINK, REFRESH-SUMMARY, FLAG, PROPOSE). It works on its own `dream/YYYY-MM-DD` branch and writes a report: every change, why, and which sessions it came from.
- **The client reviews it.** Each region gets keep, edit or drop. Questions about the client (flags) are answered, saved for a session, or dropped. Profile proposals are confirmed or declined. The dream then lands as **one commit**, which `git revert` can undo at any time.
- **Nothing is lost in between.** The startup script keeps undreamed session notes on the reading list and says when a dream is due (3+ sessions and 2+ days, or the reading list getting heavy).

### What a dream never does
- Edit session notes or the client's memory files.
- Edit the protocols, persona or CLAUDE.md.
- Edit the profile's never-do list, or change the profile without the client's yes.
- Add anything that isn't in a session note.
- Decide between two conflicting things about the client; it asks instead.
- Raise a boundary subject anywhere new.
- Merge itself, or run in a cloud session.

## How it relates to the arc review

Dreaming partly supersedes the `base` patch's arc review, but it doesn't replace it. **Install `base` first, and keep its arc review.**

- **Superseded:**
  - the arc review's backend housekeeping: "Maintenance: Context File Consolidation", which moves to the dreams' rotating library pass in part 5;
  - the `thread-registry` patch's arc-review "consolidation pass", which becomes the "threads" library pass;
  - the folding rules in `base`'s session end, which part 3 moves to dreams.
- **Not superseded:** the arc review conversation. The zoom-out against the client's goal, the collusion guard ("held but unexamined") and the autonomy check all need the client in the room, and a dream never talks to the client. The `arc.md` entry and the session-index collapse stay with the arc review too.
- **Dreaming relies on `base`:**
  - maintainer mode, which is the only place a dream runs;
  - the session-note template's "Context Touched Today", which is how a dream finds its regions;
  - `context/GUIDE.md` conventions, which dreams keep files consistent with;
  - `mentions.md`, for PROMOTE;
  - `arc.md`, which dreams read while orienting;
  - the two-week arc rhythm, which the threads pass and the rotation are paced to.

So after part 5 the split is: the arc review is the conversation, and dreams are the housekeeping.

## What's in the box

```
dreaming/
  README.md                        ← you are here (human overview)
  INSTALL.md                       ← the integration guide — hand THIS to your assistant in maintainer mode
  templates/
    dream.md                       → .therapy/protocols/dream.md
    dream-review.md                → .therapy/protocols/dream-review.md
    dream-flags.md                 → .therapy/protocols/dream-flags.md   (optional)
    dreamer.md                     → .claude/agents/dreamer.md
    dreams-index.md                → dreams/index.md
    dreams-flags.md                → dreams/flags.md
    startup-dream-additions.py     → pasted into .therapy/scripts/startup.py (part 3)
    dream_metrics.py               → .therapy/scripts/dream_metrics.py   (part 3)
    dream-audit.md                 → .therapy/protocols/dream-audit.md   (part 4)
    audit_next.py                  → .therapy/scripts/audit_next.py      (part 4)
    dreams-audit.md                → dreams/audit.md                     (part 4)
  background/
    research-synthesis.md          ← the research behind it (definitions, approaches, risks)
```

## How to install

**Easiest: let your assistant do it.** In maintainer mode, give it this folder and say: *"Install this dreaming patch into your own setup, following INSTALL.md. Adapt it to my files — don't assume they look like the reference. Ask me the decisions first. Do parts 1 and 2 now; part 3 only after we've reviewed a dream or two."*

**By hand.** Work through `INSTALL.md` in order.

It installs in five parts, matching how it was built for Sage:
1. **Manual dreams and review.** Purely additive; nothing about sessions changes.
2. **The dreamer helper agent.** Dreams run in a clean context window.
3. **Session end captures, dreams consolidate.** Session end gets lighter, and the startup script learns about dreams. Do this only after dreams have proven themselves.
4. **Audit dreams** (optional). Go back over the older notes a few context files at a time, checking each claim against the session it came from.
5. **Arc-review maintenance moves to dreams.** Three whole-library passes (threads, summaries, consolidation) take turns, one per dream, so the arc review is just the conversation.

**Already have dreams installed?** INSTALL.md's "Updating an install that already has dreams (2026-11-09)" section has a bug fix for same-day sessions, which you should apply, plus the audit dream. The 2026-11-10 section adds length limits for thread entries.

## Decisions to make with the client first

INSTALL lists them:
1. Who reviews dreams, and whether the assistant may ask flagged questions in normal sessions.
2. Whether dream reports are visible or hidden.
3. Whether the profile stays propose-only (strongly recommended).
4. Whether dreams are restricted to the client's own machine.

Sage's answers were: flags may be asked in sessions (one at a time, gently), visible reports, profile propose-only, and own machine only.

## Design notes worth knowing

- **Session notes are the source of truth, and they're never edited.** Every change has to cite the sessions it came from, and the dream rebuilds from the notes, not from the file's previous wording. Re-paraphrasing a paraphrase is how memory drifts.
- **Keep the kind of each claim.** What the client said, what the assistant observed, and the client's own rules stay distinct. A dream never turns an observation into a fact, or a one-off wish into a rule. The research name for the failure this prevents is "authority collapse". It showed up in almost every consolidator tested.
- **Flag, don't resolve, conflicts about the person.** A newer statement can be a hard day, not a new truth. Facts about the world (dates, jobs, events) are updated normally.
- **One reviewable unit.** One branch, one report, one commit. Git gives the install what vendor systems build "memory versions" for.
- **Self-check with the next greeting.** Before committing, the dream runs the startup script and checks the next session would know what it needs: events, handling rules, and every memory miss fixed.
- **Every few sessions, not nightly.** The due rule (3+ sessions and 2+ days since the last dream) exists because over-consolidation erodes rare details.

## Honest limits

- The rules are prompt instructions. They make bad edits unlikely, not impossible. The review and the diff check are the real guard.
- A dream can't recover what session end never wrote down. The Memory Misses section in each session note is how gaps surface.
- After part 3, context files lag behind their notes until the next dream. The startup script bridges up to six undreamed sessions, then says the dream is overdue.
- In the reference install, the first dream (10 sessions) changed 9 files, cut the startup reading by about 2%, and every change was kept in review. Your mileage will vary.

## Changelog

- **2026-11-11:**
  - **Change:** dream review records quoted words the client confirmed in the flag's Answer (`Confirmed words: …`), so the base patch's evidence check treats them as backed. See INSTALL.md, "Updating an install that already has dreams (2026-11-11)".
- **2026-11-10:**
  - **Fix:** `audit_next.py` gave a file only the plain note for a date it cites (07-02), when the evidence was often in that day's lettered notes (07-02b, 07-02d). A plain date now brings in every note from that day.
  - **New:** length limits for thread entries in the threads library pass (description ~400 characters of current state, Sessions = first + latest three, Surfacing in one or two sentences). Folding dated add-ons kept the registry's length; now the pass cuts it. See INSTALL.md, "Updating an install that already has dreams (2026-11-10)".
  - **New:** when startup prints only part of the thread registry (`opus-5-5-rebaseline`, same date), those bytes still count toward the dream threshold (BLOCK C).
  - **New:** `dream_metrics.py`, which prints every number a dream report records, measured the same way before and after, including the startup size projected after merge. Replaces summing file sizes by hand.
- **2026-11-09:**
  - **Fix:** a session held later on the day a dream merged (`…b`) was treated as covered, dropped off the startup list and never dreamed. "Undreamed" now compares full session names, and the dream index records them.
  - **New:** audit dreams (part 4).
  - **New:** arc-review maintenance moves to dreams as a rotating library pass (part 5; Sage's "Phase 4").
- **2026-10-30:** first release (parts 1–3).

## Not in this patch yet

Sage has one more phase planned. It will come as an update to this patch once it's built and tested:
- **Phase 5: scheduled dreams.** A local scheduled task starts a dream when one is due. Optionally, only low-risk changes (link fixes, index trims, mentions housekeeping) merge without review. Anything describing the client always waits for review.
