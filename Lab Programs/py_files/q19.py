import pandas as pd
df=pd.read_csv("../csv_files/world_alcohol_consumption.csv")
print("Shape:",df.shape)
print("Columns:",df.columns.tolist())