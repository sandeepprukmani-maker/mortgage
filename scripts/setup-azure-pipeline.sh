#!/bin/bash
# Automated Azure Pipeline Setup
# This script configures Azure DevOps Pipeline, Service Connection, and Environments

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}  Azure Pipeline Setup Automation${NC}"
echo -e "${BLUE}=========================================${NC}"
echo ""

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo -e "${RED}ERROR: Azure CLI not found${NC}"
    echo "Install: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
fi

# Check if Azure DevOps extension is installed
if ! az extension list | grep -q azure-devops; then
    echo -e "${YELLOW}Installing Azure DevOps extension...${NC}"
    az extension add --name azure-devops
fi

echo -e "${GREEN}✓ Azure CLI ready${NC}"
echo ""

# Login check
echo -e "${BLUE}Checking Azure login...${NC}"
if ! az account show &> /dev/null; then
    echo -e "${YELLOW}Please login to Azure:${NC}"
    az login
fi

SUBSCRIPTION_ID=$(az account show --query id -o tsv)
SUBSCRIPTION_NAME=$(az account show --query name -o tsv)
echo -e "${GREEN}✓ Logged in to Azure${NC}"
echo "  Subscription: $SUBSCRIPTION_NAME"
echo "  ID: $SUBSCRIPTION_ID"
echo ""

# Gather information
echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}  Configuration${NC}"
echo -e "${BLUE}=========================================${NC}"
echo ""

# Azure DevOps Organization
read -p "Enter your Azure DevOps organization name (e.g., vivantify-devops): " DEVOPS_ORG
if [ -z "$DEVOPS_ORG" ]; then
    echo -e "${RED}ERROR: Organization name required${NC}"
    exit 1
fi

# Project name
read -p "Enter project name [valargen-main]: " PROJECT_NAME
PROJECT_NAME=${PROJECT_NAME:-valargen-main}

# Repository name
read -p "Enter repository name [valargen-main]: " REPO_NAME
REPO_NAME=${REPO_NAME:-valargen-main}

# Staging VM details
echo ""
echo -e "${BLUE}Staging VM Configuration:${NC}"
read -p "Resource Group [valargen-staging-rg]: " STAGING_RG
STAGING_RG=${STAGING_RG:-valargen-staging-rg}

read -p "VM Name [valargen-staging-vm]: " STAGING_VM
STAGING_VM=${STAGING_VM:-valargen-staging-vm}

read -p "VM IP [4.227.184.143]: " STAGING_IP
STAGING_IP=${STAGING_IP:-4.227.184.143}

# Production VM details (optional)
echo ""
read -p "Configure production environment? (y/n): " SETUP_PROD
if [[ $SETUP_PROD =~ ^[Yy]$ ]]; then
    read -p "Production Resource Group: " PROD_RG
    read -p "Production VM Name: " PROD_VM
    read -p "Production VM IP: " PROD_IP
fi

echo ""
echo -e "${GREEN}Configuration Summary:${NC}"
echo "  Organization: $DEVOPS_ORG"
echo "  Project: $PROJECT_NAME"
echo "  Repository: $REPO_NAME"
echo "  Staging RG: $STAGING_RG"
echo "  Staging VM: $STAGING_VM"
echo ""
read -p "Continue with setup? (y/n): " CONFIRM
if [[ ! $CONFIRM =~ ^[Yy]$ ]]; then
    echo "Setup cancelled"
    exit 0
fi

echo ""
echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}  Starting Setup${NC}"
echo -e "${BLUE}=========================================${NC}"
echo ""

# Set default DevOps organization and project
export AZURE_DEVOPS_EXT_PAT_REQUIRED=true
az devops configure --defaults organization=https://dev.azure.com/$DEVOPS_ORG project=$PROJECT_NAME

# 1. Create Service Principal for deployment
echo -e "${BLUE}[1/6] Creating Service Principal...${NC}"
SP_NAME="valargen-pipeline-sp-$(date +%s)"
SP_JSON=$(az ad sp create-for-rbac \
    --name "$SP_NAME" \
    --role "Virtual Machine Contributor" \
    --scopes "/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$STAGING_RG" \
    --sdk-auth)

