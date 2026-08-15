# 02 — Sentinel Analytics Rules & SOAR Playbooks

**SC-200 domain:** Manage a security operations environment (analytics rules) · Respond to security incidents (SOAR)
**MITRE ATT&CK:** T1110 (Brute Force) · T1078.004 (Cloud Accounts) · T1531 (Account Access Removal — used defensively)

## Scenario

Writing a detection is half the job; the other half is making sure the response happens in seconds, not the hours it takes a human analyst to notice, triage, and act. This project pairs two **Microsoft Sentinel scheduled analytics rules** with a **Logic Apps SOAR playbook** that automatically contains a compromised account the moment an incident is created — the exact "Configure Security Orchestration Automation and Response (SOAR) in Microsoft Sentinel" skill SC-200 tests.

## What this project demonstrates

1. Two **ARM-deployable Sentinel scheduled analytics rules** (brute force, malicious inbox rule creation).
2. A **Logic Apps playbook** (ARM template) triggered by a Sentinel incident that disables the user, revokes active sessions, and posts a Teams alert — with a human-approval step before the disable action fires.

## Files

```
02-sentinel-analytics-soar-playbooks/
├── README.md
├── analytics-rules/
│   ├── brute-force-detection-rule.json        # Scheduled rule: repeated failed sign-ins → success
│   └── malicious-inbox-rule-detection.json    # Scheduled rule: auto-forwarding/hide rules (BEC indicator)
└── playbooks/
    ├── auto-disable-compromised-user-playbook.json  # Logic App ARM template
    └── README.md                                    # Deployment + logic walkthrough
```

## Analytics rules

| Rule | Query logic | Incident severity |
|---|---|---|
| `brute-force-detection-rule.json` | 10+ failed sign-ins for one account within 15 minutes, followed by a success | High |
| `malicious-inbox-rule-detection.json` | New Exchange inbox rule created with auto-forward to an external domain or that hides/deletes+moves security alert mail | High |

Both rules are written to **auto-create a Sentinel incident** and **auto-trigger the playbook** in `playbooks/`, using Sentinel's "automated response" trigger — no manual step required between detection and containment.

## SOAR playbook logic

`auto-disable-compromised-user-playbook.json` implements this flow:

1. **Trigger:** Microsoft Sentinel incident created (via the "When Azure Sentinel incident creation rule was triggered" connector)
2. **Enrich:** Look up the affected user's UPN and current sign-in risk in Entra ID
3. **Gate:** Post an approval card to a Teams SOC channel (auto-timeout after 15 minutes → proceeds automatically for High severity)
4. **Contain:** Disable the user account (`PATCH /users/{id}` `accountEnabled: false`) and revoke all refresh tokens (`POST /users/{id}/revokeSignInSessions`)
5. **Notify:** Post a summary to Teams and add a comment to the Sentinel incident documenting the automated action taken
6. **Escalate:** Update incident status to "Active" and assign to the on-call Tier 2 analyst

This mirrors Microsoft's own reference architecture for [Sentinel automation rules and playbooks](https://learn.microsoft.com/en-us/azure/sentinel/automate-incident-handling-with-automation-rules).

## Analyst takeaway

SC-200 explicitly tests "use playbooks to remediate threats" and "use playbooks to manage incidents." This project shows the full loop: detection rule → incident → automated, auditable, human-gated containment — the SOAR maturity level that separates a manual SOC from an automated one.

## Sources

- [Microsoft Sentinel automation rules](https://learn.microsoft.com/en-us/azure/sentinel/automate-incident-handling-with-automation-rules)
- [Tutorial: Use playbooks with automation rules](https://learn.microsoft.com/en-us/azure/sentinel/tutorial-respond-threats-playbook)
- [MITRE ATT&CK T1110 — Brute Force](https://attack.mitre.org/techniques/T1110/)
