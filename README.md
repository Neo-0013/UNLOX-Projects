# UNLOX Cybersecurity & Cloud Projects Portfolio

[![Author](https://img.shields.io/badge/Author-Nawaz%20RK%20%28%40Neo--0013%29-blue.svg)](https://github.com/Neo-0013)
[![Roll No](https://img.shields.io/badge/Roll%20No-18206-orange.svg)](#student-profile)
[![Academy](https://img.shields.io/badge/Academy-UNLOX-0284c7.svg)](https://unlox.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A unified, modular repository containing all hands-on cybersecurity, penetration testing, and cloud security engineering projects completed as part of the **UNLOX Academy** curriculum.

---

## 👨‍💻 Student Profile
- **Student Name:** Nawaz RK
- **Roll Number / Student ID:** `18206`
- **GitHub Profile:** [@Neo-0013](https://github.com/Neo-0013)
- **Primary Workstation:** Kali Linux & VirtualBox Labs

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
│   └── 01-vapt-cloud-staging/         # Mini-Project 1: VAPT Lifecycle & AWS Cloud Staging
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

| # | Project Title | Focus Areas | Target / Tech Stack | Status | Deliverable |
| :-: | :--- | :--- | :--- | :-: | :--- |
| **01** | [**VAPT & Secure Cloud Staging**](mini-projects/01-vapt-cloud-staging/) | Discovery, Port Scanning, CVE Exploit, CVSS v3.1, AWS EC2 & S3 Hardening | Metasploitable 2, Kali Linux, LocalStack 3.8, AWS CLI | **Completed (100/100)** | [18206_NawazRK_VAPTMiniProject.pdf](mini-projects/01-vapt-cloud-staging/submission/18206_NawazRK_VAPTMiniProject.pdf) |

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
