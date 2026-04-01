#!/usr/bin/env bash
# setup-mlops.sh -- Provision Azure ML resources for the MLOps track
set -euo pipefail

###############################################################################
# Configuration
###############################################################################
REGION="${1:-swedencentral}"
RG="rg-ai300-mlops"
WORKSPACE="mlw-ai300"
COMPUTE_INSTANCE="ci-ai300"
COMPUTE_CLUSTER="cc-ai300"
INSTANCE_SIZE="Standard_DS11_V2"
CLUSTER_SIZE="Standard_DS11_V2"
CLUSTER_MAX_NODES=2

MS_REPO="https://github.com/MicrosoftLearning/mslearn-azure-ml.git"
MS_REPO_DIR="mslearn-azure-ml"

###############################################################################
# Pre-flight checks
###############################################################################
echo "============================================"
echo "  MLOps Track Setup"
echo "============================================"
echo ""
echo "Region:            $REGION"
echo "Resource group:    $RG"
echo "Workspace:         $WORKSPACE"
echo "Compute instance:  $COMPUTE_INSTANCE ($INSTANCE_SIZE)"
echo "Compute cluster:   $COMPUTE_CLUSTER ($CLUSTER_SIZE, max $CLUSTER_MAX_NODES nodes)"
echo ""

if ! command -v az &>/dev/null; then
  echo "ERROR: Azure CLI (az) is not installed. Install it first."
  exit 1
fi

if ! az account show &>/dev/null; then
  echo "ERROR: Not logged in to Azure. Run 'az login' first."
  exit 1
fi

SUBSCRIPTION=$(az account show --query name -o tsv)
echo "Active subscription: $SUBSCRIPTION"
echo ""
read -rp "Proceed? (y/N) " confirm
[[ "$confirm" =~ ^[Yy]$ ]] || { echo "Aborted."; exit 0; }

###############################################################################
# 1. Register ML provider
###############################################################################
echo ""
echo "[1/7] Registering Microsoft.MachineLearningServices provider..."
az provider register --namespace Microsoft.MachineLearningServices --wait || true

###############################################################################
# 2. Create resource group
###############################################################################
echo "[2/7] Creating resource group '$RG' in $REGION..."
az group create --name "$RG" --location "$REGION" -o none

###############################################################################
# 3. Create workspace
###############################################################################
echo "[3/7] Creating Azure ML workspace '$WORKSPACE'..."
az ml workspace create \
  --name "$WORKSPACE" \
  --resource-group "$RG" \
  --location "$REGION" \
  -o none

# Set CLI defaults so subsequent commands omit -g / -w
az configure --defaults group="$RG" workspace="$WORKSPACE"

###############################################################################
# 4. Create compute instance
###############################################################################
echo "[4/7] Creating compute instance '$COMPUTE_INSTANCE'..."
az ml compute create \
  --name "$COMPUTE_INSTANCE" \
  --type ComputeInstance \
  --size "$INSTANCE_SIZE" \
  -o none

###############################################################################
# 5. Create compute cluster
###############################################################################
echo "[5/7] Creating compute cluster '$COMPUTE_CLUSTER'..."
az ml compute create \
  --name "$COMPUTE_CLUSTER" \
  --type AmlCompute \
  --size "$CLUSTER_SIZE" \
  --min-instances 0 \
  --max-instances "$CLUSTER_MAX_NODES" \
  -o none

###############################################################################
# 6. Clone MS repo and create data assets
###############################################################################
echo "[6/7] Cloning Microsoft Learning repo for data files..."
if [ ! -d "$MS_REPO_DIR" ]; then
  git clone "$MS_REPO" "$MS_REPO_DIR"
else
  echo "  Repo already cloned, pulling latest..."
  git -C "$MS_REPO_DIR" pull --ff-only
fi

echo "[7/7] Creating data assets..."

# diabetes-training (mltable)
MLTABLE_PATH="$MS_REPO_DIR/Labs/11/data"
if [ -d "$MLTABLE_PATH" ]; then
  echo "  Creating 'diabetes-training' (mltable)..."
  az ml data create \
    --name diabetes-training \
    --path "$MLTABLE_PATH" \
    --type mltable \
    -o none
else
  echo "  WARNING: MLTable data path not found at $MLTABLE_PATH -- skipping."
fi

# diabetes-data (uri_file)
CSV_PATH="$MS_REPO_DIR/Labs/11/data/diabetes.csv"
if [ -f "$CSV_PATH" ]; then
  echo "  Creating 'diabetes-data' (uri_file)..."
  az ml data create \
    --name diabetes-data \
    --path "$CSV_PATH" \
    --type uri_file \
    -o none
else
  # Fallback: try alternate location
  CSV_PATH="$MS_REPO_DIR/Labs/01/data/diabetes.csv"
  if [ -f "$CSV_PATH" ]; then
    echo "  Creating 'diabetes-data' (uri_file) from alternate path..."
    az ml data create \
      --name diabetes-data \
      --path "$CSV_PATH" \
      --type uri_file \
      -o none
  else
    echo "  WARNING: diabetes.csv not found -- skipping."
  fi
fi

###############################################################################
# Summary
###############################################################################
echo ""
echo "============================================"
echo "  Setup Complete"
echo "============================================"
echo ""
echo "  Resource Group:     $RG"
echo "  Workspace:          $WORKSPACE"
echo "  Region:             $REGION"
echo "  Compute Instance:   $COMPUTE_INSTANCE ($INSTANCE_SIZE)"
echo "  Compute Cluster:    $COMPUTE_CLUSTER ($CLUSTER_SIZE, max $CLUSTER_MAX_NODES)"
echo "  Data Assets:        diabetes-training (mltable)"
echo "                      diabetes-data (uri_file)"
echo ""
echo "  Studio URL:  https://ml.azure.com"
echo ""
echo "  CLI defaults set -- you can omit -g and -w in az ml commands."
echo "============================================"
