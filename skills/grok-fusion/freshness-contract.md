# Freshness Contract

Work only with verified, current information. Memory is a hypothesis, not a source.

## Hard rules

1. Any claim about an external library, framework, API shape, version, pricing, limit, or best practice must be verified during this run via live web search, registry lookup, or reading the actual lockfile/config — never stated from memory.
2. Every evidence record carries `retrieved_at` (date of the read/search in this run) and `published_or_updated` when the source shows one.
3. A source older than 12 months, or undated, is labeled `STALE` and must be re-verified or explicitly accepted as a risk.
4. Decisions that shape the spine require at least two independent primary sources for their critical external claims.
5. Dependency versions come from the registry or lockfile read in this run. Never pin a version from memory.
6. If live verification tools are unavailable, label the claim `SPECULATIVE` and record it in unknowns instead of proceeding silently.

## Budget priority

Verification and research calls are never skipped to save tokens or time. Word caps limit artifact length, never the number of verification, search, or corroboration calls. When in doubt, verify again.
