import pandas as pd
df=pd.read_csv("../csv_files/school_students.csv")
print(df.groupby("school_code")["age"].agg(["mean","min","max"]))