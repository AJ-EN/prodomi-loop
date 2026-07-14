"""Run consecutive deterministic Prodomi Loop proof rehearsals."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys
import time


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--max-seconds", type=float, default=90)
    arguments = parser.parse_args()

    for run_number in range(1, arguments.runs + 1):
        started = time.monotonic()
        result = subprocess.run(
            [sys.executable, "scripts/replay_loop.py"],
            cwd=REPOSITORY_ROOT,
            check=False,
        )
        elapsed = time.monotonic() - started
        print(f"Rehearsal {run_number}/{arguments.runs}: {elapsed:.2f}s")
        if result.returncode != 0 or elapsed > arguments.max_seconds:
            print("REHEARSAL FAILED")
            return 1

    print("REHEARSAL READY: all runs passed within the time limit.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
