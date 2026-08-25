import pandas as pd
df=pd.read_csv("../csv_files/people.csv")
df["name"]=df["name"].str.swapcase()
print(df)