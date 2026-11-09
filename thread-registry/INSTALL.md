# INSTALL — Thread Registry Patch

Integration guide for adding the thread registry to an `inner-dialogue`-style setup. Written to be applied against files that have **diverged** from the reference setup — every change is anchored on a *concept* to find, not a line number. If you are an assistant reading this in maintainer mode: work through it against *this* setup's actual files, adapt names and pronouns, and don't assume the reference structure matches yours.

Two tiers: **Mandatory** (the feature itself) and **Optional** (only if your setup has the named module). Do the mandatory steps in order; do each optional step only if the anchor it names actually exists here.

Before you start: skim `templates/threads.md` — it's self-documenting (schema, lifecycle, type model, promotion rule live in its own header). Most of the behavior lives *in that file*; the steps below are mostly about wiring the rest of the system to read and maintain it.

---

## Terminology mapping (do this first)

The reference setup calls the assistant **Sage**; this guide calls the person "the client". Before applying anything:

- Replace "the client" with whatever this setup calls the person, in their real pronouns.
- If this setup's context library uses different folder names than `context/people|places|concepts|events`, map accordingly. The registry only assumes a `context/` folder and (ideally) a `context/mentions.md` and `context/index.md` — if those don't exist, see the notes inline.
- **Linking convention:** the reference build used Obsidian `[[double-bracket]]` links to reference people/concepts. This setup may not. Use whatever cross-reference style this setup already uses in its context files — plain names are completely fine. Don't introduce a linking format the setup isn't already running.

---

## MANDATORY

### 1. Add the registry file

Copy `templates/threads.md` → `context/threads.md` in this setup. Leave it empty for now (seeding happens in step 6). If there's no `context/` folder, put it wherever this setup keeps its context library, and adjust the paths referenced below to match.

### 2. Document the type in the context-library guide

Find this setup's context-library documentation (the reference calls it `context/GUIDE.md` — the file that explains how context files, `mentions.md`, status levels, etc. work). Add:

