# run_monitoring.py
# Source: Microsoft Learning - mslearn-genaiops
# Adapted for AI-300 Lab Guide
# License: MIT
#
# Configures Azure Monitor with OpenTelemetry, instruments OpenAI SDK,
# and runs 4 versions x 5 test prompts with custom spans.

import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace
from opentelemetry.instrumentation.openai import OpenAIInstrumentor

load_dotenv()

# ---------------------------------------------------------------------------
# Configure telemetry
# ---------------------------------------------------------------------------
configure_azure_monitor(
    connection_string=os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
)
OpenAIInstrumentor().instrument()
tracer = trace.get_tracer(__name__)

print("OpenTelemetry configured with Azure Monitor exporter")
print("OpenAI SDK auto-instrumented")

# ---------------------------------------------------------------------------
# Set up project client
# ---------------------------------------------------------------------------
credential = DefaultAzureCredential()
project_client = AIProjectClient(
    credential=credential,
    endpoint=os.getenv("AZURE_AI_PROJECT_ENDPOINT"),
)

# ---------------------------------------------------------------------------
# Test prompts (same as Lab 10)
# ---------------------------------------------------------------------------
test_prompts = [
    {"id": "day-hike-gear", "prompt": "What gear do I need for a day hike?"},
    {"id": "overnight-camping", "prompt": "I'm planning an overnight camping trip. What should I prepare?"},
    {"id": "three-day-backpacking", "prompt": "Help me plan a 3-day backpacking route."},
    {"id": "winter-hiking", "prompt": "What precautions should I take for winter hiking?"},
    {"id": "trail-difficulty", "prompt": "How do I assess trail difficulty for beginners?"},
]

# ---------------------------------------------------------------------------
# Agent versions to test (set these from your deployed agents)
# ---------------------------------------------------------------------------
agent_versions = {
    "v1": os.getenv("AGENT_ID_V1"),
    "v2": os.getenv("AGENT_ID_V2"),
    "v3": os.getenv("AGENT_ID_V3"),
    "v4": os.getenv("AGENT_ID_V4"),
}

# Filter out versions without agent IDs
agent_versions = {k: v for k, v in agent_versions.items() if v}

if not agent_versions:
    print("Error: Set at least one AGENT_ID_V* environment variable.")
    exit(1)

print(f"\nTesting {len(agent_versions)} versions x {len(test_prompts)} prompts")
print(f"= {len(agent_versions) * len(test_prompts)} total interactions\n")

# ---------------------------------------------------------------------------
# Run tests with custom spans
# ---------------------------------------------------------------------------
for version, agent_id in agent_versions.items():
    with tracer.start_as_current_span(f"trail-guide-{version}") as version_span:
        version_span.set_attribute("agent.version", version)
        version_span.set_attribute("agent.id", agent_id)
        print(f"--- {version} (agent: {agent_id}) ---")

        for test in test_prompts:
            with tracer.start_as_current_span(f"test-{test['id']}") as test_span:
                test_span.set_attribute("test.id", test["id"])
                test_span.set_attribute("test.prompt", test["prompt"])

                thread = project_client.agents.create_thread()
                message = project_client.agents.create_message(
                    thread_id=thread.id, role="user", content=test["prompt"]
                )
                run = project_client.agents.create_and_process_run(
                    thread_id=thread.id, agent_id=agent_id
                )
                messages = project_client.agents.list_messages(thread_id=thread.id)
                response = messages.data[0].content[0].text.value

                test_span.set_attribute("response.total_tokens", run.usage.total_tokens)
                test_span.set_attribute("response.length", len(response))

                print(f"  {test['id']}: {run.usage.total_tokens} tokens")

print("\nAll tests complete. Traces will appear in Application Insights in 2-5 minutes.")
