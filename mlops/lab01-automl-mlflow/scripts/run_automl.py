"""
run_automl.py - Submit an AutoML classification job to Azure ML.

Source: Microsoft Learning - mslearn-mlops
Original: https://github.com/MicrosoftLearning/mslearn-mlops
License: MIT
Adapted for AI-300 Lab Guide
"""

from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential
from azure.ai.ml import MLClient, Input, automl
from azure.ai.ml.constants import AssetTypes


def get_ml_client():
    """Authenticate and return an MLClient instance."""
    try:
        credential = DefaultAzureCredential()
        credential.get_token("https://management.azure.com/.default")
    except Exception:
        credential = InteractiveBrowserCredential()
    return MLClient.from_config(credential=credential)


def submit_automl_job(ml_client):
    """Configure and submit an AutoML classification job."""
    # Reference the MLTable data asset
    my_training_data_input = Input(
        type=AssetTypes.MLTABLE,
        path="azureml:diabetes-training:1",
    )

    # Configure the AutoML classification job
    classification_job = automl.classification(
        compute="cc-ai300",
        experiment_name="auto-ml-class-dev",
        training_data=my_training_data_input,
        target_column_name="Diabetic",
        primary_metric="accuracy",
        n_cross_validations=5,
        enable_model_explainability=True,
    )

    # Set resource limits
    classification_job.set_limits(
        timeout_minutes=60,
        trial_timeout_minutes=20,
        max_trials=5,
        enable_early_termination=True,
    )

    # Set training configuration
    classification_job.set_training(
        blocked_training_algorithms=["LogisticRegression"],
        enable_onnx_compatible_models=True,
    )

    # Submit the job
    returned_job = ml_client.jobs.create_or_update(classification_job)
    print(f"AutoML job submitted: {returned_job.name}")
    print(f"Monitor at: {returned_job.studio_url}")
    return returned_job


if __name__ == "__main__":
    client = get_ml_client()
    submit_automl_job(client)
