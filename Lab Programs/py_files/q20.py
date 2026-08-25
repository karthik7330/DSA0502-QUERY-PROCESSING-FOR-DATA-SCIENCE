import pandas as pd
df=pd.read_csv("../csv_files/people.csv")
s="ha"
r=df[df["name"].str.contains(s,case=False,na=False)]
print(r)
print("Indexes:",r.index.tolist())