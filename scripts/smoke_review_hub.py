"""Smoke-test the Review Hub server, live replay stream, and decision gate."""

from __future__ import annotations

import json
from pathlib import Path
import socket
import subprocess
import sys
import time
from urllib.error import URLError
from urllib.request import Request, urlopen


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def available_port() -> int:
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        return int(listener.getsockname()[1])


def wait_until_ready(base_url: str) -> None:
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        try:
            with urlopen(f"{base_url}/api/state", timeout=1) as response:
                if response.status == 200:
                    return
        except URLError:
            time.sleep(0.1)
    raise RuntimeError("Review Hub server did not become ready")


def main() -> int:
    port = available_port()
    base_url = f"http://127.0.0.1:{port}"
    server = subprocess.Popen(
        [sys.executable, "-u", "review-hub/server.py", "--port", str(port)],
        cwd=REPOSITORY_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    try:
        wait_until_ready(base_url)
        with urlopen(base_url, timeout=3) as response:
            page = response.read().decode("utf-8")
        if "RUN LIVE PROOF" not in page or "Promotion gate · locked" not in page:
            raise RuntimeError("Review Hub did not render the locked live-proof state")

        with urlopen(f"{base_url}/api/replay", timeout=30) as response:
            event_stream = response.read().decode("utf-8")
        required_events = ["event: setup", "event: check", "event: complete"]
        if not all(event in event_stream for event in required_events):
            raise RuntimeError("Replay stream omitted required evidence events")
        if '"promotion_unlocked":true' not in event_stream:
            raise RuntimeError("Replay did not unlock capability promotion")

        body = json.dumps({"decision": "promote"}).encode("utf-8")
        request = Request(
            f"{base_url}/api/decision",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=3) as response:
            decision = json.loads(response.read())
        if decision.get("decision") != "promoted":
            raise RuntimeError("Promotion decision was not recorded")

        print("REVIEW HUB READY: live replay streamed and promotion recorded.")
        return 0
    finally:
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()
            server.wait(timeout=5)


if __name__ == "__main__":
    raise SystemExit(main())
