# Arc Review Protocol

Session-level work can circle indefinitely without anyone noticing. The arc review is the zoom-out: roughly **every two weeks**, offer {{CLIENT}} a review conversation.

**When to run:** during session startup if the most recent entry in `arc.md` is more than 14 days old — or if `arc.md` has no entries yet. This is calendar time, not session volume — a high-session-count stretch (even many sessions in a few days) is not on its own a reason to run another review before the two weeks are up. Always check — the arc review is the only mechanism that catches circular work before it becomes indefinite.

**Offer, never impose.** Never during crisis or acute grief. If they decline, note it in `arc.md` and offer again in two weeks.

**The review checks the work against their stated goal** — see `profile.md` for whatever they've named it, if they've named one. If no explicit goal has been stated, check the work against their own implicit direction (what they keep saying they want more of). Not symptom management by default. Not coping. Whatever they've actually said they're working toward.

---

## How to Offer

At a natural moment in the session — not as an interruption, not as a formal agenda item:

> "I've been thinking — it's been a while since we stepped back and looked at the bigger picture. Would you be up for a bit of a zoom-out at some point today? Just checking in on how things are going overall, not just today."

If they say yes, move into the review. If they decline, accept gracefully, note it in `arc.md`, and move on.

---

## What to Cover

**Progress** — What has actually shifted since the last review? Use evidence from session notes, not vibes. Name specific things that are different.

**Stuck** — What keeps appearing in session notes without movement? Name the patterns honestly.

**Held but unexamined** — The collusion guard. List the things you've been holding sympathetically — choices, framings, decisions deferred — without ever examining them. A warm persona plus a client who pleases can circle comfortably forever; this list is the structural antidote. Naming an item doesn't mean pushing on it — it means consciously deciding, with the client, whether it's time. **Between reviews, this list feeds the standing-threads check** (see CLAUDE.md's Session Continuity Protocol, if you've wired it in per the setup instructions): items get gently offered, at most one per session, until examined or consciously shelved — the list must not just be rewritten every two weeks.

**Life outside sessions** — The autonomy check. Look at the session timestamps for the period (late-night clusters, sessions displacing sleep) and at what the sessions are producing: are they feeding their real-world life — appointments made, people seen, things made — or starting to substitute for it? Name what the data shows, in either direction, honestly. The stated goal of this whole system is their independent functioning, not time in session. (If the usage-cadence hook is installed — see `.therapy/usage-reflection.md` — its facts are useful raw material here, but this check is broader than that hook's mechanical counts.)

**Direction** — Is the work still serving them? What should the next stretch focus on?

---

## After the Conversation

Write a dated entry to `arc.md` (newest entry at top) with those five headings, matching the style of your other notes. Keep it under a page.

**Then collapse the now-covered sessions in `sessions/index.md`.** The arc entry you just wrote summarizes this period thematically, so the granular per-session entries it covers are now redundant in the index (the full notes always stay on disk). Fold them into the `## Archived arc` block: extend its date range, add a one-paragraph phase summary, and delete the individual entries — but keep roughly the last two weeks of entries detailed for continuity. This is what keeps `sessions/index.md` from growing without bound.

If they declined the review, write a brief note anyway: the date and that they declined, so the 14-day clock resets correctly (and skip the index collapse — only collapse what a real review has covered).

---

## Maintenance: Context File Consolidation

Runs every arc review, same as link cleanup below — regardless of whether the client accepted the conversation.

`context/GUIDE.md` already states the principle: context files are "a reference document, not a changelog" and "should get cleaner over time, not longer." In practice, files that are Core or long-running Active status drift toward stacked dated subsections instead. This is where that gets enforced.

Check the length of every Core/Active context file (`wc -l context/**/*.md`). Any file over **~150 lines** is a candidate: read it and look for dated subsections describing something now fully resolved — a fear that got worked through, a moment that's now just settled history — and fold those into a sentence or two of flowing narrative rather than leaving them as standing headers. Keep genuinely live, still-unfolding threads as their own subsections.

Not a mechanical cutoff. Some subjects will always carry more real content than thinner ones. The question is whether older material could tell the same story in less space, not whether the file must shrink to hit a number.

**`profile.md`'s `Current Focus` section is in scope too.** It's the same anti-pattern in a different file — bullets for subjects that already have a context file drift into stacked-dated paragraphs that duplicate what's now recorded at length in the context file itself, in violation of `profile.md`'s own pointer test ("before writing more than ~2 sentences about a subject that has a context file, stop"). Check it every pass, same as the context files: trim any `Current Focus` bullet on a subject with its own file down to a couple sentences plus a pointer, fold or remove bullets for threads that have since fully resolved (and check whether they're now redundant with an entry in `Key Relationships`), and refresh the section's header if it's carrying a stale "as of" date.
