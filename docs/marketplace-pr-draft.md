# Grok Build marketplace PR draft

**Status: DO-NOT-SUBMIT** — claim level `PACKAGING` / smoke `PARTIAL` (E2/E3 live probe still pending).

| Gate | Required | Current |
|---|---|---|
| Dual manifests + `validate_plugin` | yes | green on v0.4.1 |
| `grok plugin validate` / install / inspect | yes | verified on Grok CLI 0.2.103 |
| `evals/results/smoke-grok-build-*.json` with `status=PASS` (E1–E6) | yes for submit | **PARTIAL** (`smoke-grok-build-2026-07-18.json`) — E2/E3 PENDING |
| SD8 `cursor_baseline` | `PASS` artifact **or** `live_pending` → claim ≤ `PARTIAL` | `live_pending` → **FULL forbidden** |
| Pin SHA | 40-char lowercase of release commit | update after push (see below) |

Public claim while draft is DO-NOT-SUBMIT: **`PACKAGING`** / **`PARTIAL`**. Do not claim `FULL` or marketplace “production ready” until E2+E3 PASS.

## Proposed catalog entry

Add to `xai-org/plugin-marketplace` → `.grok-plugin/marketplace.json`:

```json
{
  "name": "grok-fusion",
  "description": "Adaptive Grok council — architecture, debugging, AppSec, resumable MVP builds, web/UI craft",
  "category": "development",
  "source": {
    "source": "url",
    "url": "https://github.com/GoodGameIsGood/grok-fusion.git",
    "sha": "0000000000000000000000000000000000000000"
  },
  "homepage": "https://github.com/GoodGameIsGood/grok-fusion",
  "keywords": [
    "fusion",
    "council",
    "architecture",
    "mvp",
    "security",
    "debugging",
    "grok"
  ]
}
```

Replace `sha` with the 40-char lowercase commit that ships v0.4.1 Grok Build packaging (run `git rev-parse HEAD` on that commit after push). Placeholder above is intentional so this file never pretends a stale pin is submit-ready.

**Before submit:**

```bash
# In grok-fusion @ release commit
git rev-parse HEAD   # paste into sha

# In a checkout of xai-org/plugin-marketplace
python3 scripts/generate-plugin-index.py
python3 scripts/validate-catalog.py
```

Open a PR. Code-owner review required. Upstream merge is out of scope for this repo’s implementation waves.

## Submit-ready checklist

Mark this doc **submit-ready** only when all are true:

1. [ ] `python3 scripts/validate_plugin.py` PASS
2. [ ] `grok plugin validate .` PASS
3. [ ] Dated `evals/results/smoke-grok-build-*.json` with `"status": "PASS"` and E1–E6 checks PASS (including live E2/E3)
4. [ ] SD8: `cursor_baseline.status` is `PASS` (with `artifact_path`) **or** explicit user waiver; if `live_pending`, public claim stays ≤ `PARTIAL`
5. [ ] `sha` field is the 40-char commit that contains the smoke-passing tree
6. [ ] Product receipt in README still denies FULL until those gates hold

## Product receipt reminder

- Ships dual-host packaging (`.cursor-plugin` + `.grok-plugin`) from one repo
- Agents on Grok Build resolve as `grok-fusion:gf-*`
- Does **not** claim Cursor Marketplace one-click or FULL Grok Build behavioral parity without smoke + SD8
