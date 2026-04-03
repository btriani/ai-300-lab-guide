#!/usr/bin/env bash
# Lab 05: Provision dev/prod MLOps environments
# Source: Microsoft Learning - mslearn-mlops
set -euo pipefail

REGION="${1:-swedencentral}"
PREFIX="${2:-ai300}"

echo "Creating dev environment..."
az group create --name "rg-${PREFIX}-dev" --location "$REGION" -o none
az ml workspace create --name "mlw-${PREFIX}-dev" --resource-group "rg-${PREFIX}-dev" --location "$REGION" -o none
az ml compute create --name "cc-${PREFIX}-dev" --type AmlCompute --size Standard_DS11_V2 --min-instances 0 --max-instances 2 --resource-group "rg-${PREFIX}-dev" --workspace-name "mlw-${PREFIX}-dev" -o none

echo "Creating prod environment..."
az group create --name "rg-${PREFIX}-prod" --location "$REGION" -o none
az ml workspace create --name "mlw-${PREFIX}-prod" --resource-group "rg-${PREFIX}-prod" --location "$REGION" -o none
az ml compute create --name "cc-${PREFIX}-prod" --type AmlCompute --size Standard_DS11_V2 --min-instances 0 --max-instances 4 --resource-group "rg-${PREFIX}-prod" --workspace-name "mlw-${PREFIX}-prod" -o none

echo "Creating shared registry..."
az ml registry create --name "reg-${PREFIX}" --resource-group "rg-${PREFIX}-dev" --location "$REGION" -o none

echo "Done. Dev, prod, and registry provisioned."
