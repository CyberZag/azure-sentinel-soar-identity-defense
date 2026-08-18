# 🛡️ Azure Sentinel, SOAR & Identity Defense — SC-200 Portfolio

![Azure](https://img.shields.io/badge/Microsoft%20Azure-0089D6?style=for-the-badge&logo=microsoftazure&logoColor=white)
![Sentinel](https://img.shields.io/badge/Microsoft%20Sentinel-SIEM%2FSOAR-purple?style=for-the-badge&logo=microsoftazure&logoColor=white)
![Defender XDR](https://img.shields.io/badge/Microsoft%20Defender%20XDR-0078D4?style=for-the-badge&logo=microsoftdefender&logoColor=white)
![Entra ID](https://img.shields.io/badge/Microsoft%20Entra%20ID-Identity%20Protection-blue?style=for-the-badge)
![KQL](https://img.shields.io/badge/KQL-Kusto%20Query%20Language-orange?style=for-the-badge)
![MITRE ATT&CK](https://img.shields.io/badge/MITRE%20ATT%26CK-Mapped-red?style=for-the-badge)
![SC-200](https://img.shields.io/badge/Cert%20Target-SC--200-green?style=for-the-badge)

---

## 🎯 Objective

This repository is a learning portfolio aligned to the **[Microsoft Certified: Security Operations Analyst Associate (SC-200)](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/sc-200)** study path. It documents Azure and security-operations concepts through lab artifacts; it does not represent an earned certification or production experience.

Alongside exam study, the repository contains draft lab artifacts — KQL detections, Sentinel analytics-rule examples, a Logic Apps playbook design, and an incident-response runbook. Each requires authorized environment-specific validation before use.

This repo is a companion to two other portfolio repos:
- [`101-cybersecurity-analyst`](https://github.com/CyberZag/101-cybersecurity-analyst) — personal cybersecurity study roadmap
- [`azure-security-labs`](https://github.com/CyberZag/azure-security-labs) — hands-on Azure identity/Sentinel labs with Python tooling

Where those repos cover *fundamentals*, this repo goes deeper into the **Sentinel SOAR automation, identity threat detection, and Defender XDR incident response** skills that SC-200 actually tests.

---

## 📋 Project Index

| # | Project | SC-200 Domain | Tools Used | MITRE Techniques | Status |
|---|---------|---------------|------------|-------------------|--------|
| 01 | [Identity Threat Detection — Entra ID](./01-identity-threat-detection-entra-id/) | Manage a security operations environment · Perform threat hunting | KQL, Microsoft Graph API, Entra ID Identity Protection | T1078 · T1621 · T1556 · T1204 | Draft — lab validation pending |
| 02 | [Sentinel Analytics Rules & SOAR Playbooks](./02-sentinel-analytics-soar-playbooks/) | Manage a security operations environment · Respond to security incidents | Microsoft Sentinel, Logic Apps, ARM templates | T1110 · T1078.004 · T1531 | Draft — lab validation pending |
| 03 | [Defender XDR Incident Response](./03-defender-xdr-incident-response/) | Respond to security incidents · Perform threat hunting | Microsoft Defender XDR, Advanced Hunting (KQL) | T1566 · T1059 · T1021 · T1550 | Simulated scenario |

### MITRE ATT&CK Technique Reference

| Technique ID | Name | Covered In |
|---|---|---|
| T1078 / T1078.004 | Valid Accounts / Cloud Accounts | Project 01, 02 |
| T1621 | Multi-Factor Authentication Request Generation (MFA fatigue) | Project 01 |
| T1556 | Modify Authentication Process | Project 01 |
| T1204 | User Execution | Project 01 |
| T1110 | Brute Force | Project 02 |
| T1531 | Account Access Removal (used defensively for containment) | Project 02 |
| T1566 | Phishing | Project 03 |
| T1059 | Command and Scripting Interpreter | Project 03 |
| T1021 | Remote Services (lateral movement) | Project 03 |
| T1550 | Use Alternate Authentication Material (token theft) | Project 03 |

---

## 🗺️ SC-200 Exam Mapping

Skills measured on [Exam SC-200: Microsoft Security Operations Analyst](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/sc-200) (current blueprint):

| SC-200 Skill Area | Weight | Demonstrated In |
|---|---|---|
| Manage a security operations environment | 40–45% | Project 01 (Entra ID hardening & detections), Project 02 (Sentinel workspace & analytics rules) |
| Respond to security incidents | 35–40% | Project 02 (SOAR playbooks), Project 03 (Defender XDR incident response runbook) |
| Perform threat hunting | 20–25% | Project 01 (KQL hunt queries), Project 03 (Advanced Hunting queries) |

See [`docs/sc-200-exam-mapping.md`](./docs/sc-200-exam-mapping.md) for the full breakdown against every project artifact.

---

## ✅ Prerequisites

- Azure subscription with Microsoft Sentinel + Microsoft Entra ID (free tier / trial is sufficient for lab work)
- Microsoft Defender XDR trial or E5 sandbox tenant for Advanced Hunting
- Python 3.8+, Azure CLI, Git
- Basic KQL familiarity; the linked [`101-cybersecurity-analyst`](https://github.com/CyberZag/101-cybersecurity-analyst) repository is a study roadmap, not a completed module set

---

## 🏗️ Real-World SOC Analyst Mapping

| Project | Real-World SOC Task | Job Role |
|---|---|---|
| 01 | Reviewing sign-in risk and hardening Conditional Access | Identity Security Analyst |
| 02 | Writing detections and automating first-response actions | Detection Engineer / Tier 2 SOC Analyst |
| 03 | Triaging and writing up a multi-stage incident | Tier 1/2 SOC Analyst, Incident Responder |

---

## ⚠️ Scope & Honesty Note

The KQL, JSON, scripts, and runbook are educational lab artifacts. They are not evidence of a production deployment, a live incident, or completed tenant validation. Review current Microsoft documentation, test in an authorized tenant, tune for the local schema, and use least-privilege credentials before relying on any artifact. The incident-response runbook is explicitly a simulated scenario, not a record of a real breach.

---

<div align="center">

**CyberZag Portfolio** · Azure Sentinel, SOAR & Identity Defense · SC-200 Track · 2026

</div>
