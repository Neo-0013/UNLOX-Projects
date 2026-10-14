# UNLOX Cybersecurity & Cloud Projects Portfolio

[![Profile](https://img.shields.io/badge/GitHub-Neo--0013-blue.svg)](https://github.com/Neo-0013)
[![Academy](https://img.shields.io/badge/Academy-UNLOX-0284c7.svg)](https://unlox.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Security: Hardened](https://img.shields.io/badge/Security-Zero%20Trust%20%2F%20Hardened-green.svg)](#standards--evaluation-compliance)

A unified, modular repository containing hands-on cybersecurity, penetration testing, and cloud security engineering projects completed as part of the **UNLOX Academy** curriculum.

---

## 🗂️ Repository Architecture

This repository is structured modularly to house both mini-projects and future capstone/major projects in isolated, self-contained directories:

```text
UNLOX-Projects/
├── README.md                          # Master portfolio documentation & project index
├── LICENSE                            # MIT License
├── .gitignore                         # Git exclusion rules
│
├── mini-projects/                     # Hands-on technical mini-projects
│   ├── README.md                      # Mini-projects registry & syllabus tracking
│   ├── 03-vapt-cloud-staging/         # Mini-Project 3: VAPT Lifecycle & AWS Cloud Staging
│   └── cybersecurity-minor-project_4/ # Mini-Project 4: Digital Forensics & Incident Response
│       ├── README.md                  # Comprehensive technical writeup & architecture
│       ├── assets/                    # Static assets & landing pages
│       ├── policies/                  # Scoped AWS IAM / S3 Bucket policies
│       ├── scripts/                   # Automated deployment, testing & teardown scripts
│       ├── screenshots/               # High-resolution terminal evidence with timestamps
│       └── submission/                # Final deliverables (PDF report & concept answers)
│
└── major-projects/                    # Capstone & major projects
    └── README.md                      # Registry for upcoming major projects
```

---

## 📌 Projects Directory

### 🔹 Mini-Projects

| # | Project Title | Focus Areas | Target / Tech Stack | Status | Deliverables |
| :-: | :--- | :--- | :--- | :-: | :--- |
| **03** | [**VAPT & Secure Cloud Staging**](mini-projects/03-vapt-cloud-staging/) | Discovery, Port Scanning, CVE Exploit, CVSS v3.1, AWS EC2 & S3 Hardening | Metasploitable 2, Kali Linux, LocalStack 3.8, AWS CLI | **Completed (100/100)** | [Submission Files](mini-projects/03-vapt-cloud-staging/submission/) |
| **04** | [**Digital Forensics & Incident Response**](mini-projects/cybersecurity-minor-project_4/) | Autopsy Ingest Modules, Evidence Integrity, Hash Verification, Incident Reporting | Autopsy, Kali Linux, Sleuth Kit | **Completed** | [Submission Files](mini-projects/cybersecurity-minor-project_4/) |

### 🔹 Major Projects

| # | Project Title | Focus Areas | Tech Stack | Status |
| :-: | :--- | :--- | :--- | :-: |
| **01** | *Upcoming Major Project* | Advanced Security Assessment / Architecture | *TBD* | ⏳ Pending Assignment |

---

## 🚀 Standards & Evaluation Compliance
All submissions in this repository strictly adhere to UNLOX grading guidelines:
- **Technical Correctness (40%):** Reproducible, scripted commands with verifiable outputs.
- **Documentation Quality (25%):** Timestamped terminal evidence accompanied by technical justifications.
- **CVSS Scoring Accuracy (15%):** Official FIRST CVSS v3.1 vector strings, base scores, and justifications.
- **AWS Infrastructure (15%):** Zero-trust Security Group IP whitelisting, S3 Block Public Access, Pre-Signed URLs, and scoped resource policies.
- **Structure & Clarity (5%):** Clean modular layout and standardized reporting.
