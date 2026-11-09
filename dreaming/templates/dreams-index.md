# Dreams

A dream is a background tidy-up of the assistant's notes. It reads the recent session notes and brings the standing files (the context library, the index, threads, mentions) up to date. Each dream is reviewed in maintainer mode before it changes anything.

- How it works: `.therapy/protocols/dream.md`
- How it's reviewed: `.therapy/protocols/dream-review.md`

One line per dream, newest last. Format:
`- YYYY-MM-DD · covered <first session> → <last session> (N sessions) · branch dream/YYYY-MM-DD · outcome: pending | merged | merged with edits | rejected | reverted · startup <before> → <after> bytes · pass <threads|summaries|consolidation>`

The "pass" field (part 5, if installed) names the library pass the dream did; the next dream does the one after it.

Audit dreams (`.therapy/protocols/dream-audit.md`, if installed) get a line of their own, `- YYYY-MM-DD · audit · N files · branch dream/YYYY-MM-DD-audit · outcome: …`, with no "covered" range; their coverage lives in `audit.md`.

The startup script reads this file. The next dream starts after the "covered" end session of the last line whose outcome is `merged` or `merged with edits`. Sessions are full names, suffix included (`2026-11-04b` comes after `2026-11-04`).

## Log

