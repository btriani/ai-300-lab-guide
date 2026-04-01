#!/usr/bin/env bash
# cleanup-all.sh -- Delete all lab resources to stop billing
set -euo pipefail

###############################################################################
# Configuration
###############################################################################
RESOURCE_GROUPS=(
  "rg-ai300-mlops"
  "rg-ai300-mlops-prod"
  "rg-ai300-genaiops"
)
WORKSPACE="mlw-ai300"
MLOps_RG="rg-ai300-mlops"
GENAIOPS_REPO_DIR="mslearn-genaiops"
SP_NAME="ai300-lab-sp"

###############################################################################
echo "============================================"
echo "  AI-300 Lab Cleanup"
echo "============================================"
echo ""
echo "This will DELETE the following:"
echo ""
for rg in "${RESOURCE_GROUPS[@]}"; do
  echo "  - Resource group: $rg"
done
echo "  - Online endpoints in $WORKSPACE"
echo "  - Service principal: $SP_NAME (if it exists)"
echo "  - azd environment (if present)"
echo ""
echo "WARNING: This action is irreversible."
echo ""
read -rp "Proceed? (y/N) " confirm
[[ "$confirm" =~ ^[Yy]$ ]] || { echo "Aborted."; exit 0; }
echo ""

###############################################################################
# 1. Delete online endpoints (they are expensive)
###############################################################################
echo "[1/4] Deleting online endpoints..."
if az ml workspace show -n "$WORKSPACE" -g "$MLOps_RG" &>/dev/null; then
  ENDPOINTS=$(az ml online-endpoint list -g "$MLOps_RG" -w "$WORKSPACE" --query "[].name" -o tsv 2>/dev/null || true)
  if [ -n "$ENDPOINTS" ]; then
    while IFS= read -r ep; do
      echo "  Deleting endpoint: $ep"
      az ml online-endpoint delete -n "$ep" -g "$MLOps_RG" -w "$WORKSPACE" -y --no-wait || true
    done <<< "$ENDPOINTS"
  else
    echo "  No online endpoints found."
  fi
else
  echo "  Workspace not found -- skipping endpoint cleanup."
fi

###############################################################################
# 2. Delete resource groups (async for speed)
###############################################################################
echo ""
echo "[2/4] Deleting resource groups..."
for rg in "${RESOURCE_GROUPS[@]}"; do
  if az group exists --name "$rg" -o tsv 2>/dev/null | grep -qi true; then
    echo "  Deleting $rg (async)..."
    az group delete --name "$rg" --yes --no-wait
  else
    echo "  $rg does not exist -- skipping."
  fi
done

###############################################################################
# 3. Delete service principal
###############################################################################
echo ""
echo "[3/4] Deleting service principal '$SP_NAME'..."
SP_ID=$(az ad sp list --display-name "$SP_NAME" --query "[0].id" -o tsv 2>/dev/null || true)
if [ -n "$SP_ID" ]; then
  az ad sp delete --id "$SP_ID"
  echo "  Deleted."
else
  echo "  Not found -- skipping."
fi

###############################################################################
# 4. Run azd down (GenAIOps)
###############################################################################
echo ""
echo "[4/4] Running azd down..."
if [ -d "$GENAIOPS_REPO_DIR" ]; then
  pushd "$GENAIOPS_REPO_DIR" > /dev/null
  if azd env list &>/dev/null; then
    azd down --force --purge || echo "  azd down completed (or no environment active)."
  else
    echo "  No azd environment found."
  fi
  popd > /dev/null
else
  echo "  GenAIOps repo directory not found -- skipping azd down."
fi

###############################################################################
# Reset CLI defaults
###############################################################################
az configure --defaults group="" workspace="" 2>/dev/null || true

###############################################################################
# Summary
###############################################################################
echo ""
echo "============================================"
echo "  Cleanup Complete"
echo "============================================"
echo ""
echo "  Resource groups are being deleted asynchronously."
echo "  Full deletion may take 5-10 minutes."
echo ""
echo "  Verify in the Azure Portal:"
echo "    https://portal.azure.com/#view/HubsExtension/BrowseResourceGroups"
echo ""
echo "  All billable resources have been removed or are"
echo "  being removed. No further charges will accrue"
echo "  once deletion completes."
echo "============================================"
