#!/usr/bin/env bash
# Lab 06: Create a service principal for GitHub Actions
# Source: Microsoft Learning - mslearn-mlops
set -euo pipefail

SP_NAME="${1:-ai300-lab-sp}"
SUBSCRIPTION_ID="${2:?Usage: $0 <sp-name> <subscription-id> <resource-group>}"
RESOURCE_GROUP="${3:?Usage: $0 <sp-name> <subscription-id> <resource-group>}"

echo "Creating service principal '${SP_NAME}'..."
echo "Scoped to: /subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${RESOURCE_GROUP}"

az ad sp create-for-rbac \
    --name "$SP_NAME" \
    --role contributor \
    --scopes "/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${RESOURCE_GROUP}" \
    --sdk-auth

echo ""
echo "Copy the JSON output above and add it as a GitHub secret named AZURE_CREDENTIALS."
echo "Also create these GitHub variables:"
echo "  AZURE_RESOURCE_GROUP = ${RESOURCE_GROUP}"
echo "  AZURE_WORKSPACE_NAME = <your-workspace-name>"
