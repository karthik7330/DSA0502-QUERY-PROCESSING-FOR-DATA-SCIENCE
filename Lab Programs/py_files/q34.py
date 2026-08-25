import numpy as np
import matplotlib.pyplot as plt
x=np.random.rand(50); y=np.random.rand(50); s=np.random.randint(20,500,50)
plt.scatter(x,y,s=s,alpha=.6); plt.title("Different Ball Sizes"); plt.show()