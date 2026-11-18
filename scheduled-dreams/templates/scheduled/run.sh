#!/usr/bin/env bash
# Scheduled dreams on the dream server, run every 15 minutes by the
# dreamer.timer systemd user unit, from a disposable clone of the install
# (~/vault by default). Protocols: .therapy/protocols/dream-ingest.md (ingest)
# and .therapy/protocols/dream.md (longform).
#
# One tick: fetch and hard-reset the clone to origin/main; wait for a quiet
# window (no commit on origin/main for 2 h); pause while any dream/* branch is
# on origin, stop at 2 failed ingest/* branches; run an ingest if notes are
# waiting, gate it, land it on main (pass) or push the branch for review
# (fail); then run a longform if one is due and push its dream/* branch.
# The agent commits on its branch and never pushes; only this script pushes,
# with DREAMER_RUNNER_PUSH=1, which the pre-push hook requires.
#
# Logs to ~/dreamer.log: time, kind, range, outcome, counts. Never content:
# no note text, no commit subjects, no gate reasons (they name files), no
# agent output. git runs quiet for the same reason.
#
# Settings (environment, all optional):
#   DREAMER_REPO           clone to work in              (~/vault)
#   DREAMER_LOG            log file                      (~/dreamer.log)
#   DREAMER_ENV_FILE       file with CLAUDE_CODE_OAUTH_TOKEN=..., mode 600
#                                                        (~/.config/dreamer/env)
#   DREAMER_STATE_DIR      lock and per-window state     (~/.local/state/dreamer)
#   DREAMER_QUIET_SECS     quiet window                  (7200)
#   DREAMER_AGENT_TIMEOUT  max agent run time, for timeout(1)  (4h)
#   CLAUDE_BIN             Claude Code CLI               (claude)
#
# The whole script is one function called on the last line, so bash has read
# all of it before the hard reset can rewrite this file on disk.

set -euo pipefail

main() {
  local repo="${DREAMER_REPO:-$HOME/vault}"
  LOG="${DREAMER_LOG:-$HOME/dreamer.log}"
  local env_file="${DREAMER_ENV_FILE:-$HOME/.config/dreamer/env}"
  STATE="${DREAMER_STATE_DIR:-$HOME/.local/state/dreamer}"
  local quiet_secs="${DREAMER_QUIET_SECS:-7200}"
  AGENT_TIMEOUT="${DREAMER_AGENT_TIMEOUT:-4h}"
  CLAUDE="${CLAUDE_BIN:-claude}"
  ENV_FILE="$env_file"
  TRANSCRIPTS="$HOME/.claude/projects"
  export GIT_TERMINAL_PROMPT=0

  mkdir -p "$STATE"
  chmod 700 "$STATE"
  touch "$LOG"
  chmod 600 "$LOG"

  command -v flock >/dev/null || { log run error "flock not installed"; return 1; }
  exec 9>"$STATE/run.lock"
  if ! flock -n 9; then
    return 0  # the previous tick is still running
  fi

  WORK="$(mktemp -d "$STATE/tick.XXXXXX")"
  trap 'rm -rf "$WORK"' EXIT

  prune_transcripts

  cd "$repo" || { log run error "no clone at DREAMER_REPO"; return 1; }

  # 1. Fetch and reset the disposable clone to origin/main.
  if ! git fetch -q --prune origin; then
    skip "fetch failed"
    return 0
  fi
  reset_to_origin_main
  install_hook

  # 2. Quiet window.
  local newest now age
  newest="$(git log -1 --format=%ct origin/main)"
  now="$(date +%s)"
  age=$(( now - newest ))
  if (( age < quiet_secs )); then
    skip "not quiet"
    return 0
  fi
  WINDOW="$(git rev-parse origin/main)"

  # 3. Pause and stop.
  local dreams ingests
  dreams="$(git for-each-ref --format='%(refname)' 'refs/remotes/origin/dream/' | grep -c . || true)"
  ingests="$(git for-each-ref --format='%(refname)' 'refs/remotes/origin/ingest/' | grep -c . || true)"
  if (( dreams > 0 )); then
    skip "paused: $dreams dream/* branch(es) on origin waiting for review"
    return 0
  fi
  if (( ingests >= 2 )); then
    skip "stopped: $ingests failed ingest/* branches on origin; delete them in maintainer mode to resume"
    return 0
  fi

  # 4. Ingest.
  local pending
  pending="$(python3 .therapy/scripts/scheduled/status.py --pending 2>/dev/null | tr -d '[:space:]')" || pending=""
  if ! [[ "$pending" =~ ^[0-9]+$ ]]; then
    log ingest error "status.py --pending gave no count"
    return 1
  fi

  if (( pending > 0 )); then
    if attempted ingest; then
      skip "ingest already failed in this window; waiting for a new commit on main"
      return 0
    fi
    load_token || return 1
    local ingest_outcome
    run_ingest "$pending"
    ingest_outcome="$RESULT"
    [ "$ingest_outcome" = "merged" ] || return 0
  fi

  # 5. Longform.
  local due_rc=0
  python3 .therapy/scripts/scheduled/status.py --longform-due >/dev/null 2>&1 || due_rc=$?
  case "$due_rc" in
    0) ;;
    1) (( pending > 0 )) || skip "quiet; nothing to ingest, longform not due"; return 0 ;;
    *) log longform error "status.py --longform-due exited $due_rc"; return 1 ;;
  esac
  if attempted longform; then
    skip "longform already failed in this window; waiting for a new commit on main"
    return 0
  fi
  load_token || return 1
  run_longform
  return 0
}

