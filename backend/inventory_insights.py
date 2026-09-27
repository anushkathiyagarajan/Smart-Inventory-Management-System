def generate_inventory_insights(df):
    """Generate business-friendly inventory insights."""

    insights = []

    # Stock status
    low_stock = (
        df["Stock Status"] == "Low Stock"
    ).sum()

    out_of_stock = (
        df["Stock Status"] == "Out of Stock"
    ).sum()

    overstocked = (
        df["Inventory Condition"] == "Overstocked"
    ).sum()

    # Product movement
    fast_moving = (
        df["Smart Recommendation"]
        .value_counts()
    )

    product_sales = (
        df.groupby("Product ID")["Units Sold"]
        .sum()
        .sort_values(ascending=False)
    )

    slow_product = (
        df.groupby("Product ID")["Units Sold"]
        .sum()
        .sort_values()
        .index[0]
    )

    fast_product = product_sales.index[0]

    # Category performance
    category_sales = (
        df.groupby("Category")["Units Sold"]
        .sum()
        .sort_values(ascending=False)
    )

    top_category = category_sales.index[0]

    # Generate insights
    insights.append(
        f"{out_of_stock:,} inventory records are currently "
        f"out of stock and require urgent attention."
    )

    insights.append(
        f"{low_stock:,} records are classified as low stock "
        f"and may require replenishment."
    )

    insights.append(
        f"{overstocked:,} records show potential overstock "
        f"conditions and should be monitored."
    )

    insights.append(
        f"Product {fast_product} has the highest total sales "
        f"volume in the dataset."
    )

    insights.append(
        f"Product {slow_product} has the lowest total sales "
        f"volume and may require closer performance monitoring."
    )

    insights.append(
        f"{top_category} has the highest total sales among "
        f"the product categories."
    )

    return insights


def get_restock_recommendations(df):
    """Return products requiring restocking."""

    recommendations = df[
        df["Smart Recommendation"].isin(
            ["Urgent Restock", "Restock Soon"]
        )
    ].copy()

    recommendations = recommendations[
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

    return recommendations.sort_values(
        "Reorder Quantity",
        ascending=False
    )


def get_movement_summary(df):
    """Summarize fast, moderate and slow-moving products."""

    product_summary = (
        df.groupby("Product ID")
        .agg(
            Total_Sales=("Units Sold", "sum"),
            Total_Inventory=("Inventory Level", "sum")
        )
    )

    product_summary["Sell_Through_Rate"] = (
        product_summary["Total_Sales"]
        / (
            product_summary["Total_Sales"]
            + product_summary["Total_Inventory"]
        ).replace(0, 1)
        * 100
    )

    product_summary["Movement"] = "Moderate Moving"

    product_summary.loc[
        product_summary["Sell_Through_Rate"] >= 30,
        "Movement"
    ] = "Fast Moving"

    product_summary.loc[
        product_summary["Sell_Through_Rate"] < 20,
        "Movement"
    ] = "Slow Moving"

    return product_summary.reset_index()