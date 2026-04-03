# =============================================================================
# Lab 03 - Hyperparameter Tuning: Run Sweep Job (standalone script)
# Source: Microsoft Learning - mslearn-mlops
# Original: experimentation/Hyperparameter tuning.ipynb
# License: MIT
# =============================================================================

from azure.ai.ml import MLClient, command, Input
from azure.ai.ml.constants import AssetTypes
from azure.ai.ml.sweep import Choice
from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential


def main():
    # --- Authenticate ---
    try:
        credential = DefaultAzureCredential()
        credential.get_token("https://management.azure.com/.default")
    except Exception:
        credential = InteractiveBrowserCredential()

    ml_client = MLClient.from_config(credential=credential)
    print(f"Connected to workspace: {ml_client.workspace_name}")

    # --- Define command job with hyperparameter search space ---
    job = command(
        code="../lab02-scripts-command-jobs/scripts",
        command=(
            "python train_model_parameters.py "
            "--training_data ${{inputs.training_data}} "
            "--reg_rate ${{inputs.reg_rate}}"
        ),
        inputs={
            "training_data": Input(
                type=AssetTypes.URI_FILE, path="azureml:diabetes-data:1"
            ),
            "reg_rate": Choice(values=[0.01, 0.1, 1]),
        },
        environment="azureml:AzureML-sklearn-1.0-ubuntu20.04-py38-cpu@latest",
        compute="cc-ai300",
    )

    # --- Configure sweep ---
    sweep_job = job.sweep(
        sampling_algorithm="grid",
        primary_metric="Accuracy",
        goal="maximize",
    )

    sweep_job.set_limits(
        max_total_trials=3, max_concurrent_trials=2, timeout=600
    )

    sweep_job.experiment_name = "sweep-diabetes"
    sweep_job.display_name = "diabetes-sweep-grid"

    # --- Submit ---
    returned_job = ml_client.jobs.create_or_update(sweep_job)
    print(f"Sweep job submitted: {returned_job.name}")
    print(f"Monitor at: {returned_job.studio_url}")


if __name__ == "__main__":
    main()
