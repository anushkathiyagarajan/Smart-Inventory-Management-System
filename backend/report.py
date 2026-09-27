import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def generate_inventory_report(df):
    """Generate a complete inventory report."""

    total_products = df["Product ID"].nunique()
    total_categories = df["Category"].nunique()
    total_stock = df["Inventory Level"].sum()
    total_value = df["Inventory Value"].sum()
    low_stock = (
        df["Stock Status"] == "Low Stock"
    ).sum()
    out_of_stock = (
        df["Stock Status"] == "Out of Stock"
    ).sum()
    overstocked = (
        df["Inventory Condition"] == "Overstocked"
    ).sum()

    top_product = (
        df.groupby("Product ID")["Units Sold"]
        .sum()
        .idxmax()
    )

    top_category = (
        df.groupby("Category")["Units Sold"]
        .sum()
        .idxmax()
    )

    report = {
        "Inventory Summary": {
            "Total Products": int(total_products),
            "Total Categories": int(total_categories),
            "Available Stock": int(total_stock),
            "Inventory Value": round(float(total_value), 2),
            "Low Stock Records": int(low_stock),
            "Out of Stock Records": int(out_of_stock),
            "Overstocked Records": int(overstocked)
        },
        "Performance": {
            "Top Selling Product": top_product,
            "Top Performing Category": top_category
        }
    }

    return report


def export_inventory_report(df):
    """Export inventory summary to CSV."""

    report = generate_inventory_report(df)

    rows = []

    for section, values in report.items():

        for metric, value in values.items():

            rows.append({
                "Section": section,
                "Metric": metric,
                "Value": value
            })

    report_df = pd.DataFrame(rows)

    output_path = DATA_DIR / "inventory_report.csv"

    report_df.to_csv(
        output_path,
        index=False
    )

    return output_path