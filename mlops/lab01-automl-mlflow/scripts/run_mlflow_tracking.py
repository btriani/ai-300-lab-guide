"""
run_mlflow_tracking.py - Train models and track experiments with MLflow.

Source: Microsoft Learning - mslearn-mlops
Original: https://github.com/MicrosoftLearning/mslearn-mlops
License: MIT
Adapted for AI-300 Lab Guide
"""

import pandas as pd
import numpy as np
import mlflow
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import roc_curve


def load_and_split_data(csv_path="data/diabetes.csv"):
    """Load the diabetes CSV and split into train/test sets."""
    df = pd.read_csv(csv_path)
    print(f"Dataset: {df.shape[0]} rows, {df.shape[1]} columns")

    X = df[
        [
            "Pregnancies",
            "PlasmaGlucose",
            "DiastolicBloodPressure",
            "TricepsThickness",
            "SerumInsulin",
            "BMI",
            "DiabetesPedigree",
            "Age",
        ]
    ].values
    y = df["Diabetic"].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.30, random_state=0
    )
    print(f"Train: {X_train.shape[0]} samples, Test: {X_test.shape[0]} samples")
    return X_train, X_test, y_train, y_test


def run_autolog_experiment(X_train, y_train):
    """Run 1: LogisticRegression with MLflow autologging."""
    with mlflow.start_run():
        mlflow.sklearn.autolog()
        model = LogisticRegression(C=1 / 0.1, solver="liblinear").fit(
            X_train, y_train
        )
    print("Run 1 complete: LogisticRegression with autologging")
    return model


def run_custom_logging_experiments(X_train, X_test, y_train, y_test):
    """Runs 2-3: LogisticRegression with custom MLflow logging."""
    mlflow.sklearn.autolog(disable=True)

    # Run 2: reg_rate = 0.1
    with mlflow.start_run():
        model = LogisticRegression(C=1 / 0.1, solver="liblinear").fit(
            X_train, y_train
        )
        y_hat = model.predict(X_test)
        acc = np.average(y_hat == y_test)
        mlflow.log_param("regularization_rate", 0.1)
        mlflow.log_metric("Accuracy", acc)
    print(f"Run 2 complete: Accuracy = {acc:.4f}")

    # Run 3: reg_rate = 0.01
    with mlflow.start_run():
        model = LogisticRegression(C=1 / 0.01, solver="liblinear").fit(
            X_train, y_train
        )
        y_hat = model.predict(X_test)
        acc = np.average(y_hat == y_test)
        mlflow.log_param("regularization_rate", 0.01)
        mlflow.log_metric("Accuracy", acc)
    print(f"Run 3 complete: Accuracy = {acc:.4f}")


def run_decision_tree_experiment(X_train, X_test, y_train, y_test):
    """Run 4: DecisionTreeClassifier with custom logging."""
    with mlflow.start_run():
        model = DecisionTreeClassifier().fit(X_train, y_train)
        y_hat = model.predict(X_test)
        acc = np.average(y_hat == y_test)
        mlflow.log_param("estimator", "DecisionTreeClassifier")
        mlflow.log_metric("Accuracy", acc)
    print(f"Run 4 complete: Accuracy = {acc:.4f}")


def run_decision_tree_with_artifact(X_train, X_test, y_train, y_test):
    """Run 5: DecisionTreeClassifier with ROC curve artifact."""
    with mlflow.start_run():
        model = DecisionTreeClassifier().fit(X_train, y_train)
        y_hat = model.predict(X_test)
        acc = np.average(y_hat == y_test)

        # Generate and log ROC curve
        y_scores = model.predict_proba(X_test)
        fpr, tpr, thresholds = roc_curve(y_test, y_scores[:, 1])

        fig = plt.figure(figsize=(6, 4))
        plt.plot([0, 1], [0, 1], "k--")
        plt.plot(fpr, tpr)
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title("ROC Curve")
        plt.savefig("ROC-Curve.png")
        plt.close()

        mlflow.log_param("estimator", "DecisionTreeClassifier")
        mlflow.log_metric("Accuracy", acc)
        mlflow.log_artifact("ROC-Curve.png")
    print(f"Run 5 complete: Accuracy = {acc:.4f} (with ROC artifact)")


if __name__ == "__main__":
    mlflow.set_experiment("mlflow-experiment-diabetes")

    X_train, X_test, y_train, y_test = load_and_split_data()
    run_autolog_experiment(X_train, y_train)
    run_custom_logging_experiments(X_train, X_test, y_train, y_test)
    run_decision_tree_experiment(X_train, X_test, y_train, y_test)
    run_decision_tree_with_artifact(X_train, X_test, y_train, y_test)

    print("\nAll 5 runs complete. View results in Azure ML Studio.")
