import marimo

__generated_with = "0.24.0"
app = marimo.App(width="full", layout_file="layouts/notebook.slides.json")


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
def _(plt, sns):
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
            # "axes.prop_cycle": plt.cycler(color=["#dc2626"]),
            "axes.prop_cycle": plt.cycler(
                color=sns.color_palette(palette="RdGy")
            ),
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # A look into a grocery store's data

    Made by Anas Hossam
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    # What does the data consist of?
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    - **Scale:** ~3.4M orders, ~32M prior order-product rows, ~50k products
    - Distributed across 21 departments, and 134 aisles
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Case Overview

    Given the order data (~3.4M orders, ~50k products), I wanted to
    understand the shape of customer behavior: what gets bought, when, and
    what makes people come back for the same items.

    Questions I started with:
    - When do different categories get ordered?
    - How loyal are customers to specific products/categories?
    - Does cart position say anything about an item?
    - Does how often someone shops affect how much they buy per trip?
    """)
    return


@app.cell
def _(GroceryData):
    data = GroceryData()
    df = data.df
    df
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Know your customers
    Before anything else, who are we even looking at?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### How Many Orders Does a Typical Customer Place?
    """)
    return


@app.cell
def _(df):
    total_orders_user = df.groupby("user_id")["order_id"].nunique()
    total_orders_user.describe()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## We now know that:
    * We have a total of 206,209 customers
    * The minimum number of orders for a customer was 3
    * The maximum number of orders was 100
    * The average customer places 16 orders
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## What's In The Cart
    Before timing or loyalty, what does this store actually sell, and
    what do people actually buy?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Most Popular Products
    """)
    return


@app.cell
def _(df, plt):
    top_products = (
        df["product_name"].value_counts().sort_values(ascending=False).head(20)
    )

    plt.figure()
    plt.barh(
        top_products.index[::-1],
        top_products.values[::-1],
    )
    plt.title("Top 20 Ordered Products")
    plt.ylabel("Product Name")
    plt.xlabel("Number of Orders")
    plt.xticks()
    plt.yticks()
    plt.grid()
    plt.tight_layout()
    plt.gcf()
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## We now know that:
    - Vegetables and fruits dominate the top order.
    - Bananas are the most ordred items on the list. With ~850 thousand orders.
    - Spinach is the most ordered vegetable
    - Whole milk is the most ordered dairy product
    <!--Note to self. Only 3 types of products appear in the chart. might be quite boring  -->
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Orders by Department
    """)
    return


@app.cell
def _(df):
    orders_by_department = df.groupby("department")["order_id"].nunique()
    orders_by_department.sort_values(ascending=False, inplace=True)
    return (orders_by_department,)


@app.cell
def _(orders_by_department, plt):
    plt.barh(
        orders_by_department.index[::-1],
        orders_by_department.values[::-1],
    )
    plt.title("Total number of orders per department")
    plt.ylabel("Departments")
    plt.xlabel("Number of Orders")
    plt.yticks()
    plt.grid()
    plt.tight_layout()
    plt.gcf()
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## We now know that:
    - The diary & Eggs and the produce departments are the top 2 departments. Which aligns with our findings in the top products section.
    - A sudden drop happens at the number of orders in the rest of the departments
    - The worst performing departments are: bulk, pets, and other
    <!--Note to self: The top section is called produce, I assume that it means vegs and fruits, but the name sounds wrong.
    how could a deparment be called bulk,missing or other? might have to look into that-->
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Orders by Aisle (Top 20)
    """)
    return


@app.cell
def _(df):
    orders_by_aisle = (
        df.groupby("aisle")["order_id"]
        .nunique()
        .sort_values(ascending=False)
        .head(20)
    )
    return (orders_by_aisle,)


@app.cell
def _(orders_by_aisle, plt):
    plt.barh(
        orders_by_aisle.index[::-1],
        orders_by_aisle.values[::-1],
    )
    plt.title("Total number of orders per aisle")
    plt.ylabel("Aisles")
    plt.xlabel("Number of Orders")
    plt.xticks(rotation=30, ha="right")
    plt.yticks()
    plt.grid()
    plt.tight_layout()
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## When People Shop
    Now that we know what's popular. when does it actually get bought?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Orders by Day of the Week
    """)
    return


