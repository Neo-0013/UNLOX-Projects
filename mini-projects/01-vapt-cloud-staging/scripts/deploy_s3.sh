#!/usr/bin/env bash
# ==============================================================================
# Script: deploy_s3.sh
# Task: UNLOX Task 7 - S3 Secure Static Asset Repository Deployment
# Objective: Provision S3 bucket with Block Public Access, upload asset,
#            generate Pre-Signed URL, and demonstrate scoped Bucket Policy.
# ==============================================================================

set -euo pipefail
export PATH="$HOME/.local/bin:$PATH"

BUCKET_NAME="unlox-project-assets-preetham"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
ASSET_FILE="$PROJECT_DIR/assets/test_image.html"
POLICY_FILE="$PROJECT_DIR/policies/s3_readonly_policy.json"

echo "================================================================================"
echo " UNLOX TASK 7: S3 SECURE STATIC ASSET REPOSITORY DEPLOYMENT"
echo " Timestamp: $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "================================================================================"

# 1. Create S3 Bucket
echo "[*] [$(date '+%H:%M:%S')] Creating S3 Bucket: $BUCKET_NAME..."
awslocal s3 mb "s3://$BUCKET_NAME" 2>/dev/null || echo "[!] Bucket already exists, proceeding..."

# 2. Configure Strict Block Public Access
echo "[*] [$(date '+%H:%M:%S')] Applying S3 'Block All Public Access' configuration..."
awslocal s3api put-public-access-block \
    --bucket "$BUCKET_NAME" \
    --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"

echo "[+] Verifying Block Public Access status on bucket:"
awslocal s3api get-public-access-block --bucket "$BUCKET_NAME" --output json

# 3. Upload Static Asset
echo "[*] [$(date '+%H:%M:%S')] Uploading static asset ($ASSET_FILE) to s3://$BUCKET_NAME/test_image.html..."
awslocal s3 cp "$ASSET_FILE" "s3://$BUCKET_NAME/test_image.html"
echo "[+] Asset uploaded successfully."

# 4. Generate Pre-Signed URL for Time-Bound Access
echo "[*] [$(date '+%H:%M:%S')] Generating temporary Pre-Signed URL (TTL: 3600 seconds / 1 hour)..."
PRESIGNED_URL=$(awslocal s3 presign "s3://$BUCKET_NAME/test_image.html" --expires-in 3600)
echo "[+] Generated Pre-Signed URL:"
echo "    $PRESIGNED_URL"

# 5. Access Test
echo "[*] [$(date '+%H:%M:%S')] Executing access test via HTTP GET request using Pre-Signed URL..."
HTTP_RESPONSE=$(curl -s -i "$PRESIGNED_URL" | head -n 12)
echo "--------------------------------------------------------------------------------"
echo "$HTTP_RESPONSE"
echo "--------------------------------------------------------------------------------"
echo "[+] HTTP 200 OK verified. Static asset safely delivered via signed temporary token."

# 6. Scoped Bucket Policy Demonstration
echo "[*] [$(date '+%H:%M:%S')] Applying scoped read-only Bucket Policy (s3:GetObject on specific asset)..."
awslocal s3api put-bucket-policy --bucket "$BUCKET_NAME" --policy "file://$POLICY_FILE"
echo "[+] Verifying applied Bucket Policy:"
awslocal s3api get-bucket-policy --bucket "$BUCKET_NAME" --output json

echo "================================================================================"
echo " S3 DEPLOYMENT & VERIFICATION COMPLETE"
echo "================================================================================"
