#!/usr/bin/env bash
# Session start: bring main up to date before the startup script runs, so the
# session reads what the server's ingests landed (.therapy/protocols/dream-ingest.md).
# Install as .claude/session-pull.sh and register it as a SessionStart hook.
# Fast-forward only, on a clean main, with a timeout. Any problem (offline,
# dirty tree, diverged, another branch) skips the pull silently: the startup
# script then reads the blocks of the notes this checkout hasn't seen ingested.
# Never prints and never fails, since SessionStart output reaches the model.
cd "${CLAUDE_PROJECT_DIR:-.}" 2>/dev/null || exit 0
[ "$(git rev-parse --abbrev-ref HEAD 2>/dev/null)" = "main" ] || exit 0
[ -z "$(git status --porcelain 2>/dev/null)" ] || exit 0
if command -v timeout >/dev/null 2>&1; then T="timeout 20"; elif command -v gtimeout >/dev/null 2>&1; then T="gtimeout 20"; else T=""; fi
GIT_TERMINAL_PROMPT=0 $T git pull --ff-only --quiet origin main >/dev/null 2>&1 || true
exit 0
