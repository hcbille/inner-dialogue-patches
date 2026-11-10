# INSTALL — Opus 5.5 Re-baseline Patch

Integration guide for re-tuning an Inner Dialogue install's instruction layer for Claude Opus 5.5, plus localizing its crisis resources. It's written to be applied against files that have **diverged** from the reference setup, so every change is anchored on a *concept* to find, not a line number. If you are an assistant reading this in maintainer mode: work through it against *this* setup's actual files, adapt names and pronouns, and don't assume the reference structure matches yours.

Work in order. Part 1 is safety-critical, so do it first, even if you stop there.

---

## Terminology mapping (do this first)

The reference setup calls the assistant **Sage**; this guide calls the person "the client". Before applying anything:

- Replace "the client" with whatever this setup calls the person, in their real pronouns.
- The reference paths are `CLAUDE.md` (always-loaded instructions), `.therapy/safety-protocol.md`, `.therapy/hooks/safety-net.js`, `.therapy/persona.md`, `.therapy/protocols/session-end.md`, `.therapy/protocols/compaction-resume.md`, `.therapy/memory/` (client-given corrections) and `.therapy/maintainer-notes.md`. Map each one to this setup's equivalent. Where one doesn't exist, skip the steps that depend on it and say so in the log entry.

---

## MANDATORY

### 1. Crisis resources for the country the client lives in

**Find out where the client lives** from the profile. If it isn't recorded, ask them in maintainer mode. Don't guess from language or name.

Then update **three places**, which must all agree:

1. The Crisis Response script in `safety-protocol.md` (the "Please reach out now" list).
2. The **Emergency Resources** fenced block in `safety-protocol.md`.
3. The `EMERGENCY_RESOURCES` string in `.therapy/hooks/safety-net.js`, if this install has the hook (kit 2.9.0+). Its comment says it's a verbatim copy of the block in (2), so keep it byte-identical.

**Worked example: a client in Sweden.** Numbers checked 2026-09-30 against krisinformation.se and Mind. Check them again before you use them:

```
If you're in crisis, please reach out to trained crisis counselors:

Sweden:
- 112 for immediate emergencies
- Självmordslinjen (Mind): call 90101 or chat at mind.se, open 24/7
- 1177 Vårdguiden: healthcare advice and where to go for psychiatric emergency care
- Jourhavande medmänniska: 08-702 16 80, every night 21:00-06:00

Outside Sweden: https://findahelpline.com

These are humans trained in crisis support.
```

