import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix, lag_plot, autocorrelation_plot
import numpy as np

data = pd.read_csv("employee_productivity.csv")

print(data.head())
print(data.info())
print(data.describe())

plt.figure()
plt.scatter(data["Working_Hours"], data["Productivity_Score"])
plt.title("Working Hours vs Productivity")
plt.xlabel("Working Hours")
plt.ylabel("Productivity Score")
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure()
plt.scatter(data["Experience"], data["Productivity_Score"])
plt.title("Experience vs Productivity")
plt.xlabel("Experience")
plt.ylabel("Productivity Score")
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure()
plt.hist(data["Productivity_Score"], bins=5)
plt.title("Productivity Score Distribution")
plt.xlabel("Productivity Score")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

plt.figure()
plt.bar(data["Employee_ID"], data["Monthly_Performance"])
plt.title("Monthly Performance by Employee")
plt.xlabel("Employee ID")
plt.ylabel("Monthly Performance")
plt.tight_layout()
plt.show()

scatter_matrix(data[["Working_Hours","Experience","Tasks_Completed","Productivity_Score"]], figsize=(8,8))
plt.suptitle("Scatter Matrix of Employee Variables")
plt.show()

plt.figure()
lag_plot(data["Monthly_Performance"])
plt.title("Lag Plot of Monthly Performance")
plt.tight_layout()
plt.show()

plt.figure()
autocorrelation_plot(data["Monthly_Performance"])
plt.title("Autocorrelation Plot of Monthly Performance")
plt.tight_layout()
plt.show()

means = []
scores = data["Productivity_Score"].values
n = len(scores)

for i in range(1000):
    sample = np.random.choice(scores, size=n, replace=True)
    means.append(sample.mean())

plt.figure()
plt.hist(means, bins=20)
plt.title("Bootstrap Distribution of Mean Productivity")
plt.xlabel("Mean Productivity")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()
