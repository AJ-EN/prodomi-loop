"""Replay Prodomi Loop's capability-promotion proof in clean Git worktrees."""

from __future__ import annotations

import argparse
from collections.abc import Callable
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
BASELINE_REF = "f0de375"
ASSISTED_REF = "5b4b8e8"
EventSink = Callable[[dict[str, Any]], None]


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


def summarize_test_output(output: str) -> tuple[int | None, list[str]]:
    match = re.search(r"Ran (\d+) tests?", output)
    test_count = int(match.group(1)) if match else None
    assertions = [
        line.removeprefix("AssertionError: ").strip()
        for line in output.splitlines()
        if line.startswith("AssertionError: ")
    ]
    return test_count, assertions


def verify(
    check_id: str,
    label: str,
    test_file: str,
    source_root: Path,
    expected_returncode: int,
    emit: EventSink,
) -> dict[str, Any]:
    started = time.monotonic()
    result = run([sys.executable, "-m", "unittest", test_file], source_root=source_root)
    elapsed_ms = round((time.monotonic() - started) * 1000)
    output = "\n".join(part.strip() for part in (result.stdout, result.stderr) if part.strip())
    test_count, assertions = summarize_test_output(output)
    record = {
        "type": "check",
        "id": check_id,
        "label": label,
        "test_file": test_file,
        "outcome": "pass" if result.returncode == 0 else "fail",
        "expected": "pass" if expected_returncode == 0 else "fail",
        "matched_expectation": result.returncode == expected_returncode,
        "test_count": test_count,
        "assertions": assertions,
        "duration_ms": elapsed_ms,
        "output": output,
    }
    emit(record)
    return record


def git_worktree(command: list[str]) -> str:
    result = subprocess.run(
        ["git", "worktree", *command],
        cwd=REPOSITORY_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError((result.stderr or result.stdout).strip())
    return (result.stdout or result.stderr).strip()


def replay(
    baseline_ref: str = BASELINE_REF,
    assisted_ref: str = ASSISTED_REF,
    emit: EventSink | None = None,
) -> dict[str, Any]:
    event_sink = emit or (lambda event: None)
    started = time.monotonic()
    checks: list[dict[str, Any]] = []
    event_sink({"type": "setup", "baseline_ref": baseline_ref, "assisted_ref": assisted_ref})

    with tempfile.TemporaryDirectory(prefix="prodomi-loop-") as temporary_directory:
        temporary_root = Path(temporary_directory)
        baseline = temporary_root / "baseline"
        assisted = temporary_root / "assisted"
        baseline_added = False
        assisted_added = False
        try:
            git_worktree(["add", "--detach", str(baseline), baseline_ref])
            baseline_added = True
            event_sink({"type": "worktree", "role": "baseline", "ref": baseline_ref})
            git_worktree(["add", "--detach", str(assisted), assisted_ref])
            assisted_added = True
            event_sink({"type": "worktree", "role": "assisted", "ref": assisted_ref})
            checks.extend(
                [
                    verify(
                        "task-a-visible",
                        "Task A visible examples",
                        "tests/test_checkout_visible.py",
                        baseline / "src",
                        0,
                        event_sink,
                    ),
                    verify(
                        "task-a-contract",
                        "Task A independent contract",
                        "acceptance/test_task_a_currency_rules.py",
                        baseline / "src",
                        1,
                        event_sink,
                    ),
                    verify(
                        "task-b-baseline",
                        "Task B baseline holdout",
                        "acceptance/test_task_b_refund_rules.py",
                        baseline / "src",
                        1,
                        event_sink,
                    ),
                    verify(
                        "task-b-assisted",
                        "Task B capability-assisted holdout",
                        "acceptance/test_task_b_refund_rules.py",
                        assisted / "src",
                        0,
                        event_sink,
                    ),
                ]
            )
        finally:
            if assisted_added:
                git_worktree(["remove", "--force", str(assisted)])
            if baseline_added:
                git_worktree(["remove", "--force", str(baseline)])
            event_sink({"type": "cleanup", "message": "Temporary worktrees removed"})

    return {
        "baseline_ref": baseline_ref,
        "assisted_ref": assisted_ref,
        "checks": checks,
        "promotion_unlocked": all(check["matched_expectation"] for check in checks),
        "duration_ms": round((time.monotonic() - started) * 1000),
    }


def console_event(event: dict[str, Any]) -> None:
    event_type = event["type"]
    if event_type == "setup":
        print(f"Creating clean worktrees at {event['baseline_ref']} and {event['assisted_ref']}...")
    elif event_type == "worktree":
        print(f"Prepared {event['role']} worktree at {event['ref']}.")
    elif event_type == "check":
        outcome = str(event["outcome"]).upper()
        expected = str(event["expected"]).upper()
        print(f"\n{event['label']}: {outcome} (expected {expected})")
        print(event["output"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline-ref", default=BASELINE_REF)
    parser.add_argument("--assisted-ref", default=ASSISTED_REF)
    parser.add_argument("--json", action="store_true", help="Print a machine-readable report")
    arguments = parser.parse_args()

    report = replay(
        baseline_ref=arguments.baseline_ref,
        assisted_ref=arguments.assisted_ref,
        emit=None if arguments.json else console_event,
    )
    if arguments.json:
        print(json.dumps(report))
    elif report["promotion_unlocked"]:
        print(f"\nPROMOTE: fresh-task evidence improved in {report['duration_ms']}ms.")
    else:
        print("\nREJECT: one or more expected verification outcomes changed.")
    return 0 if report["promotion_unlocked"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
