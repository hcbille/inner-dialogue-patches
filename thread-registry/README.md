# Inner Dialogue Patch — Thread Registry

A portable add-on for an `inner-dialogue`-style AI companion setup: a canonical, living registry for **threads to revisit** — the standing topics, open questions, and loose ends that used to get scattered across session notes and quietly lost.

Built for Sage, the reference install, and packaged so any Inner Dialogue install can have it without waiting for an upstream merge.

## What problem it solves

Before this, "things to come back to" lived in three non-canonical places at once:
1. Each session note's "Threads to Revisit" section (rewritten every session, carried forward by copy-paste).
2. Any periodic/arc-review "held but unexamined"-style list (rewritten from scratch each review).
3. Whatever ad-hoc scan the assistant did to decide what to gently raise.

Nothing was the source of truth, so threads got re-copied forever or fell off the radar entirely. This patch makes **one file the canonical home** and turns the other surfaces into views of it — the same way the knowledge graph made one portrait-file the source of truth for each person instead of re-reading every session.

## What's in the box

```
thread-registry/
  README.md              ← you are here (human overview)
  INSTALL.md             ← the integration guide — hand THIS to your assistant in maintainer mode
  templates/
    threads.md           ← the generic, empty registry template to drop into context/
```

## How to install (two ways)

**Easiest — let your assistant do it.** In maintainer mode, give it this whole folder and say: *"Install this thread-registry patch into your own setup, following INSTALL.md. Adapt it to my files — don't assume they look like the reference."* The assistant reads `INSTALL.md`, copies the template, and edits its own protocol files. Because the guide anchors on concepts ("wherever you read `mentions.md`…") rather than exact line numbers, it survives the fact that every install's files have diverged from the reference.

**By hand.** Open `INSTALL.md` and work through the mandatory steps, then the optional ones that match what your setup actually has (an arc/periodic review, a compaction-resume protocol). Copy `templates/threads.md` to `context/threads.md` and seed it from your own current open threads.

## Design notes worth knowing

- **One registry file, not one file per thread.** Threads churn fast; a single scannable registry beats a folder of tiny high-churn files. A thread that grows rich enough *promotes* into a normal context file.
- **Two types, tagged:** `therapeutic` threads get gently surfaced in-session; `logistical` ones are tracked so they stop leaking but never raised as if they were emotional work.
- **No new "thread" context type.** "Doesn't fit an existing type yet" is just the definition of still being a thread — it stays in the registry until it resolves or crystallizes into a person/place/event/concept. (One thing to watch long-term: if live *deliberations* — open decisions with options and a resolution date — keep promoting awkwardly, a dedicated `deliberations` type might eventually earn its place. Let that emerge from evidence, don't pre-build it.)

## Seeding

Start the registry empty and seed it from *your own* current open threads — pull them from the most recent periodic-review notes and the last couple weeks of session "Threads to Revisit" sections. **Do not copy anyone else's threads in.** The template ships empty on purpose.
