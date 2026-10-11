#!/usr/bin/env bash
# ==============================================================================
# Script: setup_environment.sh
# Objective: Verify Docker, launch LocalStack Community container, and configure awslocal
# Author: UNLOX Cloud Security Team / Student Submission
# ==============================================================================

set -euo pipefail

echo "[*] [$(date '+%Y-%m-%d %H:%M:%S')] Verifying Docker service..."
if ! command -v docker &>/dev/null; then
    echo "[!] Docker is not installed. Please install docker before proceeding."
    exit 1
fi

if ! docker ps &>/dev/null; then
    echo "[!] Docker daemon is not accessible. Make sure docker is running (sudo systemctl start docker)."
    exit 1
fi
echo "[+] Docker is operational."

CONTAINER_NAME="localstack_staging"
echo "[*] [$(date '+%Y-%m-%d %H:%M:%S')] Checking LocalStack container status..."
if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "[+] LocalStack container '${CONTAINER_NAME}' is already running."
elif docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "[*] Restarting existing LocalStack container..."
    docker start "${CONTAINER_NAME}"
else
    echo "[*] Spawning LocalStack Community container on port 4566..."
    docker run -d \
        --name "${CONTAINER_NAME}" \
        -p 4566:4566 \
        -e SERVICES=ec2,s3,iam \
        localstack/localstack:3.8.0
fi

echo "[*] Waiting for LocalStack services to become ready..."
for i in {1..30}; do
    if curl -s http://localhost:4566/_localstack/health | grep -q '"ec2": "available"'; then
        echo "[+] LocalStack EC2 and S3 endpoints are ready and healthy!"
        break
    fi
    sleep 2
done

# Ensure awslocal helper is available
mkdir -p "$HOME/.local/bin"
cat << 'AEOF' > "$HOME/.local/bin/awslocal"
#!/usr/bin/env bash
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1
exec aws --endpoint-url=http://localhost:4566 "$@"
AEOF
chmod +x "$HOME/.local/bin/awslocal"

echo "[+] Setup completed successfully at $(date '+%Y-%m-%d %H:%M:%S')."
