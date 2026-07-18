#!/usr/bin/env python3
"""Deterministic optional specialist selection for Grok Fusion Phase D."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Iterable

PACK_SUGGESTIONS: dict[str, list[str]] = {
    "simple-code-edit": ["test_strategist", "dx_tooling"],
    "debugging": ["test_strategist", "concurrency", "observability"],
    "research": ["docs_accuracy"],
    "product-mvp": ["ux_accessibility", "privacy_compliance", "release_rollback"],
    "architecture": ["api_compat", "data_model_integrity", "observability"],
    "refactoring-migration": ["data_migration", "api_compat", "test_strategist"],
    "professional-planning": ["test_strategist", "api_compat", "data_migration"],
    "writing-explanation": ["docs_accuracy"],
    "visual-ui": ["visual_design_critique", "ux_accessibility", "frontend_state"],
    "appsec-review": ["authz_tenancy", "threat_abuse", "privacy_compliance"],
}

SEVERITY_RANK = {
    "authz_tenancy": 100,
    "data_migration": 100,
    "api_compat": 100,
    "threat_abuse": 100,
    "privacy_compliance": 100,
    "release_rollback": 80,
    "concurrency": 70,
    "visual_design_critique": 25,
}

PATH_TRIGGERS: list[tuple[str, str]] = [
    ("api_compat", "api/"),
    ("api_compat", "openapi"),
    ("data_migration", "migration"),
    ("data_migration", "prisma"),
    ("data_migration", "alembic"),
    ("dependency_supply_chain", "package.json"),
    ("dependency_supply_chain", "cargo.toml"),
    ("dependency_supply_chain", "go.mod"),
    ("frontend_state", ".tsx"),
    ("frontend_state", ".vue"),
    ("visual_design_critique", ".css"),
    ("visual_design_critique", ".scss"),
    ("visual_design_critique", ".html"),
    ("visual_design_critique", ".tsx"),
    ("visual_design_critique", ".jsx"),
    ("visual_design_critique", "/landing"),
    ("visual_design_critique", "landing."),
    ("dx_tooling", "scripts/"),
    ("dx_tooling", ".github/workflows"),
    ("docs_accuracy", "readme"),
    ("docs_accuracy", "docs/"),
    ("i18n_localization", "locales/"),
    ("cache_consistency", "redis"),
    ("search_indexing", "search"),
    ("mobile_offline", "offline"),
    ("authz_tenancy", "auth/"),
    ("authz_tenancy", "oauth"),
    ("authz_tenancy", "rbac"),
    ("authz_tenancy", "permission"),
    ("authz_tenancy", "/middleware"),
]

# Values are list[str]; select() iterates each role for a matched gate.
GATE_ROLES: dict[str, list[str]] = {
    "G1": ["data_migration"],
    "G2": ["api_compat", "authz_tenancy"],
    "G3": ["release_rollback"],
}


def rank(role: str) -> int:
    return SEVERITY_RANK.get(role, 10)


def select(
    pack: str,
    gates: Iterable[str],
    paths: Iterable[str],
    preferred: Iterable[str],
    disabled: Iterable[str],
    max_optional: int,
    scenario: str,
) -> dict:
    triggers: list[str] = []
    ordered: list[str] = []
    security_gates = {g.strip().upper() for g in gates if g.strip().upper() in GATE_ROLES}

    def add(role: str, trigger: str) -> None:
        if role in disabled:
            return
        if trigger not in triggers:
            triggers.append(trigger)
        if role not in ordered:
            ordered.append(role)

    for gate in gates:
        gate = gate.strip().upper()
        if gate in GATE_ROLES:
            for role in GATE_ROLES[gate]:
                add(role, gate)

    # Debugging pack: pin preferred debug specialists ahead of generic severity
    # when no G1/G2/security-class gate is forcing higher-priority roles alone.
    debug_preferred = ["test_strategist", "concurrency", "observability"]
    if pack == "debugging" and not (security_gates & {"G1", "G2"}):
        for role in debug_preferred:
            add(role, "pack:debugging:pinned")
        for role in preferred:
            add(role, f"preferred:{role}")
    else:
        for role in PACK_SUGGESTIONS.get(pack, []):
            add(role, f"pack:{pack}")
        for role in preferred:
            if role not in disabled and role not in ordered:
                ordered.append(role)
                triggers.append(f"preferred:{role}")

    if pack != "debugging" or (security_gates & {"G1", "G2"}):
        path_blob = " ".join(p.lower() for p in paths)
        for role, needle in PATH_TRIGGERS:
            if needle in path_blob:
                add(role, f"path:{needle}")
        if pack == "debugging":
            for role in debug_preferred:
                add(role, "pack:debugging")
    else:
        path_blob = " ".join(p.lower() for p in paths)
        for role, needle in PATH_TRIGGERS:
            if needle in path_blob:
                add(role, f"path:{needle}")

    if pack == "debugging" and not (security_gates & {"G1", "G2"}):
        # Keep pin order: debug preferred first, then others by severity.
        pinned = [r for r in debug_preferred if r in ordered]
        rest = [r for r in ordered if r not in pinned]
        indexed = list(enumerate(rest))
        indexed.sort(key=lambda item: (-rank(item[1]), item[0]))
        ordered = pinned + [role for _, role in indexed]
    else:
        indexed = list(enumerate(ordered))
        indexed.sort(key=lambda item: (-rank(item[1]), item[0]))
        ordered = [role for _, role in indexed]

    selected_roles = ordered[: max(0, max_optional)]
    dropped = ordered[max(0, max_optional) :]

    return {
        "triggers_matched": triggers,
        "selected": [{"role": r, "scenario": scenario} for r in selected_roles],
        "dropped_by_cap": dropped,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pack", default="")
    parser.add_argument("--gates", default="", help="Comma-separated G1,G2,G3")
    parser.add_argument("--paths", default="", help="Comma-separated paths")
    parser.add_argument("--preferred", default="", help="Comma-separated role ids")
    parser.add_argument("--disabled", default="", help="Comma-separated role ids")
    parser.add_argument("--max", type=int, default=3)
    parser.add_argument("--scenario", default="recheck", choices=("recheck", "improve", "advise"))
    args = parser.parse_args(argv)

    result = select(
        pack=args.pack.strip(),
        gates=[g for g in args.gates.split(",") if g.strip()],
        paths=[p for p in args.paths.split(",") if p.strip()],
        preferred=[p for p in args.preferred.split(",") if p.strip()],
        disabled=[d for d in args.disabled.split(",") if d.strip()],
        max_optional=args.max,
        scenario=args.scenario,
    )
    json.dump(result, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
