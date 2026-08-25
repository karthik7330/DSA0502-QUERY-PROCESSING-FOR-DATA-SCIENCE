import pandas as pd
import numpy as np

df = pd.DataFrame(np.random.randn(10, 4), columns=["A", "B", "C", "D"])

df.iloc[1, 1] = np.nan
df.iloc[4, 2] = np.nan
df.iloc[7, 0] = np.nan

styled_df = df.style.highlight_null()

print(df)

styled_df.to_html("q11_output.html")

print("\nOutput saved to q11_output.html")