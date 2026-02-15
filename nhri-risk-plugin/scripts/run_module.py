#!/usr/bin/env python3
"""Single-entry dispatcher for NHRI V4 module scripts."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent  # scripts/ -> nhri-risk-plugin/
SCRIPTS = PLUGIN_ROOT / "scripts"

MODULE_COMMANDS = {
    "spec-popavg": ["python", str(SCRIPTS / "get_population_avg.py")],
    "validate": ["python", str(SCRIPTS / "validate_input.py")],
    "evaluate": ["python", str(SCRIPTS / "nhri_risk_eval.py")],
    "regress-generate": ["python", str(SCRIPTS / "generate_vectors.py")],
    "regress-compare": ["python", str(SCRIPTS / "compare_outputs.py")],
    "api-scaffold": ["python", str(SCRIPTS / "scaffold_adapter.py")],
    "report": ["python", str(SCRIPTS / "render_report.py")],
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--module", required=True, choices=sorted(MODULE_COMMANDS.keys()))
    parser.add_argument(
        "args",
        nargs=argparse.REMAINDER,
        help="Pass-through args. Prefix with -- to separate module args.",
    )
    ns = parser.parse_args()

    passthrough = list(ns.args)
    if passthrough and passthrough[0] == "--":
        passthrough = passthrough[1:]

    cmd = MODULE_COMMANDS[ns.module] + passthrough
    completed = subprocess.run(cmd, cwd=str(PLUGIN_ROOT))
    raise SystemExit(completed.returncode)


if __name__ == "__main__":
    main()
