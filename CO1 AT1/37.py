import pandas as pd


suppliers = pd.read_csv("Suppliers.csv")
deliveries = pd.read_csv("Deliveries.csv")

data = pd.merge(deliveries, suppliers, on="SupplierID")


data["Delayed"] = data["ActualDays"] > data["ExpectedDays"]

data["Efficiency"] = (data["ExpectedDays"] / data["ActualDays"]) * 100

print("Delivery Efficiency")

print(data[["SupplierName", "DeliveryID", "Efficiency"]])

print("\nDelayed Suppliers")

delayed = data[data["Delayed"] == True]

print(delayed[["SupplierName", "DeliveryID"]])

print("\nSupplier Performance Summary")

summary = data.groupby("SupplierName").agg({
    "Efficiency":"mean",
    "Delayed":"sum"
})

print(summary)

cleaned_data = data.drop_duplicates()

cleaned_data.to_csv("Cleaned_Suppliers.csv", index=False)

print("\nCleaned dataset exported successfully.")