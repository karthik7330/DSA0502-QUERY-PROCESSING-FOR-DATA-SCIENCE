import matplotlib.pyplot as plt
g=["G1","G2","G3","G4"]; m=[80,75,90,85]; w=[85,80,88,92]; x=range(4)
plt.bar([i-.2 for i in x],m,.4,label="Men"); plt.bar([i+.2 for i in x],w,.4,label="Women")
plt.xticks(list(x),g); plt.xlabel("Group"); plt.ylabel("Score"); plt.title("Scores by Group and Gender"); plt.legend(); plt.show()