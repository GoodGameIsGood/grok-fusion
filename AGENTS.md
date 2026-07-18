# Grok Fusion — project agent instructions

This repository develops the **grok-fusion** plugin. Before answering or editing here:

1. Load the `grok-fusion` skill (`skills/grok-fusion/SKILL.md` or `/grok-fusion`).
2. Load `.grok-fusion/config.json` (this repo ships `quality_profile: max` / `force_mvp`).
3. Follow `runtime-contract.md` host matrix (Cursor Task tool or Grok Build `task`/`spawn_subagent`).
4. Run the Task probe for Standard/Heavy/MVP; fail closed if subagents are unavailable. On Grok Build spawn **`grok-fusion:gf-worker`** (and siblings), not bare `gf-*` alone.
5. End with `Fusion tier: …` matching the actual tier (on `max`, always `MVP`).

**Grok Build checklist:** `[subagents] enabled = true` in `~/.grok/config.toml` (плашка Subagents). If off, the session hook and the parent must show the subagents-OFF banner from `runtime-contract.md` so you see it immediately.

## Scope of this file

- Applies when the working tree is **this repo** (dev) or when a consumer copies this snippet (Option B / Option C).
- **Not** a substitute for marketplace plugin auto-route. G1 FULL auto-parity on Grok Build requires smoke proof that plugin `rules/grok-fusion-auto.mdc` fires; until then treat auto-route as PARTIAL and keep this `AGENTS.md` (or the Option C consumer snippet in README).

## Must not

- Do not simulate `gf-*` subagents inline.
- Do not claim FULL Grok Build parity without recorded `evals/results/smoke-grok-build-*.json` PASS plus SD8 Cursor baseline rules.
- Do not redesign the Fusion pipeline.
