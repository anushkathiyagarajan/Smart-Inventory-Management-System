import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def load_inventory_data():
    """Load the processed inventory dataset."""
    
    file_path = DATA_DIR / "inventory_data.csv"

    if not file_path.exists():
        raise FileNotFoundError(
            f"Inventory dataset not found: {file_path}"
        )

    df = pd.read_csv(file_path)

    return df


def load_forecast():
    """Load the latest demand forecast."""

    file_path = DATA_DIR / "demand_forecast.csv"

    if not file_path.exists():
        return pd.DataFrame()

    return pd.read_csv(file_path)


def load_model_comparison():
    """Load forecasting model comparison results."""

    file_path = DATA_DIR / "forecast_model_comparison.csv"

    if not file_path.exists():
        return pd.DataFrame()

    return pd.read_csv(file_path)