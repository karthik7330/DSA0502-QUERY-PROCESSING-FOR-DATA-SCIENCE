import pandas as pd

orders = pd.read_csv("Orders.csv")
returns = pd.read_csv("Returns.csv")

data = pd.merge(orders, returns, on="OrderID", how="left")

data["Returned"] = data["OrderID"].isin(returns["OrderID"])

total_orders = len(orders)

returned_orders = data["Returned"].sum()

return_percentage = (returned_orders / total_orders) * 100

print("Return Percentage =", round(return_percentage, 2), "%")

returned_products = data[data["Returned"] == True]

print("\nFrequently Returned Products")

product_returns = returned_products.groupby("ProductName").size()

print(product_returns)

print("\nCategory-wise Returns")

category_returns = returned_products.groupby("Category").size()

print(category_returns)

cleaned_data = data.drop_duplicates()

cleaned_data.to_csv("Cleaned_Orders.csv", index=False)

print("\nCleaned dataset exported successfully.")
