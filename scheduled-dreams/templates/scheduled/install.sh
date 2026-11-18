#!/usr/bin/env bash
# Install scheduled dreams on the dream server, as the unprivileged user that
# runs them, from the clone at ~/vault (or $DREAMER_REPO):
#   bash ~/vault/.therapy/scripts/scheduled/install.sh
# Installs the push guard as the clone's pre-push hook and the systemd user
# units into ~/.config/systemd/user. Doesn't enable the timer; prints how.
# Safe to run again.
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo="${DREAMER_REPO:-$HOME/vault}"
units="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
env_file="${DREAMER_ENV_FILE:-$HOME/.config/dreamer/env}"

[ -d "$repo/.git" ] || { echo "No git clone at $repo (set DREAMER_REPO)." >&2; exit 1; }

hooks="$(git -C "$repo" rev-parse --git-path hooks)"
case "$hooks" in /*) ;; *) hooks="$repo/$hooks" ;; esac
mkdir -p "$hooks"
install -m 755 "$here/pre-push" "$hooks/pre-push"
echo "Installed push guard: $hooks/pre-push"

if [ -z "$(git -C "$repo" config user.name || true)" ]; then
  git -C "$repo" config user.name "Dreamer"
  git -C "$repo" config user.email "dreamer@localhost"
  echo "Set this clone's commit identity to Dreamer."
fi

mkdir -p "$units"
install -m 644 "$here/dreamer.service" "$units/dreamer.service"
install -m 644 "$here/dreamer.timer" "$units/dreamer.timer"
if [ "$repo" != "$HOME/vault" ]; then
  sed -i.bak "s#%h/vault#$repo#g" "$units/dreamer.service" && rm -f "$units/dreamer.service.bak"
fi
echo "Installed units: $units/dreamer.service, $units/dreamer.timer"

missing=()
for cmd in git python3 flock timeout claude; do
  command -v "$cmd" >/dev/null || [ -x "$HOME/.local/bin/$cmd" ] || missing+=("$cmd")
done
[ ${#missing[@]} -eq 0 ] || echo "Warning: not found on PATH: ${missing[*]}"
[ -f /etc/inner-dialogue-dreamer ] || echo "Warning: /etc/inner-dialogue-dreamer is missing; the dream protocols' machine check will stop (create it as root)."
if [ ! -f "$env_file" ]; then
  echo "Warning: $env_file is missing. Create it with one line CLAUDE_CODE_OAUTH_TOKEN=... (from 'claude setup-token') and chmod 600."
elif [ "$(stat -c %a "$env_file" 2>/dev/null || stat -f %Lp "$env_file")" != "600" ]; then
  echo "Warning: $env_file must be mode 600: chmod 600 $env_file"
fi

cat <<EOF

Not enabled yet. To turn scheduled dreams on:
  systemctl --user daemon-reload
  systemctl --user enable --now dreamer.timer
  sudo loginctl enable-linger $(id -un)    # so the timer runs while nobody is logged in
Check:   systemctl --user list-timers dreamer.timer ; tail ~/dreamer.log
Run one tick now:  systemctl --user start dreamer.service
Turn off:          systemctl --user disable --now dreamer.timer
EOF
