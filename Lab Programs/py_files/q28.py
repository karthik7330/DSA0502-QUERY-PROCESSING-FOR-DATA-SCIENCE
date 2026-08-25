import matplotlib.pyplot as plt
l=["Python","Java","C++","JavaScript","C","R"]; p=[90,75,65,60,55,40]
plt.barh(l,p); plt.xlabel("Popularity"); plt.ylabel("Language"); plt.title("Programming Languages"); plt.show()