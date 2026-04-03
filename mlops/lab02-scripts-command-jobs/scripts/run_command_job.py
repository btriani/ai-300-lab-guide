"""
run_command_job.py - Submit a command job to Azure ML via Python SDK.

Source: Microsoft Learning - mslearn-mlops
Original: https://github.com/MicrosoftLearning/mslearn-mlops
License: MIT
Adapted for AI-300 Lab Guide
"""

from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential
from azure.ai.ml import MLClient, command, Input
from azure.ai.ml.constants import AssetTypes


def get_ml_client():
    """Authenticate and return an MLClient instance."""
    try:
        credential = DefaultAzureCredential()
        credential.get_token("https://management.azure.com/.default")
    except Exception:
        credential = InteractiveBrowserCredential()
    return MLClient.from_config(credential=credential)


def submit_command_job(ml_client):
    """Configure and submit a command job."""
    job = command(
        code="./scripts",
        command=(
            "python train_model_parameters.py "
            "--training_data ${{inputs.training_data}} "
            "--reg_rate ${{inputs.reg_rate}}"
        ),
        inputs={
            "training_data": Input(
                type=AssetTypes.URI_FILE, path="azureml:diabetes-data:1"
            ),
            "reg_rate": 0.01,
        },
        environment="azureml:AzureML-sklearn-1.0-ubuntu20.04-py38-cpu@latest",
        compute="cc-ai300",
        experiment_name="diabetes-training",
        display_name="diabetes-train-sdk",
    )

    returned_job = ml_client.jobs.create_or_update(job)
    print(f"Job submitted: {returned_job.name}")
    print(f"Monitor at: {returned_job.studio_url}")
    return returned_job


if __name__ == "__main__":
    client = get_ml_client()
    submit_command_job(client)
