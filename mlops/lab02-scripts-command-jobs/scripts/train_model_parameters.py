"""
train_model_parameters.py - Training script with argparse parameters.

Source: Microsoft Learning - mslearn-mlops
Original: https://github.com/MicrosoftLearning/mslearn-mlops
License: MIT
Adapted for AI-300 Lab Guide

Usage:
    python train_model_parameters.py --training_data <path> --reg_rate 0.01
"""

import argparse
import glob
import os

import pandas as pd
import numpy as np
import mlflow
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, roc_curve


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--training_data",
        dest="training_data",
        type=str,
        help="Path to training data (CSV file or folder containing CSVs)",
    )
    parser.add_argument(
        "--reg_rate",
        dest="reg_rate",
        type=float,
        default=0.01,
        help="Regularization rate (default: 0.01)",
    )
    return parser.parse_args()


def get_data(path):
    """Load data from a CSV file or folder of CSVs."""
    if os.path.isdir(path):
        csv_files = glob.glob(os.path.join(path, "*.csv"))
        if not csv_files:
            raise FileNotFoundError(f"No CSV files found in {path}")
        df = pd.concat((pd.read_csv(f) for f in csv_files), sort=False)
    else:
        df = pd.read_csv(path)
    return df


def split_data(df):
    """Split the dataframe into train and test sets."""
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
    return X_train, X_test, y_train, y_test


def train_model(reg_rate, X_train, X_test, y_train, y_test):
    """Train a LogisticRegression model and log metrics with MLflow."""
    mlflow.log_param("regularization_rate", reg_rate)

    model = LogisticRegression(C=1 / reg_rate, solver="liblinear").fit(
        X_train, y_train
    )
    return model


def eval_model(model, X_test, y_test):
    """Evaluate the model and log metrics and artifacts with MLflow."""
    y_hat = model.predict(X_test)
    acc = np.average(y_hat == y_test)
    mlflow.log_metric("Accuracy", acc)
    print(f"Accuracy: {acc:.4f}")

    y_scores = model.predict_proba(X_test)
    auc = roc_auc_score(y_test, y_scores[:, 1])
    mlflow.log_metric("AUC", auc)
    print(f"AUC: {auc:.4f}")

    # Generate and log ROC curve
    fpr, tpr, thresholds = roc_curve(y_test, y_scores[:, 1])
    fig = plt.figure(figsize=(6, 4))
    plt.plot([0, 1], [0, 1], "k--")
    plt.plot(fpr, tpr)
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve")
    plt.savefig("ROC-Curve.png")
    plt.close()

    mlflow.log_artifact("ROC-Curve.png")


def main():
    """Main training pipeline."""
    args = parse_args()
    print(f"Training data path: {args.training_data}")
    print(f"Regularization rate: {args.reg_rate}")

    mlflow.autolog()

    df = get_data(args.training_data)
    print(f"Dataset: {df.shape[0]} rows, {df.shape[1]} columns")

    X_train, X_test, y_train, y_test = split_data(df)
    print(f"Train: {X_train.shape[0]} samples, Test: {X_test.shape[0]} samples")

    model = train_model(args.reg_rate, X_train, X_test, y_train, y_test)
    eval_model(model, X_test, y_test)


if __name__ == "__main__":
    main()
