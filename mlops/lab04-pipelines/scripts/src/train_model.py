# =============================================================================
# Lab 04 - Pipelines: Train Model Component
# Source: Microsoft Learning - mslearn-mlops
# Original: experimentation/Pipelines.ipynb
# License: MIT
# =============================================================================

import argparse
import glob
import os

import mlflow
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split


def main():
    parser = argparse.ArgumentParser(description="Train diabetes model")
    parser.add_argument(
        "--training_data", type=str, help="Path to folder containing training CSVs"
    )
    parser.add_argument(
        "--reg_rate", type=float, default=0.01, help="Regularisation rate"
    )
    parser.add_argument(
        "--model_output", type=str, help="Path to save the trained model"
    )
    args = parser.parse_args()

    # Enable MLflow autologging
    mlflow.autolog()

    # Read all CSVs from the training_data folder
    csv_files = glob.glob(os.path.join(args.training_data, "*.csv"))
    print(f"Found {len(csv_files)} CSV file(s) in {args.training_data}")
    df = pd.concat([pd.read_csv(f) for f in csv_files], ignore_index=True)
    print(f"Combined data shape: {df.shape}")

    # Split features and target
    feature_cols = [
        "Pregnancies",
        "PlasmaGlucose",
        "DiastolicBloodPressure",
        "TricepsThickness",
        "SerumInsulin",
        "BMI",
        "DiabetesPedigree",
        "Age",
    ]
    target_col = "Diabetic"

    X = df[feature_cols]
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"Train set: {X_train.shape[0]} rows, Test set: {X_test.shape[0]} rows")

    # Train logistic regression (C = 1 / reg_rate)
    model = LogisticRegression(C=1 / args.reg_rate, max_iter=1000)
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    y_proba = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, y_proba)

    mlflow.log_metric("Accuracy", accuracy)
    mlflow.log_metric("AUC", auc)
    print(f"Accuracy: {accuracy:.4f}  |  AUC: {auc:.4f}")

    # Save model as MLflow model
    os.makedirs(args.model_output, exist_ok=True)
    mlflow.sklearn.save_model(model, args.model_output)
    print(f"Model saved to {args.model_output}")


if __name__ == "__main__":
    main()