- **To its folder-structure diagram** (if it has one): a line for `threads.md ← the open-thread registry (things to revisit)` alongside `mentions.md`.
- **A short section** documenting the new type. It doesn't need to restate the schema (that lives in `threads.md`'s own header) — it needs to establish three things:
  1. `threads.md` is the **canonical** home for threads-to-revisit; the per-session "Threads to Revisit" notes and any periodic-review "held but unexamined" list are now **derived views** of it, not parallel lists.
  2. It's a protocol-referenced tracking file like `mentions.md` — read/scanned at session start, reconciled at session end, **not** a Core subject and **not** listed in `index.md`.
  3. The entry bar ("must outlive the session it was named in") and the **no-fifth-type** rule (an unclassifiable thread stays a thread; it promotes into an existing type or waits — don't invent a new folder for it).

If this setup has no context-library guide file, skip — `threads.md`'s own header is the reference.

### 3. Read it at session start

Find this setup's session-start / startup protocol — specifically wherever it reads `context/mentions.md` or the context index. Add a read of `context/threads.md` alongside it, with a note like:

> **Also read `context/threads.md`** — the open-thread registry (the canonical list of standing topics to revisit). Scan the Open set so it's in context before the greeting; it drives the standing-threads check.

If this setup has no explicit startup file, add the read wherever it establishes session context before greeting the client.

### 4. Point the standing-threads check at the registry

Find whatever mechanism this setup uses to gently resurface carried-over topics — a "standing threads check," "continuity check," "things to revisit," or similar. Rewrite it to draw from the registry instead of scanning prose:

> Read `context/threads.md`. From the **Open + therapeutic** set, take the item whose *Last surfaced* date is more than 7 days old and is the stalest — name it gently **once** at a natural moment ("A while back you mentioned X — want to pick that up sometime, or let it rest?"). If they decline or ask to set it down, mark that entry **Shelved** (today's date) and stop carrying it as active — a Shelved thread gets only a rare, light "still feel right?" check, never a push. Never surface a **logistical** thread as if it were emotional work. At most one standing thread per session, never during crisis or acute distress.

If this setup has **no** such mechanism, add a lightweight version of the above to the startup or continuity protocol. Even with no surfacing mechanism at all, the registry still works as a durable, canonical list — this step is what makes it *proactive*.

### 5. Reconcile it at session end

Find this setup's session-end / wrap-up protocol. Add a **reconcile step** (place it after the session note and context-file updates, before the commit/save step). Two parts:

**(a) Demote the per-session snapshot.** Wherever the session-note template has a "Threads to Revisit" section, mark it as a *same-day snapshot only* and stop the copy-paste carry-forward — no more "carried forward, still untouched…" lists ported between session notes. The registry owns carry-forward now.

**(b) The reconcile step itself.** Read `context/threads.md`, then from today's session:

1. **Bump what was touched** — for any existing entry that came up today, set *Last surfaced* to today and append today's session file to its **Sessions** list. (This is what keeps a live thread from being re-surfaced next week.)
2. **Add genuinely-new standing threads** — for anything in today's "Threads to Revisit" snapshot expected to outlive this session, add an entry per the schema (set Type, Opened = today, Last surfaced = today, Subjects, Sessions, description, Surfacing rule). Skip anything that opened *and* closed within today's session.
3. **Close what resolved** — set Status: Closed (today), move to `## Archived` with a one-line outcome.
4. **Shelve what they set down** — set Status: Shelved (today), adjust the Surfacing rule.
5. **Promote what outgrew the file** — if a thread has real texture across several sessions, has become a worked arc rather than a reminder, **and clearly fits an existing context type** (usually a concept): create the file, seed it with a "Prior thread" section (description + full Sessions trail), add it to `index.md`, then set the entry to Promoted and move it to `## Archived` as a pointer. **If it doesn't clearly fit a type, leave it Open — it isn't ripe.**

---

## OPTIONAL — only if this setup has the named module

### 6. Periodic / arc review (if present)

If this setup has a periodic zoom-out review (the reference calls it the "arc review", ~every two weeks) with a "held but unexamined"-style collusion-guard list:

- Reframe that list as an **audit of the registry** rather than a from-scratch rewrite: at each review, read the Open + therapeutic set and ask which threads are being held sympathetically without ever being examined; reconcile as you go (close resolved, shelve set-down, correct stale *Last surfaced* dates). Let the review's written list be a *snapshot* of that audit, not a parallel list that drifts.
- Add a **consolidation pass** to the review's maintenance section: prune old Archived entries, catch threads that should have been closed/shelved but weren't, correct stale metadata, and flag promotion candidates.

If there's no periodic review, skip this entirely — the feature is fully functional without it (session-end reconciliation keeps the registry honest).

### 7. Compaction / resume protocol (if present)

If this setup has a post-compaction or resume protocol that reloads key files after the context window is summarized, add `context/threads.md` to that reload set (near wherever it reloads the context index or recent sessions), noting it holds the canonical open-thread set.

If there's no such protocol, skip.

---

## SEEDING (do this last, once wired in)

Seed `context/threads.md` from *this* setup's own current open threads — harvest them from the most recent periodic-review notes (if any) and the last ~2 weeks of session "Threads to Revisit" sections. For each: write the entry, set Opened to when it first came up (best effort), Last surfaced to the most recent session that touched it, and the Sessions trail from the notes you found it in. Tag Type honestly (therapeutic vs. logistical) and give each a Surfacing rule — especially any thread that should **not** be raised unprompted (mark those explicitly).

**Never seed in threads from another person's setup.** The template ships empty for exactly this reason.

---

## VERIFY

- Open `context/threads.md` and confirm every **subject reference** in the seeded entries points at a real context file in this setup (create/fix as needed), using whatever naming/linking convention this setup uses. If this setup has a link-cleanup script, run it.
- Do a dry run of the standing-threads check logic against the seeded Open set — does it pick a sensible stalest item, and correctly skip logistical and Shelved ones?
- Commit/save through this setup's normal mechanism.

That's the whole feature. The registry is now the single source of truth for threads to revisit, and every other surface reads from it.
