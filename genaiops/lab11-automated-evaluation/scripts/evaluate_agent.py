# evaluate_agent.py
# Source: Microsoft Learning - mslearn-genaiops, src/evaluators/evaluate_agent.py
# Adapted for AI-300 Lab Guide
# License: MIT
#
# Full 5-step evaluation pipeline:
#   1. Upload JSONL dataset
#   2. Create evaluation with cloud evaluators and data_mapping
#   3. Run evaluation
#   4. Poll for completion (every 30s)
#   5. Retrieve per-item and aggregate scores

import os
import time
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

load_dotenv()

credential = DefaultAzureCredential()
project_client = AIProjectClient(
    credential=credential,
    endpoint=os.getenv("AZURE_AI_PROJECT_ENDPOINT"),
)

# ---------------------------------------------------------------------------
# Step 1: Upload dataset
# ---------------------------------------------------------------------------
dataset_path = os.getenv("EVALUATION_DATASET_PATH", "data/evaluation_dataset.jsonl")
print(f"Step 1: Uploading dataset from {dataset_path}")

dataset = project_client.datasets.upload_file(
    name="trail-guide-eval-dataset",
    file_path=dataset_path,
)
print(f"  Dataset uploaded: {dataset.id}")

# ---------------------------------------------------------------------------
# Step 2: Create evaluation with cloud evaluators and data_mapping
# ---------------------------------------------------------------------------
print("Step 2: Creating evaluation definition")

evaluators = {
    "intent_resolution": {
        "id": "azureai://intent-resolution-evaluator",
    },
    "relevance": {
        "id": "azureai://relevance-evaluator",
    },
    "groundedness": {
        "id": "azureai://groundedness-evaluator",
    },
}

# data_mapping binds dataset columns to evaluator inputs using ${data.field} syntax
data_mapping = {
    "intent_resolution": {
        "query": "${data.query}",
        "response": "${data.response}",
    },
    "relevance": {
        "query": "${data.query}",
        "response": "${data.response}",
    },
    "groundedness": {
        "query": "${data.query}",
        "response": "${data.response}",
        "context": "${data.context}",
    },
}

# ---------------------------------------------------------------------------
# Step 3: Run evaluation
# ---------------------------------------------------------------------------
print("Step 3: Running evaluation")

evaluation = project_client.evaluations.create(
    data=dataset.id,
    evaluators=evaluators,
    data_mapping=data_mapping,
    display_name="trail-guide-v4-evaluation",
    description="Automated evaluation of trail-guide agent V4",
)
print(f"  Evaluation started: {evaluation.id}")

# ---------------------------------------------------------------------------
# Step 4: Poll for completion
# ---------------------------------------------------------------------------
print("Step 4: Polling for results (every 30s)")

while True:
    status = project_client.evaluations.get(evaluation.id)
    print(f"  Status: {status.status}")
    if status.status in ("Completed", "Failed", "Canceled"):
        break
    time.sleep(30)

if status.status != "Completed":
    print(f"  Evaluation {status.status}. Check the Azure portal for details.")
    exit(1)

# ---------------------------------------------------------------------------
# Step 5: Retrieve scores
# ---------------------------------------------------------------------------
print("Step 5: Retrieving scores")

results = project_client.evaluations.get_results(evaluation.id)

print("\n--- Aggregate Scores ---")
for evaluator_name, score in results.metrics.items():
    print(f"  {evaluator_name}: {score:.2f}/5")

print(f"\n--- Per-Item Results ({len(results.rows)} items) ---")
for i, row in enumerate(results.rows[:5]):
    print(f"  [{i}] intent={row.get('intent_resolution', 'N/A')} "
          f"relevance={row.get('relevance', 'N/A')} "
          f"groundedness={row.get('groundedness', 'N/A')}")

if len(results.rows) > 5:
    print(f"  ... and {len(results.rows) - 5} more items")

print("\nEvaluation complete. View full results in the Azure AI Foundry portal.")
