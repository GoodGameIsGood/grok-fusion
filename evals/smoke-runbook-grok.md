# Grok Build smoke runbook

Manual checks after installing the plugin on **Grok Build**. Do not claim `FULL` Grok↔Cursor parity until this runbook’s E1–E6 checks are recorded as `PASS` in `evals/results/smoke-grok-build-*.json` **and** SD8 Cursor baseline rules are satisfied (see TEMPLATE `cursor_baseline`).

Claim ladder: `PACKAGING` → `HOST_SMOKE_PASS` → `FULL` (see README). Packaging alone is not FULL.

**Lab note (2026-07-18):** On Grok Build CLI `0.2.103`, `grok plugin validate .` and `grok plugin install . --trust` succeed; `grok inspect` shows skills `grok-fusion` / `grok-design` / `grok-web-ui` / `grok-security` and agents `grok-fusion:gf-*`. Project `AGENTS.md` loads. Live council probe (E2/E3) still needs an authenticated session — record separately.

## Install (Option C)

```bash
# From a clone of this repo
grok plugin validate .
grok plugin install . --trust
# Or for one session without install:
grok --plugin-dir /path/to/grok-fusion
```

GitHub install (after push):

```bash
grok plugin install GoodGameIsGood/grok-fusion --trust
```

Enable subagents in `~/.grok/config.toml`:

```toml
[subagents]
enabled = true
```

Prefer a strong non-Fast Grok model. Confirm with:

```bash
grok plugin details grok-fusion
grok inspect
```

Expect: `grok plugin details` lists **hooks**. With subagents off, `python3 scripts/warn_subagents_disabled.py` prints the bilingual OFF banner to stderr.

## Mandatory scenarios (E1–E6)

1. Prefer plugin `rules/grok-fusion-auto.mdc` if the host loads it (prove in G1 row).
2. If rules do **not** auto-fire: keep repo `AGENTS.md` (this tree) or paste the Option C snippet from README into the **consumer** project. That is PARTIAL auto — not FULL auto-parity.
3. `grok inspect` showing `AGENTS.md` under Project Instructions counts as PARTIAL auto evidence for this repo only.

## Mandatory scenarios (E1–E6)

| ID | Scenario | Pass criteria |
|---|---|---|
| E1 | Install loads surfaces | `grok plugin validate` OK; `/grok-fusion` or skill available; agents resolve as `grok-fusion:gf-*` (record form); craft skills visible |
| E2 | Subagents off | With `[subagents] enabled=false`, Standard+ yields **Fusion did not run** — no Fusion footer over a solo answer |
| E3 | Standard+ probe | With subagents on, probe nonce/schema passes before council; fail closed on Task/spawn failure |
| E4 | Dual-tree | `python3 scripts/validate_plugin.py` PASS; intentional agents/rules/skills drift FAIL then restore |
| E5 | Claim ladder | Public/`FULL` language only after this artifact `status=PASS` + SD8; else `PARTIAL` / `HOST_SMOKE_PASS` / `PACKAGING` |
| E6 | Marketplace order | Marketplace draft submit-ready only after this smoke `PASS` + 40-char SHA pin (see `docs/marketplace-pr-draft.md`) |

Craft skills paths (Option A plugin / Option B copy): `skills/grok-fusion/`, `skills/grok-design/`, `skills/grok-web-ui/`, `skills/grok-security/`.

## Additional checks (record in `checks[]`)

| Check | Pass criteria |
|---|---|
| G1 auto-route | Rules auto-fire **or** Option C AGENTS proven; if neither, fail closed (no silent Fusion) |
| G2 probe authority | Operator-visible Grok model (+ pin if available); `model_family_self_report` weak only |
| G3 isolation | One tool-message batch per phase; no inline `gf-*` simulation |
| Agent ID form | Document bare vs `grok-fusion:gf-*` that worked |
| Fail closed non-Grok | Wrong/missing model authority → Fusion did not run |
| Footer | `Fusion tier:` matches actual work; on `max`, `MVP` |

## Cursor non-regression (SD8)

Fill TEMPLATE `cursor_baseline`:

- `status: PASS` + `artifact_path` to a dated Cursor smoke record per `evals/smoke-runbook.md`, **or**
- `status: live_pending` → max public claim `PARTIAL` (`FULL` forbidden), **or**
- `status: waived` only with explicit user waiver noted in `notes`

Cross-ref: [smoke-runbook.md](smoke-runbook.md) (Cursor). Structural CI (`validate_plugin`) is necessary but not sufficient for live Cursor Task/badge rows.

## Record results

Copy `evals/results/smoke-grok-build-TEMPLATE.json` to `evals/results/smoke-grok-build-YYYY-MM-DD.json`, fill checks, set `status`, and set `cursor_baseline`.

## Structural commands

```bash
python3 -m py_compile scripts/validate_plugin.py
python3 scripts/validate_plugin.py
grok plugin validate .
```
