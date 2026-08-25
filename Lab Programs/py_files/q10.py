import pandas as pd
import numpy as np

df = pd.DataFrame(np.random.randn(10, 4), columns=["A", "B", "C", "D"])

def highlight(value):
    if value < 0:
        return "color: red"
    else:
        return "color: black"

styled_df = df.style.map(highlight)

print(df)
styled_df.to_html("q10_output.html")

print("\nOutput saved to q10_output.html")