#!/usr/bin/env bash
# Run long steps (setup, voice, render) in the background so a tool time limit can't kill them.
#
#   bash scripts/job.sh start <name> <command...>   start a job, returns immediately
#   bash scripts/job.sh wait  <name> [seconds]      wait up to N s (default 150), print status + log tail
#   bash scripts/job.sh status <name>               print status + log tail without waiting
#
# Status is one of: running | done | failed (exit N). Call `wait` repeatedly until it isn't "running".
set -u
JOBS="${SHORTS_STUDIO_HOME:-$HOME/.shorts-studio}/jobs"
mkdir -p "$JOBS"
cmd="${1:-}"; name="${2:-}"
[ -n "$cmd" ] && [ -n "$name" ] || { sed -n '2,9p' "$0"; exit 2; }
log="$JOBS/$name.log"; st="$JOBS/$name.status"

show() {
  s="$(cat "$st" 2>/dev/null || echo 'not started')"
  echo "job '$name': $s"
  tail -n "${1:-12}" "$log" 2>/dev/null | sed 's/^/  | /'
}

case "$cmd" in
  start)
    shift 2
    [ "$(cat "$st" 2>/dev/null)" = running ] && { echo "job '$name' is already running"; exit 0; }
    echo running > "$st"; : > "$log"
    nohup bash -c 'log="$1"; st="$2"; shift 2; "$@" >>"$log" 2>&1; c=$?
      if [ $c -eq 0 ]; then echo done > "$st"; else echo "failed (exit $c)" > "$st"; fi' \
      _ "$log" "$st" "$@" >/dev/null 2>&1 < /dev/null &
    echo "started job '$name' (log: $log)"
    ;;
  wait)
    limit="${3:-150}"; t=0
    while [ "$(cat "$st" 2>/dev/null)" = running ] && [ $t -lt "$limit" ]; do sleep 3; t=$((t + 3)); done
    show 15
    ;;
  status) show 15 ;;
  *) sed -n '2,9p' "$0"; exit 2 ;;
esac
