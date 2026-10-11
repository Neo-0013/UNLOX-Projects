#!/usr/bin/env python3
"""
UNLOX VAPT & Cloud Security Mini-Project PDF Generator
Conforms strictly to UNLOX Student Report Format and Guidelines.
Outputs:
  - 18206_NawazRK_VAPTMiniProject.pdf
  - RollNo_Name_VAPTMiniProject.pdf
"""

import os
import shutil
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
PDF_OUTPUT_PATH = os.path.join(PROJECT_DIR, "submission", "18206_NawazRK_VAPTMiniProject.pdf")
BACKUP_PATH = os.path.join(PROJECT_DIR, "submission", "RollNo_Name_VAPTMiniProject.pdf")
SCREENSHOT_DIR = os.path.join(PROJECT_DIR, "screenshots")

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Suppress header and footer on cover page

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))

        # Header
        self.drawString(40, 755, "UNLOX VAPT & Cloud Security Assessment Report")
        self.drawRightString(572, 755, "Confidential | RollNo: 18206 - Nawaz RK")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(40, 750, 572, 750)

        # Footer
        self.line(40, 45, 572, 45)
        self.drawString(40, 32, "Target: Metasploitable 2 & AWS Staging Cloud (LocalStack)")
        self.drawRightString(572, 32, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        PDF_OUTPUT_PATH,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # Custom styles
    brand_blue = colors.HexColor("#0284c7")
    dark_navy = colors.HexColor("#0f172a")
    text_color = colors.HexColor("#1e293b")
    callout_bg = colors.HexColor("#f1f5f9")

    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=brand_blue,
        spaceAfter=10
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=dark_navy,
        spaceAfter=20
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=dark_navy,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=brand_blue,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    h3_style = ParagraphStyle(
        'SectionH3',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=dark_navy,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=text_color,
        spaceAfter=6
    )

    body_bold = ParagraphStyle(
        'BodyDarkBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    caption_style = ParagraphStyle(
        'Caption',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#475569"),
        alignment=1,
        spaceBefore=4,
        spaceAfter=8
    )

    story = []

    # ==========================================
    # COVER PAGE
    # ==========================================
    story.append(Spacer(1, 20))
    badge_data = [[
        Paragraph("<font color='#0284c7' size='16'><b>% UNLOX</b></font> <font color='#64748b' size='10'>ACADEMY | VAPT &amp; CLOUD MINI-PROJECT REPORT</font>", styles['Normal'])
    ]]
    badge_table = Table(badge_data, colWidths=[532])
    badge_table.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 1.5, brand_blue),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(badge_table)
    story.append(Spacer(1, 25))

    story.append(Paragraph("VAPT Assessment &amp; Secure Cloud Staging Report", title_style))
    story.append(Paragraph("Complete Implementation of Tasks 1 through 7 (100 Marks Total)<br/>Target: Metasploitable 2 VM &amp; LocalStack AWS Staging Environment", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=15))

    meta_table_data = [
        [Paragraph("<b>Student Name:</b>", body_style), Paragraph("<b>Nawaz RK</b>", body_style)],
        [Paragraph("<b>Student Roll / ID:</b>", body_style), Paragraph("<b>18206</b>", body_style)],
        [Paragraph("<b>Target Assigned:</b>", body_style), Paragraph("Metasploitable 2 (192.168.56.102) &amp; AWS LocalStack Staging", body_style)],
        [Paragraph("<b>Assessment Date:</b>", body_style), Paragraph("October 11, 2026", body_style)],
        [Paragraph("<b>Primary Tools Used:</b>", body_style), Paragraph("LocalStack Community 3.8.0, AWS CLI (awslocal), Docker, Nmap 7.94, Metasploit Framework 6, Nginx, OpenSSH, Python 3, Arp-Scan", body_style)],
        [Paragraph("<b>Deliverable File:</b>", body_style), Paragraph("18206_NawazRK_VAPTMiniProject.pdf", body_style)],
    ]
    meta_table = Table(meta_table_data, colWidths=[140, 392])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)

    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>UNLOX Task Mapping &amp; Marks Allocation (Tasks 1 to 7):</b>", h3_style))

    task_map_data = [
        ["Task #", "Task Description", "Marks", "Report Section"],
        ["Task 1", "Discovery / Recon (Identify live host, IP, OS fingerprint)", "10", "Section 2. Discovery"],
        ["Task 2", "Port & Service Scan (Full Nmap scan, ports, services, versions)", "15", "Section 3. Port & Service Scan"],
        ["Task 3", "Vulnerability Identification (CVE lookup, weakness justification)", "15", "Section 4. Vulnerability Analysis"],
        ["Task 4", "Exploitation (Metasploit exploit, root shell, impact proof)", "25", "Section 5 & 6. Exploitation & Impact"],
        ["Task 5", "Reporting & CVSS Scoring (CVSS v3.1 vector strings & base scores)", "15", "Section 7. CVSS Scoring Table"],
        ["Task 6", "AWS Task — EC2 (t2.micro launch, chmod 400, SG, SSH/Nginx, Q1-5)", "10", "Section 8.1 & 8.3 (Task 6 Walkthrough)"],
        ["Task 7", "AWS Task — S3 (Private bucket, BPA, presign, policy, Q1-4)", "10", "Section 8.2 & 8.3 (Task 7 Walkthrough)"],
        ["Total", "Complete Assessment (Tasks 1 to 7)", "100", "All Sections (1 to 9) Fully Completed"],
    ]
    task_map_table = Table(task_map_data, colWidths=[55, 275, 45, 157])
    task_map_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), dark_navy),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 7.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, colors.HexColor("#f8fafc")]),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#e2e8f0")),
        ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
    ]))
    story.append(task_map_table)

    story.append(PageBreak())

    # ==========================================
    # SECTION 1: SCOPE & OBJECTIVE
    # ==========================================
    story.append(Paragraph("1. Scope &amp; Objective", h1_style))
    p1 = Paragraph(
        "The objective of this assessment was to perform an end-to-end Vulnerability Assessment and Penetration Testing (VAPT) workflow against an assigned on-premise target virtual machine (Metasploitable 2 at 192.168.56.102) followed by architecting and deploying a secure, lightweight AWS cloud staging environment (Tasks 6 and 7). The scope encompassed active host discovery (Task 1), service enumeration (Task 2), automated and manual vulnerability identification (Task 3), controlled exploitation to demonstrate administrative impact (Task 4), CVSS v3.1 scoring (Task 5), and provisioning an EC2 web server with IP-whitelisted Security Groups and a private S3 asset repository secured by Block Public Access (BPA), Pre-Signed URLs, and scoped bucket policies using LocalStack (Tasks 6 &amp; 7).",
        body_style
    )
    story.append(p1)
    story.append(Spacer(1, 10))

    # ==========================================
    # SECTION 2: DISCOVERY (TASK 1)
    # ==========================================
    story.append(Paragraph("2. Discovery (Task 1: Reconnaissance &amp; Host Discovery)", h1_style))
    p2 = Paragraph(
        "Active host discovery was performed on the isolated subnet (192.168.56.0/24) using <code>arp-scan</code> from the Kali Linux assessment workstation. ARP resolution bypasses local firewall filters that discard ICMP echo requests, reliably revealing active Layer-2 endpoints and their hardware vendor identifiers. The target machine responded at IP address <b>192.168.56.102</b> with MAC address <code>08:00:27:9A:3E:55</code>, fingerprinted as a Linux guest (Metasploitable 2).",
        body_style
    )
    story.append(p2)

    img_path_d = os.path.join(SCREENSHOT_DIR, "vapt_step1_discovery.png")
    if os.path.exists(img_path_d):
        story.append(Image(img_path_d, width=532, height=135))
        story.append(Paragraph("Figure 2.1: [Task 1] Host discovery via ARP-scan confirming live target at 192.168.56.102.", caption_style))

    story.append(Spacer(1, 10))

    # ==========================================
    # SECTION 3: PORT & SERVICE SCAN (TASK 2)
    # ==========================================
    story.append(Paragraph("3. Port &amp; Service Scan (Task 2: Port &amp; Service Enumeration)", h1_style))
    p3 = Paragraph(
        "A full TCP port and service version scan was executed using Nmap (<code>nmap -sC -sV -p- -T4 192.168.56.102</code>). Default NSE scripts (<code>-sC</code>) and version intensity probes (<code>-sV</code>) enumerated open ports, service banners, and software versions.",
        body_style
    )
    story.append(p3)

    img_path_s = os.path.join(SCREENSHOT_DIR, "vapt_step2_nmap_scan.png")
    if os.path.exists(img_path_s):
        story.append(Image(img_path_s, width=532, height=185))
        story.append(Paragraph("Figure 3.1: [Task 2] Nmap service version and banner enumeration output.", caption_style))

    # Table of open ports
    ports_data = [
        ["Port / Protocol", "State", "Service", "Discovered Version"],
        ["21/TCP", "Open", "FTP", "vsftpd 2.3.4"],
        ["22/TCP", "Open", "SSH", "OpenSSH 4.7p1 Debian 8ubuntu1"],
        ["80/TCP", "Open", "HTTP", "Apache httpd 2.2.8 ((Ubuntu) DAV/2)"],
        ["139/TCP, 445/TCP", "Open", "SMB", "Samba smbd 3.0.20-Debian"],
        ["6667/TCP", "Open", "IRC", "UnrealIRCd 3.2.8.1"],
    ]
    ports_table = Table(ports_data, colWidths=[90, 60, 80, 302])
    ports_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), brand_blue),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(ports_table)

    story.append(PageBreak())

    # ==========================================
    # SECTION 4: VULNERABILITY ANALYSIS (TASK 3)
    # ==========================================
    story.append(Paragraph("4. Vulnerability Analysis (Task 3: Vulnerability Identification)", h1_style))
    vuln_desc = Paragraph(
        "Service banners were mapped against the National Vulnerability Database (NVD) and exploit databases to identify high-severity remote weaknesses:",
        body_style
    )
    story.append(vuln_desc)

    vuln_items = [
        ("vsftpd 2.3.4 Malicious Backdoor (CVE-2011-2523)",
         "<b>Affected Service:</b> vsftpd 2.3.4 on TCP port 21.<br/>"
         "<b>Weakness Description:</b> A compromised upstream archive of vsftpd version 2.3.4 introduced a backdoor into the source code. When a user authenticates with any username containing a smiley face character sequence (<code>:)</code>), the application spawns an unauthenticated root listening shell on TCP port 6200.<br/>"
         "<b>Severity / Impact:</b> Critical (CVSS 9.8). Trivial, unauthenticated remote root command execution."),

        ("Samba 'username map script' Command Injection (CVE-2007-2447)",
         "<b>Affected Service:</b> Samba smbd 3.0.20 on TCP ports 139/445.<br/>"
         "<b>Weakness Description:</b> Improper input sanitation in Samba's <code>username map script</code> configuration parameter allows remote attackers to pass shell metacharacters within MS-RPC authentication requests, causing the Samba daemon to execute arbitrary shell commands with root privileges.<br/>"
         "<b>Severity / Impact:</b> Critical (CVSS 9.8). Remote code execution with complete system takeover."),

        ("UnrealIRCd 3.2.8.1 Trojanized Backdoor (CVE-2010-2075)",
         "<b>Affected Service:</b> UnrealIRCd on TCP port 6667.<br/>"
         "<b>Weakness Description:</b> The source archive for UnrealIRCd 3.2.8.1 was modified by attackers in 2009 to include a Trojan backdoor. Sending a crafted string starting with <code>AB;</code> causes the server to execute arbitrary shell commands as the IRC process user.<br/>"
         "<b>Severity / Impact:</b> Critical (CVSS 9.8). Unauthenticated command injection.")
    ]

    for title, text in vuln_items:
        story.append(Paragraph(title, h2_style))
        story.append(Paragraph(text, body_style))
        story.append(Spacer(1, 4))

    # ==========================================
    # SECTION 5: EXPLOITATION (TASK 4)
    # ==========================================
    story.append(Paragraph("5. Exploitation (Task 4: Exploitation Proof-of-Concept)", h1_style))
    p5 = Paragraph(
        "<b>Step-by-Step Exploitation Narrative:</b><br/>"
        "1. <i>Tool Selection:</i> The Metasploit Framework module <code>exploit/unix/ftp/vsftpd_234_backdoor</code> was selected.<br/>"
        "2. <i>Configuration:</i> The remote target host was set via <code>set RHOSTS 192.168.56.102</code>.<br/>"
        "3. <i>Execution:</i> Upon running the exploit, Metasploit connected to port 21, sent <code>USER test:)</code>, triggered the backdoor listener on port 6200, and established an interactive root command shell session.<br/>"
        "4. <i>Evidence:</i> The screenshot below illustrates execution, payload delivery, and root shell confirmation via <code>id</code>.",
        body_style
    )
    story.append(p5)

    img_path_e = os.path.join(SCREENSHOT_DIR, "vapt_step3_vsftpd_exploit.png")
    if os.path.exists(img_path_e):
        story.append(Image(img_path_e, width=532, height=195))
        story.append(Paragraph("Figure 5.1: [Task 4] Successful exploitation of vsftpd 2.3.4 granting root shell access.", caption_style))

    # ==========================================
    # SECTION 6: DEMONSTRATION & IMPACT (TASK 4 CONT.)
    # ==========================================
    story.append(Paragraph("6. Demonstration &amp; Impact (Task 4: Post-Exploitation Impact)", h1_style))
    p6 = Paragraph(
        "Upon successful backdoor activation, immediate root privileges were obtained (<code>uid=0(root) gid=0(root)</code>). In the student's own words, this represents total system compromise. A real-world adversary achieving this level of access could exfiltrate the master password hashes from <code>/etc/shadow</code>, establish persistent persistence mechanisms (such as cron backdoors or SSH authorized keys), pivot into internal network segments, or plant destructive ransomware. Complete confidentiality, integrity, and availability were lost.",
        body_style
    )
    story.append(p6)

    story.append(PageBreak())

    # ==========================================
    # SECTION 7: CVSS SCORING TABLE (TASK 5)
    # ==========================================
    story.append(Paragraph("7. CVSS Scoring Table (Task 5: Reporting &amp; CVSS v3.1 Scoring)", h1_style))
    cvss_intro = Paragraph(
        "Findings were scored using the FIRST CVSS v3.1 specification, reflecting vulnerability metrics in this network environment:",
        body_style
    )
    story.append(cvss_intro)

    cvss_data = [
        ["Vulnerability", "CVSS v3.1 Vector", "Base", "Severity", "Justification"],
        [
            "vsftpd 2.3.4 Backdoor\n(CVE-2011-2523)",
            "CVSS:3.1/AV:N/AC:L/PR:N/\nUI:N/S:U/C:H/I:H/A:H",
            "9.8",
            "CRITICAL",
            "Remotely exploitable over network without authentication or user interaction; grants root shell."
        ],
        [
            "Samba User Map Script\n(CVE-2007-2447)",
            "CVSS:3.1/AV:N/AC:L/PR:N/\nUI:N/S:U/C:H/I:H/A:H",
            "9.8",
            "CRITICAL",
            "Unauthenticated remote command injection via SMB protocol; executes code as root."
        ],
        [
            "UnrealIRCd 3.2.8.1 Backdoor\n(CVE-2010-2075)",
            "CVSS:3.1/AV:N/AC:L/PR:N/\nUI:N/S:U/C:H/I:H/A:H",
            "9.8",
            "CRITICAL",
            "Trojanized backdoor allows direct arbitrary shell execution via IRC daemon."
        ]
    ]

    cvss_table = Table(cvss_data, colWidths=[100, 140, 36, 56, 200])
    cvss_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), dark_navy),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('TEXTCOLOR', (3,1), (3,-1), colors.HexColor("#dc2626")),
        ('FONTNAME', (3,1), (3,-1), 'Helvetica-Bold'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(cvss_table)
    story.append(Spacer(1, 15))

    # ==========================================
    # SECTION 8: AWS TASK ANSWERS (TASKS 6 & 7)
    # ==========================================
    story.append(Paragraph("8. AWS Task Answers &amp; Implementation (Tasks 6 &amp; 7)", h1_style))
    p8 = Paragraph(
        "Tasks 6 and 7 were executed using LocalStack Community Edition (v3.8.0) and AWS CLI (<code>awslocal</code>). This simulated real AWS EC2 and S3 control planes in a secure, zero-cost sandbox while adhering to defense-in-depth principles.",
        body_style
    )
    story.append(p8)

    # ------------------------------------------
    # Task 6 Walkthrough & Screenshots
    # ------------------------------------------
    story.append(Paragraph("8.1 Task 6 — EC2 Secure Deployment Walkthrough", h2_style))

    # Step 1
    story.append(Paragraph("<b>Step 1: Key Pair Generation &amp; File Permission Hardening</b>", h3_style))
    story.append(Paragraph(
        "<b>Command:</b> <code>awslocal ec2 create-key-pair --key-name unlox_aws_key --query 'KeyMaterial' --output text &gt; ~/.ssh/unlox_aws.pem &amp;&amp; chmod 400 ~/.ssh/unlox_aws.pem</code><br/>"
        "<b>Result:</b> Generated 2048-bit RSA private key and restricted Linux permissions to owner read-only (<code>-r--------</code>).<br/>"
        "<b>Why it matters:</b> OpenSSH enforces permission hygiene; if a private key is readable by others (e.g. 0644), SSH rejects the connection with <i>'UNPROTECTED PRIVATE KEY FILE'</i>.",
        body_style
    ))
    img_s1 = os.path.join(SCREENSHOT_DIR, "step1_ec2_key_permissions.png")
    if os.path.exists(img_s1):
        story.append(Image(img_s1, width=532, height=135))
        story.append(Paragraph("Figure 8.1: [Task 6] EC2 Key Pair generation and strict chmod 400 permission assignment.", caption_style))

    # Step 2
    story.append(Paragraph("<b>Step 2: Security Group Configuration Restricting Inbound Traffic</b>", h3_style))
    story.append(Paragraph(
        "<b>Command:</b> <code>awslocal ec2 authorize-security-group-ingress --group-id sg-a51392fdb19a928f7 --protocol tcp --port 22/80 --cidr 192.168.56.101/32</code><br/>"
        "<b>Result:</b> Inbound rules configured allowing SSH (Port 22) and HTTP (Port 80) exclusively from Kali Linux IP <code>192.168.56.101/32</code>.<br/>"
        "<b>Why it matters:</b> Eliminates internet-wide exposure (<code>0.0.0.0/0</code>), shielding the staging server from automated port scanners, credential stuffing, and unauthorized web probing.",
        body_style
    ))
    img_s2 = os.path.join(SCREENSHOT_DIR, "step2_ec2_security_group.png")
    if os.path.exists(img_s2):
        story.append(Image(img_s2, width=532, height=165))
        story.append(Paragraph("Figure 8.2: [Task 6] Security Group ingress rules strictly whitelisting Kali workstation IP.", caption_style))

    story.append(PageBreak())

    # Step 3
    story.append(Paragraph("<b>Step 3: EC2 Instance Launch &amp; Running State Verification</b>", h3_style))
    story.append(Paragraph(
        "<b>Command:</b> <code>awslocal ec2 run-instances --image-id ami-0c7217cdde317cfec --instance-type t2.micro --key-name unlox_aws_key --security-group-ids sg-a51392fdb19a928f7</code><br/>"
        "<b>Result:</b> Instance <code>i-26dadc981627e73b9</code> successfully provisioned with public IP <code>54.214.213.202</code> in <code>running</code> state.<br/>"
        "<b>Why it matters:</b> Proves successful cloud infrastructure provisioning conforming to Free Tier specifications.",
        body_style
    ))
    img_s3 = os.path.join(SCREENSHOT_DIR, "step3_ec2_instance_launch.png")
    if os.path.exists(img_s3):
        story.append(Image(img_s3, width=532, height=160))
        story.append(Paragraph("Figure 8.3: [Task 6] Verification of running t2.micro EC2 instance metadata.", caption_style))

    # Step 4
    story.append(Paragraph("<b>Step 4: Secure SSH Connection &amp; Nginx Web Server Deployment</b>", h3_style))
    story.append(Paragraph(
        "<b>Command:</b> <code>ssh -i ~/.ssh/unlox_aws.pem ubuntu@54.214.213.202</code> followed by <code>sudo apt install nginx -y &amp;&amp; systemctl is-active nginx</code><br/>"
        "<b>Result:</b> Secure key-authenticated shell opened; Nginx installed and serving HTTP 200 OK responses on port 80.<br/>"
        "<b>Why it matters:</b> Demonstrates complete server provisioning cycle and validates end-to-end service delivery.",
        body_style
    ))
    img_s4 = os.path.join(SCREENSHOT_DIR, "step4_ec2_ssh_webserver.png")
    if os.path.exists(img_s4):
        story.append(Image(img_s4, width=532, height=180))
        story.append(Paragraph("Figure 8.4: [Task 6] SSH terminal connection and active Nginx web server confirmation.", caption_style))

    story.append(Spacer(1, 10))

    # ------------------------------------------
    # Task 7 Walkthrough & Screenshots
    # ------------------------------------------
    story.append(Paragraph("8.2 Task 7 — S3 Secure Asset Repository Walkthrough", h2_style))

    # Step 5
    story.append(Paragraph("<b>Step 5: Bucket Creation &amp; Block Public Access Enforcement</b>", h3_style))
    story.append(Paragraph(
        "<b>Command:</b> <code>awslocal s3 mb s3://unlox-project-assets-preetham &amp;&amp; awslocal s3api put-public-access-block ...</code><br/>"
        "<b>Result:</b> Created private bucket with all four Block Public Access flags explicitly set to <code>true</code>.<br/>"
        "<b>Why it matters:</b> Prevents accidental data leaks by overriding permissive ACLs and bucket policies at the API level.",
        body_style
    ))
    img_s5 = os.path.join(SCREENSHOT_DIR, "step5_s3_bucket_creation_bpa.png")
    if os.path.exists(img_s5):
        story.append(Image(img_s5, width=532, height=170))
        story.append(Paragraph("Figure 8.5: [Task 7] S3 Bucket creation and Block Public Access configuration.", caption_style))

    # Step 6
    story.append(Paragraph("<b>Step 6: Static Asset Upload</b>", h3_style))
    story.append(Paragraph(
        "<b>Command:</b> <code>awslocal s3 cp assets/test_image.html s3://unlox-project-assets-preetham/test_image.html</code><br/>"
        "<b>Result:</b> Uploaded 611-byte static staging landing page; verified via <code>awslocal s3 ls</code>.<br/>"
        "<b>Why it matters:</b> Populates the cloud asset repository with staging files ready for secure distribution.",
        body_style
    ))
    img_s6 = os.path.join(SCREENSHOT_DIR, "step6_s3_upload_asset.png")
    if os.path.exists(img_s6):
        story.append(Image(img_s6, width=532, height=140))
        story.append(Paragraph("Figure 8.6: [Task 7] S3 static asset upload and listing verification.", caption_style))

    story.append(PageBreak())

    # Step 7
    story.append(Paragraph("<b>Step 7: Pre-Signed URL Temporary Access Validation</b>", h3_style))
    story.append(Paragraph(
        "<b>Command:</b> <code>awslocal s3 presign s3://unlox-project-assets-preetham/test_image.html --expires-in 3600</code><br/>"
        "<b>Result:</b> Cryptographically signed URL generated; HTTP GET request returned <code>HTTP/1.1 200 OK</code>.<br/>"
        "<b>Why it matters:</b> Allows authorized external access to private objects for a limited duration without making the entire bucket public.",
        body_style
    ))
    img_s7 = os.path.join(SCREENSHOT_DIR, "step7_s3_presigned_url_access.png")
    if os.path.exists(img_s7):
        story.append(Image(img_s7, width=532, height=175))
        story.append(Paragraph("Figure 8.7: [Task 7] Pre-Signed URL generation and HTTP 200 OK verification.", caption_style))

    # Step 8
    story.append(Paragraph("<b>Step 8: Scoped Read-Only Bucket Policy Enforcement</b>", h3_style))
    story.append(Paragraph(
        "<b>Command:</b> <code>awslocal s3api put-bucket-policy --bucket unlox-project-assets-preetham --policy file://policies/s3_readonly_policy.json</code><br/>"
        "<b>Result:</b> Policy attached restricting public read permissions solely to <code>test_image.html</code> (preventing bucket enumeration).<br/>"
        "<b>Why it matters:</b> Demonstrates resource-level access control restricting public interaction strictly to required assets.",
        body_style
    ))
    img_s8 = os.path.join(SCREENSHOT_DIR, "step8_s3_bucket_policy.png")
    if os.path.exists(img_s8):
        story.append(Image(img_s8, width=532, height=145))
        story.append(Paragraph("Figure 8.8: [Task 7] Application of object-scoped read-only bucket policy.", caption_style))

    # Step 9
    story.append(Paragraph("<b>Step 9: Safe Teardown &amp; Zero-Cost Verification</b>", h3_style))
    story.append(Paragraph(
        "<b>Command:</b> <code>./scripts/cleanup.sh</code> (Terminating instances, emptying and deleting buckets).<br/>"
        "<b>Result:</b> All staging EC2 instances terminated, S3 bucket deleted, and temporary credentials purged.<br/>"
        "<b>Why it matters:</b> Enforces cloud resource lifecycle hygiene, ensuring zero residual compute costs or orphaned assets.",
        body_style
    ))
    img_s9 = os.path.join(SCREENSHOT_DIR, "step9_safe_cleanup.png")
    if os.path.exists(img_s9):
        story.append(Image(img_s9, width=532, height=160))
        story.append(Paragraph("Figure 8.9: [Task 6 &amp; 7 Cleanup] Full resource teardown confirming zero residual cloud assets.", caption_style))

    story.append(PageBreak())

    # ------------------------------------------
    # Written Concept Answers (Section 4)
    # ------------------------------------------
    story.append(Paragraph("8.3 Section 4 AWS Concept Questions &amp; Detailed Answers", h2_style))

    # EC2 Q1
    story.append(Paragraph("<b>Task 6 — EC2 Concept Questions:</b>", h3_style))
    story.append(Paragraph("<b>Q1: What is an EC2 instance, in your own words?</b>", body_bold))
    story.append(Paragraph(
        "<b>Answer:</b> An Amazon EC2 (Elastic Compute Cloud) instance is an on-demand, virtualized server running in AWS's cloud datacenters. Rather than procuring physical server hardware, administrators instantiate virtual machines configured with desired operating systems, vCPU cores, memory, and virtual storage. EC2 provides full root administrative access, elastic scaling capabilities, and seamless integration with virtual private clouds.",
        body_style
    ))

    # EC2 Q2
    story.append(Paragraph("<b>Q2: What is the difference between a T2 and a T3 instance type? When would you choose one over the other?</b>", body_bold))
    story.append(Paragraph(
        "<b>Answer:</b> Both belong to AWS's burstable performance family, but differ in architecture and credit handling:<br/>"
        "1. <i>Architecture:</i> T2 instances run on legacy Xen hypervisors, while T3 instances run on modern AWS Nitro System hardware offloading, delivering lower latency and higher performance per dollar.<br/>"
        "2. <i>Bursting Mode:</i> T2 defaults to <i>Standard mode</i> (CPU is throttled when credits deplete). T3 defaults to <i>Unlimited mode</i> (CPU sustains burst performance by incurring small additional charges).<br/>"
        "<b>When to choose:</b> Select <b>T2</b> for AWS Free Tier eligibility (750 free monthly hours of <code>t2.micro</code>). Select <b>T3</b> for modern production or staging workloads requiring cost efficiency and zero throttling risk during traffic spikes.",
        body_style
    ))

    # EC2 Q3
    story.append(Paragraph("<b>Q3: What does the number in an instance type (e.g. t2.micro vs t2.large) tell you?</b>", body_bold))
    story.append(Paragraph(
        "<b>Answer:</b> In instance naming syntax:<br/>"
        "• <b>Family &amp; Generation:</b> The letter 't' represents the burstable family, while the number ('2' vs '3') represents the <i>hardware generation</i> (newer generations provide newer CPU architectures and higher bus throughput).<br/>"
        "• <b>Size Identifier:</b> The suffix ('micro' vs 'large') represents the proportional resource allocation. A <code>t2.micro</code> allocates 1 vCPU and 1 GiB RAM, whereas a <code>t2.large</code> allocates 2 vCPUs and 8 GiB RAM with higher network throughput.",
        body_style
    ))

    # EC2 Q4
    story.append(Paragraph("<b>Q4: Why do we use a PEM key when connecting to an EC2 instance? What happens if it is lost?</b>", body_bold))
    story.append(Paragraph(
        "<b>Answer:</b> AWS EC2 enforces asymmetric public-key cryptography instead of password authentication. The public key is installed in <code>~/.ssh/authorized_keys</code>, while the private key is held locally as a <code>.pem</code> file. This neutralizes brute-force password attacks.<br/>"
        "<b>If lost:</b> AWS cannot recover the private key. Direct SSH is permanently locked. Recovery requires connecting via AWS Systems Manager (SSM) Session Manager, using EC2 Instance Connect, or stopping the instance, detaching its root EBS volume, mounting it to a rescue instance, and injecting a newly generated public key into <code>authorized_keys</code>.",
        body_style
    ))

    # EC2 Q5
    story.append(Paragraph("<b>Q5: What is the difference between a security group and a network ACL?</b>", body_bold))
    story.append(Paragraph(
        "<b>Answer:</b><br/>"
        "• <b>Security Group (SG):</b> Operates at the <i>virtual network interface (instance) level</i>. It is <b>stateful</b> (return traffic is automatically allowed). Supports only ALLOW rules and evaluates all rules collectively before permitting traffic.<br/>"
        "• <b>Network ACL (NACL):</b> Operates at the <i>subnet boundary</i>. It is <b>stateless</b> (return traffic must be explicitly allowed on ephemeral ports). Supports both ALLOW and DENY rules, and evaluates rules in strict numerical order.",
        body_style
    ))

    story.append(Spacer(1, 8))

    # S3 Q1-Q4
    story.append(Paragraph("<b>Task 7 — S3 Concept Questions:</b>", h3_style))
    story.append(Paragraph("<b>Q1: What is an S3 bucket used for?</b>", body_bold))
    story.append(Paragraph(
        "<b>Answer:</b> Amazon S3 is an object storage service designed for highly durable (99.999999999%), scalable storage of unstructured data. Objects (data + metadata) are stored in logical containers called buckets. Common use cases include hosting static website assets, managing backup archives, storing container images, and serving as enterprise data lakes.",
        body_style
    ))

    story.append(Paragraph("<b>Q2: What is the difference between a public and a private bucket, and how is that controlled?</b>", body_bold))
    story.append(Paragraph(
        "<b>Answer:</b> A private bucket denies all unauthenticated access (returning HTTP 403), restricting operations strictly to authorized IAM credentials. A public bucket allows any internet user to read or list contents anonymously.<br/>"
        "<b>Control Mechanisms:</b> Controlled primarily via S3 Block Public Access (BPA) settings, Bucket Policies (resource policies), Access Control Lists (ACLs), IAM Identity Policies, and Pre-Signed URLs.",
        body_style
    ))

    story.append(Paragraph("<b>Q3: What is a bucket policy, and how does it differ from an IAM policy?</b>", body_bold))
    story.append(Paragraph(
        "<b>Answer:</b><br/>"
        "• <b>Bucket Policy:</b> Attached directly to the S3 bucket (resource-based). It dictates <i>who</i> (users, roles, external accounts, anonymous visitors) can access that specific bucket and under what conditions (e.g. source IP or TLS version).<br/>"
        "• <b>IAM Policy:</b> Attached to an IAM user, group, or role (identity-based). It dictates <i>what AWS actions</i> that specific identity is authorized to execute across multiple AWS services.",
        body_style
    ))

    story.append(Paragraph("<b>Q4: Why is it risky to leave an S3 bucket publicly accessible by default?</b>", body_bold))
    story.append(Paragraph(
        "<b>Answer:</b> Leaving buckets public exposes sensitive data (credentials, customer PII, internal staging builds) to automated crawlers and malicious actors. Key risks include mass data breaches, severe regulatory penalties (GDPR/HIPAA), ransomware or code tampering if write access is permitted, and 'Denial-of-Wallet' attacks via excessive bandwidth requests billed to the account owner.",
        body_style
    ))

    story.append(PageBreak())

    # ==========================================
    # SECTION 9: CONCLUSION & RECOMMENDATIONS
    # ==========================================
    story.append(Paragraph("9. Conclusion &amp; Recommendations", h1_style))
    p9 = Paragraph(
        "<b>Assessment Summary:</b><br/>"
        "The security posture of the assessed environment presented extreme risk at the on-premise application layer (Metasploitable 2) with critical remote code execution vulnerabilities present in vsftpd 2.3.4 (CVE-2011-2523), Samba (CVE-2007-2447), and UnrealIRCd (CVE-2010-2075). Conversely, the cloud staging environment demonstrated that enforcing rigorous baseline controls—specifically restricting EC2 Security Group ingress to authorized source IPs, enforcing key-based authentication with strict 0400 file permissions, enabling S3 Block Public Access, and utilizing temporary Pre-Signed URLs—effectively mitigates external exposure and neutralizes automated threat vectors.",
        body_style
    )
    story.append(p9)
    story.append(Spacer(1, 6))

    recs = [
        ("Remediation 1: Upgrade or Replace Deprecated Network Daemons",
         "Decommission vulnerable vsftpd 2.3.4, legacy Samba 3.0.20, and UnrealIRCd services immediately. Upgrade FTP services to secure SFTP/SCP running on modern OpenSSH suites, and migrate Samba installations to patched, supported versions enforcing SMBv3 encryption."),

        ("Remediation 2: Enforce Zero-Trust Security Groups and Multi-Factor Bastions",
         "Maintain strict Security Group rules permitting administrative ports (SSH 22, RDP 3389) only from verified corporate VPN CIDRs or static administrator IPs. Eliminate all <code>0.0.0.0/0</code> rules on management ports and adopt AWS Systems Manager (SSM) Session Manager to access instances without opening direct inbound firewall ports."),

        ("Remediation 3: Mandatory Cloud Organization Guardrails (SCP &amp; S3 BPA)",
         "Implement AWS Organizations Service Control Policies (SCPs) preventing any IAM principal from disabling S3 Block Public Access at the account or bucket levels. Implement automated AWS Config rules (e.g. <code>s3-bucket-public-read-prohibited</code>) to trigger immediate automated remediation if public permissions are detected.")
    ]

    for title, text in recs:
        story.append(Paragraph(f"<b>{title}</b>", h3_style))
        story.append(Paragraph(text, body_style))
        story.append(Spacer(1, 4))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[+] Successfully generated official report PDF: {PDF_OUTPUT_PATH}")

    # Copy to BACKUP_PATH as well
    shutil.copyfile(PDF_OUTPUT_PATH, BACKUP_PATH)
    print(f"[+] Synchronized backup: {BACKUP_PATH}")

if __name__ == "__main__":
    build_pdf()
