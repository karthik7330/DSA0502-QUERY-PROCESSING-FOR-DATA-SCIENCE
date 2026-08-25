import pandas as pd
import numpy as np

df = pd.DataFrame(np.random.randn(10,4), columns=["A","B","C","D"])

styled = df.style.set_properties(
    **{"background-color":"black","color":"yellow"}
)

styled.to_html("q12_output.html")

print(df)
print("Styled output saved in q12_output.html")