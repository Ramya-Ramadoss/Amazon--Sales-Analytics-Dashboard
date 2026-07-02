import os
import pandas as pd

def load_raw_data(file_path="data/raw/Amazon_Sales.xlsx"):
    """
    Loads the raw Excel dataset.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Raw data file not found at: {file_path}")
    print(f"Loading raw data from: {file_path}...")
    df = pd.read_excel(file_path, sheet_name="Amazon")
    print(f"Successfully loaded raw data. Shape: {df.shape}")
    return df

def load_processed_data(file_path="data/processed/cleaned_sales.csv"):
    """
    Loads the cleaned CSV dataset.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Processed data file not found at: {file_path}")
    print(f"Loading processed data from: {file_path}...")
    df = pd.read_csv(file_path)
    # Ensure OrderDate is parsed as datetime
    if "OrderDate" in df.columns:
        df["OrderDate"] = pd.to_datetime(df["OrderDate"])
    print(f"Successfully loaded processed data. Shape: {df.shape}")
    return df
