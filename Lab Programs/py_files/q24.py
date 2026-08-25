import pandas as pd
import matplotlib.pyplot as plt
df=pd.read_csv("../csv_files/financial_data.csv")
plt.plot(df["Date"],df["Open"],label="Open"); plt.plot(df["Date"],df["Close"],label="Close")
plt.xlabel("Date"); plt.ylabel("Price"); plt.title("Financial Data"); plt.legend(); plt.xticks(rotation=45); plt.tight_layout(); plt.show()