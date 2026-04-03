# check_traces.py
# Source: Microsoft Learning - mslearn-genaiops
# Adapted for AI-300 Lab Guide
# License: MIT
#
# Fetches traces from Application Insights and renders a parent-child
# tree in the terminal.

import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient

load_dotenv()

credential = DefaultAzureCredential()
logs_client = LogsQueryClient(credential)

workspace_id = os.getenv("LOG_ANALYTICS_WORKSPACE_ID")
if not workspace_id:
    print("Error: Set LOG_ANALYTICS_WORKSPACE_ID environment variable.")
    exit(1)

# ---------------------------------------------------------------------------
# Query for trail-guide spans from the last hour
# ---------------------------------------------------------------------------
query = """
dependencies
| where timestamp > ago(1h)
| where name contains "trail-guide" or name contains "test-"
| project timestamp, id, name, duration,
         parent_id = customDimensions["ai.operation.parentId"],
         total_tokens = customDimensions["response.total_tokens"],
         version = customDimensions["agent.version"]
| order by timestamp asc
"""

print("Querying Application Insights for trail-guide traces...")
print(f"Workspace: {workspace_id}\n")

response = logs_client.query_workspace(
    workspace_id=workspace_id,
    query=query,
    timespan=timedelta(hours=1),
)

if not response.tables or len(response.tables[0].rows) == 0:
    print("No traces found in the last hour.")
    print("Note: There is a 2-5 minute ingestion delay for Application Insights.")
    exit(0)

# ---------------------------------------------------------------------------
# Build and render the tree
# ---------------------------------------------------------------------------
rows = response.tables[0].rows
columns = [col.name for col in response.tables[0].columns]

spans = []
for row in rows:
    span = dict(zip(columns, row))
    spans.append(span)

# Group by parent
children_map = {}
roots = []
for span in spans:
    parent = span.get("parent_id")
    if not parent:
        roots.append(span)
    else:
        children_map.setdefault(parent, []).append(span)


def print_tree(span, indent=0):
    """Recursively print span tree."""
    prefix = "  " * indent + ("|- " if indent > 0 else "")
    tokens = span.get("total_tokens", "")
    tokens_str = f" [{tokens} tokens]" if tokens else ""
    duration = span.get("duration", "")
    duration_str = f" ({duration}ms)" if duration else ""
    print(f"{prefix}{span['name']}{duration_str}{tokens_str}")

    for child in children_map.get(span.get("id"), []):
        print_tree(child, indent + 1)


print(f"Found {len(spans)} spans:\n")
for root in roots:
    print_tree(root)
    print()

print("View full trace details in the Azure AI Foundry portal.")
