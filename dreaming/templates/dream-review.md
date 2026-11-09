# Dream Review Protocol

How a dream lands. Run it in maintainer mode, either right after a dream or whenever the client says "review the dream". No dream reaches `main` without going through this.

## 1. Open it

1. Find the dream branch: `git branch -a --list '*dream/*'`. If there's more than one, review the oldest first.
2. Read its report on that branch: `dreams/YYYY-MM-DD.md`.
3. Tell the client the summary in a few plain lines: what changed, and how many flags and profile proposals are waiting.

## 2. Check it obeyed the rules

Before showing any content, run:

```bash
git diff main...dream/YYYY-MM-DD --name-only
```

- Nothing may be listed under `sessions/` or `.therapy/memory/`, and none of the files protected by the dream protocol's rule 6. If anything is, say so and restore those paths from `main` on the branch before going on.
- `git diff main...dream/YYYY-MM-DD --stat` shows which files grew. Each one should be explained in the report, either by a PROMOTE or by a new fact session end missed.

**Audit dreams** (`dream/YYYY-MM-DD-audit`, report `dreams/YYYY-MM-DD-audit.md`) are reviewed the same way, with one addition: walk the report's "Unsupported claims" with the client first, before the changes. Each one is a claim no session note backed up. The client says whether it's true (keep it: they've now confirmed it in this review), wrong (fix or drop it), or not worth deciding (leave it as the audit left it).

## 3. Walk the changes, one region at a time

For each region (a context file, the index, threads, mentions, topic links):

1. Describe the change in plain words, and show the diff if the client wants to see it.
2. The client answers **keep**, **edit** or **drop**.
   - **Edit:** make the change on the branch.
   - **Drop:** restore that region from `main`, e.g. `git checkout main -- context/people/x.md`.
3. Keep a list of what was dropped or edited. It goes in the report, and later improves the dream protocol.

The client can say "keep the rest" at any point.

## 4. Flags

For each flag in the report, the client either:

- **answers it now:** record the answer in `dreams/flags.md` (`answered`, today's date, their answer in their own words) and make the resulting change on the branch;
- **saves it for a session:** leave it `open`, so the assistant can ask it gently later (`.therapy/protocols/dream-flags.md`);
- **drops it:** mark it `dropped`. It's never asked again.

## 5. Profile proposals

`profile.md` changes only through the client:

- **Confirmed:** apply the change on the branch, with today's date stamp if the profile uses them. This counts as live confirmation.
- **Reworded:** use their wording, with today's stamp.
- **Declined:** leave the profile as it is.
- **"Not now":** add it to `dreams/flags.md` as `open`.

## 6. Land it

1. On the branch, update the report:
   - set **Status:** to `merged` (or `merged with edits`);
   - add a short **Review** section listing what was dropped or edited, and why if the client said.
2. On the branch, set this dream's line in `dreams/index.md` to `outcome: merged` or `merged with edits`. For an audit that's rejected, also restore `dreams/audit.md` from `main`, so those files come up again.
3. Commit those edits on the branch.
4. Squash-merge, so the dream is exactly one commit on `main`:

   ```bash
   git checkout main && git pull && git merge --squash dream/YYYY-MM-DD && git commit -m "Dream YYYY-MM-DD (reviewed): <one-line summary>" && git push origin main
   ```

   If the squash merge conflicts because `main` moved (a session ran in between), keep both sides. The session's changes win for anything it touched, because it came after the dream's evidence.
5. Delete the branch:

   ```bash
   git branch -D dream/YYYY-MM-DD && git push origin --delete dream/YYYY-MM-DD
   ```

## Rejecting a whole dream

1. Delete the branch, locally and on the remote.
2. On `main`, add the dream's line to `dreams/index.md` with `outcome: rejected` and a few words on why.
3. Keep the report: copy it to `main` with **Status:** `rejected`.

A rejected dream doesn't advance the "covered through" point, so the next dream covers those sessions again. Improve the dream protocol first.

## Undoing a merged dream later

1. Find the commit:

   ```bash
   git log --oneline --grep "^Dream YYYY-MM-DD"
   ```

2. Revert it:

   ```bash
   git revert <sha> && git push origin main
   ```

3. In `dreams/index.md`, set the outcome to `reverted` (with the date). Add a line to the report saying why.

A reverted dream doesn't count as merged, so its sessions are covered again.

## Afterwards

Add a short entry to the maintainer notes: the dream's date, what was kept, edited and dropped, and any change it suggests to the dream protocol.
