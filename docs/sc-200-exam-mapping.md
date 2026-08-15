# SC-200 Exam Domain → Repository Mapping

Based on the official [Study guide for Exam SC-200: Microsoft Security Operations Analyst](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/sc-200) (current skills-measured blueprint).

## Skills at a glance

| Domain | Weight |
|---|---|
| Manage a security operations environment | 40–45% |
| Respond to security incidents | 35–40% |
| Perform threat hunting | 20–25% |

## Domain 1 — Manage a security operations environment (40–45%)

| Sub-skill | Repo artifact |
|---|---|
| Identify and remediate security risks related to Conditional Access events | [`01-identity-threat-detection-entra-id/scripts/conditional_access_policy_audit.py`](../01-identity-threat-detection-entra-id/scripts/conditional_access_policy_audit.py) |
| Configure detection alerts in Microsoft Entra ID Identity Protection | [`01-identity-threat-detection-entra-id/kql/risky-sign-ins-hunt.kql`](../01-identity-threat-detection-entra-id/kql/risky-sign-ins-hunt.kql) |
| Design and configure Microsoft Sentinel analytics rules | [`02-sentinel-analytics-soar-playbooks/analytics-rules/`](../02-sentinel-analytics-soar-playbooks/analytics-rules/) |
| Define incident creation logic | Both analytics rule JSON templates include `incidentConfiguration` blocks |

## Domain 2 — Respond to security incidents (35–40%)

| Sub-skill | Repo artifact |
|---|---|
| Configure Security Orchestration Automation and Response (SOAR) in Microsoft Sentinel | [`02-sentinel-analytics-soar-playbooks/playbooks/auto-disable-compromised-user-playbook.json`](../02-sentinel-analytics-soar-playbooks/playbooks/auto-disable-compromised-user-playbook.json) |
| Use playbooks to remediate and manage incidents | Same playbook — approval-gated disable + session revocation + incident comment |
| Respond to alerts and incidents in Microsoft Defender XDR | [`03-defender-xdr-incident-response/runbooks/incident-response-runbook.md`](../03-defender-xdr-incident-response/runbooks/incident-response-runbook.md) |
| Manage incidents across Microsoft Defender products (cross-domain investigation) | Same runbook — correlates Defender for Office 365, Cloud Apps, and Endpoint signals into one incident |

## Domain 3 — Perform threat hunting (20–25%)

| Sub-skill | Repo artifact |
|---|---|
| Create custom hunting queries | All `.kql` files across Projects 01 and 03 |
| Identify threats by using KQL | [`01-identity-threat-detection-entra-id/kql/mfa-fatigue-detection.kql`](../01-identity-threat-detection-entra-id/kql/mfa-fatigue-detection.kql), [`01-identity-threat-detection-entra-id/kql/impossible-travel-detection.kql`](../01-identity-threat-detection-entra-id/kql/impossible-travel-detection.kql) |
| Create Advanced Hunting queries (Defender XDR) | [`03-defender-xdr-incident-response/hunting-queries/`](../03-defender-xdr-incident-response/hunting-queries/) |
| Analyze relationships between entities | Runbook's attack-story correlation across `EmailEvents` → `CloudAppEvents` → `DeviceProcessEvents` → `DeviceNetworkEvents` |

## Next additions planned

- Microsoft Defender for Cloud workload-protection alert triage (not yet covered — smallest gap against the current blueprint)
- Sentinel workbook for tracking incident response metrics (security operations efficiency workbook)
- Exposure management / threat intelligence enrichment workflow, extending [`101-cybersecurity-analyst`](https://github.com/CyberZag/101-cybersecurity-analyst) module 06 (Cyber Threat Intelligence)
