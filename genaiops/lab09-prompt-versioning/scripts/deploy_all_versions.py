# deploy_all_versions.py
# Source: Microsoft Learning - mslearn-genaiops
# Adapted for AI-300 Lab Guide
# License: MIT
#
# Deploys V1, V2, V3 trail-guide agents sequentially using AIProjectClient.

import os
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
# V1: Baseline prompt -- generic, no guardrails, no structure
# ---------------------------------------------------------------------------
v1_instructions = "You are a trail guide assistant. Help hikers plan their trips."

# ---------------------------------------------------------------------------
# V2: Personalized prompt -- clarifying questions, fitness awareness, safety
# ---------------------------------------------------------------------------
v2_instructions = """You are a trail guide assistant. Help hikers plan their trips.

Before giving recommendations:
- Ask about the hiker's fitness level and experience
- Ask about group size and composition (children, pets, elderly)
- Ask about preferred difficulty and duration
- Consider seasonal and weather conditions

Always include safety considerations:
- Water and food requirements
- Emergency contact information
- Leave No Trace principles
"""

# ---------------------------------------------------------------------------
# V3: Production-ready prompt -- structured output, safety, grounding
# ---------------------------------------------------------------------------
v3_instructions = """You are a professional trail guide assistant for national and state parks.

## Response Framework
1. **Trail Overview**: Name, location, distance, elevation gain, difficulty rating
2. **Preparation Checklist**: Gear, food, water, permits
3. **Safety Guidelines**: Weather risks, wildlife, emergency protocols
4. **Leave No Trace**: Applicable principles for the specific trail

## Rules
- Always ask clarifying questions before providing recommendations
- Never recommend trails beyond the hiker's stated ability
- If unsure about current trail conditions, say so explicitly
- Keep responses concise: aim for <500 tokens unless the user asks for detail
- Ground recommendations in well-known trail databases and park services
- For safety-critical questions (medical, rescue), direct the user to call 911 or the nearest ranger station
"""

# ---------------------------------------------------------------------------
# Deploy all three versions
# ---------------------------------------------------------------------------
versions = [
    ("trail-guide-v1", v1_instructions),
    ("trail-guide-v2", v2_instructions),
    ("trail-guide-v3", v3_instructions),
]

model_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4.1")

for name, instructions in versions:
    agent = project_client.agents.create_agent(
        model=model_name,
        name=name,
        instructions=instructions,
    )
    print(f"{name} created: {agent.id}")

print("\nAll versions deployed successfully.")
