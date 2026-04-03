"""
Lab 07: Deploy a model to a managed online endpoint.
Source: Microsoft Learning - mslearn-mlops

Standalone CLI-runnable script for creating/updating managed online endpoints
and deployments in Azure ML.

Usage:
    python deploy_to_online_endpoint.py --endpoint-name <name> --deployment-name <name>
"""

import argparse
import datetime

from azure.ai.ml import MLClient
from azure.ai.ml.entities import (
    ManagedOnlineDeployment,
    ManagedOnlineEndpoint,
    Model,
)
from azure.ai.ml.constants import AssetTypes
from azure.identity import DefaultAzureCredential


def get_ml_client() -> MLClient:
    """Authenticate and return an MLClient from the workspace config."""
    credential = DefaultAzureCredential()
    ml_client = MLClient.from_config(credential=credential)
    print(f"Connected to workspace: {ml_client.workspace_name}")
    return ml_client


def ensure_endpoint(
    ml_client: MLClient, endpoint_name: str
) -> ManagedOnlineEndpoint:
    """Create the endpoint if it does not already exist."""
    try:
        endpoint = ml_client.online_endpoints.get(endpoint_name)
        print(f"Endpoint '{endpoint_name}' already exists.")
    except Exception:
        print(f"Creating endpoint '{endpoint_name}'...")
        endpoint = ManagedOnlineEndpoint(
            name=endpoint_name,
            description="Diabetes classification endpoint",
            auth_mode="key",
        )
        ml_client.begin_create_or_update(endpoint).result()
        print(f"Endpoint '{endpoint_name}' created.")
    return endpoint


def create_or_update_deployment(
    ml_client: MLClient,
    endpoint_name: str,
    deployment_name: str,
    model_path: str = "./model",
    instance_type: str = "Standard_D2as_v4",
    instance_count: int = 1,
) -> ManagedOnlineDeployment:
    """Create or update a deployment under the given endpoint."""
    print(f"Creating deployment '{deployment_name}' on endpoint '{endpoint_name}'...")
    model = Model(
        path=model_path,
        type=AssetTypes.MLFLOW_MODEL,
        description="Diabetes classification model",
    )
    deployment = ManagedOnlineDeployment(
        name=deployment_name,
        endpoint_name=endpoint_name,
        model=model,
        instance_type=instance_type,
        instance_count=instance_count,
    )
    ml_client.online_deployments.begin_create_or_update(deployment).result()
    print(f"Deployment '{deployment_name}' created.")
    return deployment


def set_traffic_to_deployment(
    ml_client: MLClient, endpoint_name: str, deployment_name: str, traffic_pct: int = 100
) -> None:
    """Route traffic to the specified deployment."""
    endpoint = ml_client.online_endpoints.get(endpoint_name)
    endpoint.traffic = {deployment_name: traffic_pct}
    ml_client.begin_create_or_update(endpoint).result()
    print(f"Traffic set: {deployment_name} = {traffic_pct}%")
    print(f"Scoring URI: {endpoint.scoring_uri}")


def main():
    parser = argparse.ArgumentParser(description="Deploy model to managed online endpoint")
    parser.add_argument(
        "--endpoint-name",
        default=f"diabetes-ep-{datetime.datetime.now().strftime('%m%d%H%M')}",
        help="Name of the managed online endpoint",
    )
    parser.add_argument(
        "--deployment-name",
        default="blue",
        help="Name of the deployment (default: blue)",
    )
    parser.add_argument(
        "--model-path",
        default="./model",
        help="Path to the MLflow model directory",
    )
    parser.add_argument(
        "--instance-type",
        default="Standard_D2as_v4",
        help="VM size for the deployment",
    )
    parser.add_argument(
        "--instance-count",
        type=int,
        default=1,
        help="Number of instances for the deployment",
    )
    args = parser.parse_args()

    ml_client = get_ml_client()
    ensure_endpoint(ml_client, args.endpoint_name)
    create_or_update_deployment(
        ml_client,
        args.endpoint_name,
        args.deployment_name,
        model_path=args.model_path,
        instance_type=args.instance_type,
        instance_count=args.instance_count,
    )
    set_traffic_to_deployment(ml_client, args.endpoint_name, args.deployment_name)

    print("\nDeployment complete.")
    print(f"  Endpoint:   {args.endpoint_name}")
    print(f"  Deployment: {args.deployment_name}")


if __name__ == "__main__":
    main()
