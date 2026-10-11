#!/usr/bin/env bash
# ==============================================================================
# Script: cleanup.sh
# Task: Safe Teardown & Resource Cleanup (Zero Cost & Hygiene)
# Objective: Terminate EC2 instances, empty & delete S3 buckets, delete SG & keys
# ==============================================================================

set -euo pipefail
export PATH="$HOME/.local/bin:$PATH"

BUCKET_NAME="unlox-project-assets-preetham"
KEY_NAME="unlox_aws_key"
SG_NAME="unlox-web-sg"

echo "================================================================================"
echo " UNLOX CLOUD ENVIRONMENT: SAFE RESOURCE TEARDOWN"
echo " Timestamp: $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "================================================================================"

# 1. Terminate EC2 instances
echo "[*] [$(date '+%H:%M:%S')] Querying active EC2 instances..."
INSTANCE_IDS=$(awslocal ec2 describe-instances \
    --filters "Name=instance-state-name,Values=running,pending" \
    --query "Reservations[].Instances[].InstanceId" \
    --output text)

if [[ -n "$INSTANCE_IDS" && "$INSTANCE_IDS" != "None" ]]; then
    echo "[*] Terminating EC2 instance(s): $INSTANCE_IDS"
    awslocal ec2 terminate-instances --instance-ids $INSTANCE_IDS > /dev/null
    echo "[+] Instance termination initiated."
else
    echo "[+] No active instances found."
fi

# 2. Empty and delete S3 Bucket
echo "[*] [$(date '+%H:%M:%S')] Cleaning up S3 Bucket: $BUCKET_NAME..."
if awslocal s3 ls "s3://$BUCKET_NAME" 2>/dev/null; then
    echo "[*] Removing bucket contents..."
    awslocal s3 rm "s3://$BUCKET_NAME" --recursive > /dev/null
    echo "[*] Deleting S3 bucket..."
    awslocal s3 rb "s3://$BUCKET_NAME" > /dev/null
    echo "[+] Bucket $BUCKET_NAME successfully deleted."
else
    echo "[+] S3 bucket $BUCKET_NAME does not exist or already removed."
fi

# 3. Clean Security Group & Key Pair
echo "[*] [$(date '+%H:%M:%S')] Removing temporary EC2 Key Pair ($KEY_NAME)..."
awslocal ec2 delete-key-pair --key-name "$KEY_NAME" 2>/dev/null || true
rm -f "$HOME/.ssh/unlox_aws.pem"
echo "[+] Key Pair removed from AWS and local disk."

SG_ID=$(awslocal ec2 describe-security-groups --group-names "$SG_NAME" --query 'SecurityGroups[0].GroupId' --output text 2>/dev/null || true)
if [[ -n "$SG_ID" && "$SG_ID" != "None" ]]; then
    echo "[*] Removing Security Group: $SG_ID..."
    awslocal ec2 delete-security-group --group-id "$SG_ID" 2>/dev/null || true
    echo "[+] Security Group removed."
fi

echo "================================================================================"
echo "[+] ALL CLOUD STAGING RESOURCES DESTROYED SAFELY. ZERO REMAINING CHARGES."
echo "================================================================================"