# --- logging -----------------------------------------------------------------

log() {  # log <kind> <outcome> [details...]
  local kind="$1" outcome="$2"; shift 2
  printf '%s · %s · %s%s\n' "$(date '+%Y-%m-%d %H:%M:%S %Z')" "$kind" "$outcome" "${*:+ · $*}" >>"$LOG"
}

skip() {  # log a skip reason only when it differs from the last tick's
  local reason="$1" last=""
  [ -f "$STATE/last-skip" ] && last="$(cat "$STATE/last-skip")"
  if [ "$reason" != "$last" ]; then
    log tick skip "$reason"
    printf '%s' "$reason" >"$STATE/last-skip"
  fi
}

ran() { rm -f "$STATE/last-skip"; }

# --- per-window attempts -----------------------------------------------------
# A window is identified by origin/main's sha. An agent run that ends without
# a usable branch (error, nothing committed, a conflict on landing) is not
# retried until main moves, so a stuck protocol doesn't burn an Opus run every
# 15 minutes. A usage-limit run is not recorded: it's retried next tick.

attempted() { [ -f "$STATE/attempt-$1" ] && [ "$(cat "$STATE/attempt-$1")" = "$WINDOW" ]; }
mark_attempted() { printf '%s' "$WINDOW" >"$STATE/attempt-$1"; }

# --- git ---------------------------------------------------------------------

reset_to_origin_main() {
  git cherry-pick --abort >/dev/null 2>&1 || true
  git rebase --abort >/dev/null 2>&1 || true
  git checkout -q -f -B main origin/main
  git reset -q --hard origin/main
  git clean -q -fd
  local b
  while read -r b; do
    [ -n "$b" ] && [ "$b" != "main" ] && git branch -q -D "$b"
  done < <(git for-each-ref --format='%(refname:short)' refs/heads/)
  return 0
}

install_hook() {  # keep the clone's push guard equal to the committed one
  local src=".therapy/scripts/scheduled/pre-push" dst
  dst="$(git rev-parse --git-path hooks)/pre-push"
  if [ -f "$src" ] && ! cmp -s "$src" "$dst"; then
    mkdir -p "$(dirname "$dst")"
    cp "$src" "$dst"
    chmod 755 "$dst"
  fi
}

