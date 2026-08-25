import pandas as pd
import matplotlib.pyplot as plt

students = pd.read_csv("students.csv")
attendance = pd.read_csv("attendance.csv")
assignments = pd.read_csv("assignments.csv")
internal = pd.read_csv("internal_marks.csv")
final = pd.read_csv("final_marks.csv")

data = students.merge(attendance, on="Student_ID", how="left")
data = data.merge(assignments, on="Student_ID", how="left")
data = data.merge(internal, on="Student_ID", how="left")
data = data.merge(final, on="Student_ID", how="left")

print("Integrated records:", len(data))
print("\nFirst five records:")
print(data.head())

print("\nMissing values:")
print(data.isnull().sum())

print("\nDuplicate records:", data.duplicated().sum())

print("\nSummary:")
print(data.describe())

# Filtering
print("\nStudents with final marks >= 85:")
print(data[data["Final_Marks"] >= 85][
    ["Student_ID", "Student_Name", "Final_Marks"]
])

# Sorting
print("\nTop students:")
print(data.sort_values("Final_Marks", ascending=False)[
    ["Student_ID", "Student_Name", "Final_Marks"]
].head(5))

# Grouping
print("\nAverage marks by department:")
print(data.groupby("Department")["Final_Marks"].mean())

print("\nAverage marks by semester:")
print(data.groupby("Semester")["Final_Marks"].mean())

# Segmentation
data["Performance_Level"] = pd.cut(
    data["Final_Marks"],
    bins=[0, 60, 75, 90, 100],
    labels=["Needs Improvement", "Average", "Good", "Excellent"]
)

print("\nPerformance groups:")
print(data["Performance_Level"].value_counts())

# Correlation
corr = data[[
    "Attendance",
    "Assignment_Marks",
    "Internal_Marks",
    "Study_Hours",
    "Final_Marks"
]].corr()

print("\nCorrelation matrix:")
print(corr)

# IQR outlier detection
q1 = data["Final_Marks"].quantile(0.25)
q3 = data["Final_Marks"].quantile(0.75)
iqr = q3 - q1
lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr

data["Final_Marks_Outlier"] = (
    (data["Final_Marks"] < lower) |
    (data["Final_Marks"] > upper)
)

print("\nOutlier limits:", lower, upper)
print("\nOutliers:")
print(data[data["Final_Marks_Outlier"]][
    ["Student_ID", "Student_Name", "Final_Marks"]
])

# Charts
data.groupby("Department")["Final_Marks"].mean().plot(
    kind="bar", title="Average Final Marks by Department"
)
plt.xlabel("Department")
plt.ylabel("Average Final Marks")
plt.tight_layout()
plt.savefig("01_department_performance.png", dpi=160)
plt.close()

plt.scatter(data["Attendance"], data["Final_Marks"])
plt.title("Attendance vs Final Marks")
plt.xlabel("Attendance (%)")
plt.ylabel("Final Marks")
plt.tight_layout()
plt.savefig("02_attendance_vs_final.png", dpi=160)
plt.close()

plt.scatter(data["Study_Hours"], data["Final_Marks"])
plt.title("Study Hours vs Final Marks")
plt.xlabel("Study Hours")
plt.ylabel("Final Marks")
plt.tight_layout()
plt.savefig("03_study_hours_vs_final.png", dpi=160)
plt.close()

plt.scatter(data["Assignment_Marks"], data["Final_Marks"])
plt.title("Assignment Marks vs Final Marks")
plt.xlabel("Assignment Marks")
plt.ylabel("Final Marks")
plt.tight_layout()
plt.savefig("04_assignment_vs_final.png", dpi=160)
plt.close()

plt.hist(data["Final_Marks"], bins=6)
plt.title("Distribution of Final Marks")
plt.xlabel("Final Marks")
plt.ylabel("Number of Students")
plt.tight_layout()
plt.savefig("05_final_marks_distribution.png", dpi=160)
plt.close()

plt.imshow(corr, interpolation="nearest")
plt.xticks(range(len(corr.columns)), corr.columns, rotation=45)
plt.yticks(range(len(corr.columns)), corr.columns)
plt.colorbar()
plt.title("Student Performance Correlation Matrix")
plt.tight_layout()
plt.savefig("06_correlation_heatmap.png", dpi=160)
plt.close()

data.to_csv("student_integrated_master.csv", index=False)
data.to_json("student_integrated_master.json", orient="records", indent=4)

print("\nSaved integrated CSV and JSON.")
