# =============================================================================
# Lab 04 - Pipelines: Prep Data Component
# Source: Microsoft Learning - mslearn-mlops
# Original: experimentation/Pipelines.ipynb
# License: MIT
# =============================================================================

import argparse
import os

import pandas as pd
from sklearn.preprocessing import MinMaxScaler


def main():
    parser = argparse.ArgumentParser(description="Prepare diabetes data")
    parser.add_argument("--input_data", type=str, help="Path to raw input data (CSV)")
    parser.add_argument("--output_data", type=str, help="Path to output folder")
    args = parser.parse_args()

    # Read raw data
    print(f"Reading data from {args.input_data}")
    df = pd.read_csv(args.input_data)
    print(f"Raw data shape: {df.shape}")

    # Drop missing values
    df = df.dropna()
    print(f"Shape after dropna: {df.shape}")

    # Scale numeric columns with MinMaxScaler
    numeric_cols = [
        "Pregnancies",
        "PlasmaGlucose",
        "DiastolicBloodPressure",
        "TricepsThickness",
        "SerumInsulin",
        "BMI",
        "DiabetesPedigree",
    ]

    scaler = MinMaxScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    print("Numeric columns scaled with MinMaxScaler")

    # Save cleaned data
    os.makedirs(args.output_data, exist_ok=True)
    output_path = os.path.join(args.output_data, "diabetes.csv")
    df.to_csv(output_path, index=False)
    print(f"Cleaned data saved to {output_path}")


if __name__ == "__main__":
    main()
