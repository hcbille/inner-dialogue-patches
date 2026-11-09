# Topic Links

Words that should bring up a context file even though they aren't anyone's name. The `context-loader` hook (`.therapy/hooks/context-loader.py`) reads this file on every message the client sends. Names and aliases are picked up automatically from `context/index.md` and each file's frontmatter, so they don't belong here.

**Format:** one line per link, `- keyword, keyword → path, path`. Paths are relative to `context/`. Keywords match whole words, case-insensitive, with a trailing possessive allowed. Keep keywords specific enough that they don't fire on ordinary sentences.

**What needs a link here:** files the index can't reach by name. That means past events (removed from the index once processed), files not listed in the index, and subjects the client usually refers to by role ("my mom", "my manager") rather than name. Links to Core files are ignored, because startup already loads them. Active files are skipped only while their date is fresh, so their links still count once they expire.

---

<!-- Build this file from the whole context library, following INSTALL.md step 5. Delete these example lines and headings first; they only show the shape. -->

## Family

- my mom, my mum, my mother → people/mother.md

## Work

- my manager, performance review → people/manager-name.md

## Money

- debt, debts, credit card → concepts/finances.md