APP_ID=$(echo $SP_JSON | jq -r '.clientId')
CLIENT_SECRET=$(echo $SP_JSON | jq -r '.clientSecret')
TENANT_ID=$(echo $SP_JSON | jq -r '.tenantId')

echo -e "${GREEN}✓ Service Principal created${NC}"
echo "  App ID: $APP_ID"
echo ""

# Save credentials
echo "$SP_JSON" > .azure-credentials.json
chmod 600 .azure-credentials.json
echo -e "${YELLOW}⚠ Credentials saved to .azure-credentials.json (keep secure!)${NC}"
echo ""

# 2. Create Service Connection in Azure DevOps
echo -e "${BLUE}[2/6] Creating Service Connection...${NC}"

# Check if user has PAT configured
if [ -z "$AZURE_DEVOPS_EXT_PAT" ]; then
    echo -e "${YELLOW}Azure DevOps Personal Access Token (PAT) required${NC}"
    echo ""
    echo "Create a PAT at: https://dev.azure.com/$DEVOPS_ORG/_usersSettings/tokens"
    echo "Required scopes: Code (Read), Build (Read & Execute), Service Connections (Read, Query, Manage)"
    echo ""
    read -sp "Enter your PAT: " AZURE_DEVOPS_EXT_PAT
    export AZURE_DEVOPS_EXT_PAT
    echo ""
    echo ""
fi

# Create service endpoint
SERVICE_ENDPOINT_CONFIG=$(cat <<EOF
{
  "authorization": {
    "parameters": {
      "serviceprincipalid": "$APP_ID",
      "authenticationType": "spnKey",
      "serviceprincipalkey": "$CLIENT_SECRET",
      "tenantid": "$TENANT_ID"
    },
    "scheme": "ServicePrincipal"
  },
  "data": {
    "subscriptionId": "$SUBSCRIPTION_ID",
    "subscriptionName": "$SUBSCRIPTION_NAME",
    "environment": "AzureCloud",
    "creationMode": "Manual"
  },
  "name": "valargen-azure-connection",
  "type": "azurerm",
  "url": "https://management.azure.com/"
}
EOF
)

echo "$SERVICE_ENDPOINT_CONFIG" > /tmp/service-endpoint.json

az devops service-endpoint create \
    --service-endpoint-configuration /tmp/service-endpoint.json \
    --org https://dev.azure.com/$DEVOPS_ORG \
    --project $PROJECT_NAME \
    || echo -e "${YELLOW}Service connection may already exist${NC}"

rm /tmp/service-endpoint.json

echo -e "${GREEN}✓ Service Connection configured${NC}"
echo ""

# 3. Create Variable Group
echo -e "${BLUE}[3/6] Creating Variable Group...${NC}"

