# Ingest log

One line per merged ingest (`.therapy/protocols/dream-ingest.md`), oldest first, appended by the ingest itself before the gate: `- <id> · covered <first> → <last> (N sessions) · outcome: merged · changes N · flags N`. The id is the run date (`YYYY-MM-DD`, or `YYYY-MM-DD-2` for a second ingest that day) and names the report `dreams/ingests/<id>.md`; first and last are session-note stems such as `2026-01-14b`. Only merged ingests reach main, so every line here says merged. The startup script reads the newest line's covered-through stem and, with the last merged longform in `dreams/index.md`, uses the later of the two to decide which notes are still unprocessed.

