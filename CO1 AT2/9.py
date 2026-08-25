import pandas as pd

df = pd.read_csv("weather.csv")

print("Highest Temperature:", df["Temperature"].max())
print("Lowest Temperature:", df["Temperature"].min())
print("Average Rainfall:", df["Rainfall"].mean())

print("\nRainfall Greater than 100 mm:")
print(df[df["Rainfall"] > 100])