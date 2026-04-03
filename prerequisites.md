# Prerequisites

Everything you need installed before starting the labs.

## 1. Azure Subscription

A pay-as-you-go subscription works fine. If you have Visual Studio or MSDN benefits, use those -- they include free Azure credits.

Sign up: [https://azure.microsoft.com/en-us/free/](https://azure.microsoft.com/en-us/free/)

> **Note:** Some labs require specific resource providers to be registered. The lab workbooks call these out, but if you run into "resource provider not registered" errors, see the [Azure docs on registering providers](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/resource-providers-and-types).

## 2. Azure CLI

Used throughout both tracks for resource management.

**macOS:**
```bash
brew install azure-cli
```

**Windows:**
```powershell
winget install Microsoft.AzureCLI
```

**Linux (Ubuntu/Debian):**
```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

**Linux (RHEL/Fedora):**
```bash
sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
sudo dnf install azure-cli
```

Full install docs: [https://learn.microsoft.com/en-us/cli/azure/install-azure-cli](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)

### Install the ML extension

Required for Labs 01-07:
```bash
az extension add --name ml --yes
```

## 3. Azure Developer CLI (azd)

Required for the GenAIOps track (Labs 08-13). This is a separate tool from the Azure CLI.

**macOS:**
```bash
brew install azd
```

**Windows:**
```powershell
winget install Microsoft.Azd
```

**Linux:**
```bash
curl -fsSL https://aka.ms/install-azd.sh | bash
```

Full install docs: [https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/install-azd](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/install-azd)

## 4. Python 3.10+

Required for SDK work in both tracks.

> **Important:** Python 3.9 has compatibility issues with the latest Azure ML and AI SDKs. Use 3.10 or newer.

**macOS:**
```bash
brew install python@3.12
```

**Windows:**

Download from [python.org](https://www.python.org/downloads/) or:
```powershell
winget install Python.Python.3.12
```

**Linux:**
```bash
sudo apt install python3.12 python3.12-venv
```

## 5. Git + GitHub Account

Required for Labs 06-07 (CI/CD with GitHub Actions) and Lab 11 (GenAI CI/CD).

- Install Git: [https://git-scm.com/downloads](https://git-scm.com/downloads)
- Create a GitHub account: [https://github.com/signup](https://github.com/signup)

You will need to fork repos and set up GitHub Actions, so make sure you can push to your own repositories.

## 6. VS Code (Optional but Recommended)

Useful for editing YAML pipelines, Python scripts, and Prompt Flow files.

Download: [https://code.visualstudio.com/](https://code.visualstudio.com/)

Recommended extensions:
- **Azure Machine Learning** -- workspace explorer, compute management
- **Prompt Flow** -- visual flow editor for Labs 09, 13
- **Python** -- IntelliSense, debugging
- **YAML** -- schema validation for pipeline definitions

## Verification Checklist

Run these commands to confirm everything is installed correctly:

```bash
# Azure CLI
az version
# Should show 2.60+ (or latest)

# ML extension
az ml --help
# Should show Azure ML commands (not "extension not found")

# Azure Developer CLI
azd version
# Should show 1.9+ (or latest)

# Python
python3 --version
# Should show 3.10+

# Git
git --version
# Should show 2.40+ (or latest)
```

## Sign In

### Azure CLI

```bash
az login
```

This opens a browser window. Sign in with the account that has your Azure subscription.

After signing in, set your default subscription:
```bash
# List subscriptions
az account list --output table

# Set default (use the subscription ID from the list)
az account set --subscription "your-subscription-id"
```

### Azure Developer CLI

```bash
azd auth login
```

This also opens a browser window. Use the same account.

> **Tip:** If you have multiple tenants, specify the tenant:
> ```bash
> az login --tenant your-tenant-id
> azd auth login --tenant-id your-tenant-id
> ```

## Next Step

You are ready to go. Start with [Lab 01: AutoML & MLflow](mlops/lab01-automl-mlflow/lab01-automl-mlflow.ipynb).
