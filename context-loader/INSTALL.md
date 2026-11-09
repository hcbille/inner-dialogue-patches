# INSTALL — Context Loader Patch

Integration guide for adding the context-loader hook to an Inner Dialogue install. It's written to be applied against files that have **diverged** from the reference setup, so every change is anchored on a *concept* to find, not a line number. If you are an assistant reading this in maintainer mode: work through it against *this* setup's actual files, adapt names and pronouns, and don't assume the reference structure matches yours.

---

## Terminology mapping (do this first)

The reference setup calls the assistant **Sage**; this guide calls the person "the client". Before applying anything:

- Replace "the client" with whatever this setup calls the person, in their real pronouns.
- The reference paths are `CLAUDE.md` (always-loaded instructions), `context/index.md` (the context library index), `.claude/settings.json` (Claude Code hooks), `.therapy/hooks/` (hook scripts), `.therapy/memory/` + `MEMORY.md` (client-given corrections and references) and `.therapy/maintainer-notes.md`. Map each one to this setup's equivalent. Where one doesn't exist, skip the steps that depend on it and say so in the log entry.
- Requires `python3` on the machine (`command -v python3`). macOS ships it with the Xcode command-line tools.

---

## MANDATORY

### 1. Install the hook

1. Copy `templates/context-loader.py` to `.therapy/hooks/context-loader.py`.
2. Open it and check the parser against this install's `context/index.md`. It expects entries shaped like:

   ```
   - **[[Name]]** (`people/name.md`) — description… **Core**
   - **Display Name** (`concepts/thing.md`) — description… **Active (YYYY-MM-DD)**
   - Name (`people/name.md`) — description…
   ```

   i.e. a bullet, a display name (bold and `[[wikilinks]]` optional, `[[target|label]]` fine), then the path in backticks inside parentheses. If this index looks different, adjust `ENTRY_RE` and `STATUS_RE`, not the index.
3. `ACTIVE_DAYS` must match whatever the startup logic uses for Active expiry (7 in the reference). Core and unexpired Active files are skipped, because startup already loads them. If this install loads different files at startup, change `startup_loaded()` to match.
4. Review `GENERIC_ALIASES`. Run the dump below and add any alias that's an everyday phrase in this client's life (for example "the office", "the plan", "index", …):

   ```bash
   python3 - <<'EOF'
   import importlib.util, datetime as dt
   spec = importlib.util.spec_from_file_location("cl", ".therapy/hooks/context-loader.py")
   cl = importlib.util.module_from_spec(spec); spec.loader.exec_module(cl)
   for k, v in sorted(cl.build_map(dt.date.today()).items()): print(repr(k), sorted(v))
   EOF
   ```

5. **`FILE_NOTES`:** if any context file has a standing rule about how it's used (typically "never raise this person/subject first"), add it here so the rule is repeated whenever the hook flags the file. Check the profile's never-do list and the memory folder for these.

### 2. Register it

In `.claude/settings.json`, add a `UserPromptSubmit` entry after any existing ones (keep the safety-net hook first):

```json
{
  "matcher": "",
  "hooks": [
    {
      "type": "command",
      "command": "python3",
      "args": ["${CLAUDE_PROJECT_DIR}/.therapy/hooks/context-loader.py"]
    }
  ]
}
```

Match the style of the existing entries (some installs use a single `command` string instead of `command` + `args`). Validate: `python3 -c "import json;json.load(open('.claude/settings.json'))"`. Claude Code reads hook settings at session start, so the hook starts working from the next session.

### 3. Gitignore the state

Add to `.gitignore`:

```
# Hook state (per-session, local)
.therapy/.cache/
```

### 4. Tighten the instruction

Find the always-loaded rule about loading context files mid-session (reference: "Loading context mid-session" in `CLAUDE.md`). Replace any "if it's more than a passing mention" wording with:

> When the client names a subject that has a context file you haven't read this session, read it before you reply on that subject, even when the mention seems passing. Files are cheap, and a missing one costs them. Do it silently, without announcing it. The `context-loader` hook backs this up: when their message matches a file's name, alias, or a keyword in `context/topic-links.md`, it adds a note listing the files. Treat that note as an instruction, not a suggestion. It names each file only once per session, so the note won't come round again.

