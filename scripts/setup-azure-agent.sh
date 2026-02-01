#!/bin/bash
# Setup Azure DevOps Self-Hosted Agent
# Run this on your VM (valargen-staging)

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}  Azure DevOps Agent Setup${NC}"
echo -e "${BLUE}=========================================${NC}"
echo ""

# Configuration
AGENT_DIR="$HOME/azagent"
ORG_URL="https://dev.azure.com/vivantify-devops"
POOL_NAME="Default"

# Check if agent already exists
if [ -d "$AGENT_DIR" ]; then
    echo -e "${YELLOW}Agent directory already exists at $AGENT_DIR${NC}"
    read -p "Remove and reinstall? (y/n): " REINSTALL
    if [[ $REINSTALL =~ ^[Yy]$ ]]; then
        cd "$AGENT_DIR"
        sudo ./svc.sh stop || true
        sudo ./svc.sh uninstall || true
        cd ..
        rm -rf "$AGENT_DIR"
    else
        echo "Setup cancelled"
        exit 0
    fi
fi

echo -e "${BLUE}[1/5] Creating agent directory...${NC}"
mkdir -p "$AGENT_DIR"
cd "$AGENT_DIR"

echo -e "${BLUE}[2/5] Downloading agent...${NC}"
AGENT_VERSION="3.236.1"
wget "https://vstsagentpackage.azureedge.net/agent/${AGENT_VERSION}/vsts-agent-linux-x64-${AGENT_VERSION}.tar.gz"
tar zxvf "vsts-agent-linux-x64-${AGENT_VERSION}.tar.gz"
rm "vsts-agent-linux-x64-${AGENT_VERSION}.tar.gz"

echo -e "${BLUE}[3/5] Installing dependencies...${NC}"
sudo ./bin/installdependencies.sh

echo ""
echo -e "${BLUE}[4/5] Configuring agent...${NC}"
echo ""
echo -e "${YELLOW}You'll need:${NC}"
echo "  1. PAT Token: ABWJGVi1aeeYUZwNEbYo1ttavjkDfYpl53tq0tfOeLMk5GudMMvQJQQJ99BLACAAAAAAAAAAAAASAZDOAL6q"
echo "  2. Agent pool: $POOL_NAME"
echo "  3. Agent name: valargen-staging-agent"
echo ""

./config.sh \
    --unattended \
    --url "$ORG_URL" \
    --auth pat \
    --token "ABWJGVi1aeeYUZwNEbYo1ttavjkDfYpl53tq0tfOeLMk5GudMMvQJQQJ99BLACAAAAAAAAAAAAASAZDOAL6q" \
    --pool "$POOL_NAME" \
    --agent "valargen-staging-agent" \
    --work "_work" \
    --acceptTeeEula \
    --replace

echo ""
echo -e "${BLUE}[5/5] Installing as service...${NC}"
sudo ./svc.sh install
sudo ./svc.sh start

echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}  Agent Setup Complete!${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo -e "${GREEN}✓ Agent installed at: $AGENT_DIR${NC}"
echo -e "${GREEN}✓ Running as service${NC}"
echo ""
echo "Check status: sudo ./svc.sh status"
echo "View logs: journalctl -u vsts.agent.vivantify-devops.Default.valargen-staging-agent -f"
echo ""
echo -e "${BLUE}Verify in Azure DevOps:${NC}"
echo "https://dev.azure.com/vivantify-devops/valargen-main/_settings/agentqueues"
echo ""
