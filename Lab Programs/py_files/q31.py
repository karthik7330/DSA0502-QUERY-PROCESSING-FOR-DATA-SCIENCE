import matplotlib.pyplot as plt
g=["A","B","C","D"]; v=[20,35,30,40]; e=[3,4,2,5]
plt.bar(g,v,yerr=e,capsize=5); plt.xlabel("Group"); plt.ylabel("Value"); plt.title("Bar Plot with Error Bars"); plt.show()