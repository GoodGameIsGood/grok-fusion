#!/usr/bin/env python3
"""Record smoke-ci eval results (CI/fixture/file-presence only — not live Cursor Task)."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "evals" / "results"
OUT_NAME = "smoke-ci-2026-07-18.json"

REQUIRED_PATHS = [
    "agents/gf-worker.md",
    "agents/gf-reviewer.md",
    "agents/gf-auditor.md",
    "skills/grok-fusion/SKILL.md",
    "skills/grok-design/SKILL.md",
    "skills/grok-web-ui/SKILL.md",
    "rules/grok-fusion-auto.mdc",
]


def run_cmd(cmd: list[str], expect_exit: int) -> dict:
    proc = subprocess.run(
        cmd,
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    ok = proc.returncode == expect_exit
    return {
        "cmd": " ".join(cmd),
        "exit_code": proc.returncode,
        "expect_exit": expect_exit,
        "ok": ok,
        "stderr_tail": (proc.stderr or "")[-400:],
        "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def check_paths() -> dict:
    missing = [p for p in REQUIRED_PATHS if not (ROOT / p).is_file()]
    return {
        "cmd": "file_presence",
        "exit_code": 0 if not missing else 1,
        "expect_exit": 0,
        "ok": not missing,
        "missing": missing,
        "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def main() -> int:
    checks: list[dict] = []
    checks.append(
        run_cmd([sys.executable, "-m", "py_compile", "scripts/validate_plugin.py"], 0)
    )
    checks.append(run_cmd([sys.executable, "scripts/validate_plugin.py"], 0))
    checks.append(
        run_cmd(
            [
                sys.executable,
                "scripts/validate_plugin.py",
                "--state",
                "evals/fixtures/valid-run",
            ],
            0,
        )
    )
    for fixture, substring in (
        ("evals/fixtures/invalid-run", None),
        ("evals/fixtures/invalid-legacy-fields", "produces"),
        ("evals/fixtures/invalid-blocked-missing-reason", "blocked_reason"),
        ("evals/fixtures/invalid-false-done", "closure"),
    ):
        result = run_cmd(
            [sys.executable, "scripts/validate_plugin.py", "--state", fixture],
            1,
        )
        if substring and result["exit_code"] == 1:
            blob = (result.get("stderr_tail") or "").lower()
            # Re-run to capture full stderr for substring if needed
            proc = subprocess.run(
                [sys.executable, "scripts/validate_plugin.py", "--state", fixture],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            blob = ((proc.stderr or "") + (proc.stdout or "")).lower()
            result["expect_substring"] = substring
            result["substring_ok"] = substring.lower() in blob
            result["ok"] = result["ok"] and result["substring_ok"]
        checks.append(result)
    checks.append(check_paths())

    all_ok = all(c.get("ok") for c in checks)
    payload = {
        "schema_version": 1,
        "kind": "smoke-ci",
        "date": "2026-07-18",
        "summary": (
            "CI/fixture/file-presence smoke recorded. "
            "Not a live Cursor Task/badge smoke; not Fable parity."
        ),
        "status": "PASS" if all_ok else "FAIL",
        "non_claims": [
            "live Cursor Task spawn",
            "model inherit badge",
            "universal capability",
            "measured Fable parity",
        ],
        "checks": checks,
    }
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    out = RESULTS_DIR / OUT_NAME
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out.relative_to(ROOT)} status={payload['status']}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
