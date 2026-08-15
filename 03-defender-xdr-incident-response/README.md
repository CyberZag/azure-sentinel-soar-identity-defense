# 03 — Microsoft Defender XDR Incident Response

**SC-200 domain:** Respond to security incidents · Perform threat hunting
**MITRE ATT&CK:** T1566 (Phishing) · T1059 (Command and Scripting Interpreter) · T1021 (Remote Services) · T1550 (Use Alternate Authentication Material)

## Scenario

This project is a **simulated multi-stage attack case study** — phishing email → endpoint compromise → lateral movement — investigated the way a SOC analyst would use Microsoft Defender XDR's cross-product correlation (Defender for Office 365 + Defender for Endpoint + Defender for Cloud Apps) with Advanced Hunting KQL.

**This is a documented, clearly labeled simulation.** No real incident occurred; the runbook demonstrates the investigation and response methodology SC-200 tests under "Respond to alerts and incidents in Microsoft Defender XDR" and "perform advanced threat hunting."

## What this project demonstrates

1. **Three Advanced Hunting KQL queries**, one per attack stage, showing how an analyst would pivot across Defender XDR tables (`EmailEvents`, `DeviceProcessEvents`, `DeviceNetworkEvents`, `CloudAppEvents`).
2. **A full incident-response runbook** structured around the NIST SP 800-61 lifecycle, adapted for a Defender XDR + Sentinel-based SOC.

## Files

```
03-defender-xdr-incident-response/
├── README.md
├── hunting-queries/
│   ├── email-phishing-indicators.kql         # Stage 1: initial access via phishing
│   ├── lateral-movement-hunt.kql             # Stage 2: endpoint compromise → lateral movement
│   └── suspicious-oauth-app-consent.kql      # Stage 3: persistence via malicious OAuth app consent
└── runbooks/
    └── incident-response-runbook.md          # Simulated case, NIST-aligned response steps
```

## Simulated attack narrative

1. **Initial access:** A user receives and clicks a phishing email with a credential-harvesting link, captured in `EmailEvents`/`UrlClickEvents`.
2. **Execution & foothold:** The user's browser session token is stolen (T1550) and used to grant a malicious OAuth application read/write access to mailbox and files (`CloudAppEvents`), while a PowerShell process on the endpoint downloads a second-stage payload (T1059, `DeviceProcessEvents`).
3. **Lateral movement:** The compromised endpoint initiates SMB/RDP connections to two additional hosts (T1021, `DeviceNetworkEvents`).
4. **Response:** Defender XDR auto-correlates the three signals into a single incident; the analyst follows the runbook to contain, eradicate, and document.

## Analyst takeaway

SC-200's "Respond to security incidents" domain is the largest single skill area on the current exam blueprint. This project shows the full loop end to end: cross-signal hunting → incident correlation → structured, NIST-aligned response documentation — not just isolated KQL snippets.

## Sources

- [Microsoft Defender XDR incidents overview](https://learn.microsoft.com/en-us/microsoft-365/security/defender/incidents-overview)
- [Advanced hunting schema reference](https://learn.microsoft.com/en-us/microsoft-365/security/defender/advanced-hunting-schema-tables)
- [NIST SP 800-61 Rev. 2 — Computer Security Incident Handling Guide](https://csrc.nist.gov/pubs/sp/800/61/r2/final)
- [SC-200 study guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/sc-200)
