#!/usr/bin/env python3
"""Deterministic structural validator for the grok-fusion Cursor plugin."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "grok-fusion"
AGENTS_DIR = ROOT / "agents"
EVALS_DIR = ROOT / "evals"
PLUGIN_JSON = ROOT / ".cursor-plugin" / "plugin.json"

CORE_FILES = [
    ".cursor-plugin/plugin.json",
    "agents/gf-worker.md",
    "agents/gf-reviewer.md",
    "agents/gf-auditor.md",
    "rules/grok-fusion-auto.mdc",
    "skills/grok-fusion/SKILL.md",
    "skills/grok-fusion/grok-harness.md",
    "skills/grok-fusion/runtime-contract.md",
    "skills/grok-fusion/freshness-contract.md",
    "skills/grok-fusion/planning-contract.md",
    "skills/grok-fusion/adaptive-router.md",
    "skills/grok-fusion/task-packs.md",
    "skills/grok-fusion/framing-and-evidence.md",
    "skills/grok-fusion/candidate-lenses.md",
    "skills/grok-fusion/candidate-card.md",
    "skills/grok-fusion/selector.md",
    "skills/grok-fusion/falsify-and-revise.md",
    "skills/grok-fusion/minority-sentinel.md",
    "skills/grok-fusion/architecture-playbook.md",
    "skills/grok-fusion/verification-gate.md",
    "skills/grok-fusion/multi-pass-verification.md",
    "skills/grok-fusion/specialist-roster.md",
    "skills/grok-fusion/project-config.md",
    "skills/grok-fusion/orchestration-checklist.md",
    "skills/grok-fusion/specialist-evidence-packs.md",
    "skills/grok-fusion/debugging-playbook.md",
    "skills/grok-fusion/implementation-track.md",
    "skills/grok-fusion/long-horizon-contract.md",
    "skills/grok-fusion/discovery-track.md",
    "skills/grok-fusion/mvp-playbook.md",
    "skills/grok-fusion/epic-track.md",
    "skills/grok-fusion/recovery-track.md",
    "skills/grok-fusion/examples.md",
    "scripts/validate_plugin.py",
    "scripts/select_optional_specialists.py",
    "evals/README.md",
    "evals/cases.yaml",
    "evals/rubric.yaml",
    "evals/negative-criteria.yaml",
    "evals/runbook.md",
    "evals/adaptive-cases.json",
    "evals/mvp-cases.json",
    "evals/smoke-runbook.md",
    "evals/fixtures/valid-run/run.json",
    "evals/fixtures/valid-run/discovery.json",
    "evals/fixtures/valid-run/dag.json",
    "evals/fixtures/valid-run/acceptance.json",
    "evals/fixtures/valid-run/spine.json",
    "evals/fixtures/valid-run/prfaq.json",
    "evals/fixtures/valid-run/lessons.json",
    "evals/fixtures/valid-run/events.jsonl",
    "evals/fixtures/valid-run/multi_pass/w0-discovery.json",
    "evals/fixtures/invalid-run/run.json",
    "evals/fixtures/invalid-run/discovery.json",
    "evals/fixtures/invalid-run/dag.json",
    "evals/fixtures/invalid-run/acceptance.json",
    "evals/fixtures/invalid-run/events.jsonl",
    ".github/workflows/validate.yml",
    "README.md",
    "LICENSE",
]

FORBIDDEN_SUBSTRINGS = [
    "TO" + "DO",
    "TB" + "D",
    "<" + "owner>",
    "show your chain " + "of thought",
    "is_background: " + "true",
]

IRON_RULE_SNIPPETS = [
    "Run the full eligible pipeline or state that Fusion did not run.",
    "Every substantive claim has evidence or an uncertainty label.",
    "Select one coherent spine; never average incompatible designs.",
    "Preserve evidence-backed dissent and minority warnings.",
    "Do not mutate the workspace unless implementation was explicitly requested.",
]

PHASE_MARKERS = [f"P{i}" for i in range(0, 8)]

REQUIRED_PLUGIN_FIELDS = {
    "name": "grok-fusion",
    "version": "0.2.0",
    "license": "MIT",
}


class Failure(Exception):
    pass


def fail(message: str) -> None:
    raise Failure(message)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        fail("missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        fail("unterminated YAML frontmatter")
    block = text[4:end]
    data: dict[str, str] = {}
    for raw_line in block.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            fail(f"invalid frontmatter line: {raw_line}")
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def check_core_files() -> None:
    for rel in CORE_FILES:
        path = ROOT / rel
        if not path.is_file():
            fail(f"missing core file: {rel}")
    commands = list((ROOT / "commands").glob("grok-fusion.*")) if (ROOT / "commands").exists() else []
    if commands:
        fail("duplicate skill/command name: commands/grok-fusion.* must not exist")


def check_plugin_json() -> None:
    try:
        data = json.loads(read_text(PLUGIN_JSON))
    except json.JSONDecodeError as exc:
        fail(f"invalid plugin.json: {exc}")
    for key, expected in REQUIRED_PLUGIN_FIELDS.items():
        if data.get(key) != expected:
            fail(f"plugin.json field {key} must be {expected!r}")
    if data.get("description") in (None, ""):
        fail("plugin.json missing description")
    author = data.get("author")
    if not isinstance(author, dict) or author.get("name") != "GoodGameIsGood":
        fail("plugin.json author.name must be 'GoodGameIsGood'")
    keywords = data.get("keywords")
    if not isinstance(keywords, list) or not keywords:
        fail("plugin.json keywords must be a non-empty list")
    allowed = {
        "name",
        "version",
        "description",
        "author",
        "license",
        "keywords",
        "repository",
        "homepage",
        "skills",
        "agents",
        "rules",
    }
    unexpected = set(data) - allowed
    if unexpected:
        fail(f"plugin.json has unexpected fields: {sorted(unexpected)}")
    for key, expected in (("skills", "./skills/"), ("agents", "./agents/"), ("rules", "./rules/")):
        if data.get(key) != expected:
            fail(f"plugin.json {key} must be {expected!r}")


def check_skill_frontmatter() -> None:
    text = read_text(SKILL_DIR / "SKILL.md")
    data = parse_frontmatter(text)
    if data.get("name") != "grok-fusion":
        fail("SKILL.md name must be grok-fusion")
    if "description" not in data or not data["description"]:
        fail("SKILL.md missing description")
    if data.get("disable-model-invocation") == "true":
        fail("SKILL.md must allow auto-invocation; do not set disable-model-invocation: true")
    line_count = len(text.splitlines())
    if line_count > 300:
        fail(f"SKILL.md has {line_count} lines; must be <= 300")
    for marker in PHASE_MARKERS:
        if marker not in text:
            fail(f"SKILL.md missing phase marker {marker}")
    for token in (
        "Quick",
        "Standard",
        "Heavy",
        "MVP",
        "adaptive-router.md",
        "task-packs.md",
        "Task tool",
        "RunEnvelope",
        "falsify-and-revise.md",
    ):
        if token not in text:
            fail(f"SKILL.md missing adaptive token {token}")


def check_schema_markers() -> None:
    framing = read_text(SKILL_DIR / "framing-and-evidence.md")
    for marker in ("framer: literal", "framer: skeptical", "framer: systems", "Canonical brief schema"):
        if marker not in framing:
            fail(f"framing-and-evidence.md missing schema marker {marker}")
    selector = read_text(SKILL_DIR / "selector.md")
    for marker in ("pair_id:", "order: A_then_B | B_then_A", "spine_id:"):
        if marker not in selector:
            fail(f"selector.md missing schema marker {marker}")
    falsify = read_text(SKILL_DIR / "falsify-and-revise.md")
    for marker in ("must_fix:", "revised_spine:", "fatal_flaw:"):
        if marker not in falsify:
            fail(f"falsify-and-revise.md missing schema marker {marker}")
    runtime = read_text(SKILL_DIR / "runtime-contract.md")
    for marker in ("Task tool", "schema_version", "Model and tool probe"):
        if marker not in runtime:
            fail(f"runtime-contract.md missing marker {marker}")
    if "spine.json" not in read_text(SKILL_DIR / "long-horizon-contract.md"):
        fail("long-horizon-contract.md missing spine.json")
    if "refactoring-migration" not in read_text(SKILL_DIR / "task-packs.md"):
        fail("task-packs.md missing refactoring-migration")
    if "Symbol grounding" not in read_text(SKILL_DIR / "grok-harness.md"):
        fail("grok-harness.md missing Symbol grounding")
    if "Epic integration check" not in read_text(SKILL_DIR / "epic-track.md"):
        fail("epic-track.md missing Epic integration check")
    if "probe_nonce" not in runtime:
        fail("runtime-contract.md missing probe_nonce")
    if "evidence_id" not in framing:
        fail("framing-and-evidence.md missing evidence_id")
    freshness = read_text(SKILL_DIR / "freshness-contract.md")
    if "retrieved_at" not in freshness:
        fail("freshness-contract.md missing retrieved_at")
    if "Budget priority" not in freshness:
        fail("freshness-contract.md missing Budget priority")
    if "Devil's advocate pass" not in read_text(SKILL_DIR / "verification-gate.md"):
        fail("verification-gate.md missing Devil's advocate pass")
    multi_pass = read_text(SKILL_DIR / "multi-pass-verification.md")
    for marker in (
        "Phase A — Per-step recheck",
        "Phase B — Double error hunt",
        "Phase C — Completion quality",
        "Phase D — Specialist panel",
        "consensus: PASS",
        "max_fix_cycles",
        "Fail-closed and resume matrix",
        "optional_panel",
        "scenario: recheck|improve|advise",
        "Verify hard gate",
        "verification_runs",
    ):
        if marker not in multi_pass:
            fail(f"multi-pass-verification.md missing {marker}")
    project_config = read_text(SKILL_DIR / "project-config.md")
    for marker in (
        "Read project config before tier",
        "quality_profile",
        "balanced",
    ):
        if marker not in project_config:
            fail(f"project-config.md missing {marker}")
    if "Read project config before tier" not in read_text(SKILL_DIR / "adaptive-router.md"):
        fail("adaptive-router.md missing Read project config before tier")
    debug_playbook = read_text(SKILL_DIR / "debugging-playbook.md")
    for marker in ("Repair Card", "must_not_break", "characterization", "Iron rule"):
        if marker not in debug_playbook:
            fail(f"debugging-playbook.md missing {marker}")
    if "debugging-playbook.md" not in read_text(SKILL_DIR / "task-packs.md"):
        fail("task-packs.md missing debugging-playbook.md link")
    if "require_repair_card" not in read_text(SKILL_DIR / "project-config.md"):
        fail("project-config.md missing require_repair_card")
    checklist = read_text(SKILL_DIR / "orchestration-checklist.md")
    if "P0" not in checklist or "multi-pass-verification.md" not in checklist:
        fail("orchestration-checklist.md missing P0→done path")
    if "debugging-playbook.md" not in checklist:
        fail("orchestration-checklist.md missing debugging-playbook.md")
    evidence_packs = read_text(SKILL_DIR / "specialist-evidence-packs.md")
    for role_id in (
        "api_compat",
        "data_migration",
        "performance",
        "ux_accessibility",
        "test_strategist",
        "dependency_supply_chain",
        "concurrency",
        "observability",
        "authz_tenancy",
        "privacy_compliance",
        "network_resilience",
        "cache_consistency",
        "frontend_state",
        "dx_tooling",
        "docs_accuracy",
        "i18n_localization",
        "cost_finops",
        "release_rollback",
        "threat_abuse",
        "data_model_integrity",
        "search_indexing",
        "mobile_offline",
    ):
        if f"## {role_id}" not in evidence_packs:
            fail(f"specialist-evidence-packs.md missing section {role_id}")
    roster = read_text(SKILL_DIR / "specialist-roster.md")
    for marker in ("Scenario templates", "Selection algorithm", "max 3"):
        if marker not in roster:
            fail(f"specialist-roster.md missing {marker}")
    for role_id in (
        "api_compat",
        "data_migration",
        "performance",
        "ux_accessibility",
        "test_strategist",
        "dependency_supply_chain",
        "concurrency",
        "observability",
        "authz_tenancy",
        "privacy_compliance",
        "network_resilience",
        "cache_consistency",
        "frontend_state",
        "dx_tooling",
        "docs_accuracy",
        "i18n_localization",
        "cost_finops",
        "release_rollback",
        "threat_abuse",
        "data_model_integrity",
        "search_indexing",
        "mobile_offline",
    ):
        if f"`{role_id}`" not in roster:
            fail(f"specialist-roster.md missing role id {role_id}")
    if "Rebuttal round" not in selector:
        fail("selector.md missing Rebuttal round")
    mvp = read_text(SKILL_DIR / "mvp-playbook.md")
    for marker in ("PR/FAQ", "EARS", "Walking skeleton"):
        if marker not in mvp:
            fail(f"mvp-playbook.md missing {marker}")
    long_horizon = read_text(SKILL_DIR / "long-horizon-contract.md")
    if "prfaq.json" not in long_horizon:
        fail("long-horizon-contract.md missing prfaq.json")
    if "lessons.json" not in long_horizon:
        fail("long-horizon-contract.md missing lessons.json")
    if "max_fix_cycles" not in long_horizon:
        fail("long-horizon-contract.md missing max_fix_cycles")
    if "per-wave max edit cycles: 3" in long_horizon:
        fail("long-horizon-contract.md still has obsolete edit-cycle budget of 3")
    planning = read_text(SKILL_DIR / "planning-contract.md")
    if "Plan quality gate" not in planning:
        fail("planning-contract.md missing Plan quality gate")
    if "ears_criteria" not in planning:
        fail("planning-contract.md missing ears_criteria")
    if "multi_pass_consensus" not in planning:
        fail("planning-contract.md missing multi_pass_consensus")
    if "professional-planning" not in read_text(SKILL_DIR / "task-packs.md"):
        fail("task-packs.md missing professional-planning")
    impl = read_text(SKILL_DIR / "implementation-track.md")
    if "multi-pass-verification.md" not in impl:
        fail("implementation-track.md missing multi-pass-verification.md")
    if "Invoke `gf-reviewer` twice" in impl:
        fail("implementation-track.md still uses legacy 2+1 review gate")


def check_auto_rule() -> None:
    path = ROOT / "rules" / "grok-fusion-auto.mdc"
    text = read_text(path)
    data = parse_frontmatter(text)
    if data.get("alwaysApply") != "true":
        fail("rules/grok-fusion-auto.mdc must set alwaysApply: true")
    if "description" not in data or not data["description"]:
        fail("rules/grok-fusion-auto.mdc missing description")
    if "Fusion tier:" not in text:
        fail("rules/grok-fusion-auto.mdc missing Fusion tier footer requirement")


def check_agents() -> None:
    for name in ("gf-worker.md", "gf-reviewer.md", "gf-auditor.md"):
        text = read_text(AGENTS_DIR / name)
        data = parse_frontmatter(text)
        expected_name = name.removesuffix(".md")
        if data.get("name") != expected_name:
            fail(f"{name} name must be {expected_name}")
        if data.get("model") != "inherit":
            fail(f"{name} must set model: inherit")
        if data.get("readonly") != "true":
            fail(f"{name} must set readonly: true")
        if data.get("is_background") != "false":
            fail(f"{name} must set is_background: false")
        if "description" not in data or not data["description"]:
            fail(f"{name} missing description")
    reviewer = read_text(AGENTS_DIR / "gf-reviewer.md")
    for marker in (
        "specialist_panel",
        "scenario",
        "specialist-roster.md",
        "specialist-evidence-packs.md",
        "Repair Card",
    ):
        if marker not in reviewer:
            fail(f"gf-reviewer.md missing {marker}")
    auditor = read_text(AGENTS_DIR / "gf-auditor.md")
    if "verify_evidence" not in auditor:
        fail("gf-auditor.md missing verify_evidence")
    for marker in ("repair_card_followed", "characterization_green", "must_not_break_checked"):
        if marker not in auditor:
            fail(f"gf-auditor.md missing {marker}")


def check_forbidden_strings() -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if ".git" in path.parts or "__pycache__" in path.parts:
            continue
        if path.suffix in {".pyc", ".pyo"}:
            continue
        try:
            text = read_text(path)
        except UnicodeDecodeError:
            continue
        for bad in FORBIDDEN_SUBSTRINGS:
            if bad in text:
                fail(f"forbidden substring {bad!r} found in {path.relative_to(ROOT)}")


def check_markdown_links() -> None:
    link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for path in SKILL_DIR.glob("*.md"):
        text = read_text(path)
        for target in link_re.findall(text):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            clean = target.split("#", 1)[0]
            if not clean:
                continue
            resolved = (path.parent / clean).resolve()
            if not resolved.exists():
                fail(f"broken link in {path.name}: {target}")


def check_iron_rules() -> None:
    text = read_text(SKILL_DIR / "grok-harness.md")
    for snippet in IRON_RULE_SNIPPETS:
        if snippet not in text:
            fail(f"grok-harness.md missing Iron Rule: {snippet}")
    skill = read_text(SKILL_DIR / "SKILL.md")
    for snippet in IRON_RULE_SNIPPETS:
        if snippet not in skill:
            fail(f"SKILL.md missing Iron Rule: {snippet}")


def parse_simple_yaml_cases(text: str) -> list[dict[str, str]]:
    cases: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if line.startswith("- "):
            if current:
                cases.append(current)
            current = {}
            rest = line[2:]
            if ":" in rest:
                key, value = rest.split(":", 1)
                current[key.strip()] = value.strip().strip('"').strip("'")
            continue
        if current is None:
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            current[key.strip()] = value.strip().strip('"').strip("'")
    if current:
        cases.append(current)
    return cases


def check_evals() -> None:
    cases_path = EVALS_DIR / "cases.yaml"
    cases = parse_simple_yaml_cases(read_text(cases_path))
    if len(cases) != 30:
        fail(f"evals/cases.yaml must contain exactly 30 cases; found {len(cases)}")
    ids = [c.get("id") for c in cases]
    if any(not i for i in ids):
        fail("evals/cases.yaml has a case without id")
    if len(set(ids)) != 30:
        fail("evals/cases.yaml case ids must be unique")
    categories = [c.get("category") for c in cases]
    expected = {
        "brownfield-architecture": 15,
        "greenfield-design": 5,
        "hard-debugging": 5,
        "research-tradeoffs": 5,
    }
    for category, count in expected.items():
        actual = categories.count(category)
        if actual != count:
            fail(f"category {category} must have {count} cases; found {actual}")
    for name in (
        "rubric.yaml",
        "negative-criteria.yaml",
        "runbook.md",
        "README.md",
        "adaptive-cases.json",
        "mvp-cases.json",
        "smoke-runbook.md",
    ):
        if not (EVALS_DIR / name).is_file():
            fail(f"missing evals/{name}")
    adaptive = json.loads(read_text(EVALS_DIR / "adaptive-cases.json"))
    mvp = json.loads(read_text(EVALS_DIR / "mvp-cases.json"))
    if not isinstance(adaptive, list) or len(adaptive) < 4:
        fail("evals/adaptive-cases.json must be a list with at least 4 cases")
    if not isinstance(mvp, list) or len(mvp) < 4:
        fail("evals/mvp-cases.json must be a list with at least 4 cases")
    for path in (
        SKILL_DIR / "long-horizon-contract.md",
        SKILL_DIR / "discovery-track.md",
        SKILL_DIR / "epic-track.md",
        SKILL_DIR / "mvp-playbook.md",
        SKILL_DIR / "recovery-track.md",
    ):
        if not path.is_file():
            fail(f"long-horizon support requires {path.name}")


def load_json(path: Path) -> object:
    try:
        return json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path}: {exc}")
    raise AssertionError("unreachable")


def _wave_map(dag: dict) -> dict[str, dict]:
    waves: dict[str, dict] = {}
    for epic in dag.get("epics", []):
        if not isinstance(epic, dict):
            fail("dag.json epics must be objects")
        for wave in epic.get("waves", []):
            if not isinstance(wave, dict) or not wave.get("id"):
                fail("each wave must be an object with id")
            wid = wave["id"]
            if wid in waves:
                fail(f"duplicate wave id: {wid}")
            waves[wid] = wave
    return waves


def _assert_acyclic(waves: dict[str, dict]) -> None:
    visiting: set[str] = set()
    visited: set[str] = set()

    def dfs(node: str) -> None:
        if node in visited:
            return
        if node in visiting:
            fail(f"dag.json contains a cycle at {node}")
        visiting.add(node)
        for dep in waves[node].get("depends_on", []):
            if dep not in waves:
                fail(f"wave {node} depends on missing wave {dep}")
            dfs(dep)
        visiting.remove(node)
        visited.add(node)

    for wid in waves:
        dfs(wid)


def _ownership_overlap(waves: dict[str, dict]) -> None:
    active_prefixes: list[tuple[str, str]] = []
    for wid, wave in waves.items():
        if wave.get("status") != "active":
            continue
        for path in wave.get("owns_paths", []):
            for other_id, other_path in active_prefixes:
                if path.startswith(other_path) or other_path.startswith(path):
                    fail(
                        f"overlapping owns_paths between {other_id}:{other_path} and {wid}:{path}"
                    )
            active_prefixes.append((wid, path))


def validate_state_dir(state_dir: Path) -> None:
    if not state_dir.is_dir():
        fail(f"state directory missing: {state_dir}")
    required = (
        "run.json",
        "spine.json",
        "prfaq.json",
        "lessons.json",
        "discovery.json",
        "dag.json",
        "acceptance.json",
        "events.jsonl",
    )
    for name in required:
        if not (state_dir / name).is_file():
            fail(f"state missing {name}")
    run = load_json(state_dir / "run.json")
    spine = load_json(state_dir / "spine.json")
    prfaq = load_json(state_dir / "prfaq.json")
    lessons = load_json(state_dir / "lessons.json")
    discovery = load_json(state_dir / "discovery.json")
    dag = load_json(state_dir / "dag.json")
    acceptance = load_json(state_dir / "acceptance.json")
    if not isinstance(run, dict) or run.get("schema_version") != 1:
        fail("run.json schema_version must be 1")
    if run.get("tier") != "MVP":
        fail("run.json tier must be MVP")
    if not run.get("run_id"):
        fail("run.json missing run_id")
    if not isinstance(spine, dict) or spine.get("schema_version") != 1:
        fail("spine.json schema_version must be 1")
    if not spine.get("spine_id"):
        fail("spine.json missing spine_id")
    if spine.get("spine_id") != run.get("spine_id"):
        fail("spine.json spine_id must equal run.json spine_id")
    if not isinstance(prfaq, dict) or prfaq.get("schema_version") != 1:
        fail("prfaq.json schema_version must be 1")
    if not prfaq.get("press_release"):
        fail("prfaq.json missing press_release")
    if not isinstance(lessons, dict) or lessons.get("schema_version") != 1:
        fail("lessons.json schema_version must be 1")
    if not isinstance(lessons.get("lessons"), list):
        fail("lessons.json lessons must be a list")
    if not isinstance(discovery, dict) or discovery.get("schema_version") != 1:
        fail("discovery.json schema_version must be 1")
    if not isinstance(dag, dict) or dag.get("schema_version") != 1:
        fail("dag.json schema_version must be 1")
    if not isinstance(acceptance, dict) or acceptance.get("schema_version") != 1:
        fail("acceptance.json schema_version must be 1")
    waves = _wave_map(dag)
    _assert_acyclic(waves)
    _ownership_overlap(waves)
    allowed_status = {"pending", "active", "blocked", "complete"}
    allowed_gates = {"G0", "G1", "G2", "G3", "G4"}
    clause_ids: set[str] = set()
    for clause in acceptance.get("product_clauses", []):
        if clause.get("id"):
            clause_ids.add(clause["id"])
        if clause.get("status") not in {"PASS", "FAIL", "UNVERIFIED"}:
            fail("acceptance product clause has invalid status")
    for clause in acceptance.get("epic_clauses", []):
        if clause.get("id"):
            clause_ids.add(clause["id"])
    wave_clauses = acceptance.get("wave_clauses", {})
    if isinstance(wave_clauses, dict):
        for clauses in wave_clauses.values():
            if not isinstance(clauses, list):
                continue
            for clause in clauses:
                if isinstance(clause, dict) and clause.get("id"):
                    clause_ids.add(clause["id"])
    for wid, wave in waves.items():
        status = wave.get("status")
        if status not in allowed_status:
            fail(f"wave {wid} has invalid status {status!r}")
        gates = wave.get("gates_required", [])
        if not isinstance(gates, list):
            fail(f"wave {wid} gates_required must be a list")
        for gate in gates:
            if gate not in allowed_gates:
                fail(f"wave {wid} has invalid gate {gate!r}")
        for cid in wave.get("acceptance_clause_ids", []):
            if cid not in clause_ids:
                fail(f"wave {wid} references missing acceptance clause {cid}")
    active = run.get("active_wave")
    if active and active not in waves:
        fail(f"active_wave {active} missing from dag.json")
    summaries_dir = state_dir / "summaries"
    if summaries_dir.is_dir():
        for path in sorted(summaries_dir.glob("*.json")):
            summary = load_json(path)
            if not isinstance(summary, dict) or summary.get("schema_version") != 1:
                fail(f"{path.name} schema_version must be 1")
            if not summary.get("wave_id"):
                fail(f"{path.name} missing wave_id")
    events = read_text(state_dir / "events.jsonl").strip()
    if events:
        for line_no, line in enumerate(events.splitlines(), start=1):
            try:
                json.loads(line)
            except json.JSONDecodeError as exc:
                fail(f"events.jsonl line {line_no} invalid JSON: {exc}")
    multi_pass_dir = state_dir / "multi_pass"
    if multi_pass_dir.is_dir():
        allowed_consensus = {"PASS", "FAIL", "IN_PROGRESS"}
        allowed_mp_status = {"in_progress", "blocked", "complete"}
        for path in sorted(multi_pass_dir.glob("*.json")):
            mp = load_json(path)
            if not isinstance(mp, dict) or mp.get("schema_version") != 1:
                fail(f"{path.name} schema_version must be 1")
            if not mp.get("id"):
                fail(f"{path.name} missing id")
            if mp.get("consensus") not in allowed_consensus:
                fail(f"{path.name} has invalid consensus")
            if mp.get("status") not in allowed_mp_status:
                fail(f"{path.name} has invalid status")
            if not isinstance(mp.get("merged_blockers"), list):
                fail(f"{path.name} merged_blockers must be a list")
            if not isinstance(mp.get("panel"), list):
                fail(f"{path.name} panel must be a list")
            if "verification_runs" in mp:
                runs = mp["verification_runs"]
                if not isinstance(runs, list):
                    fail(f"{path.name} verification_runs must be a list")
                if mp.get("status") == "complete" and mp.get("consensus") == "PASS":
                    ok = False
                    for run in runs:
                        if isinstance(run, dict) and run.get("exit_code") == 0:
                            ok = True
                            break
                    if not ok:
                        fail(f"{path.name} complete PASS requires a verification_runs entry with exit_code 0")
            if "optional_selection" in mp:
                sel = mp["optional_selection"]
                if not isinstance(sel, dict):
                    fail(f"{path.name} optional_selection must be an object")
                for key in ("triggers_matched", "selected", "dropped_by_cap"):
                    if key not in sel or not isinstance(sel[key], list):
                        fail(f"{path.name} optional_selection missing list {key}")
                if "G1" in sel.get("triggers_matched", []):
                    roles = [
                        e.get("role")
                        for e in sel.get("selected", [])
                        if isinstance(e, dict)
                    ]
                    if "data_migration" not in roles:
                        fail(f"{path.name} G1 trigger requires data_migration in optional_selection.selected")
            if "optional_panel" in mp:
                optional = mp["optional_panel"]
                if not isinstance(optional, list):
                    fail(f"{path.name} optional_panel must be a list")
                known_optional = {
                    "api_compat",
                    "data_migration",
                    "performance",
                    "ux_accessibility",
                    "test_strategist",
                    "dependency_supply_chain",
                    "concurrency",
                    "observability",
                    "authz_tenancy",
                    "privacy_compliance",
                    "network_resilience",
                    "cache_consistency",
                    "frontend_state",
                    "dx_tooling",
                    "docs_accuracy",
                    "i18n_localization",
                    "cost_finops",
                    "release_rollback",
                    "threat_abuse",
                    "data_model_integrity",
                    "search_indexing",
                    "mobile_offline",
                }
                allowed_scenarios = {"recheck", "improve", "advise"}
                allowed_verdicts = {"SHIP", "REWORK", "BLOCK"}
                if mp.get("status") == "complete" and len(optional) > 3:
                    fail(f"{path.name} complete optional_panel must have ≤3 entries")
                for idx, entry in enumerate(optional):
                    if not isinstance(entry, dict):
                        fail(f"{path.name} optional_panel[{idx}] must be an object")
                    role = entry.get("role")
                    if role not in known_optional:
                        fail(f"{path.name} optional_panel[{idx}] unknown role {role!r}")
                    if entry.get("scenario") not in allowed_scenarios:
                        fail(f"{path.name} optional_panel[{idx}] invalid scenario")
                    if entry.get("verdict") not in allowed_verdicts:
                        fail(f"{path.name} optional_panel[{idx}] invalid verdict")
            if mp.get("status") == "complete" and mp.get("consensus") != "PASS":
                fail(f"{path.name} complete requires consensus PASS")
            if mp.get("consensus") == "PASS" and mp.get("merged_blockers"):
                fail(f"{path.name} PASS with open merged_blockers")


def check_readme_claims() -> None:
    readme = read_text(ROOT / "README.md")
    banned_claims = [
        "beats Fable",
        "beats solo Fable",
        "surpasses Fable",
        "proven to exceed Fable",
    ]
    for claim in banned_claims:
        if claim.lower() in readme.lower():
            if "designed to compete" in readme.lower():
                continue
            evidence = EVALS_DIR / "benchmark-results.json"
            if not evidence.is_file():
                fail("README claims Fable superiority without recorded benchmark evidence")
    if "universal" in readme.lower() and "until" not in readme.lower():
        if not (EVALS_DIR / "benchmark-results.json").is_file():
            # Allow discussing universality as a goal when paired with honest caveats.
            if "smoke-runbook" not in readme.lower() and "adaptive" not in readme.lower():
                fail("README claims universal capability without evaluation evidence")


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    try:
        if args and args[0] == "--state":
            if len(args) != 2:
                fail("--state requires a run directory path")
            validate_state_dir(Path(args[1]))
            print("OK: grok-fusion state directory is valid")
            return 0
        check_core_files()
        check_plugin_json()
        check_skill_frontmatter()
        check_auto_rule()
        check_schema_markers()
        check_agents()
        check_forbidden_strings()
        check_markdown_links()
        check_iron_rules()
        check_evals()
        check_readme_claims()
    except Failure as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print("OK: grok-fusion plugin structure and contracts are valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())