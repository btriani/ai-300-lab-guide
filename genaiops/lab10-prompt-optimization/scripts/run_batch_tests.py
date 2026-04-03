# run_batch_tests.py
# Source: Microsoft Learning - mslearn-genaiops
# Adapted for AI-300 Lab Guide
# License: MIT
#
# Runs 5 standardized test prompts against an agent and outputs results as JSON.

import json
import os
import sys
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
# Standardized test prompts
# ---------------------------------------------------------------------------
test_prompts = [
    {"id": "day-hike-gear", "prompt": "What gear do I need for a day hike?"},
    {"id": "overnight-camping", "prompt": "I'm planning an overnight camping trip. What should I prepare?"},
    {"id": "three-day-backpacking", "prompt": "Help me plan a 3-day backpacking route."},
    {"id": "winter-hiking", "prompt": "What precautions should I take for winter hiking?"},
    {"id": "trail-difficulty", "prompt": "How do I assess trail difficulty for beginners?"},
]

# ---------------------------------------------------------------------------
# Resolve agent ID from env or CLI argument
# ---------------------------------------------------------------------------
agent_id = sys.argv[1] if len(sys.argv) > 1 else os.getenv("AZURE_AI_AGENT_ID")
if not agent_id:
    print("Error: Provide agent ID as argument or set AZURE_AI_AGENT_ID env var.")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Run tests
# ---------------------------------------------------------------------------
results = []
for test in test_prompts:
    thread = project_client.agents.create_thread()
    message = project_client.agents.create_message(
        thread_id=thread.id, role="user", content=test["prompt"]
    )
    run = project_client.agents.create_and_process_run(
        thread_id=thread.id, agent_id=agent_id
    )
    messages = project_client.agents.list_messages(thread_id=thread.id)
    response = messages.data[0].content[0].text.value

    result = {
        "id": test["id"],
        "prompt": test["prompt"],
        "response": response,
        "total_tokens": run.usage.total_tokens,
        "prompt_tokens": run.usage.prompt_tokens,
        "completion_tokens": run.usage.completion_tokens,
    }
    results.append(result)
    print(f"  {test['id']}: {run.usage.total_tokens} tokens", file=sys.stderr)

# ---------------------------------------------------------------------------
# Output JSON
# ---------------------------------------------------------------------------
output = {
    "agent_id": agent_id,
    "test_count": len(results),
    "total_tokens": sum(r["total_tokens"] for r in results),
    "results": results,
}
print(json.dumps(output, indent=2))
