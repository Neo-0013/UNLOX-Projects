# UNLOX VAPT & Cloud Security Project: Final Submission Guide

Follow this step-by-step checklist to finalize your project, push your repository to GitHub, and submit your official PDF report.

---

## Step 1: Personalize Student Details (Optional)

If your instructor assigned you an exact Roll Number or preferred format other than `2026-UNLOX-042` / `Preetham`:

1. Open `scripts/generate_report_pdf.py` in your text editor.
2. Edit lines 55, 137, and 138:
   ```python
   # Replace with your details:
   self.drawRightString(572, 755, "Confidential | RollNo: YOUR_ROLL_NO")
   Paragraph("YOUR_NAME", body_style),
   Paragraph("YOUR_ROLL_NO", body_style),
   ```
3. Re-run the PDF compiler:
   ```bash
   python3 scripts/generate_report_pdf.py
   ```
4. If you rename the output PDF to match your exact roll number and name (e.g., `2026UNLOX042_Preetham_VAPTMiniProject.pdf`), simply copy or rename:
   ```bash
   mv submission/RollNo_Name_VAPTMiniProject.pdf submission/2026UNLOX042_Preetham_VAPTMiniProject.pdf
   ```

---

## Step 2: Push Repository to GitHub

You need to provide a public or private GitHub repository link to your instructor / portal.

1. **Log in to GitHub** in your browser and create a new repository:
   - Repository Name: `secure-cloud-staging-unlox` (or `unlox-vapt-cloud-project`)
   - Description: `UNLOX Secure Cloud Staging Environment & VAPT Mini-Project`
   - Public / Private: As per your course instruction (usually Public or Private with instructor invited).
   - **Do not** initialize with README or .gitignore (we already have them created locally).

2. **In your Kali Terminal**, run:
   ```bash
   cd /home/neo/.gemini/antigravity/scratch/secure-cloud-staging-unlox

   # Stage and commit all files
   git add .
   git commit -m "feat: complete UNLOX VAPT and AWS cloud staging project with scripts, screenshots, and report"

   # Set branch to main
   git branch -M main

   # Add your remote URL (replace YOUR_USERNAME and REPO_NAME)
   git remote add origin https://github.com/YOUR_USERNAME/secure-cloud-staging-unlox.git

   # Push to GitHub
   git push -u origin main
   ```

---

## Step 3: Verify Your Deliverable PDF

The generated report is located at:
`submission/RollNo_Name_VAPTMiniProject.pdf`

Verify it adheres to all UNLOX grading requirements:
- [x] **Cover Page:** Student name, roll number, target assigned, assessment date, tools used.
- [x] **Section 1 (Scope & Objective):** Concise paragraph detailing targets and goals.
- [x] **Section 2 (Discovery):** ARP scan identifying live target with timestamped screenshot.
- [x] **Section 3 (Port & Service Scan):** Full Nmap command, screenshot, and formatted table of open ports, services, versions.
- [x] **Section 4 (Vulnerability Analysis):** vsftpd 2.3.4, Samba user map script, and UnrealIRCd with CVEs and weakness descriptions.
- [x] **Section 5 (Exploitation):** Step-by-step narrative of Metasploit execution with root shell screenshot.
- [x] **Section 6 (Demonstration & Impact):** Impact explanation in student's own words.
- [x] **Section 7 (CVSS Scoring Table):** Accurate CVSS v3.1 vectors, base scores, severity, and justifications.
- [x] **Section 8 (AWS Task Answers):** 9 embedded screenshots covering EC2 launch config, chmod 400, security group whitelist, running instance, SSH/Nginx test, S3 bucket creation, Block Public Access, static asset upload, Pre-Signed URL HTTP 200, bucket policy, and cleanup, followed by authoritative answers to all 9 concept questions.
- [x] **Section 9 (Conclusion & Recommendations):** Risk summary and 3 actionable remediation recommendations.

---

## Step 4: Final Submission

1. **Upload the PDF:** Submit `RollNo_Name_VAPTMiniProject.pdf` directly to the course portal.
2. **Submit Repository Link:** Paste your GitHub repository URL:
   `https://github.com/YOUR_USERNAME/secure-cloud-staging-unlox`
