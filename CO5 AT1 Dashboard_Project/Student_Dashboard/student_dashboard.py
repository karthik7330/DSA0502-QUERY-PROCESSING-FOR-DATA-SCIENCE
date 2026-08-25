import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix

st.set_page_config(page_title="Student Academic Performance Dashboard", layout="wide")
st.title("Student Academic Performance Dashboard")

df = pd.read_csv("student_performance.csv")

st.sidebar.header("Filters")
min_att = st.sidebar.slider("Minimum Attendance", 0, 100, 0)
filtered = df[df["Attendance"] >= min_att]

st.subheader("Dataset")
st.dataframe(filtered, use_container_width=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Students", len(filtered))
c2.metric("Average Attendance", round(filtered["Attendance"].mean(), 2))
c3.metric("Average Final Score", round(filtered["Final_Score"].mean(), 2))
c4.metric("Highest Final Score", filtered["Final_Score"].max())

col1, col2 = st.columns(2)

with col1:
    st.subheader("Final Score by Student")
    fig, ax = plt.subplots()
    ax.bar(filtered["Student_ID"], filtered["Final_Score"])
    ax.set_xlabel("Student")
    ax.set_ylabel("Final Score")
    ax.tick_params(axis="x", rotation=90)
    st.pyplot(fig)

with col2:
    st.subheader("Final Score Distribution")
    fig, ax = plt.subplots()
    ax.hist(filtered["Final_Score"], bins=8, edgecolor="black")
    ax.set_xlabel("Final Score")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

col3, col4 = st.columns(2)

with col3:
    st.subheader("Attendance vs Final Score")
    fig, ax = plt.subplots()
    ax.scatter(filtered["Attendance"], filtered["Final_Score"])
    ax.set_xlabel("Attendance")
    ax.set_ylabel("Final Score")
    st.pyplot(fig)

with col4:
    st.subheader("Final Score Frequency")
    freq = filtered["Final_Score"].value_counts().sort_index()
    fig, ax = plt.subplots()
    ax.bar(freq.index.astype(str), freq.values)
    ax.set_xlabel("Final Score")
    ax.set_ylabel("Frequency")
    ax.tick_params(axis="x", rotation=90)
    st.pyplot(fig)

st.subheader("Scatter Matrix")

numeric = filtered[[
    "Attendance",
    "Internal_Marks",
    "Assignment_Marks",
    "Laboratory_Marks",
    "Final_Score"
]]

fig, axes = plt.subplots(5, 5, figsize=(15, 15))

for i in range(5):
    for j in range(5):
        if i == j:
            axes[i, j].hist(numeric.iloc[:, i], bins=8, edgecolor="black")
        else:
            axes[i, j].scatter(
                numeric.iloc[:, j],
                numeric.iloc[:, i]
            )

        axes[i, j].set_xlabel(numeric.columns[j])
        axes[i, j].set_ylabel(numeric.columns[i])

plt.tight_layout()
st.pyplot(fig)
plt.close(fig)
st.subheader("Performance Summary")
avg = filtered["Final_Score"].mean()
if avg >= 75:
    st.success("Overall performance is good.")
elif avg >= 50:
    st.warning("Overall performance is moderate.")
else:
    st.error("Overall performance needs improvement.")

st.subheader("Potential Low-Performance Students")
low = filtered[filtered["Final_Score"] < 60]
st.dataframe(low, use_container_width=True)
