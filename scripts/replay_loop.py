"""Replay Prodomi Loop's controlled capability-promotion proof in worktrees."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys
import tempfile


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
BASELINE_REF = "f0de375"
ASSISTED_REF = "5b4b8e8"


def run(command: list[str], *, source_root: Path) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["PRODOMI_SOURCE_ROOT"] = str(source_root)
    return subprocess.run(
        command,
        cwd=REPOSITORY_ROOT,
        env=environment,
        text=True,
        capture_output=True,
        check=False,
    )


def verify(label: str, test_file: str, source_root: Path, expected_returncode: int) -> bool:
    result = run([sys.executable, "-m", "unittest", test_file], source_root=source_root)
    outcome = "PASS" if result.returncode == 0 else "FAIL"
    expected = "PASS" if expected_returncode == 0 else "FAIL"
    print(f"\n{label}: {outcome} (expected {expected})")
    print(result.stdout or result.stderr, end="")
    return result.returncode == expected_returncode


def add_worktree(path: Path, revision: str) -> None:
    subprocess.run(
        ["git", "worktree", "add", "--detach", str(path), revision],
        cwd=REPOSITORY_ROOT,
        check=True,
    )


def remove_worktree(path: Path) -> None:
    subprocess.run(
        ["git", "worktree", "remove", "--force", str(path)],
        cwd=REPOSITORY_ROOT,
        check=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline-ref", default=BASELINE_REF)
    parser.add_argument("--assisted-ref", default=ASSISTED_REF)
    arguments = parser.parse_args()

    with tempfile.TemporaryDirectory(prefix="prodomi-loop-") as temporary_directory:
        temporary_root = Path(temporary_directory)
        baseline = temporary_root / "baseline"
        assisted = temporary_root / "assisted"
        add_worktree(baseline, arguments.baseline_ref)
        add_worktree(assisted, arguments.assisted_ref)
        try:
            checks = [
                verify("Task A visible examples", "tests/test_checkout_visible.py", baseline / "src", 0),
                verify("Task A independent contract", "acceptance/test_task_a_currency_rules.py", baseline / "src", 1),
                verify("Task B baseline holdout", "acceptance/test_task_b_refund_rules.py", baseline / "src", 1),
                verify("Task B capability-assisted holdout", "acceptance/test_task_b_refund_rules.py", assisted / "src", 0),
            ]
        finally:
            remove_worktree(baseline)
            remove_worktree(assisted)

    if all(checks):
        print("\nPROMOTE: fresh-task evidence improved under the same independent contract.")
        return 0

    print("\nREJECT: one or more expected verification outcomes changed.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
