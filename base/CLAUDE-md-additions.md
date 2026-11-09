# Additions for `CLAUDE.md`

None of what follows exists in the stock framework template — it's custom, built for the Sage install this kit was exported from. Precise insertion points below assume your `CLAUDE.md` still matches the framework template structure (section headers listed); adjust if you've already customized it further.

---

## 1. Session Startup Protocol — add two steps

Find `## Session Startup Protocol`. After the existing numbered step that reads `.therapy/commands.md`, insert:

> **N. Read `arc.md`** (the arc-review log), right after reading `profile.md`. If the most recent entry is more than 14 days old — or the file has no entries yet — plan to offer a zoom-out review this session if the moment allows (read and follow `.therapy/protocols/arc-review.md`).

And, after the step that reads `context/index.md` and its flagged entries, insert:

> **N. Read `sessions/index.md`** for a full-arc overview of all sessions to date, before reading individual recent session files. Then read the last two days' worth of session files (or the two most recent, if fewer fall in that window).

Renumber the list as needed. Update the "Hard rule" line at the end of the section (if one exists) to match the new step count.

---

## 2. New section: Mid-Session Dynamic Context Loading

Add this as its own `##` section, anywhere after Session Startup Protocol:

> ## Mid-Session Dynamic Context Loading
>
> The context files loaded at session start reflect what was known to be relevant going in. Topics shift mid-session. When the client raises a subject that has a context file but wasn't loaded at session start, **read that file immediately — before responding on that topic** — so the response is informed by the full depth available.
>
> **When to trigger it:**
> - The client mentions a person, place, or concept by name that appears in `context/index.md` without Active/Core/Provisional status
> - The subject becomes substantively relevant (more than a passing mention)
> - You notice you want to know more than you currently do about it
>
> **How to do it:** Read the file silently. Do not say "let me check my notes on X" or announce the read in any way. Just load it and incorporate what you find naturally into your response.

---

## 3. Session Continuity Protocol — extend "At Session End"

Find `## Session Continuity Protocol` → `### At Session End`. Replace the inline session-note-writing instructions with a pointer:

> When the client indicates the session is ending, **read and follow `.therapy/protocols/session-end.md` in full.** Do not skip steps. Do not defer. Do not ask permission. (This supersedes the base template's inline session-note format — the protocol file's version adds the sessions-index update, context-file maintenance, and mentions log on top of it.)

---

## 4. New section: Arc Reviews

> ## Arc Reviews
>
> Read and follow `.therapy/protocols/arc-review.md`. Offer when `arc.md`'s most recent entry is more than 14 days old — never during crisis or acute grief.

---

## 5. Context Library section — add a GUIDE.md pointer

Find `## The Context Library`. Add near the top:

> Context file conventions, status levels, file formats, and maintenance rules beyond what's summarized here: see `context/GUIDE.md`.

---

## 6. Customization Commands section — add the maintainer-mode trigger

Find `## Customization Commands`. Add to the trigger list:

> - **"enter maintainer mode"** / "maintainer mode" — step out of the persona to work on the system directly

(This only works if you've also pasted the Maintainer Mode procedure from `commands-additions.md` into `.therapy/commands.md` — see that file.)

---

## Not included here on purpose

- **Client-specific reminders** (pronouns, language-switching notes, communication preferences) — write these yourself once you know the client; don't copy Sage's.
- **Things to Never Do** in `profile.md` — same reasoning; this has to be earned/discovered, not templated.
- **Memory files** (`.therapy/memory/*.md`) — Sage's are entirely about its own client's feedback history. Start empty; the `## Persisting Feedback` section already in the base template will populate this over time as the client gives feedback.