### 5. Build the topic links from the whole context library

Don't ship the examples. Build `context/topic-links.md` for this client now, so the hook is useful from the first session. This is the longest step. Budget for reading every context file.

1. **Copy the template.** Copy `templates/topic-links.md` to `context/topic-links.md` and delete the example lines, keeping the header.
2. **See what the hook already reaches.** Run this. It prints every context file with the words that already match it:

   ```bash
   python3 - <<'EOF'
   import importlib.util, datetime as dt, glob
   spec = importlib.util.spec_from_file_location("cl", ".therapy/hooks/context-loader.py")
   cl = importlib.util.module_from_spec(spec); spec.loader.exec_module(cl)
   inv = {}
   for k, v in cl.build_map(dt.date.today()).items():
       for r in v: inv.setdefault(r, []).append(k)
   for f in sorted(glob.glob("context/**/*.md", recursive=True)):
       print(f, "|", ", ".join(sorted(inv.get(f, []))) or "(nothing: startup-loaded, or unreachable by name)")
   EOF
   ```

   Files marked "nothing" are either Core/Active (fine, since startup loads them) or unreachable. Unreachable files are your first priority.
3. **Read every context file.** That means `context/index.md`, `mentions.md` and `threads.md`, and every file under `people/`, `places/`, `concepts/` and `events/`, including past events. Batch the reads. Read with one question in mind: *what words does the client actually use when this subject comes up, other than its name?*
4. **Write links for these kinds of words.** They are listed roughly in order of value:
   - **Files unreachable by name.** Past events whose lines were removed from the index, files never listed in the index (sub-folders like artwork or project ideas), and files whose only aliases are in `GENERIC_ALIASES`. Link each one to the words the client used for it: the trip's destination, the festival's name, the project's title.
   - **Roles instead of names.** "my mom", "my dad", "my sister", "my manager", "my girlfriend", "grandparents", "my counsellor", in every language the client uses. Link each one to that person's file.
   - **Doorway words.** A month tied to an anniversary, a city tied to a relationship, a service, a medication, a workplace system, a legal term, a pet's name. Link the word to the subject it opens.
   - **Names below the alias floor.** The hook ignores index names and aliases shorter than three letters. Topic links bypass that limit, so a two-letter name ("Bo", "Li") can go here if it isn't also an everyday word in the client's languages.
   - **Other spellings and languages.** The client's own terms for a concept, with and without diacritics ("café", "cafe"), and the English term alongside the one in the client's other language. Add both "x's" and "xs" forms where the client drops apostrophes.
5. **Skip Core files.** Startup always loads them, and the hook ignores links to them. Do link Active files: the hook only skips those while their date is fresh.
6. **Keep keywords specific.** Each keyword fires on every sentence that contains it. Prefer a phrase ("my manager", "the old flat") over a common single word, and check every keyword against both of the client's languages. The reference dropped a company name that is also an everyday verb, "trip", a word that means different things in the client's two languages, and "art". Also check the existing aliases the step-2 dump printed. Numeric or very short aliases ("1.0") fire on unrelated text, so add them to `GENERIC_ALIASES` or remove them from the frontmatter.
7. **Ask before linking to a boundary file.** If a file carries a "never raise first" rule, loading it silently from a topic word is the client's decision. Ask them in maintainer mode before writing those links. Record their answer in the always-loaded instructions next to that rule (for example: "Also load it silently when the client raises a subject that belongs to this person without naming them. Reading the file is preparation. It never licenses naming them first."). If they say no, write no links to that file.
8. **Group the links** under `##` headings by area of life (family, partner, work, money, health, creative work…). The hook ignores headings, and the grouping makes the file easy to maintain.
9. **Validate.** Check that every path exists, then run sample messages through the matcher:

   ```bash
   python3 - <<'EOF'
   import importlib.util, datetime as dt
   from pathlib import Path
   spec = importlib.util.spec_from_file_location("cl", ".therapy/hooks/context-loader.py")
   cl = importlib.util.module_from_spec(spec); spec.loader.exec_module(cl)
   missing = [p.strip() for line in Path("context/topic-links.md").read_text().splitlines()
              if (m := cl.TOPIC_RE.match(line)) for p in m.group(2).split(",")
              if not (Path("context") / p.strip()).exists()]
   print("missing paths:", missing)
   amap = cl.build_map(dt.date.today())
   for msg in ["I talked to my mom today", "thinking about the trip again"]:   # use real phrasings from recent sessions
       print(repr(msg), "->", cl.matches(msg, amap))
   EOF
   ```

   Replace the sample messages with real phrasings from the client's recent session notes, plus a couple of ordinary sentences that should match nothing.

