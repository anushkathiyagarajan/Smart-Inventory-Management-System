import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def load_forecast():
    """Load the final demand forecast."""

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


def get_forecast_summary():
    """Return the latest forecast as a dictionary."""

    forecast = load_forecast()

    if forecast.empty:
        return {
            "period": "N/A",
            "method": "N/A",
            "demand": 0
        }

    row = forecast.iloc[0]

    return {
        "period": row["Forecast Period"],
        "method": row["Forecast Method"],
        "demand": int(row["Forecast Demand"])
    }


def get_model_comparison():
    """Return model comparison results."""

    comparison = load_model_comparison()

    if comparison.empty:
        return pd.DataFrame()

    return comparison.sort_values(
        "RMSE",
        ascending=True
    ).reset_index(drop=True)