runner_push() {  # runner_push <src> <dst ref>
  DREAMER_RUNNER_PUSH=1 git push -q origin "$1:$2" >/dev/null 2>&1
}

new_branch() {  # the newest local branch under <prefix>/ the agent created
  git for-each-ref --sort=-committerdate --format='%(refname:short)' "refs/heads/$1/" | head -n1
}

free_remote_name() {  # ingest/<id>, or ingest/<id>-r2... if origin already has that name
  local name="$1" n=2
  local cand="$name"
  while git show-ref -q --verify "refs/remotes/origin/$cand"; do
    cand="$name-r$n"; n=$((n + 1))
  done
  printf '%s' "$cand"
}

ingest_range() {  # "covered A → B (N sessions) · changes N · flags N" from the added index line
  git diff -U0 "$1" "$2" -- dreams/ingests/index.md 2>/dev/null \
    | sed -n 's/^+- [0-9-]* · \(covered [^·]*\)·.*\(changes [0-9]*\) · \(flags [0-9]*\).*/\1· \2 · \3/p' \
    | head -n1
}

# --- the agent ---------------------------------------------------------------

load_token() {
  if [ ! -f "$ENV_FILE" ]; then
    log run error "env file missing"; return 1
  fi
  local perm
  perm="$(stat -c %a "$ENV_FILE" 2>/dev/null || stat -f %Lp "$ENV_FILE")"
  if [ "$perm" != "600" ]; then
    log run error "env file must be mode 600 (is $perm)"; return 1
  fi
  TOKEN="$(sed -n -E 's/^(export[[:space:]]+)?CLAUDE_CODE_OAUTH_TOKEN=//p' "$ENV_FILE" | tail -n1)"
  TOKEN="${TOKEN%\"}"; TOKEN="${TOKEN#\"}"; TOKEN="${TOKEN%\'}"; TOKEN="${TOKEN#\'}"
  if [ -z "$TOKEN" ]; then
    log run error "no CLAUDE_CODE_OAUTH_TOKEN in env file"; return 1
  fi
}

# Tools the dreamer may use unattended. Anything not listed is denied without
# a prompt (dontAsk + --permission-prompts none). Bash is limited to the
# protocol's scripts, read-only commands and local git; pushing, fetching,
# history rewriting and reading the environment are denied outright.
ALLOWED_TOOLS=(
  "Read" "Grep" "Glob" "Edit" "Write"
  "Bash(python3 .therapy/scripts/*)"
  "Bash(git status*)" "Bash(git diff*)" "Bash(git log*)" "Bash(git show*)"
  "Bash(git branch*)" "Bash(git rev-parse*)" "Bash(git ls-files*)" "Bash(git grep*)"
  "Bash(git add *)" "Bash(git commit *)" "Bash(git checkout -b *)" "Bash(git checkout -- *)"
  "Bash(git mv context/events/pending-*)"
  "Bash(ls*)" "Bash(wc *)" "Bash(grep *)" "Bash(head *)" "Bash(tail *)" "Bash(cat *)"
  "Bash(sort*)" "Bash(uniq*)" "Bash(cut *)" "Bash(date*)" "Bash(uname*)" "Bash(echo *)"
  "Bash(pwd)" "Bash(test *)" "Bash(stat *)" "Bash(du *)" "Bash(diff *)"
)
DISALLOWED_TOOLS=(
  "Bash(git push*)" "Bash(git fetch*)" "Bash(git pull*)" "Bash(git reset*)"
  "Bash(git rebase*)" "Bash(git merge*)" "Bash(git config*)" "Bash(git remote*)"
  "Bash(env*)" "Bash(printenv*)" "Bash(set)" "Bash(export*)"
  "Bash(curl*)" "Bash(wget*)" "Bash(ssh*)" "Bash(rm *)"
  "WebFetch" "WebSearch"
  "Read(~/.config/**)" "Read(~/.ssh/**)" "Read(~/.claude/**)"
  "Edit(.git/**)" "Write(.git/**)" "Edit(.claude/**)" "Write(.claude/**)"
  "Edit(.therapy/scripts/**)" "Write(.therapy/scripts/**)"
)

