# Audit coverage

An audit dream goes back over older session notes and checks a few context files at a time against them (`.therapy/protocols/dream-audit.md`). This file records how far each file has got. `.therapy/scripts/audit_next.py` reads it to plan the next run, and `--status` prints a summary.

One line per audited file:
`- context/<folder>/<file>.md · through <last session read> · last YYYY-MM-DD · complete | partial · full | cited`

- **complete:** every note on the file's list has been read, up to the last merged regular dream.
- **partial:** a big file audited in chunks; the next run picks up after "through".
- **full / cited:** whether the audit reread every note mentioning the file, or the notes the file cites.

A file that isn't listed hasn't been audited yet.

## Files