# Check if variable group exists
if az pipelines variable-group list --org https://dev.azure.com/$DEVOPS_ORG --project $PROJECT_NAME --query "[?name=='valargen-secrets'].id" -o tsv 2>/dev/null | grep -q .; then
    echo -e "${YELLOW}Variable group 'valargen-secrets' already exists, updating...${NC}"
    GROUP_ID=$(az pipelines variable-group list --org https://dev.azure.com/$DEVOPS_ORG --project $PROJECT_NAME --query "[?name=='valargen-secrets'].id" -o tsv)

    az pipelines variable-group variable update \
        --group-id $GROUP_ID \
        --name STAGING_VM_IP \
        --value "$STAGING_IP" \
        --org https://dev.azure.com/$DEVOPS_ORG \
        --project $PROJECT_NAME || true
else
    az pipelines variable-group create \
        --name valargen-secrets \
        --variables \
            STAGING_VM_IP="$STAGING_IP" \
            STAGING_RESOURCE_GROUP="$STAGING_RG" \
            STAGING_VM_NAME="$STAGING_VM" \
        --authorize true \
        --org https://dev.azure.com/$DEVOPS_ORG \
        --project $PROJECT_NAME
fi

if [[ $SETUP_PROD =~ ^[Yy]$ ]]; then
    GROUP_ID=$(az pipelines variable-group list --org https://dev.azure.com/$DEVOPS_ORG --project $PROJECT_NAME --query "[?name=='valargen-secrets'].id" -o tsv)

    az pipelines variable-group variable create \
        --group-id $GROUP_ID \
        --name PRODUCTION_VM_IP \
        --value "$PROD_IP" \
        --org https://dev.azure.com/$DEVOPS_ORG \
        --project $PROJECT_NAME || true

    az pipelines variable-group variable create \
        --group-id $GROUP_ID \
        --name PRODUCTION_RESOURCE_GROUP \
        --value "$PROD_RG" \
        --org https://dev.azure.com/$DEVOPS_ORG \
        --project $PROJECT_NAME || true

    az pipelines variable-group variable create \
        --group-id $GROUP_ID \
        --name PRODUCTION_VM_NAME \
        --value "$PROD_VM" \
        --org https://dev.azure.com/$DEVOPS_ORG \
        --project $PROJECT_NAME || true
fi

echo -e "${GREEN}✓ Variable Group created${NC}"
echo ""

# 4. Create Environments
echo -e "${BLUE}[4/6] Creating Environments...${NC}"

# Create staging environment
az devops invoke \
    --area distributedtask \
    --resource environments \
    --route-parameters project=$PROJECT_NAME \
    --http-method POST \
    --in-file /dev/stdin \
    --org https://dev.azure.com/$DEVOPS_ORG <<EOF || echo "Staging environment may already exist"
{
  "name": "staging",
  "description": "Staging environment for testing"
}
EOF

# Create production environment
az devops invoke \
    --area distributedtask \
    --resource environments \
    --route-parameters project=$PROJECT_NAME \
    --http-method POST \
    --in-file /dev/stdin \
    --org https://dev.azure.com/$DEVOPS_ORG <<EOF || echo "Production environment may already exist"
{
  "name": "production",
  "description": "Production environment - requires approval"
}
EOF

echo -e "${GREEN}✓ Environments created${NC}"
echo ""

# 5. Create Pipeline
echo -e "${BLUE}[5/6] Creating Pipeline...${NC}"

# Check if pipeline exists
if az pipelines list --org https://dev.azure.com/$DEVOPS_ORG --project $PROJECT_NAME --query "[?name=='valargen-main'].id" -o tsv 2>/dev/null | grep -q .; then
    echo -e "${YELLOW}Pipeline already exists${NC}"
else
    az pipelines create \
        --name valargen-main \
        --description "Valargen CI/CD Pipeline" \
        --repository $REPO_NAME \
        --repository-type tfsgit \
        --branch master \
        --yml-path azure-pipelines.yml \
        --skip-first-run \
        --org https://dev.azure.com/$DEVOPS_ORG \
        --project $PROJECT_NAME || echo -e "${YELLOW}Pipeline creation may require manual setup${NC}"
fi

echo -e "${GREEN}✓ Pipeline configured${NC}"
echo ""

# 6. Summary
echo -e "${BLUE}[6/6] Setup Complete!${NC}"
echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}  Setup Summary${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo -e "${GREEN}✓ Service Principal created${NC}"
echo "  Name: $SP_NAME"
echo "  App ID: $APP_ID"
echo ""
echo -e "${GREEN}✓ Service Connection: valargen-azure-connection${NC}"
echo -e "${GREEN}✓ Variable Group: valargen-secrets${NC}"
echo -e "${GREEN}✓ Environments: staging, production${NC}"
echo -e "${GREEN}✓ Pipeline: valargen-main${NC}"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo ""
echo "1. Add production approvers (if configured):"
echo "   https://dev.azure.com/$DEVOPS_ORG/$PROJECT_NAME/_settings/environments"
echo "   → Select 'production' → Approvals and checks → Add approval"
echo ""
echo "2. Test the pipeline:"
echo "   git commit -m \"Test: Pipeline setup\""
echo "   git push origin master"
echo ""
echo "3. Monitor deployment:"
echo "   https://dev.azure.com/$DEVOPS_ORG/$PROJECT_NAME/_build"
echo ""
echo -e "${YELLOW}⚠ IMPORTANT: Keep .azure-credentials.json secure!${NC}"
echo "   Add to .gitignore: echo '.azure-credentials.json' >> .gitignore"
echo ""
echo -e "${GREEN}Setup complete! 🎉${NC}"