join_by_comma() { local IFS=,; printf '%s' "$*"; }

new_uuid() {
  if [ -r /proc/sys/kernel/random/uuid ]; then cat /proc/sys/kernel/random/uuid
  else python3 -c 'import uuid; print(uuid.uuid4())'; fi
}

# run_agent <kind> <prompt>: sets AGENT to ok | limit | error, SID to the session id.
run_agent() {
  local kind="$1" prompt="$2" out="$WORK/$1.json" err="$WORK/$1.err" rc=0
  SID="$(new_uuid)"
  local -a tmo=()
  command -v timeout >/dev/null && tmo=(timeout "$AGENT_TIMEOUT")
  ran
  if [ "$kind" = ingest ]; then log ingest start "notes waiting $PENDING"; else log "$kind" start; fi
  env CLAUDE_CODE_OAUTH_TOKEN="$TOKEN" DREAMER_SCHEDULED=1 \
    ${tmo[@]+"${tmo[@]}"} "$CLAUDE" -p "$prompt" \
      --agent dreamer --model opus \
      --output-format json \
      --session-id "$SID" \
      --permission-mode dontAsk --permission-prompts none \
      --allowedTools="$(join_by_comma "${ALLOWED_TOOLS[@]}")" \
      --disallowedTools="$(join_by_comma "${DISALLOWED_TOOLS[@]}")" \
      --settings '{"disableAllHooks": true}' \
      </dev/null >"$out" 2>"$err" || rc=$?
  AGENT="$(python3 - "$out" "$err" "$rc" <<'PY'
import json, re, sys
out, err, rc = sys.argv[1], sys.argv[2], int(sys.argv[3])
LIMIT = re.compile(r"usage limit|limit reached|hit your (usage )?limit|out of (extra )?usage|"
                   r"rate[_ ]limit|429|resets? (at|in)", re.I)
text = open(err, errors="ignore").read()
data = None
try:
    raw = open(out, errors="ignore").read().strip()
    data = json.loads(raw.splitlines()[-1]) if raw else None
except Exception:
    data = None
if isinstance(data, dict):
    text += " " + str(data.get("result", "")) + " " + str(data.get("subtype", ""))
    text += " " + json.dumps(data.get("errors", ""))
    is_error = bool(data.get("is_error")) or data.get("subtype") not in (None, "success")
else:
    is_error = True
if (is_error or rc != 0) and LIMIT.search(text):
    print("limit")
elif is_error or rc != 0:
    print("error")
else:
    print("ok")
PY
)"
  rm -f "$out" "$err"  # agent output can hold content; never kept
}

forget_transcript() {  # a successful run's transcript goes at once
  [ -n "${SID:-}" ] && [ -d "$TRANSCRIPTS" ] || return 0
  find "$TRANSCRIPTS" -mindepth 1 -maxdepth 2 -name "$SID*" -exec rm -rf {} + 2>/dev/null || true
}

prune_transcripts() {  # failed runs' transcripts stay 7 days
  [ -d "$TRANSCRIPTS" ] || return 0
  find "$TRANSCRIPTS" -mindepth 1 -type f -mtime +7 -delete 2>/dev/null || true
  find "$TRANSCRIPTS" -mindepth 1 -type d -empty -delete 2>/dev/null || true
}

# --- ingest ------------------------------------------------------------------

