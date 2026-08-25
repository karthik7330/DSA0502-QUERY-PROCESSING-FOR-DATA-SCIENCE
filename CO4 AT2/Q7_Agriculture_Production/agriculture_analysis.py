import pandas as pd
import re
import matplotlib.pyplot as plt

raw = pd.read_csv(
    "Production-Department_of_Agriculture_and_Cooperation_1.csv"
)

raw.columns = [str(c).strip() for c in raw.columns]

# Convert the wide annual dataset to a long analysis table
year_cols = [
    c for c in raw.columns
    if re.fullmatch(r"3-\d{4}", c)
    and 2003 <= int(c.split("-")[1]) <= 2014
]

data = raw[
    ["Particulars","Frequency","Unit"] + year_cols
].melt(
    id_vars=["Particulars","Frequency","Unit"],
    var_name="Year",
    value_name="Value"
)

data["Year"] = data["Year"].str.extract(r"(\d{4})").astype(int)
data["Value"] = pd.to_numeric(data["Value"], errors="coerce")
data = data.dropna(subset=["Value"])

print("RAW DATA SHAPE:", raw.shape)
print("LONG DATA SHAPE:", data.shape)
print("\nFIRST FIVE RECORDS:")
print(data.head())
print("\nMISSING VALUES:")
print(data.isnull().sum())
print("\nDUPLICATES:", data.duplicated().sum())
print("\nSUMMARY:")
print(data["Value"].describe())

foodgrain = data[
    data["Particulars"].str.contains(
        "Agricultural Production Foodgrains",
        case=False,
        na=False
    )
]

yearly = foodgrain.groupby("Year")["Value"].mean()
print("\nALL-INDIA FOODGRAIN PRODUCTION BY YEAR:")
print(yearly)

top = data.groupby("Particulars")["Value"].mean().sort_values(
    ascending=False
).head(10)

print("\nTOP 10 AGRICULTURAL SERIES:")
print(top)

# Correlation of selected high-value series across years
selected = top.index
pivot = data[data["Particulars"].isin(selected)].pivot_table(
    index="Year", columns="Particulars", values="Value", aggfunc="mean"
)

corr = pivot.corr()
print("\nCORRELATION:")
print(corr)

# IQR outlier detection
q1 = data["Value"].quantile(0.25)
q3 = data["Value"].quantile(0.75)
iqr = q3 - q1
lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr

data["outlier"] = (
    (data["Value"] < lower) |
    (data["Value"] > upper)
)

print("\nOUTLIER LIMITS:", lower, upper)
print("\nOUTLIERS:")
print(data[data["outlier"]][["Particulars","Year","Value"]].head(20))

# Charts
yearly.plot(kind="line", marker="o",
    title="All-India Foodgrain Production Trend, 2003–2014")
plt.xlabel("Year")
plt.ylabel("Production (dataset unit)")
plt.tight_layout()
plt.savefig("01_foodgrain_yearly_trend.png", dpi=160)
plt.close()

top.sort_values().plot(kind="barh",
    title="Top 10 Agricultural Series by Average Value")
plt.xlabel("Average Value")
plt.tight_layout()
plt.savefig("02_top_agricultural_series.png", dpi=160)
plt.close()

plt.figure(figsize=(10,6))
for col in pivot.columns[:6]:
    plt.plot(pivot.index, pivot[col], marker="o",
             label=str(col)[:35])
plt.title("Selected Agricultural Series Over Time")
plt.xlabel("Year")
plt.ylabel("Value")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig("03_selected_series_trends.png", dpi=160)
plt.close()

plt.figure(figsize=(9,6))
plt.imshow(corr, interpolation="nearest")
plt.xticks(range(len(corr.columns)),
           [str(x)[:20] for x in corr.columns],
           rotation=75, fontsize=7)
plt.yticks(range(len(corr.columns)),
           [str(x)[:20] for x in corr.columns], fontsize=7)
plt.colorbar()
plt.title("Agricultural Series Correlation Matrix")
plt.tight_layout()
plt.savefig("04_correlation_matrix.png", dpi=160)
plt.close()

plt.hist(data["Value"], bins=20)
plt.title("Distribution of Agricultural Values")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("05_value_distribution.png", dpi=160)
plt.close()

plt.figure(figsize=(11,6))
plt.imshow(pivot.T, aspect="auto", interpolation="nearest")
plt.yticks(range(len(pivot.columns)),
           [str(x)[:25] for x in pivot.columns], fontsize=7)
plt.xticks(range(len(pivot.index)), pivot.index, rotation=45)
plt.colorbar()
plt.title("Agricultural Series by Year")
plt.xlabel("Year")
plt.ylabel("Series")
plt.tight_layout()
plt.savefig("06_year_series_heatmap.png", dpi=160)
plt.close()

data.to_csv("agriculture_long_2003_2014.csv", index=False)
data.to_json("agriculture_long_2003_2014.json", orient="records", indent=4)

print("\nSaved agriculture_long_2003_2014.csv and agriculture_long_2003_2014.json")
print("\nNote: this resource is an all-India dataset and has no state/district field,")
print("so a geographic map is not valid for this specific dataset.")
