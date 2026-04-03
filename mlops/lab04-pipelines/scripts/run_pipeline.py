# =============================================================================
# Lab 04 - Pipelines: Run Pipeline Job (standalone script)
# Source: Microsoft Learning - mslearn-mlops
# Original: experimentation/Pipelines.ipynb
# License: MIT
# =============================================================================

from azure.ai.ml import MLClient, Input, load_component
from azure.ai.ml.constants import AssetTypes
from azure.ai.ml.dsl import pipeline
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

    # --- Load components ---
    prep_data = load_component(source="scripts/prep-data.yml")
    train_model = load_component(source="scripts/train-model.yml")
    print(f"Components loaded: {prep_data.name}, {train_model.name}")

    # --- Build pipeline ---
    @pipeline()
    def diabetes_classification(pipeline_job_input):
        clean_data = prep_data(input_data=pipeline_job_input)
        train = train_model(training_data=clean_data.outputs.output_data)
        return {
            "pipeline_job_transformed_data": clean_data.outputs.output_data,
            "pipeline_job_trained_model": train.outputs.model_output,
        }

    # --- Configure and submit ---
    pipeline_job = diabetes_classification(
        Input(type=AssetTypes.URI_FILE, path="azureml:diabetes-data:1")
    )
    pipeline_job.outputs.pipeline_job_transformed_data.mode = "upload"
    pipeline_job.outputs.pipeline_job_trained_model.mode = "upload"
    pipeline_job.settings.default_compute = "cc-ai300"
    pipeline_job.settings.default_datastore = "workspaceblobstore"

    pipeline_job = ml_client.jobs.create_or_update(
        pipeline_job, experiment_name="pipeline_diabetes"
    )
    print(f"Pipeline submitted: {pipeline_job.name}")
    print(f"Monitor at: {pipeline_job.studio_url}")


if __name__ == "__main__":
    main()
