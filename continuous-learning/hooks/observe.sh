#!/bin/bash
# Continuous Learning v2 - Observation Hook
#
# Captures tool use events for pattern analysis.
# Claude Code passes hook data via stdin as JSON.
#
# Cross-platform: Windows (Git Bash/MSYS2), macOS, Linux
# Adapted from everything-claude-code (MIT License)
#
# Hook config (in plugin.json - auto-registered):
# PreToolUse/PostToolUse → observe.sh pre/post

set -e

CONFIG_DIR="${HOME}/.claude/homunculus"
OBSERVATIONS_FILE="${CONFIG_DIR}/observations.jsonl"
MAX_FILE_SIZE_MB=10
TRIGGER_FILE="${CONFIG_DIR}/.analyze-trigger"

# Ensure directory exists
mkdir -p "$CONFIG_DIR"

# Skip if disabled
if [ -f "$CONFIG_DIR/disabled" ]; then
  exit 0
fi

# Cross-platform: detect python command (Windows often has 'python' not 'python3')
if command -v python3 &>/dev/null; then
  PYTHON=python3
else
  PYTHON=python
fi

# Read JSON from stdin (Claude Code hook format)
INPUT_JSON=$(cat)

# Exit if no input
if [ -z "$INPUT_JSON" ]; then
  exit 0
fi

# Parse and write observation in a single Python call (cross-platform, no date/du dependency)
echo "$INPUT_JSON" | $PYTHON -c "
import json, sys, os
from datetime import datetime, timezone
from pathlib import Path

config_dir = Path(os.path.expanduser('~')) / '.claude' / 'homunculus'
obs_file = config_dir / 'observations.jsonl'
max_size_mb = $MAX_FILE_SIZE_MB
trigger_file = config_dir / '.analyze-trigger'

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

# Extract fields - Claude Code hook format
hook_type = data.get('hook_type', 'unknown')
tool_name = data.get('tool_name', data.get('tool', 'unknown'))
tool_input = data.get('tool_input', data.get('input', {}))
tool_output = data.get('tool_output', data.get('output', ''))
session_id = data.get('session_id', 'unknown')

# Truncate large inputs/outputs
if isinstance(tool_input, dict):
    tool_input_str = json.dumps(tool_input)[:5000]
else:
    tool_input_str = str(tool_input)[:5000]

if isinstance(tool_output, dict):
    tool_output_str = json.dumps(tool_output)[:5000]
else:
    tool_output_str = str(tool_output)[:5000]

# Determine event type
event = 'tool_start' if 'Pre' in hook_type else 'tool_complete'

# Cross-platform timestamp (no dependency on 'date' command)
timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

# Build observation
observation = {
    'timestamp': timestamp,
    'event': event,
    'tool': tool_name,
    'session': session_id
}
if event == 'tool_start' and tool_input_str:
    observation['input'] = tool_input_str
if event == 'tool_complete' and tool_output_str:
    observation['output'] = tool_output_str

# Archive if file too large (cross-platform: os.path.getsize instead of 'du -m')
if obs_file.exists():
    try:
        size_mb = obs_file.stat().st_size / (1024 * 1024)
        if size_mb >= max_size_mb:
            archive_dir = config_dir / 'observations.archive'
            archive_dir.mkdir(parents=True, exist_ok=True)
            archive_name = f'observations-{datetime.now().strftime(\"%Y%m%d-%H%M%S\")}.jsonl'
            obs_file.rename(archive_dir / archive_name)
    except OSError:
        pass

# Write observation
with open(obs_file, 'a', encoding='utf-8') as f:
    f.write(json.dumps(observation) + '\n')

# Signal observer: use file-based trigger (cross-platform, works on Windows)
# Also try SIGUSR1 for Unix systems where it's more responsive
import signal
pid_file = config_dir / '.observer.pid'
if pid_file.exists():
    try:
        pid = int(pid_file.read_text().strip())
        os.kill(pid, 0)  # Check if process exists
        # Try SIGUSR1 (Unix only), fall back to file trigger
        try:
            os.kill(pid, signal.SIGUSR1)
        except (OSError, AttributeError, ValueError):
            # SIGUSR1 not available (Windows) or failed — use file trigger
            trigger_file.touch()
    except (OSError, ValueError):
        # Process doesn't exist or invalid PID — use file trigger anyway
        trigger_file.touch()
"

exit 0
