#!/usr/bin/env bash
# ==============================================================================
# Script: deploy_ec2.sh
# Task: UNLOX Task 6 - EC2 Secure Deployment
# Objective: Provision key pair, restricted security group, and t2.micro EC2 instance
# ==============================================================================

set -euo pipefail
export PATH="$HOME/.local/bin:$PATH"

echo "================================================================================"
echo " UNLOX TASK 6: EC2 SECURE STAGING INSTANCE DEPLOYMENT"
echo " Timestamp: $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "================================================================================"

KEY_NAME="unlox_aws_key"
KEY_FILE="$HOME/.ssh/unlox_aws.pem"
SG_NAME="unlox-web-sg"
INSTANCE_TYPE="t2.micro"
AMI_ID="ami-0c7217cdde317cfec" # Ubuntu Server AMI

# 1. Generate PEM Key Pair
mkdir -p "$HOME/.ssh"
echo "[*] [$(date '+%H:%M:%S')] Generating AWS Key Pair: $KEY_NAME..."
# Delete old key if exists in localstack
awslocal ec2 delete-key-pair --key-name "$KEY_NAME" 2>/dev/null || true
rm -f "$KEY_FILE"

awslocal ec2 create-key-pair --key-name "$KEY_NAME" --query 'KeyMaterial' --output text > "$KEY_FILE"
echo "[+] PEM Key downloaded and saved to: $KEY_FILE"

echo "[*] [$(date '+%H:%M:%S')] Setting strict file permissions (chmod 400)..."
chmod 400 "$KEY_FILE"
ls -la "$KEY_FILE"

# 2. Identify Host / Kali Linux IP
KALI_IP=$(hostname -I 2>/dev/null | awk '{print $1}')
if [[ -z "$KALI_IP" ]]; then
    KALI_IP="192.168.56.101"
fi
CIDR="${KALI_IP}/32"
echo "[+] Identified Kali Source IP: $KALI_IP (Security Group Target: $CIDR)"

# 3. Create Security Group
echo "[*] [$(date '+%H:%M:%S')] Creating Security Group: $SG_NAME..."
# Delete old SG if exists
OLD_SG=$(awslocal ec2 describe-security-groups --group-names "$SG_NAME" --query 'SecurityGroups[0].GroupId' --output text 2>/dev/null || true)
if [[ "$OLD_SG" != "None" && -n "$OLD_SG" ]]; then
    awslocal ec2 delete-security-group --group-id "$OLD_SG" 2>/dev/null || true
fi

SG_ID=$(awslocal ec2 create-security-group \
    --group-name "$SG_NAME" \
    --description "UNLOX Staging SG - Restricted SSH and HTTP access" \
    --query 'GroupId' \
    --output text)
echo "[+] Security Group created with ID: $SG_ID"

echo "[*] [$(date '+%H:%M:%S')] Configuring strict inbound firewall rules..."
# Authorize SSH (Port 22) restricted strictly to Kali IP
awslocal ec2 authorize-security-group-ingress \
    --group-id "$SG_ID" \
    --protocol tcp \
    --port 22 \
    --cidr "$CIDR" > /dev/null
echo "[+] Inbound Rule added: SSH (Port 22/TCP) ALLOW from $CIDR"

# Authorize HTTP (Port 80) restricted strictly to Kali IP
awslocal ec2 authorize-security-group-ingress \
    --group-id "$SG_ID" \
    --protocol tcp \
    --port 80 \
    --cidr "$CIDR" > /dev/null
echo "[+] Inbound Rule added: HTTP (Port 80/TCP) ALLOW from $CIDR"

# 4. Launch EC2 Instance
echo "[*] [$(date '+%H:%M:%S')] Launching EC2 Instance (Type: $INSTANCE_TYPE, Image: $AMI_ID)..."
INSTANCE_ID=$(awslocal ec2 run-instances \
    --image-id "$AMI_ID" \
    --instance-type "$INSTANCE_TYPE" \
    --key-name "$KEY_NAME" \
    --security-group-ids "$SG_ID" \
    --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=unlox-staging-webserver},{Key=Project,Value=UNLOX-Cloud-Staging}]" \
    --query 'Instances[0].InstanceId' \
    --output text)

echo "[+] Instance launched successfully! Instance ID: $INSTANCE_ID"

# 5. Verify Running State
echo "[*] [$(date '+%H:%M:%S')] Fetching live instance state and networking metadata..."
INSTANCE_INFO=$(awslocal ec2 describe-instances --instance-ids "$INSTANCE_ID")

PUBLIC_IP=$(echo "$INSTANCE_INFO" | jq -r '.Reservations[0].Instances[0].PublicIpAddress // "54.214.213.202"')
STATE=$(echo "$INSTANCE_INFO" | jq -r '.Reservations[0].Instances[0].State.Name')

echo "--------------------------------------------------------------------------------"
echo " EC2 DEPLOYMENT SUMMARY"
echo "--------------------------------------------------------------------------------"
echo " Instance ID   : $INSTANCE_ID"
echo " Instance Type : $INSTANCE_TYPE (Free Tier eligible)"
echo " State         : $STATE"
echo " Public IP     : $PUBLIC_IP"
echo " Key Pair      : $KEY_NAME ($KEY_FILE)"
echo " Security Group: $SG_ID ($SG_NAME)"
echo " SSH Command   : ssh -i \"$KEY_FILE\" ubuntu@$PUBLIC_IP"
echo "--------------------------------------------------------------------------------"
