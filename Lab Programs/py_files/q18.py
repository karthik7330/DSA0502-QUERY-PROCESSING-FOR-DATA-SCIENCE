import pandas as pd
df=pd.read_csv("../csv_files/school_students.csv")
for name,group in df.groupby(["school_code","class"]): print("\n",name,"\n",group)