# Cursor smoke runbook

Manual checks after installing the plugin. Do not claim universality until these pass.

## Install

1. Install to `~/.cursor/plugins/local/grok-fusion` or copy:
   - `skills/grok-fusion/`
   - `agents/gf-worker.md`
   - `agents/gf-reviewer.md`
   - `agents/gf-auditor.md`
   - `rules/grok-fusion-auto.mdc`
2. Enable third-party plugins if required by Cursor settings.
3. Reload the window.
4. Select the strongest non-Fast Grok model.

## Checks

| Check | Pass criteria |
|---|---|
| Skill visible | `/grok-fusion` appears and auto rule loads |
| Agents visible | `gf-worker`, `gf-reviewer`, `gf-auditor` are available |
| Task spawning | Standard/Heavy runs create real Task subagents, not inline simulation |
| Model inherit | Subagent badges match parent Grok |
| Fail closed | Disabling Task or forcing non-Grok fallback yields “Fusion did not run” |
| Quick routing | Single-file rename stays Quick and finishes with low call count |
| Standard routing | Ordinary debug/research uses Standard footer |
| Heavy routing | Architecture/security prompts use Heavy |
| MVP resume | Creating an MVP run writes `.grok-fusion/runs/<id>/` and can resume |
| Safety gates | Migration/breaking changes pause at G1/G2 |
| Freshness | External library/version claims carry retrieved_at from live lookups |
| Self-critique | Final answers include resolved or reported devil's advocate objection |
| Multi-pass consensus | Mutating/plan runs show per-step recheck, double error hunt, completion quality, and ≥5 specialist votes with consensus PASS before done |

## Commands

```bash
python3 -m py_compile scripts/validate_plugin.py
python3 scripts/validate_plugin.py
python3 scripts/validate_plugin.py --state evals/fixtures/valid-run
```

Invalid fixture must fail:

```bash
python3 scripts/validate_plugin.py --state evals/fixtures/invalid-run; test $? -ne 0
```