**Anywhere else:** look the numbers up from an official national source (the government crisis-information site, the national suicide-prevention line's own site). Write each line with its real hours. Don't write numbers from memory. If some lines aren't 24/7, drop any blanket "available 24/7" claim.

Match the Crisis Response script's list to the same numbers.

### 2. Say when text should reach the client

Find the section of the always-loaded instructions that governs how the assistant talks to the client (the reference: "How you talk to [client]" in `CLAUDE.md`; if `narration-hardening` is installed, it's next to that rule). Add:

> A lot of the assistant's work is quiet tool use: the startup reads, loading a context file mid-session, the session-end writes. Your default during long runs of tool calls is to post short progress updates, and the app may prompt you for one. In these sessions, don't. Work silently and let your next words be the ones meant for the client. Before the greeting, say nothing at all. At other times, if something genuinely needs saying while you work, say it the way a person would ("give me a second to look back at my notes"), never as a report on your own process.

If the setup's no-narration rule lives only in a memory file, this is the moment to put a short version in the always-loaded file too. (`narration-hardening` explains why.)

### 3. Session-end runs through without stopping

At the top of the session-end protocol, replace any "Do not skip steps. Do not defer. Do not ask permission." line with:

> Run every step, in order, when the session ends. No need to ask permission. After the goodbye the client has gone, so work through to the push in one go: don't stop partway to summarize what you've written or to announce the next step. Nobody is there to answer, and a stop leaves the notes half-written.

If the protocol has a step that *does* talk to the client after the goodbye (the reference's stranded-branch line), name it as the one exception. Add one sentence to `CLAUDE.md`'s session-end pointer saying the same.

---

## RECOMMENDED

### 4. Startup reading list from a script

1. Copy `templates/startup.py` to `.therapy/scripts/startup.py`.
2. Open it and adapt `FIXED_HEAD`, `CONTEXT_TRIO` and `OPTIONAL` to this install's actual files. The parser expects context index entries shaped like `- **Name** (\`people/name.md\`) — … **Core**` or `**Active (YYYY-MM-DD)**`, events named `context/events/YYYY-MM-DD-slug.md` or `pending-slug.md`, and sessions named `sessions/YYYY-MM-DD[letter].md`. If this setup's formats differ, adjust the regexes rather than the files.
3. Run `python3 .therapy/scripts/startup.py` from the install root. Compare its list against what the current startup instructions ask for. They should match, apart from Active entries past their 7-day expiry, which the script leaves out on purpose. If the script says MISSING, fix the list or the file.
4. In `CLAUDE.md`, replace the step-by-step startup file list, including any "internally enumerate…" or "do not skip any" wording, with:

   > 1. Run `python3 .therapy/scripts/startup.py` from the install root. It prints today's reading list and the date-driven flags: near-term events, whether an arc review is due, and Active context entries that have expired.
   > 2. Read every file on the list. Batch the reads in parallel rather than opening them one at a time. If the script reports a missing file, read the rest and fix the gap at session end.
   > 3. Then greet the client.

   Keep a short description of what each kind of file is for (safety, persona, profile, memory, context index, sessions). That's context the model can't get elsewhere. Only the enumeration mechanics go.
5. Point the post-compaction resume protocol at the same script instead of its own numbered list.
6. If `context/GUIDE.md` says to remove expired Active tags *at session start*, change it: the script skips them at start, and session-end drops the tag.
7. If a memory file says "complete all N startup steps", update it to refer to the script.

### 5. Crisis-language matching in the client's other languages

Only if the client writes in a language other than English. The hook's patterns are English-only. Add a short first-person list for each language the client uses, and include it in the match check. Here is a Swedish list as a model:

```js
// JS \b is ASCII-only, so word edges next to å/ä/ö use explicit
// [a-zåäö] lookarounds instead.
var SV_PATTERNS = [
  /(?<![a-zåäö])jag\s+vill\s+(?:inte\s+leva|dö)(?![a-zåäö])/,
  /(?<![a-zåäö])vill\s+inte\s+leva\s+(?:längre|mer)(?![a-zåäö])/,
  /(?<![a-zåäö])orkar\s+inte\s+leva(?![a-zåäö])/,
  /(?<![a-zåäö])(?:ta|tar|tog|tagit|ska\s+ta)\s+livet\s+av\s+mig(?![a-zåäö])/,
  /(?<![a-zåäö])(?:ta|tar|tog|tagit)\s+mitt\s+(?:eget\s+)?liv(?![a-zåäö])/,
  /(?<![a-zåäö])(?:skada|skadar|skadat|skadade)\s+mig\s+själv(?![a-zåäö])/,
  /(?<![a-zåäö])(?:skär|skar|skurit|skära)\s+mig(?![a-zåäö])/,
  /(?<![a-zåäö])jag\s+(?:har\s+)?(?:självmordstankar|tänker\s+på\s+(?:självmord|att\s+dö|att\s+ta\s+livet\s+av\s+mig))(?![a-zåäö])/,
  /(?<![a-zåäö])(?:ta|tar|tog|tagit)\s+en\s+överdos(?![a-zåäö])/,
  /(?<![a-zåäö])(?:alla\s+)?(?:vore|skulle\s+vara|är)\s+bättre\s+(?:av\s+)?utan\s+mig(?![a-zåäö])/
];
```

Wire it in where the hook checks its tiers (`matchesAny(TIER1_PATTERNS, …) || matchesAny(TIER2_PATTERNS, …)`, add `|| matchesAny(SV_PATTERNS, text)`), and update the header comment's LIMITATION note. Leave out everyday idioms that would fire constantly. In Swedish, "orkar inte mer" ("I can't take any more") is ordinary tiredness talk, so only "orkar inte leva" is on the list. Patterns must be lowercase, because the hook lowercases input.

Smoke-test from the install root, with positives and negatives:

```bash
t() { printf '%s' "{\"prompt\": \"$1\"}" | node .therapy/hooks/safety-net.js | head -c 60; echo " <- $1"; }
t "jag vill inte leva längre"; t "jag har skurit mig"; t "I want to die"; t "jag orkar inte mer med jobbet"; t "vi skär tomater"
```

The first three should print a notice and the last two nothing. Then run `node --check .therapy/hooks/safety-net.js`.

### 6. Re-baseline the instruction text

A judgment pass over `CLAUDE.md`, the protocols, and `context/GUIDE.md`. The aim is **fit, not length**. Nothing gets deleted just for being long, and context the model can't get elsewhere always stays.

- **Say each rule once, at normal volume, with its reason.** Where a rule appears in several places, or is stacked with "HARD RULE / absolute / no exceptions / do not skip", keep one clear statement with its "because". Current models follow instructions closely, and piled-on emphasis makes them rigid rather than reliable.
- **Remove history narratives and migration phrasing** from instruction files: dated incident stories, "removed on DATE because…", "this replaces the old…", "now also…", "no longer…". The model never saw the old version, so relative phrasing points at something that doesn't exist. Move the history into maintainer notes.
- **Fix stale references**, such as step numbers that have shifted ("see step 7" when it's now step 8) and paths that moved. Check each one against the actual file.
- **Look for generic kit text that contradicts the client's own rules.** For example, a generic ethics line that says to "regularly check whether they're working with a therapist" clashes with a client who has asked not to be pushed about it. The client's rule wins, so rewrite the generic line to fit it.
- **Remove "think carefully" or "think step by step" instructions** in chat-facing prompts, and any instruction to write reasoning out in the reply. Opus 5.5 always thinks, and prompts that push it to reproduce its reasoning in the text can be refused.
- **Leave these alone:** never-do lists, boundaries and contracts the client asked for, the crisis protocol's substance, exact git/shell commands, and file architecture.

### 7. Persona

- Replace numeric length rules ("usually 2 to 4 sentences") with qualitative guidance: spare by default, and in full when the client asks for something concrete.
- Cut long stock-phrase banks down to a handful of varied lines, labeled *illustrative, not phrases to reuse*. The model copies examples closely.
- **Check every persona line against the client's recorded corrections.** For example, a persona section on "affirming effort and courage" clashes with a client who has asked not to be praised for coping. Lines like that come out, replaced by an "acknowledge, don't praise" note. Look for the equivalent clashes here.
- If the setup has accountability contracts or other standing "challenge me on this" asks, add an exception to the persona's "challenge rarely" default that names them.

---

## OPTIONAL

### 8. Memory-file hygiene

- A memory file that has grown into a dated incident log (several "Recurrence (DATE): …" paragraphs) works better as **rule / Why / How to apply**, with a few short, varied examples of the failure's shapes. Git history keeps the log.
- Reference material only needed occasionally, like an SSH repair checklist, doesn't need to be in the every-session startup read. Move it to something like `.therapy/reference/`, and point to it from the step that needs it.

---

## VERIFY

- Confirm the Emergency Resources block and the hook's `EMERGENCY_RESOURCES` string are identical:

  ```bash
  diff <(sed -n '/^```$/,/^```$/p' .therapy/safety-protocol.md | sed '1d;$d') \
       <(node -e "const s=require('fs').readFileSync('.therapy/hooks/safety-net.js','utf8');console.log(eval(s.match(/var EMERGENCY_RESOURCES =([\s\S]*?);\n/)[1]))") \
    && echo IN_SYNC
  ```

  (This assumes the Emergency Resources block is the only bare-fenced block in the file. Adjust if not.)
- Run `python3 .therapy/scripts/startup.py` and check it exits 0 with no MISSING line.
- Re-read the new "text reaching the client" paragraph and confirm it sits in the always-loaded file, not an on-demand one.
- Grep the instruction files for leftovers: `grep -rnE "internally enumerate|HARD RULE|no exceptions|no longer|replaces the old" CLAUDE.md .therapy`.
- Start a fresh session and watch the opening. The first thing the client sees should be the greeting, with no status lines before it.
- Log everything in `.therapy/maintainer-notes.md`: what changed, which files, and which parts were skipped and why.

**Framework note:** `safety-protocol.md`, `persona.md` and `hooks/safety-net.js` are hash-tracked by the Inner Dialogue updater. Once edited, `inner-dialogue update` skips them and keeps these versions. That's intended, but it means future upstream changes to those files have to be merged by hand.

**Honest limit:** parts 2 and 3 are prompt fixes, not hard filters. They make early stops and process narration less likely, and they can't guarantee either never happens.

---

## Updating an install that already has this patch (2026-11-10)

**The thread registry is printed in part, not listed whole.** Only matters if this setup has `context/threads.md` (the `thread-registry` patch). The greeting and the standing-threads check use only the open therapeutic and shelved entries, so startup no longer reads the schema, logistical entries and archive.

1. In `.therapy/scripts/startup.py`, copy from `templates/startup.py`:
   - `context/threads.md` out of `CONTEXT_TRIO` (it stays in `OPTIONAL`);
   - the `THREADS` and `THREAD_SECTIONS` constants;
   - the `threads_excerpt()` function;
   - in `main()`, the `threads = threads_excerpt()` / `context = …` lines before `reads`, and the block after the reading list that prints the sections.
2. If the `dreaming` patch is installed, count the printed sections toward the startup size, so the dream threshold still sees them: after the `startup_bytes = sum(...)` line add `startup_bytes += len(threads.encode()) if threads else 0`.
3. In `CLAUDE.md`, where the startup section describes the registry, add: the script prints its Open — Therapeutic and Shelved sections, which count as read; the rest is read at session end, or when one of those threads comes up.
4. Run `python3 .therapy/scripts/startup.py`. `context/threads.md` should be gone from the list, and a `===== context/threads.md (Open — Therapeutic, Shelved)` block should follow it. If the file is listed instead, a heading doesn't match `THREAD_SECTIONS`.
5. Log it in `.therapy/maintainer-notes.md`.
