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
                file.stem: pd.read_csv(file) for file in self._data_dir.glob("*.csv")
            }

            self.cleaning(data_dict)
            self.export()

    def cleaning(self, data_dict):
        # Merge train and prior (I don't even know what was the point of splitting them)
        df = pd.concat(
            [data_dict["order_products__prior"], data_dict["order_products__train"]],
            ignore_index=True,
        )

        # Orders dataframe cleaning
        orders = data_dict["orders"].copy()
        # eval_set isn't needed
        orders = orders.drop(columns=["eval_set"])
        # first order = -1 instead of nan
        orders["days_since_prior_order"] = orders["days_since_prior_order"].fillna(-1)

        # merging
        df = pd.merge(df, orders, how="left", on="order_id")
        df = pd.merge(df, data_dict["products"], how="left", on="product_id")
        df = pd.merge(df, data_dict["aisles"], how="left", on="aisle_id")
        df = pd.merge(df, data_dict["departments"], how="left", on="department_id")
        self.df = df.copy()

    def export(self):
        # cache a version of the merged dataframe
        self.df.to_pickle(self._data_dir / "merged.pkl")


if __name__ == "__main__":
    data = GroceryData()
    df = data.df
    top_products = df["product_name"].value_counts()
    plt.figure(figsize=(12, 5))
    plt.plot(top_products)
    plt.title("Top ordered products", fontsize=16)
    plt.xlabel("Product Name", fontsize=13)
    plt.ylabel("Number of Orders", fontsize=13)
    plt.xticks(fontsize=11)
    plt.yticks(fontsize=11)
    plt.grid(True)
    plt.legend()
    plt.show()
