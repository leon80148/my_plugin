#!/bin/bash
# Continuous Learning v2 - Observer Agent Launcher
#
# Starts the background observer agent that analyzes observations
# and creates instincts. Uses Haiku model for cost efficiency.
#
# Cross-platform: Windows (Git Bash/MSYS2), macOS, Linux
# Adapted from everything-claude-code (MIT License)
#
# Usage:
#   start-observer.sh start   # Start observer in background (default)
#   start-observer.sh stop    # Stop running observer
#   start-observer.sh status  # Check if observer is running

set -e

CONFIG_DIR="${HOME}/.claude/homunculus"
PID_FILE="${CONFIG_DIR}/.observer.pid"
LOG_FILE="${CONFIG_DIR}/observer.log"
OBSERVATIONS_FILE="${CONFIG_DIR}/observations.jsonl"
TRIGGER_FILE="${CONFIG_DIR}/.analyze-trigger"

# Cross-platform: detect python command
if command -v python3 &>/dev/null; then
  PYTHON=python3
else
  PYTHON=python
fi

mkdir -p "$CONFIG_DIR"

# Cross-platform process check using Python (most reliable across all platforms)
is_process_running() {
  local pid=$1
  $PYTHON -c "
import os, sys
try:
    os.kill(int(sys.argv[1]), 0)
    sys.exit(0)
except (OSError, ProcessLookupError):
    sys.exit(1)
except ValueError:
    sys.exit(1)
" "$pid" 2>/dev/null
  return $?
}

# Cross-platform process termination using Python
stop_process() {
  local pid=$1
  $PYTHON -c "
import os, sys, signal
pid = int(sys.argv[1])
try:
    os.kill(pid, signal.SIGTERM)
    sys.exit(0)
except OSError:
    pass
# Windows fallback: taskkill
import subprocess
try:
    r = subprocess.run(['taskkill', '/PID', str(pid), '/F'],
                       capture_output=True, timeout=5)
    sys.exit(0 if r.returncode == 0 else 1)
except FileNotFoundError:
    sys.exit(1)
" "$pid" 2>/dev/null
  return $?
}

# Get observation count (cross-platform)
get_obs_count() {
  if [ -f "$OBSERVATIONS_FILE" ]; then
    $PYTHON -c "
with open('$OBSERVATIONS_FILE', encoding='utf-8') as f:
    print(sum(1 for _ in f))
" 2>/dev/null || echo "0"
  else
    echo "0"
  fi
}

case "${1:-start}" in
  stop)
    if [ -f "$PID_FILE" ]; then
      pid=$(cat "$PID_FILE")
      if is_process_running "$pid"; then
        echo "Stopping observer (PID: $pid)..."
        stop_process "$pid"
        rm -f "$PID_FILE" "$TRIGGER_FILE"
        echo "Observer stopped."
      else
        echo "Observer not running (stale PID file)."
        rm -f "$PID_FILE"
      fi
    else
      echo "Observer not running."
    fi
    exit 0
    ;;

  status)
    if [ -f "$PID_FILE" ]; then
      pid=$(cat "$PID_FILE")
      if is_process_running "$pid"; then
        obs_count=$(get_obs_count)
        echo "Observer is running (PID: $pid)"
        echo "Log: $LOG_FILE"
        echo "Observations: $obs_count lines"
        exit 0
      else
        echo "Observer not running (stale PID file)"
        rm -f "$PID_FILE"
        exit 1
      fi
    else
      echo "Observer not running"
      exit 1
    fi
    ;;

  start)
    # Check if already running
    if [ -f "$PID_FILE" ]; then
      pid=$(cat "$PID_FILE")
      if is_process_running "$pid"; then
        echo "Observer already running (PID: $pid)"
        exit 0
      fi
      rm -f "$PID_FILE"
    fi

    echo "Starting observer agent..."

    # Resolve path to observer-daemon.py (relative to this script)
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    DAEMON_SCRIPT="${SCRIPT_DIR}/observer-daemon.py"

    if [ ! -f "$DAEMON_SCRIPT" ]; then
      echo "Error: observer-daemon.py not found at $DAEMON_SCRIPT"
      exit 1
    fi

    # Launch observer daemon as background Python process
    $PYTHON "$DAEMON_SCRIPT" >> "$LOG_FILE" 2>&1 &

    # Detach from terminal
    if command -v disown &>/dev/null; then
      disown 2>/dev/null || true
    fi

    # Wait for PID file
    sleep 2

    if [ -f "$PID_FILE" ]; then
      echo "Observer started (PID: $(cat "$PID_FILE"))"
      echo "Log: $LOG_FILE"
    else
      echo "Failed to start observer"
      exit 1
    fi
    ;;

  *)
    echo "Usage: $0 {start|stop|status}"
    exit 1
    ;;
esac
