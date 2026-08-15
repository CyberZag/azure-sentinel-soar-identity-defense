"""
conditional_access_policy_audit.py

Audits Microsoft Entra ID Conditional Access policies for common coverage gaps using the
Microsoft Graph API. Built for the SC-200 "Manage a security operations environment" domain:
identifying and remediating security risks related to Conditional Access events.

Requires:
    pip install azure-identity msgraph-sdk

Permissions:
    Delegated: Policy.Read.All (interactive device-code sign-in, no client secret stored)

Usage:
    python conditional_access_policy_audit.py --tenant-id <TENANT_ID>
"""

import argparse
import asyncio
import sys
from dataclasses import dataclass, field

from azure.identity import DeviceCodeCredential
from msgraph import GraphServiceClient

SCOPES = ["Policy.Read.All"]

LEGACY_AUTH_CLIENT_APPS = {"exchangeActiveSync", "other"}


@dataclass
class Finding:
    policy_name: str
    severity: str
    issue: str


@dataclass
class AuditReport:
    findings: list = field(default_factory=list)

    def add(self, policy_name: str, severity: str, issue: str) -> None:
        self.findings.append(Finding(policy_name, severity, issue))

    def print_report(self) -> None:
        if not self.findings:
            print("No Conditional Access coverage gaps detected.")
            return
        print(f"{'Severity':<8} {'Policy':<40} Issue")
        print("-" * 100)
        for f in sorted(self.findings, key=lambda x: {"HIGH": 0, "MEDIUM": 1, "LOW": 2}[x.severity]):
            print(f"{f.severity:<8} {f.policy_name[:38]:<40} {f.issue}")


def audit_policy(policy, report: AuditReport) -> None:
    name = policy.display_name or "(unnamed policy)"
    state = policy.state

    if state == "disabled":
        return  # disabled policies are out of scope for enforcement gaps, but still worth an inventory note

    conditions = policy.conditions
    grant_controls = policy.grant_controls

    # 1. Legacy authentication not blocked
    client_app_types = set(conditions.client_app_types or []) if conditions else set()
    if client_app_types & LEGACY_AUTH_CLIENT_APPS:
        blocks_legacy = grant_controls and "block" in (grant_controls.built_in_controls or [])
        if not blocks_legacy:
            report.add(name, "HIGH", "Targets legacy auth client types but does not enforce a block control")

    # 2. Admin roles not covered by MFA requirement
    users = conditions.users if conditions else None
    include_roles = getattr(users, "include_roles", None) or []
    if include_roles:
        requires_mfa = grant_controls and "mfa" in (grant_controls.built_in_controls or [])
        if not requires_mfa:
            report.add(name, "HIGH", "Applies to privileged roles but does not require MFA grant control")

    # 3. Report-only policies stale beyond review window
    if state == "enabledForReportingButNotEnforced":
        report.add(name, "MEDIUM", "Still in report-only mode — confirm this is intentional, not forgotten")

    # 4. All-users exclusion without documented break-glass note
    exclude_users = getattr(users, "exclude_users", None) or []
    include_users = getattr(users, "include_users", None) or []
    if "All" in include_users and exclude_users:
        report.add(
            name,
            "LOW",
            f"Excludes {len(exclude_users)} account(s) from an 'All users' policy — verify break-glass accounts only",
        )


async def run_audit(tenant_id: str) -> AuditReport:
    credential = DeviceCodeCredential(tenant_id=tenant_id)
    client = GraphServiceClient(credentials=credential, scopes=SCOPES)

    report = AuditReport()
    policies_response = await client.identity.conditional_access.policies.get()
    policies = policies_response.value if policies_response else []

    for policy in policies:
        audit_policy(policy, report)

    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tenant-id", required=True, help="Microsoft Entra tenant ID or verified domain")
    args = parser.parse_args()

    report = asyncio.run(run_audit(args.tenant_id))
    report.print_report()
    return 0


if __name__ == "__main__":
    sys.exit(main())
