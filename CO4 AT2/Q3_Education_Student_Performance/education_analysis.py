import pandas as pd
import matplotlib.pyplot as plt

# Real UCI Student Performance files
math = pd.read_csv("student-mat.csv", sep=";")
portuguese = pd.read_csv("student-por.csv", sep=";")

# Same matching logic as the uploaded student-merge.R file
keys = [
    "school","sex","age","address","famsize","Pstatus","Medu","Fedu",
    "Mjob","Fjob","reason","nursery","internet"
]

data = pd.merge(
    math, portuguese,
    on=keys, how="inner",
    suffixes=("_math", "_por")
)

data["student_id"] = ["S" + str(i).zfill(3) for i in range(1, len(data)+1)]
data["avg_final_grade"] = data[["G3_math","G3_por"]].mean(axis=1)
data["avg_mid_grade"] = data[["G1_math","G1_por","G2_math","G2_por"]].mean(axis=1)
data["avg_absences"] = data[["absences_math","absences_por"]].mean(axis=1)

data["performance_level"] = pd.cut(
    data["avg_final_grade"],
    bins=[-float("inf"), 9, 13, 16, float("inf")],
    labels=["Needs Improvement","Average","Good","Excellent"]
)

print("Math records:", len(math))
print("Portuguese records:", len(portuguese))
print("Integrated records:", len(data))
print("\nFirst five records:")
print(data.head())
print("\nMissing values:")
print(data.isnull().sum())
print("\nDuplicates:", data.duplicated().sum())
print("\nSummary:")
print(data[["avg_final_grade","avg_absences","failures_math","studytime_math"]].describe())

print("\nSchool performance:")
print(data.groupby("school")["avg_final_grade"].mean().sort_values(ascending=False))

print("\nGender performance:")
print(data.groupby("sex")["avg_final_grade"].mean())

print("\nStudy-time performance:")
print(data.groupby("studytime_math")["avg_final_grade"].mean())

corr = data[[
    "avg_final_grade","avg_mid_grade","avg_absences",
    "failures_math","studytime_math","G1_math","G2_math","G3_math",
    "G1_por","G2_por","G3_por"
]].corr()

print("\nCorrelation matrix:")
print(corr)

q1 = data["avg_final_grade"].quantile(0.25)
q3 = data["avg_final_grade"].quantile(0.75)
iqr = q3 - q1
lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr

data["grade_outlier"] = (
    (data["avg_final_grade"] < lower) |
    (data["avg_final_grade"] > upper)
)

print("\nOutlier limits:", lower, upper)
print("\nGrade outliers:")
print(data[data["grade_outlier"]][
    ["student_id","school","sex","avg_final_grade"]
])

# Charts
data.groupby("school")["avg_final_grade"].mean().plot(kind="bar",
    title="Average Final Grade by School")
plt.xlabel("School")
plt.ylabel("Average Final Grade")
plt.tight_layout()
plt.savefig("01_school_performance.png", dpi=160)
plt.close()

data.groupby("sex")["avg_final_grade"].mean().plot(kind="bar",
    title="Average Final Grade by Gender")
plt.xlabel("Gender")
plt.ylabel("Average Final Grade")
plt.tight_layout()
plt.savefig("02_gender_performance.png", dpi=160)
plt.close()

data.groupby("studytime_math")["avg_final_grade"].mean().sort_index().plot(
    kind="bar", title="Average Final Grade by Study Time")
plt.xlabel("Study Time Code")
plt.ylabel("Average Final Grade")
plt.tight_layout()
plt.savefig("03_studytime_vs_grade.png", dpi=160)
plt.close()

plt.scatter(data["avg_absences"], data["avg_final_grade"])
plt.title("Absences vs Average Final Grade")
plt.xlabel("Average Absences")
plt.ylabel("Average Final Grade")
plt.tight_layout()
plt.savefig("04_absences_vs_grade.png", dpi=160)
plt.close()

plt.hist(data["avg_final_grade"], bins=10)
plt.title("Distribution of Average Final Grades")
plt.xlabel("Average Final Grade")
plt.ylabel("Number of Students")
plt.tight_layout()
plt.savefig("05_grade_distribution.png", dpi=160)
plt.close()

plt.imshow(corr, interpolation="nearest")
plt.xticks(range(len(corr.columns)), corr.columns, rotation=75, fontsize=7)
plt.yticks(range(len(corr.columns)), corr.columns, fontsize=7)
plt.colorbar()
plt.title("Education Correlation Matrix")
plt.tight_layout()
plt.savefig("06_correlation_matrix.png", dpi=160)
plt.close()

data.to_csv("education_integrated_master.csv", index=False)
data.to_json("education_integrated_master.json", orient="records", indent=4)

print("\nSaved education_integrated_master.csv and education_integrated_master.json")
