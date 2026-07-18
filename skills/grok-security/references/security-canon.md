# Security Canon

AppSec-first guidance for `grok-security`. Prefer evidence over vibe.

## Frameworks

| Layer | Use |
|---|---|
| OWASP Top 10:2025 | Risk awareness (A01–A10) |
| ASVS 5.0 L1 | Default verification checklist (escalate L2 on High/authz) |
| CWE | Tag every Finding (`CWE-xxx`) |
| STRIDE | Trust-boundary pass on auth/API/data-flow changes |
| LLM / Agentic Top 10 | Only when reviewing AI/agent/MCP/tool code (see appendix) |

## Ordered review passes

1. Access control / tenancy / IDOR (A01)
2. Authn / sessions / tokens (A07)
3. Injection & unsafe sinks (A05)
4. Crypto & secrets (A02/A04)
5. Misconfiguration / fail-open / verbose errors (A02/A10)
6. Supply chain (A03)
7. Integrity (webhooks, deserialization) (A08)
8. Abuse: **rate limits**, **size limits**, **uploads**, **open redirects**
9. Security logging without secret leakage (A09)
10. Exceptional conditions mishandling (A10)

## Defensive-only (hard)

- **Forbidden:** exploit payloads, weaponized PoCs, attacking remote/prod systems
- **Evidence allowlist only:** `path:line` | `missing_control` | `config_absence`
- Same allowlist for Remediation `characterization_cmds` (static checks only)
- Prefer parameterized queries, encoding, server-side authz, allowlists, fail-closed, secret removal + rotation guidance

## Abuse checklist (mirror threat_abuse panel)

- Rate limits on public/auth endpoints
- Size limits on uploads/bodies
- Upload type/path hardening
- No user-controlled open redirects

## LLM / agentic appendix (AI-code only)

Load only when the diff touches models, tools, RAG, MCP, or agent orchestration.

Topics (≤40 lines total for this section in practice — keep brief):

1. Prompt injection / indirect injection into tool calls
2. Excessive agency / tool misuse beyond least privilege
3. Secrets or PII in prompts, logs, or tool args
4. Untrusted model output reaching sinks (code/SQL/shell)
5. Supply-chain / poisoned instructions for agents

Do not expand into full red-team playbooks. No exploit PoCs.
