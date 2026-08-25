import pandas as pd
df=pd.read_csv("../csv_files/school_students.csv")
g=df.groupby("school_code")
print(type(g))
for name,group in g: print("\n",name,"\n",group)