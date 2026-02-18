#!/usr/bin/env python3
"""
Continuous Learning v2 - Observer Daemon

Background process that monitors observations and triggers analysis.
Cross-platform: Windows, macOS, Linux.

Adapted from everything-claude-code (MIT License)
"""
from __future__ import annotations

import os
import sys
import time
import subprocess
import signal
from pathlib import Path
from datetime import datetime

config_dir = Path(os.path.expanduser('~')) / '.claude' / 'homunculus'
pid_file = config_dir / '.observer.pid'
log_file = config_dir / 'observer.log'
obs_file = config_dir / 'observations.jsonl'
trigger_file = config_dir / '.analyze-trigger'
poll_interval = 30   # Check trigger file every 30 seconds
full_interval = 300  # Full analysis every 5 minutes
min_observations = 10

# Ensure directory exists
config_dir.mkdir(parents=True, exist_ok=True)

# Write PID
pid_file.write_text(str(os.getpid()), encoding='utf-8')


def log(msg: str) -> None:
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f'[{ts}] {msg}\n')


def cleanup(*args) -> None:
    try:
        pid_file.unlink(missing_ok=True)
        trigger_file.unlink(missing_ok=True)
    except Exception:
        pass
    log('Observer stopped')
    sys.exit(0)


signal.signal(signal.SIGTERM, cleanup)
signal.signal(signal.SIGINT, cleanup)

# Try to register SIGUSR1 handler (Unix only)
try:
    def on_usr1(*args):
        log('Received SIGUSR1, triggering analysis')
        analyze()
    signal.signal(signal.SIGUSR1, on_usr1)
except (AttributeError, ValueError):
    pass  # SIGUSR1 not available on Windows


def analyze() -> None:
    if not obs_file.exists():
        return
    try:
        obs_count = sum(1 for _ in open(obs_file, encoding='utf-8'))
    except Exception:
        return
    if obs_count < min_observations:
        return

    log(f'Analyzing {obs_count} observations...')

    # Use Claude Code with Haiku to analyze observations
    claude_cmd = 'claude'
    try:
        result = subprocess.run(
            [claude_cmd, '--model', 'haiku', '--max-turns', '3', '--print',
             f'Read {obs_file} and identify patterns. If you find 3+ occurrences '
             f'of the same pattern, create an instinct file in '
             f'{config_dir}/instincts/personal/ following the YAML frontmatter format '
             f'(id, trigger, confidence, domain, source fields). '
             f'Be conservative - only create instincts for clear patterns.'],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            log('Analysis complete')
        else:
            log(f'Analysis failed (exit {result.returncode})')
    except FileNotFoundError:
        log('claude CLI not found, skipping analysis')
    except subprocess.TimeoutExpired:
        log('Analysis timed out')
    except Exception as e:
        log(f'Analysis error: {e}')

    # Archive processed observations
    try:
        archive_dir = config_dir / 'observations.archive'
        archive_dir.mkdir(parents=True, exist_ok=True)
        archive_name = f'processed-{datetime.now().strftime("%Y%m%d-%H%M%S")}.jsonl'
        obs_file.rename(archive_dir / archive_name)
        obs_file.touch()
    except Exception:
        pass


log(f'Observer started (PID: {os.getpid()})')

elapsed = 0
try:
    while True:
        time.sleep(poll_interval)
        elapsed += poll_interval

        # Check file-based trigger (cross-platform, works on Windows)
        if trigger_file.exists():
            try:
                trigger_file.unlink()
            except Exception:
                pass
            analyze()
            elapsed = 0

        # Periodic analysis
        if elapsed >= full_interval:
            analyze()
            elapsed = 0
except KeyboardInterrupt:
    pass
finally:
    cleanup()
