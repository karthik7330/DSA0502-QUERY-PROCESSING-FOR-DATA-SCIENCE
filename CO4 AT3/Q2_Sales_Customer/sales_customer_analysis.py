import pandas as pd
import matplotlib.pyplot as plt

customers = pd.read_csv("customers.csv")
sales = pd.read_csv("sales.csv")

data = pd.merge(
    customers, sales,
    on="Customer_ID",
    how="left"
)

print("Integrated records:", len(data))
print("\nFirst five records:")
print(data.head())

print("\nMissing values:")
print(data.isnull().sum())

print("\nDuplicates:", data.duplicated().sum())

print("\nSummary:")
print(data.describe())

# Filtering
print("\nHigh-value purchases >= 15000:")
print(data[data["Purchase_Amount"] >= 15000][
    ["Customer_Name","Purchase_Amount"]
])

# Sorting
print("\nTop purchases:")
print(data.sort_values(
    "Purchase_Amount", ascending=False
)[["Customer_Name","Purchase_Amount"]].head(5))

# Grouping
print("\nSales by location:")
print(data.groupby("Location")["Purchase_Amount"].sum())

# Customer segmentation
data["Customer_Segment"] = pd.cut(
    data["Purchase_Amount"],
    bins=[0, 7500, 15000, float("inf")],
    labels=["Low Value","Medium Value","High Value"]
)

print("\nCustomer segments:")
print(data["Customer_Segment"].value_counts())

# Correlation
corr = data[[
    "Age",
    "Purchase_Frequency",
    "Discount",
    "Purchase_Amount"
]].corr()

print("\nCorrelation matrix:")
print(corr)

# IQR outlier detection
q1 = data["Purchase_Amount"].quantile(0.25)
q3 = data["Purchase_Amount"].quantile(0.75)
iqr = q3 - q1
lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr

data["Purchase_Outlier"] = (
    (data["Purchase_Amount"] < lower) |
    (data["Purchase_Amount"] > upper)
)

print("\nOutlier limits:", lower, upper)
print("\nPurchase outliers:")
print(data[data["Purchase_Outlier"]][
    ["Customer_Name","Purchase_Amount"]
])

# Charts
plt.scatter(data["Age"], data["Purchase_Amount"])
plt.title("Customer Age vs Purchase Amount")
plt.xlabel("Age")
plt.ylabel("Purchase Amount")
plt.tight_layout()
plt.savefig("01_age_vs_purchase.png", dpi=160)
plt.close()

plt.scatter(data["Purchase_Frequency"], data["Purchase_Amount"])
plt.title("Purchase Frequency vs Purchase Amount")
plt.xlabel("Purchase Frequency")
plt.ylabel("Purchase Amount")
plt.tight_layout()
plt.savefig("02_frequency_vs_purchase.png", dpi=160)
plt.close()

plt.scatter(data["Discount"], data["Purchase_Amount"])
plt.title("Discount vs Purchase Amount")
plt.xlabel("Discount (%)")
plt.ylabel("Purchase Amount")
plt.tight_layout()
plt.savefig("03_discount_vs_purchase.png", dpi=160)
plt.close()

data.groupby("Customer_Segment")["Purchase_Amount"].mean().plot(
    kind="bar", title="Average Purchase by Customer Segment"
)
plt.xlabel("Customer Segment")
plt.ylabel("Average Purchase Amount")
plt.tight_layout()
plt.savefig("04_customer_segments.png", dpi=160)
plt.close()

data.groupby("Location")["Purchase_Amount"].sum().sort_values().plot(
    kind="barh", title="Sales by Location"
)
plt.xlabel("Total Purchase Amount")
plt.ylabel("Location")
plt.tight_layout()
plt.savefig("05_location_sales.png", dpi=160)
plt.close()

plt.imshow(corr, interpolation="nearest")
plt.xticks(range(len(corr.columns)), corr.columns, rotation=45)
plt.yticks(range(len(corr.columns)), corr.columns)
plt.colorbar()
plt.title("Sales and Customer Correlation Matrix")
plt.tight_layout()
plt.savefig("06_correlation_heatmap.png", dpi=160)
plt.close()

data.to_csv("sales_customer_integrated.csv", index=False)
data.to_json("sales_customer_integrated.json", orient="records", indent=4)

print("\nSaved integrated CSV and JSON.")