run_ingest() {
  PENDING="$1"
  RESULT="none"
  local base
  base="$(git rev-parse origin/main)"
  run_agent ingest "Run an ingest per .therapy/protocols/dream-ingest.md."
  case "$AGENT" in
    limit) log ingest discarded "usage limit; nothing pushed, not counted"; RESULT="limit"; return 0 ;;
    error) log ingest error "agent run failed; nothing pushed"; mark_attempted ingest; RESULT="error"; return 0 ;;
  esac

  local branch
  branch="$(new_branch ingest)"
  if [ -z "$branch" ]; then
    log ingest error "agent made no ingest/* branch; nothing pushed"; mark_attempted ingest; RESULT="error"; return 0
  fi
  if [ "$(git rev-list --count "$base..$branch")" = "0" ]; then
    log ingest error "branch has no commit; nothing pushed"; mark_attempted ingest; RESULT="error"; return 0
  fi
  git checkout -q -f "$branch"
  git reset -q --hard
  git clean -q -fd

  local range gate_rc=0 gate_out
  range="$(ingest_range "$base" "$branch")"
  gate_out="$(python3 .therapy/scripts/scheduled/gate.py --base "$base" 2>&1)" || gate_rc=$?
  if (( gate_rc != 0 )); then
    local reasons remote
    reasons="$(printf '%s\n' "$gate_out" | grep -c '^- ' || true)"
    remote="$(free_remote_name "$branch")"
    if runner_push "$branch" "refs/heads/$remote"; then
      log ingest gate-failed "${range:-range unknown} · $reasons reason(s) · branch pushed for review"
    else
      log ingest error "gate failed ($reasons reason(s)) and pushing the branch failed"
    fi
    RESULT="failed"
    return 0
  fi

  # Land: the gate guarantees one commit on top of base, so that commit is the
  # squash. Fast-forward main to it, or replay it if main moved meanwhile.
  local commit target
  commit="$(git rev-parse "$branch")"
  if ! git fetch -q origin; then
    log ingest discarded "fetch before landing failed; retry next window"; RESULT="discarded"; return 0
  fi
  if [ "$(git rev-parse origin/main)" = "$base" ]; then
    target="$commit"
  else
    git checkout -q -f --detach origin/main
    if ! git cherry-pick --allow-empty-message "$commit" >/dev/null 2>&1; then
      git cherry-pick --abort >/dev/null 2>&1 || true
      log ingest discarded "${range:-range unknown} · main moved and the commit conflicts; retry next window"
      RESULT="discarded"; return 0
    fi
    if ! python3 .therapy/scripts/scheduled/gate.py --base origin/main >/dev/null 2>&1; then
      log ingest discarded "${range:-range unknown} · main moved and the replayed commit fails the gate; retry next window"
      RESULT="discarded"; return 0
    fi
    target="$(git rev-parse HEAD)"
  fi
  if ! runner_push "$target" refs/heads/main; then
    log ingest discarded "${range:-range unknown} · push to main refused (main moved?); retry next window"
    RESULT="discarded"; return 0
  fi
  git fetch -q origin || true
  git checkout -q -f -B main "$target"
  git branch -q -D "$branch" 2>/dev/null || true
  log ingest merged "${range:-range unknown}"
  forget_transcript
  RESULT="merged"
}

# --- longform ----------------------------------------------------------------

run_longform() {
  local base
  base="$(git rev-parse HEAD)"
  run_agent longform "Run a dream per .therapy/protocols/dream.md."
  case "$AGENT" in
    limit) log longform discarded "usage limit; nothing pushed, not counted"; return 0 ;;
    error) log longform error "agent run failed; nothing pushed"; mark_attempted longform; return 0 ;;
  esac
  local branch commits
  branch="$(new_branch dream)"
  if [ -z "$branch" ]; then
    log longform error "agent made no dream/* branch; nothing pushed"; mark_attempted longform; return 0
  fi
  commits="$(git rev-list --count "$base..$branch")"
  if [ "$commits" = "0" ]; then
    log longform error "branch has no commit; nothing pushed"; mark_attempted longform; return 0
  fi
  local remote
  remote="$(free_remote_name "$branch")"
  if runner_push "$branch" "refs/heads/$remote"; then
    log longform pushed "$remote · $commits commit(s) · waiting for review"
    forget_transcript
  else
    log longform error "pushing the dream branch failed"; mark_attempted longform
  fi
}

main "$@"; exit $?
