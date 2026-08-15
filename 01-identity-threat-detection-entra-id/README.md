# 01 — Identity Threat Detection: Microsoft Entra ID

**SC-200 domain:** Manage a security operations environment · Perform threat hunting
**MITRE ATT&CK:** T1078 (Valid Accounts) · T1621 (MFA Request Generation) · T1556 (Modify Authentication Process) · T1204 (User Execution)

## Scenario

Identity is the number-one attack surface Microsoft reports across its security signal data — compromised credentials, MFA fatigue, and legacy authentication bypass are the most common entry points into cloud tenants. This project builds the detection and audit layer a SOC/identity analyst uses to catch identity compromise **before** it becomes a Sentinel incident.

## What this project demonstrates

1. **KQL hunt queries** against Entra ID sign-in and audit logs to surface risky authentication patterns.
2. **A Python auditing script** using Microsoft Graph API to find Conditional Access policy gaps (the kind of manual review SC-200's "Manage a security operations environment" domain tests).

## Files

```
01-identity-threat-detection-entra-id/
├── README.md
├── kql/
│   ├── risky-sign-ins-hunt.kql          # Correlates Entra ID Identity Protection risk with sign-in logs
│   ├── impossible-travel-detection.kql  # Geo-velocity detection across consecutive sign-ins
│   └── mfa-fatigue-detection.kql        # Rapid repeated MFA push notifications (T1621)
└── scripts/
    └── conditional_access_policy_audit.py  # Graph API audit: flags CA gaps (legacy auth, admin MFA, etc.)
```

## KQL Queries

| Query | Table(s) | What it catches |
|---|---|---|
| `risky-sign-ins-hunt.kql` | `SigninLogs`, `AADUserRiskEvents` | Sign-ins flagged medium/high risk that succeeded, especially from atypical locations or anonymized IPs |
| `impossible-travel-detection.kql` | `SigninLogs` | Two successful sign-ins for the same user from locations that are physically impossible to travel between in the elapsed time |
| `mfa-fatigue-detection.kql` | `SigninLogs` | 5+ MFA prompts for the same user within 10 minutes followed by an eventual approval — the classic "MFA bombing" pattern (T1621) |

## Python audit script

`conditional_access_policy_audit.py` calls the Microsoft Graph `/identity/conditionalAccess/policies` endpoint and flags:
- Policies that exclude "All users" without a documented break-glass exception
- Admin roles not covered by a "require MFA" grant control
- Legacy authentication (`clientAppTypes: exchangeActiveSync`, `other`) not blocked
- Policies in "Report-only" mode that have been sitting unenforced for the review period

Run it with:

```bash
python conditional_access_policy_audit.py --tenant-id <TENANT_ID>
```

It authenticates using `DeviceCodeCredential` from `azure-identity` (interactive login — no secrets stored), requiring `Policy.Read.All` delegated permission.

## Analyst takeaway

A Tier 1 SOC analyst triages the alert; a Tier 2/identity analyst asks *why the control didn't stop it in the first place*. This project pairs a detection layer (KQL) with a prevention-gap audit (Graph API script) — exactly the "detect + configure protections" loop SC-200 measures under Manage a security operations environment.

## Sources

- [Microsoft Entra ID Protection risk detections](https://learn.microsoft.com/en-us/entra/id-protection/concept-identity-protection-risks)
- [Conditional Access: Common policies](https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-conditional-access-policy-common)
- [MITRE ATT&CK T1621 — Multi-Factor Authentication Request Generation](https://attack.mitre.org/techniques/T1621/)
