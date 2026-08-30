import marimo

__generated_with = "0.24.0"
app = marimo.App(width="full", layout_file="layouts/main_nb.slides.json")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    from pathlib import Path
    import pandas as pd
    from matplotlib import pyplot as plt
    import seaborn as sns
    from GroceryData import GroceryData

    return GroceryData, mo, np, pd, plt, sns


@app.cell
def _(plt):
    # Global Matplotlib Settings
    plt.rcParams.update(
        {
            # Dimensions and Background
            "figure.figsize": (12, 6),
            "figure.facecolor": "#ffffff",
            "axes.facecolor": "#ffffff",
            # Fonts and Text Colors
            "text.color": "#333333",
            "axes.labelcolor": "#333333",
            "xtick.color": "#333333",
            "ytick.color": "#333333",
            "font.size": 12,
            "axes.titlesize": 16,
            "axes.labelsize": 13,
            "xtick.labelsize": 11,
            "ytick.labelsize": 11,
            # Borders and Grids
            "axes.edgecolor": "#cccccc",
            "grid.color": "#e5e5e5",
            "grid.alpha": 0.7,
            "grid.linestyle": "--",
            # Colors
            "axes.prop_cycle": plt.cycler(
                color=["#2563eb", "#16a34a", "#d97706", "#dc2626"]
            ),
        }
    )
    return


@app.cell
def _(GroceryData):
    data = GroceryData()
    df = data.df
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 2- Visualization
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    1. Top ordered products
    """)
    return


@app.cell
def _(df, plt):
    top_products = (
        df["product_name"].value_counts().sort_values(ascending=False).head(20)
    )

    plt.figure()
    plt.bar(
        top_products.index,
        top_products.values,
    )
    plt.title("Top 20 Ordered Products")
    plt.xlabel("Product Name")
    plt.ylabel("Number of Orders")
    plt.xticks(rotation=30, ha="right")
    plt.yticks()
    plt.grid()
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(df, plt):
    worst_products = (
        df["product_name"].value_counts().sort_values(ascending=True).head(20)
    )

    plt.figure()
    plt.bar(
        worst_products.index,
        worst_products.values,
    )
    plt.title("worst 20 Ordered Products")
    plt.xlabel("Product Name")
    plt.ylabel("Number of Orders")
    plt.xticks(rotation=30, ha="right")
    plt.yticks()
    plt.grid()
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    2. Number of orders per user
    """)
    return


@app.cell
def _(df):
    total_orders_user = df.groupby("user_id")["order_id"].nunique()
    print(total_orders_user.describe())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We now know that:
    * We have a total of 206209 Users
    * The minimum amout of orders for a user was 3
    * The maximum amount of orders was 100 orders
    * With am average of 16 orders per user
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    3. Number of orders per day
    """)
    return


@app.cell
def _(df, pd):
    days = [
        "Sunday",
        "Monday",
        "Tuseday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
    ]
    total_orders_day = df.groupby("order_dow")["order_id"].nunique()
    total_orders_day = pd.Series(
        total_orders_day.values,
        days,
    )
    print(total_orders_day.head(10))
    return days, total_orders_day


@app.cell
def _(plt, total_orders_day):
    plt.bar(
        total_orders_day.index,
        total_orders_day.values,
    )
    plt.title("Total number of orders per day")
    plt.xlabel("Day")
    plt.ylabel("Number of Orders")
    plt.xticks(rotation=30, ha="right")
    plt.yticks()
    plt.grid()
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    4. Number of orders per hour
    """)
    return


@app.cell
def _(df):
    total_orders_hour = df.groupby("order_hour_of_day")["order_id"].nunique()
    print(total_orders_hour.head(10))
    hours = ["12AM"]
    for i in range(1, 24):
        if i < 12:
            hours.append(f"{i}AM")
        elif i == 12:
            hours.append(f"12PM")
        else:
            hours.append(f"{i % 12}PM")
    print(hours)
    return hours, total_orders_hour


