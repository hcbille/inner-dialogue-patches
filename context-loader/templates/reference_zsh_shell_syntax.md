---
name: reference_zsh_shell_syntax
description: This machine's Bash tool runs zsh, not bash; quote anything starting with = and other zsh-special characters, or the whole chained command line silently aborts
metadata:
  type: reference
---

The Bash tool on this machine runs **zsh**. zsh expands some unquoted words that bash would leave alone. When an expansion fails, zsh aborts the **whole command line**, so every command chained after it with `;` never runs. The only sign is an error at the end of the output, which is easy to miss when the first command's output looks complete.

**Why:** in the reference setup, a chained read (`cat a.md; echo =====; cat b.md; grep ...`) failed with `(eval):1: ==== not found`. Unquoted `=====` triggered zsh's `=cmd` expansion (it looks up the path of a command named `====`). Only the first file loaded, and the rest were silently skipped until the client asked about the error.

**How to apply:**
- Quote separators and any argument that starts with `=`: `echo "====="`, never `echo =====`.
- Also quote or escape the other zsh-special characters when they're meant literally:
  - `*`, `?` and `[...]`. An unmatched glob is an error in zsh (`no matches found`), not passed through literally like in bash. Quote patterns handed to grep/find (`grep -n "foo*"`, `find . -name "*.md"`).
  - `!` inside double quotes (history expansion). Use single quotes.
  - `~` and `^` in unusual positions, such as `git` revisions like `HEAD^`. Quote them: `"HEAD^"`.
- Quote paths that contain spaces (iCloud paths like `Mobile Documents/com~apple~CloudDocs` always do).
- After any chained command, check the tail of the output for an error before trusting that every part ran. If one part failed, re-run the missed parts and say so; don't answer from partial reads.
- **Don't confuse this with an ordinary non-zero exit.** A chained command's exit code is the last command's, so `...; ls missing-dir` gets labelled an error even though everything before it ran. Tell the two apart by the message: `zsh: no matches found` or `(eval):1: ... not found` from an expansion means the line aborted, while plain output followed by a failing last command means only that command failed. Keep optional existence checks at the start of a chain, or add `2>/dev/null || true`, so they don't mislabel the whole thing.
