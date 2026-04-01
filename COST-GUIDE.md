# Cost Guide

Realistic cost estimates for completing all 13 labs. Total: **~$15-30** depending on how quickly you work and whether you shut down resources between sessions.

## Per-Lab Cost Breakdown

| # | Lab | Compute | Model Calls | Other | Est. Total |
|---|-----|---------|-------------|-------|------------|
| 01 | AutoML & MLflow | ~$0.50-1.00 (cluster) | -- | Storage ~$0.01 | ~$1-2 |
| 02 | Sweep Jobs | ~$0.50-1.00 (cluster, multi-node) | -- | Storage ~$0.01 | ~$1-2 |
| 03 | Pipelines & Components | ~$0.50-1.00 (cluster) | -- | Storage ~$0.01 | ~$1-2 |
| 04 | Managed Online Endpoints | ~$0.50-1.50 (endpoint + instance) | -- | ACR ~$0.17 | ~$1-3 |
| 05 | Responsible AI Dashboard | ~$0.50-1.00 (cluster) | -- | Storage ~$0.01 | ~$1-2 |
| 06 | CI/CD with GitHub Actions | ~$0.50-1.00 (cluster via Actions) | -- | Storage ~$0.01 | ~$1-2 |
| 07 | MLOps End-to-End | ~$0.50-1.50 (cluster + endpoint) | -- | ACR ~$0.17 | ~$1-3 |
| 08 | Azure AI Foundry Basics | -- | GPT-4.1-mini: ~$0.05 | -- | <$1 |
| 09 | Prompt Flow | ~$0.50 (instance) | GPT-4.1-mini: ~$0.10 | -- | ~$1-2 |
| 10 | Content Safety & Filters | -- | GPT-4.1-mini: ~$0.05 | -- | <$1 |
| 11 | GenAI CI/CD with azd | -- | GPT-4.1-mini: ~$0.10 | App Service ~$0.50 | ~$1-2 |
| 12 | RAG Evaluation | -- | GPT-4.1: ~$0.50-1.00 | AI Search ~$0.50 | ~$1-2 |
| 13 | GenAIOps End-to-End | ~$0.50 (instance) | GPT-4.1: ~$1.00-2.00 | App Service ~$0.50 | ~$2-4 |

## Per-Service Pricing Reference

Prices as of early 2026. Always verify at [Azure Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/).

### Compute

| Service | SKU | Price |
|---------|-----|-------|
| Compute Instance | DS11_v2 | $0.171/hr |
| Compute Cluster | DS11_v2 | $0.171/hr/node (scales to 0 when idle) |
| Managed Online Endpoint | DS11_v2 | ~$0.17-0.21/hr (includes hosting overhead) |

### Models (Pay-as-you-go)

| Model | Input | Output |
|-------|-------|--------|
| GPT-4.1 | $2.00 / 1M tokens | $8.00 / 1M tokens |
| GPT-4.1-mini | $0.40 / 1M tokens | $1.60 / 1M tokens |

For lab exercises, typical token usage is low (a few thousand tokens per call). A full lab session rarely exceeds $1 in model costs.

### Supporting Services

| Service | Price | Notes |
|---------|-------|-------|
| Container Registry (Basic) | $0.167/day (~$5/mo) | Required for Labs 04, 07 |
| Application Insights | Free | Under 5 GB/mo ingestion |
| Blob Storage | $0.018/GB/mo | Negligible for lab data |
| Azure AI Search (Free tier) | $0 | Sufficient for Lab 12 |

## Stop the Billing Clock

### After MLOps Track (Labs 01-07)

These resources bill continuously if left running:

```bash
# Stop compute instance (biggest ongoing cost)
az ml compute stop --name your-instance-name \
  --resource-group your-resource-group \
  --workspace-name your-workspace-name

# Delete managed online endpoint (bills even with zero traffic)
az ml online-endpoint delete --name your-endpoint-name \
  --resource-group your-resource-group \
  --workspace-name your-workspace-name --yes

# Compute cluster scales to 0 automatically — no action needed
```

If you are done with the MLOps track and moving to GenAIOps, you can delete the entire resource group:

```bash
az group delete --name your-resource-group --yes --no-wait
```

### After GenAIOps Track (Labs 08-13)

```bash
# Delete azd-provisioned resources
azd down --purge

# If you created resources manually, delete the resource group
az group delete --name your-resource-group --yes --no-wait
```

## Full Cleanup

Run the cleanup script to remove all lab resources:

```bash
./scripts/cleanup.sh
```

This deletes resource groups, purges soft-deleted keys and AI services, and removes local azd state.

## Tips to Minimize Cost

1. **Stop your compute instance between labs.** This is the single biggest cost saver. A running instance costs ~$4/day even if you are not using it.
2. **Delete managed online endpoints immediately after testing.** They bill per-hour whether or not they receive traffic.
3. **Use early termination in AutoML (Lab 01).** Set a timeout of 15-20 minutes instead of letting it run longer. You will get a good enough model for learning purposes.
4. **Use the Free tier for Azure AI Search (Lab 12).** It is sufficient for the lab exercises.
5. **Use GPT-4.1-mini instead of GPT-4.1 for experimentation.** Switch to GPT-4.1 only when the lab specifically requires it.
6. **Batch your lab sessions.** Doing 2-3 labs in one sitting means fewer start/stop cycles and less risk of forgetting to shut things down.
7. **Set a budget alert.** In the Azure portal, go to Cost Management > Budgets and set a $30 alert so you get notified if something runs away.
