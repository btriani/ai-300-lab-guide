#!/usr/bin/env bash
# check-prerequisites.sh -- Verify all tools required for AI-300 labs are installed
set -euo pipefail

PASS=0
FAIL=0
WARN=0

###############################################################################
# Helpers
###############################################################################
check_cmd() {
  local name="$1"
  local cmd="$2"
  local version_flag="${3:---version}"

  if command -v "$cmd" &>/dev/null; then
    local ver
    ver=$($cmd $version_flag 2>&1 | head -1)
    printf "  [PASS] %-20s %s\n" "$name" "$ver"
    ((PASS++))
  else
    printf "  [FAIL] %-20s not found\n" "$name"
    ((FAIL++))
  fi
}

check_python_version() {
  if command -v python3 &>/dev/null; then
    local ver
    ver=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    local major minor
    major=$(echo "$ver" | cut -d. -f1)
    minor=$(echo "$ver" | cut -d. -f2)
    if [ "$major" -ge 3 ] && [ "$minor" -ge 10 ]; then
      printf "  [PASS] %-20s %s (>= 3.10 required)\n" "Python version" "$ver"
      ((PASS++))
    else
      printf "  [WARN] %-20s %s (3.10+ recommended, 3.9+ minimum)\n" "Python version" "$ver"
      ((WARN++))
    fi
  fi
}

check_az_extension() {
  local ext="$1"
  if az extension show --name "$ext" &>/dev/null 2>&1; then
    local ver
    ver=$(az extension show --name "$ext" --query version -o tsv 2>/dev/null)
    printf "  [PASS] %-20s %s\n" "az ext: $ext" "$ver"
    ((PASS++))
  else
    printf "  [FAIL] %-20s not installed (run: az extension add -n %s)\n" "az ext: $ext" "$ext"
    ((FAIL++))
  fi
}

check_az_login() {
  if az account show &>/dev/null 2>&1; then
    local sub
    sub=$(az account show --query name -o tsv)
    printf "  [PASS] %-20s logged in (%s)\n" "Azure login" "$sub"
    ((PASS++))
  else
    printf "  [FAIL] %-20s not logged in (run: az login)\n" "Azure login"
    ((FAIL++))
  fi
}

###############################################################################
echo "============================================"
echo "  AI-300 Prerequisites Check"
echo "============================================"
echo ""

echo "--- Core Tools ---"
check_cmd "Azure CLI (az)" "az" "version --query \"\\\"azure-cli\\\"\" -o tsv"
check_cmd "Azure Dev CLI (azd)" "azd" "version"
check_cmd "Python 3" "python3" "--version"
check_cmd "pip" "pip3" "--version"
check_cmd "Git" "git" "--version"
check_cmd "jq" "jq" "--version"

echo ""
echo "--- Python Version ---"
check_python_version

echo ""
echo "--- Azure CLI Extensions ---"
check_az_extension "ml"

echo ""
echo "--- Azure Authentication ---"
check_az_login

echo ""
echo "--- Optional Tools ---"
check_cmd "GitHub CLI (gh)" "gh" "--version"
check_cmd "Docker" "docker" "--version"

###############################################################################
# Summary
###############################################################################
echo ""
echo "============================================"
TOTAL=$((PASS + FAIL + WARN))
echo "  Results: $PASS passed, $FAIL failed, $WARN warnings (of $TOTAL checks)"

if [ "$FAIL" -eq 0 ]; then
  echo "  Status:  Ready to go!"
else
  echo "  Status:  Fix the FAIL items above before starting labs."
fi
echo "============================================"

exit "$FAIL"
