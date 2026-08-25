import pandas as pd
df=pd.read_csv("../csv_files/sales_region_manager_salesman.csv")
print(pd.pivot_table(df,values="Sale_Amount",index=["Region","Manager","Salesman"],aggfunc="sum"))