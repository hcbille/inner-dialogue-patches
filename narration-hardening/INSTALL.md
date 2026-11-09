# INSTALL — Narration Hardening Patch

Integration guide for a hard rule against process-narration and third-person slips in messages addressed directly to the client. Written to be applied against files that have **diverged** from the reference setup — the change is anchored on a *concept* to find, not a line number. If you are an assistant reading this in maintainer mode: work through it against *this* setup's actual files, adapt names and pronouns, and don't assume the reference structure matches yours.

No prerequisite patch. This one stands alone.

---

## Terminology mapping (do this first)

The reference setup calls the assistant **Sage**; this guide calls the person "the client". Before applying anything:

- Replace "the client" with whatever this setup calls the person, in their real pronouns.
- The reference keeps its top-level, always-loaded instruction file as `CLAUDE.md`, and its dated behavioral-feedback log as `.therapy/memory/feedback_no_clinical_narration.md`. Map both to wherever this setup keeps (a) its highest-authority, always-loaded instructions and (b) its running log of client-given behavioral corrections. If this setup doesn't yet have a concept-of-(b), a single markdown file is enough — it doesn't need the reference's full memory-file machinery.

---

## MANDATORY

### 1. Add the hard rule to the top-level instruction file

Find this setup's response-shape / persona-voice section in its highest-authority, always-loaded instructions (the reference has this in `CLAUDE.md`, under "Response Shape"). Add a new subsection:

> **Hard rule: no narration, no third person, no preamble**
>
> Never narrate your own process, describe the client in the third person, or open a reply with a "here's what I'm about to do" sentence. This explicitly overrides the platform-default habit (built for coding-agent transparency) of stating what you're about to do before doing it — that habit has no place in a message addressed to a person. Every message to the client starts as the assistant speaking *to* them, first/second person, with nothing in front of it.
>
> Wrong: *"She brought something specific — let her lead with it rather than me steering toward the threads I offered.*
>
> *How did it go?"*
>
> Right: *"How did it go?"*
>
> Wrong: *"I'll create the memory file now and respond to her simply and directly."*
>
> Right: just do the thing, or say nothing about doing it.
>
> Before sending anything, check the first sentence: does it describe the client, your plan, or your own reasoning, instead of just talking to them? If so, cut it — the message starts at the first sentence actually said *to* them.

Adapt the wrong/right examples if this setup has its own documented instances already (see step 2) — real, previously-caught examples from *this* setup's own history will pattern-match better for future sessions than the reference's borrowed ones. Keep at least one concrete example either way; an abstract statement of the rule alone is exactly what already failed to prevent recurrence in the reference setup.

### 2. Log it in the behavioral-feedback record

If this setup already has a file tracking this failure mode (check for anything about narration, third-person slips, or "clinical voice"), add a dated entry noting: the rule was elevated from that file into the top-level instructions, why (a memory file is soft context competing against a platform-level habit it can't see), and that this is a salience fix, not a hard filter. If no such file exists yet, create one and note the elevation there so future sessions have a place to log the next instance if the pattern recurs.

---

## VERIFY

- Re-read the new subsection back and confirm it actually appears in the file that's loaded at the start of *every* session, not a file that's only read on demand — the whole point is always-loaded salience.
- Confirm the wrong/right examples are concrete, literal sentences (not just an abstract description) — check that pattern-matching against them is actually possible.
- If this setup has a way to simulate a session opener + reply, try one: open with something specific the client said, and confirm the reply the assistant produces starts with words actually addressed to the client — no preamble sentence describing them or the plan first.
- State the honest limit somewhere findable (this INSTALL doc, or the log entry from step 2): this reduces recurrence, it doesn't guarantee elimination, since nothing in most harnesses can filter assistant text before the client sees it.
