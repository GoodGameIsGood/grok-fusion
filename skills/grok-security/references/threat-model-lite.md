# Threat model lite (STRIDE)

Use on new or changed trust boundaries (auth, public APIs, data stores, file/upload, agent tools). Keep short; attach outcomes to Finding Cards or plan notes.

## When to run

- Architecture / API / authz changes
- New public endpoints, uploads, webhooks
- Multi-tenant or privilege changes
- AI/agent tool surfaces (also load security-canon LLM appendix)

## STRIDE prompts

| Threat | Ask |
|---|---|
| Spoofing | Can a caller pretend to be another user/service? |
| Tampering | Can request/body/storage be altered in transit or at rest? |
| Repudiation | Are security-relevant actions attributable in logs (without secrets)? |
| Information disclosure | Can sensitive data leak via errors, logs, or IDOR? |
| Denial of service | Are rate/size/cost bounds present? |
| Elevation of privilege | Can a low-privilege principal reach admin/tenant-crossing actions? |

## Output shape

For each relevant STRIDE row that fails or is unverified:

- Map to OWASP id + CWE when possible
- Emit Finding Card with allowlisted evidence
- List unread boundaries under `residual_unknowns`

Do not produce attack scripts. Prefer missing-control and path:line evidence.