@app.cell
def _(hours, np, plt, total_orders_hour):
    plt.bar(
        total_orders_hour.index,
        total_orders_hour.values,
    )
    plt.title("Total number of orders per hour")
    plt.xlabel("hour")
    plt.ylabel("Number of Orders")
    plt.xticks(np.arange(0, 24, step=1), labels=hours, rotation=30)
    plt.yticks()
    plt.grid()
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    5. Number of orders per hour and day
    """)
    return


@app.cell
def _(df, pd):
    order_day_hour = pd.crosstab(
        df["order_dow"],
        df["order_hour_of_day"],
        values=df["order_id"],
        aggfunc="nunique",
    )
    return (order_day_hour,)


@app.cell
def _(days, hours, order_day_hour, sns):
    sns.heatmap(order_day_hour, yticklabels=days, xticklabels=hours)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    6. Number of orders per department.
    """)
    return


@app.cell
def _(df):
    orders_by_department = df.groupby("department")["order_id"].nunique()
    orders_by_department.sort_values(ascending=False, inplace=True)
    return (orders_by_department,)


@app.cell
def _(orders_by_department, plt):
    plt.bar(
        orders_by_department.index,
        orders_by_department.values,
    )
    plt.title("Total number of orders per department")
    plt.xlabel("Departments")
    plt.ylabel("Number of Orders")
    plt.xticks(rotation=30, ha="right")
    plt.yticks()
    plt.grid()
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    7. Number of orders per aisle.
    """)
    return


@app.cell
def _(df):
    orders_by_aisle = df.groupby("aisle")["order_id"].nunique()
    orders_by_aisle.sort_values(ascending=False, inplace=True)
    return (orders_by_aisle,)


@app.cell
def _(orders_by_aisle, plt):
    plt.bar(
        orders_by_aisle.head(20).index,
        orders_by_aisle.head(20).values,
    )
    plt.title("Total number of orders per aisle")
    plt.xlabel("aisles")
    plt.ylabel("Number of Orders")
    plt.xticks(rotation=30, ha="right")
    plt.yticks()
    plt.grid()
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    8. Reorder rate
    """)
    return


@app.cell
def _(df):
    valid_reorder = df[df["order_number"] > 1]
    return (valid_reorder,)


@app.cell
def _(valid_reorder):
    valid_reorder["reordered"].mean()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    8. Reorder rate by Department
    """)
    return


@app.cell
def _(valid_reorder):
    reorder_dept = (
        valid_reorder.groupby("department")["reordered"]
        .mean()
        .sort_values(ascending=False)
    )
    return (reorder_dept,)


@app.cell
def _(plt, reorder_dept):
    plt.bar(reorder_dept.index, reorder_dept.values)
    plt.title("Reorder Rate by Department")
    plt.xlabel("Department")
    plt.ylabel("Reorder Probability (0 to 1)")
    plt.xticks(rotation=45, ha="right")
    plt.grid()
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    9. Reorder rate by Aisle
    """)
    return


@app.cell
def _(valid_reorder):
    reorder_aisle = (
        valid_reorder.groupby("aisle")["reordered"]
        .mean()
        .sort_values(ascending=False)
        .head(20)
    )
    return (reorder_aisle,)


@app.cell
def _(plt, reorder_aisle):
    plt.bar(reorder_aisle.index, reorder_aisle.values)
    plt.title("Top 20 Aisles by Reorder Rate")
    plt.xlabel("Aisle")
    plt.ylabel("Reorder Probability (0 to 1)")
    plt.xticks(rotation=45, ha="right")
    plt.grid()
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    10. Product placement order vs Reorder rate
    """)
    return


@app.cell
def _(valid_reorder):
    # We cap the cart size at 30 items for the chart so outliers (like a 100-item cart) don't ruin the plot
    cart_reorder = (
        valid_reorder[valid_reorder["add_to_cart_order"] <= 30]
        .groupby("add_to_cart_order")["reordered"]
        .mean()
    )
    return (cart_reorder,)


@app.cell
def _(cart_reorder, plt):
    # Using a line plot here because it shows the trend of probability dropping as items are added later
    plt.plot(cart_reorder.index, cart_reorder.values, marker="o")
    plt.title("Does Cart Position Affect Reordering?")
    plt.xlabel("Position in Cart (1st, 2nd, 3rd...)")
    plt.ylabel("Reorder Probability")
    plt.grid()
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    11. Average delay between each order
    """)
    return


@app.cell
def _(df):
    unique_orders = df.drop_duplicates(subset=["order_id"])

    time_since_last_order = unique_orders[unique_orders["days_since_prior_order"] > -1]
    return (time_since_last_order,)


@app.cell
def _(time_since_last_order):
    print(time_since_last_order["days_since_prior_order"].mean())
    return


if __name__ == "__main__":
    app.run()
