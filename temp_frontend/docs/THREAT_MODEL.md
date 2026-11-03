# Securebox Threat Model

## Assets
- User Source Code
- API Keys / Secrets
- Host System Integrity
- AI Model Weights/Configs

## Threat Actors
- Malicious AI Skills (Prompt Injection, Data Exfiltration)
- Compromised Dependencies (Supply Chain Attack)
- Malicious Repositories (Path Traversal, Symlink Escapes)

## Mitigation Strategies
| Threat | Mitigation | Verification |
|---|---|---|
| **Sandbox Escape** | Rootless Docker, No-New-Privileges, Resource Limits | Sandbox Security Tests |
| **Secret Leakage** | Source-level masking, no-plaintext logs | Audit Log Review |
| **Unsafe Repair** | `git apply --check`, Human Approval | Repair Workflow Tests |
| **Path Traversal** | `pathlib.Path` boundary checks | Adversarial Tests |
| **SSRF** | Default Network Isolation (`--network none`) | Network Probe Tests |

## Residual Risks
- Zero-day vulnerabilities in the Docker runtime or Linux kernel.
- Advanced prompt injection that bypasses static inspection but remains "safe" to a human reviewer.
