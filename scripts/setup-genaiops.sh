#!/usr/bin/env bash
# setup-genaiops.sh -- Provision Azure AI Foundry resources for the GenAIOps track
set -euo pipefail

###############################################################################
# Configuration
###############################################################################
MS_REPO="https://github.com/MicrosoftLearning/mslearn-genaiops.git"
MS_REPO_DIR="mslearn-genaiops"
AZD_ENV_NAME="ai300-genaiops"
VENV_DIR=".venv"

###############################################################################
# Pre-flight checks
###############################################################################
echo "============================================"
echo "  GenAIOps Track Setup"
echo "============================================"
echo ""

# Check azd
if ! command -v azd &>/dev/null; then
  echo "ERROR: Azure Developer CLI (azd) is not installed."
  echo ""
  echo "Install it:"
  echo "  macOS:   brew install azure-dev"
  echo "  Linux:   curl -fsSL https://aka.ms/install-azd.sh | bash"
  echo "  Windows: winget install microsoft.azd"
  exit 1
fi
echo "[OK] azd found: $(azd version)"

# Check az
if ! command -v az &>/dev/null; then
  echo "ERROR: Azure CLI (az) is not installed."
  exit 1
fi
echo "[OK] az  found: $(az version --query '\"azure-cli\"' -o tsv)"

# Check Python
if ! command -v python3 &>/dev/null; then
  echo "ERROR: Python 3 is not installed."
  exit 1
fi
PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo "[OK] Python found: $PYTHON_VERSION"

# Check git
if ! command -v git &>/dev/null; then
  echo "ERROR: git is not installed."
  exit 1
fi
echo "[OK] git found"

echo ""

###############################################################################
# 1. Clone Microsoft GenAIOps repo
###############################################################################
echo "[1/5] Cloning Microsoft GenAIOps repo..."
if [ -d "$MS_REPO_DIR" ]; then
  echo "  Repo already exists. Pulling latest..."
  git -C "$MS_REPO_DIR" pull --ff-only
else
  git clone "$MS_REPO" "$MS_REPO_DIR"
fi
cd "$MS_REPO_DIR"

###############################################################################
# 2. Authenticate
###############################################################################
echo ""
echo "[2/5] Authenticating..."
if ! az account show &>/dev/null; then
  echo "  Running 'az login'..."
  az login
fi
if ! azd auth login --check-status &>/dev/null; then
  echo "  Running 'azd auth login'..."
  azd auth login
fi
echo "  Authenticated."

###############################################################################
# 3. Create azd environment and provision
###############################################################################
echo ""
echo "[3/5] Creating azd environment '$AZD_ENV_NAME' and provisioning..."
azd env new "$AZD_ENV_NAME" || echo "  Environment may already exist, continuing..."
echo ""
echo "  Running 'azd up' -- this provisions infrastructure and deploys."
echo "  You will be prompted to select a subscription and region."
echo ""
azd up

###############################################################################
# 4. Generate .env file
###############################################################################
echo ""
echo "[4/5] Generating .env file..."
azd env get-values > .env
echo "  .env file written with $(wc -l < .env | tr -d ' ') variables."

###############################################################################
# 5. Create Python virtual environment and install dependencies
###############################################################################
echo ""
echo "[5/5] Setting up Python environment..."
if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv "$VENV_DIR"
  echo "  Virtual environment created at $VENV_DIR"
else
  echo "  Virtual environment already exists."
fi

source "$VENV_DIR/bin/activate"

if [ -f "requirements.txt" ]; then
  pip install --upgrade pip -q
  pip install -r requirements.txt -q
  echo "  Dependencies installed from requirements.txt."
elif [ -f "src/api/requirements.txt" ]; then
  pip install --upgrade pip -q
  pip install -r src/api/requirements.txt -q
  echo "  Dependencies installed from src/api/requirements.txt."
else
  echo "  WARNING: No requirements.txt found. Install dependencies manually."
fi

###############################################################################
# Summary
###############################################################################
echo ""
echo "============================================"
echo "  Setup Complete"
echo "============================================"
echo ""
echo "  Repo:          $MS_REPO_DIR/"
echo "  azd env:       $AZD_ENV_NAME"
echo "  .env file:     $MS_REPO_DIR/.env"
echo "  Python venv:   $MS_REPO_DIR/$VENV_DIR/"
echo ""
echo "  Activate the virtual environment:"
echo "    source $MS_REPO_DIR/$VENV_DIR/bin/activate"
echo ""
echo "  Foundry Portal: https://ai.azure.com"
echo "============================================"
