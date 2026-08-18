# 02 — Sentinel Analytics Rules & SOAR Playbooks

**SC-200 domain:** Manage a security operations environment (analytics rules) · Respond to security incidents (SOAR)
**MITRE ATT&CK:** T1110 (Brute Force) · T1078.004 (Cloud Accounts) · T1531 (Account Access Removal — used defensively)

## Scenario

This educational design pairs two Sentinel analytics-rule examples with a Logic Apps SOAR playbook template. It illustrates a possible detection-to-containment workflow for SC-200 study; it has not been presented as a deployed or validated automation.

## What this project demonstrates

1. Two Sentinel analytics-rule JSON examples (brute force and malicious inbox rule creation).
2. A Logic Apps playbook template that models account disablement, session revocation, and Teams notification with an approval gate.

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

The JSON describes intended incident creation and automation-rule behavior. Before use, validate the resource types, connector configuration, permissions, API versions, and response safety controls in an authorized test tenant.

## SOAR playbook logic

`auto-disable-compromised-user-playbook.json` models this flow:

1. **Trigger:** Microsoft Sentinel incident created (via the "When Azure Sentinel incident creation rule was triggered" connector)
2. **Enrich:** Look up the affected user's UPN and current sign-in risk in Entra ID
3. **Gate:** Post an approval card to a Teams SOC channel (auto-timeout after 15 minutes → proceeds automatically for High severity)
4. **Contain:** Disable the user account (`PATCH /users/{id}` `accountEnabled: false`) and revoke all refresh tokens (`POST /users/{id}/revokeSignInSessions`)
5. **Notify:** Post a summary to Teams and add a comment to the Sentinel incident documenting the automated action taken
6. **Escalate:** Update incident status to "Active" and assign to the on-call Tier 2 analyst

This mirrors Microsoft's own reference architecture for [Sentinel automation rules and playbooks](https://learn.microsoft.com/en-us/azure/sentinel/automate-incident-handling-with-automation-rules).

## Analyst takeaway

SC-200 explicitly tests "use playbooks to remediate threats" and "use playbooks to manage incidents." This project documents the intended loop — detection rule → incident → human-gated containment — for study and review. It is not evidence of an operational SOC automation.

## Sources

- [Microsoft Sentinel automation rules](https://learn.microsoft.com/en-us/azure/sentinel/automate-incident-handling-with-automation-rules)
- [Tutorial: Use playbooks with automation rules](https://learn.microsoft.com/en-us/azure/sentinel/tutorial-respond-threats-playbook)
- [MITRE ATT&CK T1110 — Brute Force](https://attack.mitre.org/techniques/T1110/)
