import pandas as pd
df=pd.read_csv("../csv_files/people.csv")
print(df[["name","score"]])