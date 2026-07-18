#!/usr/bin/env python3
"""Warn when Grok Build / host subagents (agents plaque) are disabled.

Used by plugin SessionStart / UserPromptSubmit hooks. Prints a user-visible
notice to stderr and emits JSON fields some hosts inject into context.
Exit 0 always (fail-open): never block the session.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

NOTICE = """\
⚠️ Grok Fusion — агенты (subagents) ВЫКЛЮЧЕНЫ
⚠️ Grok Fusion — subagents / Task agents are OFF

Без этой плашки council не запустится (Fusion did not run).
Without this toggle the Fusion council cannot start.

Как включить / How to enable:
• Grok Build: в `~/.grok/config.toml` добавьте:
    [subagents]
    enabled = true
  или Extensions (/plugins) → Subagents → enable, затем новый сеанс.
• Cursor: убедитесь, что Task tool и custom agents `gf-*` доступны.

После включения перезапустите сессию / reload the session.
"""


def _parse_toml_bool_enabled(text: str) -> bool | None:
    """Return True/False if [subagents] enabled= is set; else None."""
    match = re.search(r"(?ms)^\[subagents\]\s*(.*?)(?=^\[|\Z)", text)
    if not match:
        return None
    block = match.group(1)
    enabled = re.search(r"(?m)^enabled\s*=\s*(true|false)\b", block, re.I)
    if not enabled:
        return None
    return enabled.group(1).lower() == "true"


def subagents_enabled() -> bool:
    env = os.environ.get("GROK_SUBAGENTS", "").strip().lower()
    if env in ("1", "true", "yes", "on"):
        return True
    if env in ("0", "false", "no", "off"):
        return False

    cfg = Path.home() / ".grok" / "config.toml"
    if cfg.is_file():
        try:
            parsed = _parse_toml_bool_enabled(cfg.read_text(encoding="utf-8", errors="replace"))
        except OSError:
            parsed = None
        if parsed is not None:
            return parsed

    # Grok Build default: subagents master switch off (GROK_SUBAGENTS default 0).
    return False


def main() -> int:
    enabled = subagents_enabled()
    event = os.environ.get("GROK_HOOK_EVENT") or os.environ.get("CURSOR_HOOK_EVENT") or ""
    if enabled:
        sys.stdout.write("{}\n")
        return 0

    # Always visible in terminal / TUI logs
    print(NOTICE, file=sys.stderr, flush=True)

    # Injection shapes used by Grok / Claude / Cursor-compatible hosts (ignored if unsupported)
    payload = {
        "systemMessage": NOTICE.strip(),
        "additionalContext": NOTICE.strip(),
        "userMessage": NOTICE.strip(),
        "hookSpecificOutput": {
            "hookEventName": event or "SessionStart",
            "additionalContext": NOTICE.strip(),
            "systemMessage": NOTICE.strip(),
        },
    }
    sys.stdout.write(json.dumps(payload, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
