import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix

data = pd.read_csv("ecommerce_sales.csv")
data["Date"] = pd.to_datetime(data["Date"])

print(data.head())
print(data.info())
print(data.describe())

monthly_revenue = data.groupby(data["Date"].dt.to_period("M"))["Revenue"].sum()

plt.figure()
plt.plot(monthly_revenue.index.astype(str), monthly_revenue.values, marker="o", label="Revenue")
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

category_revenue = data.groupby("Product_Category")["Revenue"].sum()

plt.figure()
plt.bar(category_revenue.index, category_revenue.values)
plt.title("Revenue by Product Category")
plt.xlabel("Product Category")
plt.ylabel("Revenue")
plt.tight_layout()
plt.show()

plt.figure()
plt.hist(data["Revenue"], bins=5)
plt.title("Revenue Distribution")
plt.xlabel("Revenue")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

rating_counts = data["Customer_Rating"].value_counts().sort_index()

plt.figure()
plt.bar(rating_counts.index.astype(str), rating_counts.values)
plt.title("Customer Rating Frequency")
plt.xlabel("Customer Rating")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

plt.figure()
plt.scatter(data["Discount"], data["Revenue"])
plt.title("Discount vs Revenue")
plt.xlabel("Discount")
plt.ylabel("Revenue")
plt.grid(True)
plt.tight_layout()
plt.show()

scatter_matrix(data[["Quantity_Sold","Revenue","Discount","Customer_Rating"]], figsize=(8,8))
plt.suptitle("Scatter Matrix of E-Commerce Variables")
plt.show()
