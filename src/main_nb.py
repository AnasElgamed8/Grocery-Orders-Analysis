import marimo

__generated_with = "0.24.0"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    from pathlib import Path
    import pandas as pd
    from matplotlib import pyplot as plt

    class GroceryData:
        def __init__(self):
            # Get the current dir, then go to the project root
            self._base_dir = Path(__file__).resolve().parent.parent
            self._data_dir = self._base_dir / "data"
            # Cached dataframe check
            try:
                self.df = pd.read_pickle(self._data_dir / "merged.pkl")
                print("Cached dataset found, using that")

            except FileNotFoundError:
                print("Couldn't find the cached dataset, starting from scratch")
                # Create a dict of dataframes, one for each file
                data_dict = {
                    file.stem: pd.read_csv(file)
                    for file in self._data_dir.glob("*.csv")
                }

                self.cleaning(data_dict)
                self.export()

        def cleaning(self, data_dict):
            # Merge train and prior (I don't even know what was the point of splitting them)
            df = pd.concat(
                [
                    data_dict["order_products__prior"],
                    data_dict["order_products__train"],
                ],
                ignore_index=True,
            )

            # Orders dataframe cleaning
            orders = data_dict["orders"].copy()
            # eval_set isn't needed
            orders = orders.drop(columns=["eval_set"])
            # first order = -1 instead of nan
            orders["days_since_prior_order"] = orders["days_since_prior_order"].fillna(
                -1
            )

            # merging
            df = pd.merge(df, orders, how="left", on="order_id")
            df = pd.merge(df, data_dict["products"], how="left", on="product_id")
            df = pd.merge(df, data_dict["aisles"], how="left", on="aisle_id")
            df = pd.merge(df, data_dict["departments"], how="left", on="department_id")
            self.df = df.copy()

        def export(self):
            # cache a version of the merged dataframe
            self.df.to_pickle(self._data_dir / "merged.pkl")

    return GroceryData, plt


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
    top_products = df["product_name"].value_counts().head(20)

    plt.figure(figsize=(12, 6))
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

    # This removes the empty legend box since you don't have multiple categories here
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


if __name__ == "__main__":
    app.run()
