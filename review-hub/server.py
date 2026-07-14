"""Local demo server for the live Prodomi Loop evidence gate."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import sys
import threading
from typing import Any
from urllib.parse import urlparse


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
STATIC_DIRECTORY = Path(__file__).resolve().parent
RUNTIME_DIRECTORY = REPOSITORY_ROOT / ".prodomi"
DECISION_FILE = RUNTIME_DIRECTORY / "demo-decision.json"
sys.path.insert(0, str(REPOSITORY_ROOT / "scripts"))

from replay_loop import replay  # noqa: E402


class DemoState:
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.running = False
        self.report: dict[str, Any] | None = None
        self.decision: dict[str, Any] | None = None

    def snapshot(self) -> dict[str, Any]:
        with self.lock:
            return {
                "status": "running" if self.running else "ready",
                "promotion_unlocked": bool(
                    self.report and self.report.get("promotion_unlocked")
                ),
                "decision": self.decision,
            }


STATE = DemoState()


class ReviewHubHandler(SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, directory=str(STATIC_DIRECTORY), **kwargs)

    def log_message(self, format: str, *args: Any) -> None:
        print(f"review-hub: {format % args}")

    def send_json(self, payload: dict[str, Any], status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def send_event(self, event: dict[str, Any]) -> None:
        payload = json.dumps(event, separators=(",", ":"))
        self.wfile.write(f"event: {event['type']}\ndata: {payload}\n\n".encode("utf-8"))
        self.wfile.flush()

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/api/state":
            self.send_json(STATE.snapshot())
            return
        if path == "/api/replay":
            self.stream_replay()
            return
        super().do_GET()

    def stream_replay(self) -> None:
        with STATE.lock:
            if STATE.running:
                self.send_json({"error": "A replay is already running"}, HTTPStatus.CONFLICT)
                return
            STATE.running = True
            STATE.report = None
            STATE.decision = None

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Connection", "close")
        self.end_headers()
        try:
            report = replay(emit=self.send_event)
            with STATE.lock:
                STATE.report = report
            self.send_event(
                {
                    "type": "complete",
                    "promotion_unlocked": report["promotion_unlocked"],
                    "duration_ms": report["duration_ms"],
                    "baseline_ref": report["baseline_ref"],
                    "assisted_ref": report["assisted_ref"],
                }
            )
        except (BrokenPipeError, ConnectionResetError):
            pass
        except Exception as error:
            try:
                self.send_event({"type": "error", "message": str(error)})
            except (BrokenPipeError, ConnectionResetError):
                pass
        finally:
            with STATE.lock:
                STATE.running = False
            self.close_connection = True

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        if path == "/api/decision":
            self.record_decision()
            return
        if path == "/api/reset":
            with STATE.lock:
                STATE.report = None
                STATE.decision = None
            self.send_json({"status": "reset"})
            return
        self.send_json({"error": "Not found"}, HTTPStatus.NOT_FOUND)

    def record_decision(self) -> None:
        content_length = int(self.headers.get("Content-Length", "0"))
        try:
            payload = json.loads(self.rfile.read(content_length) or b"{}")
        except json.JSONDecodeError:
            self.send_json({"error": "Invalid JSON"}, HTTPStatus.BAD_REQUEST)
            return

        decision = payload.get("decision")
        if decision not in {"promote", "reject"}:
            self.send_json({"error": "Decision must be promote or reject"}, HTTPStatus.BAD_REQUEST)
            return

        with STATE.lock:
            if not STATE.report or not STATE.report.get("promotion_unlocked"):
                self.send_json(
                    {"error": "Run and pass the holdout replay before deciding"},
                    HTTPStatus.CONFLICT,
                )
                return
            record = {
                "decision": "promoted" if decision == "promote" else "rejected",
                "decided_at": datetime.now(timezone.utc).isoformat(),
                "capability": "skills/currency-rules/SKILL.md",
                "baseline_ref": STATE.report["baseline_ref"],
                "assisted_ref": STATE.report["assisted_ref"],
                "holdout_improved": True,
            }
            STATE.decision = record

        RUNTIME_DIRECTORY.mkdir(exist_ok=True)
        DECISION_FILE.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        self.send_json(record)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8000)
    arguments = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", arguments.port), ReviewHubHandler)
    print(f"Prodomi Loop Review Hub: http://127.0.0.1:{arguments.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nReview Hub stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
