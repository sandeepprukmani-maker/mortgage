# Azure Pipeline Setup Guide

Complete guide to setting up CI/CD for Valargen using Azure Pipelines.

## Prerequisites

- Azure DevOps account
- Azure subscription
- Service Principal with VM access
- Repository connected to Azure DevOps

## Setup Steps

### 1. Create Azure DevOps Project

1. Go to [Azure DevOps](https://dev.azure.com)
2. Create new project: `valargen-main`
3. Connect to your Git repository

### 2. Create Service Connection

**Navigate to:** Project Settings → Service connections → New service connection

#### Create Azure Resource Manager Connection:

```
Connection name: valargen-azure-connection
Subscription: Your Azure subscription
Resource group: valargen-staging-rg (or leave blank for all)
Service principal: Auto-create or use existing
```

**Required permissions:**
- Virtual Machine Contributor
- Reader

**Grant access to all pipelines:** ✓

### 3. Create Variable Group

**Navigate to:** Pipelines → Library → + Variable group

#### Create Variable Group: `valargen-secrets`

Add these variables:

| Variable | Value | Secret? |
|----------|-------|---------|
| `STAGING_VM_IP` | 4.227.184.143 | No |
| `STAGING_RESOURCE_GROUP` | valargen-staging-rg | No |
| `STAGING_VM_NAME` | valargen-staging-vm | No |
| `PRODUCTION_VM_IP` | your-prod-ip | No |
| `PRODUCTION_RESOURCE_GROUP` | valargen-production-rg | No |
| `PRODUCTION_VM_NAME` | valargen-production-vm | No |

**Link to pipeline:** Allow all pipelines to access this variable group

### 4. Create Environments

**Navigate to:** Pipelines → Environments → New environment

#### Create Staging Environment:

```
Name: staging
Description: Staging environment for testing
Resource: None (manual)
Approvals: None (auto-deploy)
```

#### Create Production Environment:

```
Name: production
Description: Production environment
Resource: None (manual)
Approvals: Required ✓
  - Add approvers: Your team leads
  - Instructions: "Review staging deployment before approving"
```

### 5. Configure Pipeline

**Navigate to:** Pipelines → New pipeline

1. **Where is your code?** → Azure Repos Git
2. **Select repository:** valargen-main
3. **Configure pipeline:** Existing Azure Pipelines YAML file
4. **Path:** `/azure-pipelines.yml`
5. **Review and Run**

### 6. Configure VM for Azure Pipeline Deployment

SSH into each VM and ensure the project is set up:

```bash
# SSH to VM
ssh vg-admin@4.227.184.143

# Ensure project directory exists
sudo mkdir -p /home/valargen/valargen-main
sudo chown vg-admin:vg-admin /home/valargen/valargen-main

# Clone repository (if first time)
cd /home/valargen
git clone https://your-repo-url.git valargen-main

# Set up environment file
cd valargen-main
cp .env.staging.sample .env.staging
# Edit .env.staging with production values
nano .env.staging

# Ensure vg-admin has docker permissions
sudo usermod -aG docker vg-admin
```

## Pipeline Workflow

### Automatic Triggers:

```
Master Branch Commit
        ↓
   Build & Test
        ↓
   Deploy to Staging (auto)
        ↓
   Manual Approval
        ↓
   Deploy to Production
```

### What Happens on Each Stage:

#### Stage 1: Build & Test
- ✓ Checkout code
- ✓ Build Docker images
- ✓ Run tests (pytest)
- ✓ Run linter (ruff)
- ✓ Publish test results

#### Stage 2: Deploy to Staging (Auto)
- ✓ Deploy to staging VM via Azure CLI
- ✓ Pull latest code
- ✓ Build containers
- ✓ Backup database
- ✓ Stop old containers
- ✓ Start new containers
- ✓ Health check (30 attempts)
- ✓ Run migrations
- ✓ Verify deployment

#### Stage 3: Deploy to Production (Manual Approval)
- ⏸ Wait for approval
- ✓ Same steps as staging
- ✓ Deploy to production VM

## Testing the Pipeline

### Test with a Small Change:

```bash
# Make a small change
echo "# Test deployment" >> README.md

# Commit and push
git add README.md
git commit -m "Test: Azure Pipeline deployment"
git push origin master

# Watch pipeline in Azure DevOps
# Go to: Pipelines → valargen-main → Latest run
```

### Monitor Pipeline:

```
Pipelines → valargen-main
  → Click on latest run
  → View logs for each stage
  → Check test results
  → Verify deployment
```

## Troubleshooting

### Pipeline Fails at "Deploy to Staging VM"

**Error:** "az vm run-command failed"

**Solution:**
```bash
# Check if service connection has VM permissions
# In Azure Portal:
# IAM → Role assignments → Verify service principal has "Virtual Machine Contributor"
```

### Pipeline Fails at "Health Check"

**Error:** "Health check FAILED after 30 attempts"

**Solution:**
```bash
# SSH to VM and check logs
ssh vg-admin@4.227.184.143
cd /home/valargen/valargen-main
docker compose logs server
```

### Pipeline Fails at "Migrations"

**Error:** "Migrations: FAILED"

**Solution:**
```bash
# Check migration files and database connection
docker exec valargen-server /app/.venv/bin/alembic current
docker exec valargen-server /app/.venv/bin/alembic history
```

## Manual Deployment (Bypass Pipeline)

If you need to deploy manually without the pipeline:

```bash
# SSH to VM
ssh vg-admin@4.227.184.143

# Navigate to project
cd /home/valargen/valargen-main

# Run deployment script
./scripts/deploy.sh
```

## Rollback Procedure

### Via Pipeline:

1. Go to Pipelines → valargen-main
2. Find successful previous deployment
3. Click "Rerun pipeline"

### Manually on VM:

```bash
# SSH to VM
ssh vg-admin@4.227.184.143
cd /home/valargen/valargen-main

# Find previous commit
git log --oneline -10

# Rollback to previous commit
git checkout <commit-hash>

# Redeploy
./scripts/deploy.sh
```

## Best Practices

### Before Deploying:

- ✓ Run tests locally: `docker exec valargen-server pytest -v`
- ✓ Review PR changes
- ✓ Check staging deployment before production approval
- ✓ Communicate deployment to team

### After Deploying:

- ✓ Verify health endpoint
- ✓ Check application logs
- ✓ Test critical user flows
- ✓ Monitor for errors

### Security:

- ✓ Never commit `.env.staging` or `.env.prod`
- ✓ Rotate secrets regularly
- ✓ Use strong passwords
- ✓ Review service principal permissions
- ✓ Enable approval gates for production

## Pipeline Configuration Reference

### Trigger Configuration:

```yaml
trigger:
  branches:
    include:
      - master
  paths:
    exclude:
      - README.md
      - docs/**
```

**Triggers on:**
- Commits to master branch
- Excludes documentation-only changes

### Service Connection:

```yaml
azureSubscription: 'valargen-azure-connection'
```

**Must match:** Service connection name in Azure DevOps

### Variable Group:

```yaml
variables:
  - group: valargen-secrets
```

**Must match:** Variable group name in Library

### Environment:

```yaml
environment: 'production'
```

**Must match:** Environment name with approval configured

## Additional Resources

- [Azure Pipelines Documentation](https://docs.microsoft.com/en-us/azure/devops/pipelines/)
- [Azure CLI VM Commands](https://docs.microsoft.com/en-us/cli/azure/vm)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

## Support

For issues with the pipeline, check:

1. Pipeline run logs in Azure DevOps
2. VM logs: `docker compose logs`
3. Health endpoint: `curl https://app.staging.valargen.com/health`
4. Azure Portal for service principal permissions

## Next Steps

After pipeline is set up:

- [ ] Test deployment to staging
- [ ] Configure production environment
- [ ] Set up production approvals
- [ ] Document deployment schedule
- [ ] Train team on approval process
- [ ] Set up monitoring/alerts
