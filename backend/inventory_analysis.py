import pandas as pd


def get_inventory_summary(df):
    """Calculate main inventory KPIs."""

    summary = {
        "total_products": df["Product ID"].nunique(),
        "total_categories": df["Category"].nunique(),
        "available_stock": int(df["Inventory Level"].sum()),
        "inventory_value": float(df["Inventory Value"].sum()),
        "low_stock_products": int(
            (df["Stock Status"] == "Low Stock").sum()
        ),
        "out_of_stock_products": int(
            (df["Stock Status"] == "Out of Stock").sum()
        ),
    }

    return summary


def category_analysis(df):
    """Analyze inventory by category."""

    result = (
        df.groupby("Category")
        .agg(
            Inventory_Level=("Inventory Level", "sum"),
            Units_Sold=("Units Sold", "sum"),
            Demand=("Demand", "sum"),
            Inventory_Value=("Inventory Value", "sum")
        )
        .reset_index()
    )

    return result.sort_values(
        "Inventory_Level",
        ascending=False
    )


def product_analysis(df):
    """Analyze product movement and performance."""

    result = (
        df.groupby("Product ID")
        .agg(
            Total_Inventory=("Inventory Level", "sum"),
            Total_Sales=("Units Sold", "sum"),
            Total_Demand=("Demand", "sum")
        )
        .reset_index()
    )

    result["Sell_Through_Rate"] = (
    result["Total_Sales"]
    / (
        result["Total_Sales"]
        + result["Total_Inventory"]
    ).replace(0, 1)
    * 100
    )

    result["Movement"] = "Moderate Moving"

    result.loc[
        result["Sell_Through_Rate"] >= 30,
        "Movement"
    ] = "Fast Moving"

    result.loc[
        result["Sell_Through_Rate"] < 20,
        "Movement"
    ] = "Slow Moving"

    return result.sort_values(
        "Total_Sales",
        ascending=False
    )


def monthly_analysis(df):
    """Analyze monthly inventory, sales and demand."""

    result = (
        df.groupby("Year-Month")
        .agg(
            Inventory_Level=("Inventory Level", "mean"),
            Units_Sold=("Units Sold", "sum"),
            Demand=("Demand", "sum")
        )
        .reset_index()
    )

    return result


def store_analysis(df):
    """Analyze inventory performance by store."""

    result = (
        df.groupby("Store ID")
        .agg(
            Inventory_Level=("Inventory Level", "sum"),
            Units_Sold=("Units Sold", "sum"),
            Demand=("Demand", "sum")
        )
        .reset_index()
    )

    return result.sort_values(
        "Inventory_Level",
        ascending=False
    )


def region_analysis(df):
    """Analyze inventory performance by region."""

    result = (
        df.groupby("Region")
        .agg(
            Inventory_Level=("Inventory Level", "sum"),
            Units_Sold=("Units Sold", "sum"),
            Demand=("Demand", "sum")
        )
        .reset_index()
    )

    return result.sort_values(
        "Inventory_Level",
        ascending=False
    )


def stock_alerts(df):
    """Return products requiring inventory attention."""

    alerts = df[
        df["Smart Recommendation"] != "No Action"
    ].copy()

    return alerts[
        [
            "Product ID",
            "Category",
            "Inventory Level",
            "Demand",
            "Reorder Level",
            "Reorder Quantity",
            "Stock Status",
            "Smart Recommendation"
        ]
    ]