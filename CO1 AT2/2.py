import pandas as pd

df = pd.read_csv("students.csv")

avg = df["Marks"].mean()
print("Average Marks:", avg)

print("\nStudents Below 40:")
print(df[df["Marks"] < 40])

df["Result"] = df["Marks"].apply(lambda x: "Pass" if x >= 40 else "Fail")

df.to_csv("updated_students.csv", index=False)

print("\nUpdated Data:")
print(df)