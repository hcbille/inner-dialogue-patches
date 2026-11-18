# Inner Dialogue Patch — Scheduled Dreams

An optional step past `dreaming`: session end writes only the session note, small "ingest" dreams keep the files current after each session, and, if you want, a server runs them by itself.

**`dreaming` doesn't need this.** Without it, an install with `dreaming` is fully self-contained: session end captures what the next greeting needs, and longform dreams, run by hand, do the rest. This patch is for installs that want session end lighter still and are willing to run ingests, by hand or on a machine that's always on.

Built for Sage, the reference install, on 2026-11-14 and 15, and packaged here on 2026-11-18. **It contains no personal content**: everything is genericized to "the client" and "the assistant".

**Prerequisites:**
- `dreaming`, parts 1–3, with at least one longform dream merged;
- `base`'s `evidence_check.py` (2026-11-11 or later);
- the startup script from `opus-5-5-rebaseline` with the `dreaming` additions;
- a git repo; for part 3, a remote and a Linux machine with systemd.

## What problem it solves

`dreaming` moved the *tidying* out of session end, but session end still wrote the index line, event files, thread bumps, Active dates, status changes and handling rules, late at night, in the session's own context. Audits in the reference install kept tracing drift back to those writes: a paraphrase that became a quote, a date filed under the wrong session, a claim that changed kind.

## The three parts

1. **Session end writes only the note.** The note ends in a seven-line **For the next session** block (events, threads, files touched, new stubs, flag answers, profile confirmations, handling-rule changes). The startup script reads the block of every note no dream has covered yet, so the next greeting still knows tomorrow's event, which threads were just surfaced and any new handling rule. The longform dream does the file work from the notes, with nothing else going on.
2. **Ingests.** A small, frequent dream that processes new notes' blocks and adds their new facts to the files they touched, inside strict limits: world facts only get superseded, claims about the client are only added or flagged, nothing is merged, archived or deleted, and the profile and boundary subjects are off limits. A gate script checks the limits, and a passing ingest lands with no review. The next longform dream checks every line it wrote. **Run by hand in maintainer mode, so no server is needed.**
3. **Scheduled on a server.** A systemd timer on a machine the client controls runs an ingest two quiet hours after a session and a longform dream when one is due. Ingests land if the gate passes; failed ingests and every longform dream are pushed as branches for review. The client's sessions pull at start and rebase at the end.

Stop after any part. Parts 1 and 2 keep everything on the client's own machine.

## What's in the box

```
scheduled-dreams/
  README.md                         ← you are here
  INSTALL.md                        ← the integration guide — hand THIS to your assistant in maintainer mode
  templates/
    session-end.md                  → .therapy/protocols/session-end.md          (part 1)
    file-conventions.md             → .therapy/protocols/file-conventions.md     (part 1)
    startup-ingest-additions.py     → blocks to paste into the startup script    (parts 1–2)
    dream-ingest.md                 → .therapy/protocols/dream-ingest.md         (part 2)
    dreams-ingests-index.md         → dreams/ingests/index.md                    (part 2)
    scheduled/gate.py               → .therapy/scripts/scheduled/gate.py         (part 2)
    scheduled/status.py             → .therapy/scripts/scheduled/status.py       (part 2)
    scheduled/run.sh                → .therapy/scripts/scheduled/                (part 3)
    scheduled/pre-push, dreamer.service, dreamer.timer, install.sh               (part 3)
    session-pull.sh                 → .claude/session-pull.sh                    (part 3)
```

## Design notes worth knowing

- **The block is the bridge.** Between a session and the dream that covers it, the note's block is the only place its events and threads are recorded. The startup script reads it, so nothing depends on how soon a dream runs.
- **Gate shape, review truth.** `gate.py` checks what a script can: one commit, allowed paths, no deletions, sizes, untouched "How to hold it" lines, boundary names, word-for-word quotes. It can't tell whether a sentence is true. The longform dream's ingest check, reviewed by the client, is what covers that.
- **Two kinds of claims, two rules.** An ingest may update a date, a job status or a plan in place. It may never overwrite what the client feels, wants or is; a newer note that seems to contradict one becomes a question for review.
- **The server is untrusted by design.** Its agent gets an allow-list of tools: no push, no fetch, no reading credentials, no editing scripts or `.git`. Only the runner pushes, and a pre-push hook refuses anything else. Logs carry times and counts, never note content.
- **Longform dreams get rarer.** With ingests doing the daily work, a longform dream is due every five sessions and five days, or ten days.

## Honest limits

- Part 3 puts a full copy of the client's notes on a second machine, with push access to the repo. That's the client's decision to make, not a default.
- Ingests are prompt-bound. The gate stops the mechanical failures, not a subtly wrong sentence. Keep longform dreams going.
- The runner is Linux and systemd only.
- In the reference install, ingests ran on Claude Opus. A smaller model will cross limits more often; the gate then stops it, and the branch waits for review.

## Changelog

- **2026-11-18:** first release (parts 1–3).
