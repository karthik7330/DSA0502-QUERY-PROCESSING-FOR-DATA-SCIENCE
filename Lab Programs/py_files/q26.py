import matplotlib.pyplot as plt
x=[1,2,3,4,5]; y=[2,4,6,8,10]
plt.subplot(2,1,1); plt.plot(x,y); plt.title("Line Plot")
plt.subplot(2,1,2); plt.bar(x,y); plt.title("Bar Plot"); plt.tight_layout(); plt.show()