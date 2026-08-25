import matplotlib.pyplot as plt
w1=[45,50,55,60,65]; h1=[150,155,160,165,170]
w2=[55,60,65,70,75]; h2=[155,160,165,170,175]
w3=[65,70,75,80,85]; h3=[160,165,170,175,180]
plt.scatter(w1,h1,label="Group 1"); plt.scatter(w2,h2,label="Group 2"); plt.scatter(w3,h3,label="Group 3")
plt.xlabel("Weight"); plt.ylabel("Height"); plt.title("Weight vs Height"); plt.legend(); plt.show()