### 6. Keep the topic links current

The file goes stale unless session end maintains it.

1. **Session-end protocol** (reference: `.therapy/protocols/session-end.md`, placed after the step that creates new context files and event files). Add:

   > **Topic links (`context/topic-links.md`).** The `context-loader` hook finds a file by its index name and frontmatter aliases, and by nothing else. Anything the client calls by another word only reaches the hook through a topic link. After the context-file steps, add or adjust links wherever one of these came up today:
   >
   > - **A subject came up under a word other than its name,** and the hook didn't flag the file (you had to find it yourself, or it wasn't loaded in time). Examples: a role ("my manager"), a term in another language, a nickname for an event, a place tied to a person. Link that word to the file.
   > - **A file the index can't reach by name.** That covers a new file not listed in the index and any event line you just deleted from the index. Give each one a link using the words the client actually used for it.
   > - **A keyword that fired on an ordinary sentence today.** Tighten it into a phrase or remove it.
   >
   > Put each link under the matching section heading, in the file's format (`- keyword, keyword → path, path`, paths relative to `context/`). Don't link Core files, because startup already loads them and the hook ignores those links. Skip this entirely if nothing today qualifies. Most sessions add nothing here.

   If the client chose a boundary rule in step 5.7, add one sentence restating it (for example: "A link to that file is only for subjects that are theirs, and it never licenses naming the person first.").
2. **Context-library guide** (reference: `context/GUIDE.md`), if this install has one:
   - Add `topic-links.md` to the folder diagram.
   - Add a short section: what the file is for, what needs a link (roles, other-language terms, event nicknames, unreachable files, names under three letters), what doesn't (names, aliases, Core files), keep keywords specific, any boundary rule, and that session end maintains it.
   - Wherever the guide says to delete a past event's line from the index, add: "Deleting the line also stops the hook matching the event's name, so give it a line in `topic-links.md` using the words the client used for it."

---

## RECOMMENDED

### 7. zsh note (macOS installs only)

If this install runs on a Mac (`echo $SHELL` shows `/bin/zsh`), copy `templates/reference_zsh_shell_syntax.md` into the memory folder and add a pointer line to `MEMORY.md`:

```
- [zsh shell syntax](reference_zsh_shell_syntax.md) — the Bash tool runs zsh: quote `=`-prefixed words, globs, `!`, `^`; a failed expansion silently aborts the whole chained command.
```

If startup loads the memory folder by glob, it's picked up automatically; otherwise add it to the startup list.

---

## VERIFY

Run from the install root, replacing `SomeName` with a real name from `context/index.md` whose file is *not* Core or Active:

```bash
t() { printf '%s' "{\"prompt\": $(python3 -c 'import json,sys;print(json.dumps(sys.argv[1]))' "$1"), \"session_id\": \"$2\"}" | python3 .therapy/hooks/context-loader.py; echo " [exit $?]"; }
t "I talked to SomeName today" v1      # expect a note naming their file
t "SomeNames thing again" v1           # expect nothing: already flagged this session
t "SomeName" v2                        # expect the note again: new session
t "hello" v1                           # expect nothing
printf 'junk' | python3 .therapy/hooks/context-loader.py; echo " [exit $?]"   # expect nothing, exit 0
rm -f .therapy/.cache/context-loader/v1.json .therapy/.cache/context-loader/v2.json
```

Then test one topic-links keyword the same way, and any `FILE_NOTES` file (the note text should appear after its path).

Log everything in `.therapy/maintainer-notes.md`: what changed, which files, how many topic links were built and which subjects they cover, which file notes were chosen (and that the client was asked about any boundary file), and anything skipped.

**Honest limit:** the hook makes missed context much less likely, not impossible. It can't see what was actually read, and after a compaction it won't re-flag files it already flagged that session.
