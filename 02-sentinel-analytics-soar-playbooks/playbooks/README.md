# Playbook: Auto-Disable Compromised User

## Flow diagram (logical)

```
Sentinel Incident Created (High/Medium severity)
        │
        ▼
Get incident entities (UPN, IP, host)
        │
        ▼
Get user details from Entra ID
        │
        ▼
Post approval card to Teams SOC channel  ──(Reject)──► Comment: manual review required
        │
   (Approve OR High-severity timeout)
        │
        ▼
Disable user account (Graph: accountEnabled = false)
        │
        ▼
Revoke all sign-in sessions (Graph: revokeSignInSessions)
        │
        ▼
Comment on incident: automated containment applied
        │
        ▼
Notify Teams + update incident status/owner
```

## Why the human-approval gate

Fully automatic account disablement without a check is a common mistake in early-stage SOAR — it creates a denial-of-service risk if a detection rule ever fires on a false positive against an executive or on-call engineer. This playbook keeps a human in the loop for anything below High severity, while still auto-proceeding on High severity if the SOC channel doesn't respond within the timeout — balancing speed with safety, which is the design trade-off SC-200 expects analysts to understand when they "use playbooks to remediate threats."

## Deployment prerequisites

1. API connections in the Logic App's resource group for:
   - `azuresentinel` (Microsoft Sentinel connector)
   - `azuread` (Microsoft Entra ID connector, requires `User.ReadWrite.All` and consent)
   - `teams` (Microsoft Teams connector)
2. An automation rule (see `analytics-rules/brute-force-detection-rule.json`) configured to call this playbook on incident creation.
3. A dedicated Teams channel for SOC approvals, with the channel ID passed as the `TeamsChannelId` parameter.

## Deploy

```bash
az deployment group create \
  --resource-group <RESOURCE_GROUP> \
  --template-file auto-disable-compromised-user-playbook.json \
  --parameters TeamsChannelId=<TEAMS_CHANNEL_ID>
```

After deployment, authorize each API connection once in the Azure Portal (Logic App > API connections > Authorize) — this is a one-time interactive step Microsoft requires per connection.
