#!/usr/bin/env python3
"""Run the geometry-aware project working copy of the RESNUCLEi exporter.

Default location: working/readers. Set FLUKA_UTIL_DIR for an explicit override.
All arguments are passed unchanged; use --help for the reader options.
"""
import os
from pathlib import Path
import subprocess
import sys


def main():
    root = Path(__file__).resolve().parents[1]
    utility_dir = Path(os.environ.get("FLUKA_UTIL_DIR", str(root / "working" / "readers"))).expanduser()
    program = utility_dir / "process-rn-tab.py"
    if not program.is_file():
        print(f"Reader missing: {program}. Set FLUKA_UTIL_DIR to its checkout.", file=sys.stderr)
        return 2
    return subprocess.run([sys.executable, "-B", str(program), *sys.argv[1:]], check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
