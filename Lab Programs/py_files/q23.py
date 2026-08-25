import pandas as pd
import matplotlib.pyplot as plt
df=pd.read_csv("../csv_files/axis_values.csv")
plt.plot(df["x"],df["y"]); plt.xlabel("X Axis"); plt.ylabel("Y Axis"); plt.title("Line Plot from File"); plt.show()