@app.cell
def _(df, pd):
    days = [
        "Sunday",
        "Monday",
        "Tuesday",
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
    total_orders_day
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
    plt.xticks()
    plt.yticks()
    plt.grid()
    plt.tight_layout()
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Orders by Hour of the Day
    """)
    return


@app.cell
def _(df):
    total_orders_hour = df.groupby("order_hour_of_day")["order_id"].nunique()
    hours = ["12AM"]
    for i in range(1, 24):
        if i < 12:
            hours.append(f"{i}AM")
        elif i == 12:
            hours.append(f"12PM")
        else:
            hours.append(f"{i % 12}PM")
    return hours, total_orders_hour


@app.cell
def _(hours, np, plt, total_orders_hour):
    plt.bar(
        total_orders_hour.index,
        total_orders_hour.values,
    )
    plt.title("Total number of orders per hour")
    plt.xlabel("Hour")
    plt.ylabel("Number of Orders")
    plt.xticks(np.arange(0, 24, step=1), labels=hours, rotation=30)
    plt.yticks()
    plt.grid()
    plt.tight_layout()
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Order Volume: Day vs. Hour
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
def _(days, hours, order_day_hour, plt, sns):
    sns.heatmap(order_day_hour, yticklabels=days, xticklabels=hours)
    plt.title("Hour to day relationship")
    plt.xlabel("Hour")
    plt.ylabel("Day")
    plt.gcf()
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## We now know that:
    - We get the most orders on Sundays and Mondays
    - We get the least orders on Thursdays
    - The least amount of orders happens between midnight and 6 AM
    - The busiest part of the day is from 10 AM to 4 PM. With 10 AM being the busiest.
    - We get the most amount of orders on Mondays at 10 AM
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Order Timing by Department
    """)
    return


@app.cell
def _(df, pd):
    department_hour = pd.crosstab(
        df["department"],
        df["order_hour_of_day"],
        values=df["order_id"],
        aggfunc="nunique",
    )
    return (department_hour,)


@app.cell
def _(department_hour, hours, plt, sns):
    sns.heatmap(department_hour, xticklabels=hours)
    plt.title("Hour to department relationship")
    plt.xlabel("Hour")
    plt.ylabel("Department")
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Takeaway: Timing x Department

    - The pattern from our previous findings presists. all of the departments get the most orders at day.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Loyalty & Reorders
    Who keeps coming back for the same thing, and what?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Overall Reorder Rate
    """)
    return


@app.cell
def _(df):
    valid_reorder = df[df["order_number"] > 1]
    return (valid_reorder,)


@app.cell
def _(plt, valid_reorder):
    rate = valid_reorder["reordered"].mean()
    plt.pie(
        [rate, 1 - rate],
        labels=["Reordered", "New Item"],
        autopct="%1.1f%%",
    )
    plt.legend()
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Reorder Rate by Department
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
    plt.barh(reorder_dept.index[::-1], reorder_dept.values[::-1])
    plt.title("Reorder Rate by Department")
    plt.ylabel("Department")
    plt.xlabel("Reorder Probability (0 to 1)")
    plt.xticks(rotation=45, ha="right")
    plt.grid()
    plt.tight_layout()
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## We now know that:
    - The reorder rate is 62.9%
    - Diary and eggs have the top reorder rate
    - Personal care and pantry have the lowest reorder rate
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Reorder Rate by Aisle (Top 20)
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
    plt.barh(reorder_aisle.index[::-1], reorder_aisle.values[::-1])
    plt.title("Top 20 Aisles by Reorder Rate")
    plt.ylabel("Aisle")
    plt.xlabel("Reorder Probability (0 to 1)")
    plt.grid()
    plt.tight_layout()
    plt.gcf()
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cart Behavior
    Does where an item lands in the cart say anything about it?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Cart Position vs. Reorder Probability
    """)
    return


@app.cell
def _(valid_reorder):
    cart_reorder = (
        valid_reorder[valid_reorder["add_to_cart_order"] <= 30]
        .groupby("add_to_cart_order")["reordered"]
        .mean()
    )
    return (cart_reorder,)


