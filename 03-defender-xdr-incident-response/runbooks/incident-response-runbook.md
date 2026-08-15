# Incident Response Runbook — Phishing-to-Lateral-Movement Case

**Status: SIMULATED case study.** No real breach occurred. This runbook documents the response methodology I would follow, using Defender XDR + Sentinel tooling, structured on [NIST SP 800-61 Rev. 2](https://csrc.nist.gov/pubs/sp/800/61/r2/final).

## Simulated incident summary

| Field | Value |
|---|---|
| Incident ID (simulated) | INC-2026-0142 |
| Severity | High |
| Affected user | `j.martin@contoso-lab.local` (lab tenant, fictional) |
| Attack stages observed | Phishing click → OAuth consent grant → encoded PowerShell execution → SMB lateral movement to 2 hosts |
| Detection sources | Defender for Office 365 (`EmailEvents`), Defender for Cloud Apps (`CloudAppEvents`), Defender for Endpoint (`DeviceProcessEvents`, `DeviceNetworkEvents`) |
| Correlation | Auto-linked into a single Defender XDR incident via shared user/device entities |

## 1. Preparation (pre-incident)

- Advanced Hunting queries in `../hunting-queries/` are saved as custom detection rules running on a 1-hour cadence.
- Sentinel automation rule (see `../../02-sentinel-analytics-soar-playbooks/`) is wired to the "brute force" and "malicious inbox rule" analytics rules so containment can start before an analyst even opens the incident.
- On-call SOC Tier 2 rotation and Teams escalation channel are defined and tested quarterly (tabletop exercise).

## 2. Detection & Analysis

1. Defender for Office 365 flags the phishing email as delivered-then-clicked (`email-phishing-indicators.kql`) — **Severity: Medium**, auto-created incident.
2. Within the hour, Defender for Cloud Apps logs a consent grant to an unverified app requesting `Mail.Read offline_access` (`suspicious-oauth-app-consent.kql`) for the same user — Defender XDR auto-correlates this into the existing incident and raises severity to **High**.
3. Defender for Endpoint then logs encoded PowerShell execution on the user's device, followed by SMB connections to two other hosts (`lateral-movement-hunt.kql`) — correlated into the same incident thread.
4. Analyst opens the unified incident in the Defender XDR portal, reviews the attack story graph, and confirms all three signals share the same identity (`j.martin@contoso-lab.local`) and a common timeline.

**Triage decision:** Confirmed true positive, active compromise with lateral movement — escalate to Tier 2, begin containment immediately.

## 3. Containment

**Short-term (minutes):**
- Isolate the affected endpoint from the network via Defender for Endpoint's "Isolate device" action (network isolation, allows security tooling to keep functioning).
- Trigger the `auto-disable-compromised-user-playbook` (see Project 02) to disable the account and revoke all refresh tokens/sessions.
- Revoke the malicious OAuth application's consent grant in Entra ID > Enterprise Applications.

**Longer-term:**
- Block the phishing sender domain and malicious URL at the mail gateway (Defender for Office 365 Tenant Allow/Block List).
- Identify and isolate the two additional hosts touched by lateral movement pending forensic review.

## 4. Eradication

- Run a full Defender for Endpoint AV/EDR scan on all three affected devices.
- Remove any persistence mechanisms found (scheduled tasks, registry run keys, additional OAuth grants) surfaced by a `DeviceRegistryEvents`/`DeviceFileEvents` follow-up hunt.
- Force a password reset for the affected user in addition to the session revocation already performed.
- Re-verify no additional inbox rules or delegate mailbox permissions were created (cross-check against `malicious-inbox-rule-detection.json` from Project 02).

## 5. Recovery

- Re-enable the user account only after password reset + MFA re-registration is confirmed.
- Lift device isolation after the AV/EDR scan returns clean and a manual review confirms no residual indicators.
- Monitor the user and the two touched hosts at heightened sensitivity (temporary custom detection rule) for 14 days.

## 6. Lessons Learned / Post-Incident Review

| Finding | Recommendation |
|---|---|
| User clicked a link from a message already routed to Junk | Targeted phishing-awareness refresher; consider Safe Links stricter tenant policy |
| Unverified third-party app was able to request `Mail.Read` + `offline_access` | Restrict user consent to admin-approved apps only (Entra ID > Enterprise Applications > Consent and permissions) |
| Encoded PowerShell was allowed to execute | Deploy an Attack Surface Reduction rule blocking obfuscated script execution; consider Constrained Language Mode |
| SMB lateral movement succeeded to 2 hosts | Review network segmentation; the workstation subnet should not have direct SMB reach to the affected hosts |

## Mapping to SC-200

This runbook exercises: *Respond to alerts and incidents in Microsoft Defender XDR*, *Respond to alerts and incidents in Microsoft Defender for Endpoint*, *manage incidents across Microsoft Defender products*, and *perform advanced threat hunting* — all listed under the current SC-200 skills outline.

## Sources

- [NIST SP 800-61 Rev. 2](https://csrc.nist.gov/pubs/sp/800/61/r2/final)
- [Microsoft Defender XDR incidents overview](https://learn.microsoft.com/en-us/microsoft-365/security/defender/incidents-overview)
- [Illicit consent grant attack detection](https://learn.microsoft.com/en-us/microsoft-365/security/office-365-security/detect-and-remediate-illicit-consent-grants)
