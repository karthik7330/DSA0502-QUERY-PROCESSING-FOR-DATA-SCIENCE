import pandas as pd
df=pd.read_csv("../csv_files/random_with_nan.csv")
print(df.fillna(0))