@app.cell
def _(cart_reorder, plt):
    plt.plot(cart_reorder.index, cart_reorder.values, marker="o")
    plt.title("Does Cart Position Affect Reordering?")
    plt.xlabel("Position in Cart (1st, 2nd, 3rd...)")
    plt.ylabel("Reorder Probability")
    plt.grid()
    plt.tight_layout()
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #We now know that:
    - Reorder rate is directly affected by cart position
    - We see a steady decrease in reorder rate as the position in cart increases
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Cart Position by Department
    """)
    return


@app.cell
def _(df):
    department_position = (
        df.groupby("department")["add_to_cart_order"]
        .mean()
        .sort_values(ascending=False)
    )
    return (department_position,)


@app.cell
def _(department_position, plt, sns):
    sns.barplot(x=department_position.index, y=department_position.values)
    plt.title("Average Cart Position by Department")
    plt.xlabel("Department")
    plt.ylabel("Avg. Add-to-Cart Position")
    plt.xticks(rotation=45, ha="right")
    plt.grid()
    plt.tight_layout()
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## We now know that:
    - Alcohol and beverages get placed earlier than other products
    - Babies department gets bought at last most of the time
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cadence & Basket Size
    How often people come back, and whether that changes how much they
    buy each time.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Average Time Between Orders
    """)
    return


@app.cell
def _(df):
    unique_orders = df.drop_duplicates(subset=["order_id"])
    time_since_last_order = unique_orders[
        unique_orders["days_since_prior_order"] > -1
    ]
    return (time_since_last_order,)


@app.cell
def _(time_since_last_order):
    x = float(time_since_last_order["days_since_prior_order"].mean())
    x
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Basket Size by Shopping Frequency
    """)
    return


@app.cell
def _(df, pd, time_since_last_order):
    basket_size = (
        df[df["days_since_prior_order"] != -1]
        .groupby("order_id")
        .size()
        .reset_index(name="basket_size")
    )
    orders_with_basket = time_since_last_order.merge(
        basket_size, on="order_id"
    )
    bins = [-1, 7, 14, 21, 30]
    labels = ["0-7d", "8-14d", "15-21d", "22-30d"]
    orders_with_basket["cadence_bucket"] = pd.cut(
        orders_with_basket["days_since_prior_order"], bins=bins, labels=labels
    )
    # 4. compare
    cadence_basket = orders_with_basket.groupby("cadence_bucket")[
        "basket_size"
    ].mean()
    cadence_basket
    return (cadence_basket,)


@app.cell
def _(cadence_basket, plt, sns):
    sns.barplot(x=cadence_basket.index, y=cadence_basket.values)
    plt.title("Cadence Bucket vs Basket Size")
    plt.xlabel("Cadence Bucket")
    plt.ylabel("Basket Size")
    plt.xticks()
    plt.grid()
    plt.tight_layout()
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## We now know that:
    - infrequent shoppers buy more products compared to other people. Though the difference isn't that big
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - Loyalty is high but concentrated: 62.9% of items are reorders overall, but that loyalty lives almost entirely in dairy/eggs and produce.
      personal care and pantry on the other hand barely get repeat purchases.


    - Shopping timing is consistent: the same daytime pattern (peak 10 AM–4 PM, quiet overnight, Sunday/Monday busiest, Thursday quietest)
      holds across every department. No category has its own rhythm.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - Cart order reflects the customers' thougts: alcohol and beverages get added early (planned purchases)
     while baby products get added last (impulse or secondary trip items).


    - Infrequent shoppers buy slightly more per trip than frequent ones. the gap is real but small.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Next Steps

    - **Promote on Thursdays.** It's the lowest-order day of the week and a targeted promotion there is guaranteed to do better, compared to an already good day like Sunday where it might not change much.

    - **Drive repeat purchases in personal care and pantry.** These have the store's lowest reorder rates despite reasonable order volume.
    We should increase the quality of our products there and put more points towards them in the loyalty system (If we have one)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - **Reposition low-traffic departments (bulk, pets, other) with bundle offers** rather than straight discounts.
    These departments aren't getting browsed in the first place, so the goal is getting them into the cart at all, not just cheaper.

    - **Use cart-position data for placement.** Items added late (baby products) are strong candidates for placement near the cashier, since they're already being treated as an afterthought. Putting them somewhere visible might increase their order rates more than fighting the user habbits

    - **Basket affinity analysis** We should check what products get bought together.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Thank You!
    """)
    return


if __name__ == "__main__":
    app.run()
