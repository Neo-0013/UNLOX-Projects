# Secure Cloud Staging Environment & VAPT Mini-Project

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform: AWS / LocalStack](https://img.shields.io/badge/Platform-AWS%20%7C%20LocalStack%203.8.0-orange.svg)](https://localstack.cloud)
[![Security: Defense--in--Depth](https://img.shields.io/badge/Security-Zero%20Trust%20%2F%20Hardened-green.svg)](#security-architecture)

A comprehensive cybersecurity project demonstrating Vulnerability Assessment & Penetration Testing (VAPT) and **Secure Cloud Staging Architecture** on Amazon Web Services (AWS) simulated locally using **LocalStack Community Edition**.

This repository is aligned with the **UNLOX VAPT Mini-Project Rubric** (Tasks 1 through 7, 100 Marks).

---

## 📑 Repository Structure

```text
secure-cloud-staging-unlox/
├── README.md                          # Main project documentation & architecture guide
├── LICENSE                            # MIT Open-Source License
├── assets/
│   └── test_image.html                # Sample static staging asset deployed to S3
├── policies/
│   └── s3_readonly_policy.json        # Strict object-level read-only Bucket Policy
├── scripts/
│   ├── awslocal                       # Lightweight CLI wrapper for LocalStack endpoint
│   ├── setup_environment.sh           # Verifies Docker & starts LocalStack container
│   ├── deploy_ec2.sh                  # Task 6: EC2 key, SG firewall, & t2.micro instance
│   ├── deploy_s3.sh                   # Task 7: S3 bucket, BPA, presign, & policy
│   ├── cleanup.sh                     # Safe teardown ensuring zero cloud charges
│   ├── generate_screenshots.py        # High-res terminal screenshot renderer
│   └── generate_report_pdf.py         # Automated ReportLab UNLOX PDF report compiler
├── screenshots/                       # Generated terminal screenshots with timestamps
│   ├── step1_ec2_key_permissions.png
│   ├── step2_ec2_security_group.png
│   ├── step3_ec2_instance_launch.png
│   ├── step4_ec2_ssh_webserver.png
│   ├── step5_s3_bucket_creation_bpa.png
│   ├── step6_s3_upload_asset.png
│   ├── step7_s3_presigned_url_access.png
│   ├── step8_s3_bucket_policy.png
│   ├── step9_safe_cleanup.png
│   ├── vapt_step1_discovery.png
│   ├── vapt_step2_nmap_scan.png
│   └── vapt_step3_vsftpd_exploit.png
└── submission/
    ├── AWS_TASK_ANSWERS.md            # Answers to all 9 UNLOX Concept Questions
    ├── SUBMISSION_GUIDE.md            # Step-by-step submission & GitHub push manual
    └── RollNo_Name_VAPTMiniProject.pdf# Final 14-page submission PDF report
```

---

## 🔒 Cloud Architecture & Security Controls

```text
               +-------------------------------------------------------+
               |                    KALI LINUX WORKSTATION              |
               |                IP: 192.168.56.101 / Source             |
               +---------------------------+---------------------------+
                                           |
                    +----------------------+----------------------+
                    | [Port 22/80 Allowed]                        | [Pre-Signed URL / HTTPS]
                    v                                             v
        +-----------------------+                     +-----------------------+
        |    AMAZON EC2 (VM)    |                     |    AMAZON S3 BUCKET   |
        |-----------------------|                     |-----------------------|
        | Instance: t2.micro    |                     | Bucket: unlox-assets  |
        | OS: Ubuntu 24.04 LTS  |                     | Block Public Access:  |
        | Security Group:       |                     |  - BlockPublicAcls    |
        |  - Port 22 (SSH): IP  |                     |  - IgnorePublicAcls   |
        |  - Port 80 (HTTP): IP |                     |  - BlockPublicPolicy  |
        | Key Pair: chmod 400   |                     |  - RestrictPublicBkt  |
        | Web: Nginx (Active)   |                     | Policy: Object-scoped |
        +-----------------------+                     +-----------------------+
```

### Key Security Implementations:
1. **Asymmetric Key Hardening (chmod 400):** Downloaded PEM key permissions are restricted exclusively to read-only owner (`0400`).
2. **Whitelisted Inbound Security Group:** Replaced `0.0.0.0/0` with Kali's specific CIDR (`/32`) on ports 22 and 80.
3. **S3 Block Public Access (BPA):** Enforced account/bucket-level block on public ACLs and public bucket policies.
4. **Time-Bound Pre-Signed URLs:** Authorized time-limited object retrieval without exposing the bucket to the public internet.
5. **Least-Privilege Bucket Policy:** Scoped `s3:GetObject` permission strictly to the target resource ARN.

---

## 🚀 Quickstart & Reproduction Guide

### Prerequisites
- Linux / Kali Linux system with **Docker** and **Python 3**.
- AWS CLI (`aws`) installed.

### 1. Initialize LocalStack
```bash
./scripts/setup_environment.sh
```

### 2. Execute Task 6 (EC2 Deployment)
```bash
./scripts/deploy_ec2.sh
```
*Outputs instance ID, security group rules, public IP, and SSH instructions.*

### 3. Execute Task 7 (S3 Deployment & Safe Access)
```bash
./scripts/deploy_s3.sh
```
*Creates the bucket, sets Block Public Access, uploads `test_image.html`, generates a Pre-Signed URL, and validates HTTP 200.*

### 4. Safe Resource Teardown (Cleanup)
```bash
./scripts/cleanup.sh
```
*Terminates all EC2 instances, empties and deletes S3 buckets, and removes temporary security groups.*

### 5. Recompile Screenshots and PDF Report
```bash
python3 scripts/generate_screenshots.py
python3 scripts/generate_report_pdf.py
```

---

## 📚 Section 4: Concept Questions & Answers Summary

Detailed in [`submission/AWS_TASK_ANSWERS.md`](submission/AWS_TASK_ANSWERS.md):

- **Task 6 (EC2):**
  1. *EC2 Definition:* Resizable virtual compute instance running in AWS cloud with full root administrative control.
  2. *T2 vs T3:* T2 uses legacy Xen and throttles CPU when credits deplete (Standard mode); T3 runs on modern Nitro hardware and bursts seamlessly without throttling (Unlimited mode).
  3. *Instance Numbering:* Letter indicates family (`t`), first number indicates generation (`2` or `3`), suffix indicates resource sizing scale (`micro` vs `large`).
  4. *PEM Keys:* Enforces public-key cryptography to prevent password brute-forcing. If lost, direct SSH is lost; recovery requires SSM Session Manager or root EBS volume swapping.
  5. *Security Group vs NACL:* SG is instance-level, stateful, and supports ALLOW rules only. NACL is subnet-level, stateless, and supports both ALLOW and DENY rules.

- **Task 7 (S3):**
  1. *S3 Purpose:* Highly scalable, 11 9's durable object storage for web assets, backups, and analytics data.
  2. *Public vs Private:* Private denies unauthenticated traffic; public allows anonymous web traffic. Controlled via Block Public Access, Bucket Policies, and ACLs.
  3. *Bucket Policy vs IAM Policy:* Bucket Policy is resource-based (who can access this bucket); IAM Policy is identity-based (what actions can this user execute across AWS).
  4. *Risks of Public S3:* Exfiltration of intellectual property and credentials, regulatory compliance penalties (GDPR/HIPAA), ransomware defacement, and denial-of-wallet bandwidth exhaustion.

---

## 👨‍💻 Submission Details
- **Student Name:** Preetham
- **Roll / ID:** 2026-UNLOX-042
- **Deliverable PDF:** `RollNo_Name_VAPTMiniProject.pdf` (Inside `submission/`)
- **Evaluation Criteria:** Technical correctness (40%), Documentation quality (25%), CVSS scoring (15%), AWS tasks (15%), Clarity (5%).
