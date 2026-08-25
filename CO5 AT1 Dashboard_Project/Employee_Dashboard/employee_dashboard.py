import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix

st.set_page_config(page_title="Employee Productivity Analysis Dashboard", layout="wide")
st.title("Employee Productivity Analysis Dashboard")

df = pd.read_csv("employee_productivity.csv")

st.sidebar.header("Filters")
min_rating = st.sidebar.slider("Minimum Performance Rating", 1, 5, 1)
filtered = df[df["Performance_Rating"] >= min_rating]

st.subheader("Dataset")
st.dataframe(filtered, use_container_width=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Employees", len(filtered))
c2.metric("Average Working Hours", round(filtered["Working_Hours"].mean(), 2))
c3.metric("Average Productivity", round(filtered["Productivity_Score"].mean(), 2))
c4.metric("Average Rating", round(filtered["Performance_Rating"].mean(), 2))

col1, col2 = st.columns(2)

with col1:
    st.subheader("Productivity Distribution")
    fig, ax = plt.subplots()
    ax.hist(filtered["Productivity_Score"], bins=8, edgecolor="black")
    ax.set_xlabel("Productivity Score")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

with col2:
    st.subheader("Performance Rating Frequency")
    freq = filtered["Performance_Rating"].value_counts().sort_index()
    fig, ax = plt.subplots()
    ax.bar(freq.index.astype(str), freq.values)
    ax.set_xlabel("Performance Rating")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

col3, col4 = st.columns(2)

with col3:
    st.subheader("Working Hours vs Productivity")
    fig, ax = plt.subplots()
    ax.scatter(filtered["Working_Hours"], filtered["Productivity_Score"])
    ax.set_xlabel("Working Hours")
    ax.set_ylabel("Productivity Score")
    st.pyplot(fig)

with col4:
    st.subheader("Experience vs Salary")
    fig, ax = plt.subplots()
    ax.scatter(filtered["Experience_Years"], filtered["Salary"])
    ax.set_xlabel("Experience (Years)")
    ax.set_ylabel("Salary")
    st.pyplot(fig)

st.subheader("Scatter Matrix")
numeric = filtered[["Working_Hours", "Experience_Years", "Productivity_Score", "Salary", "Performance_Rating"]]
scatter_matrix(numeric, figsize=(12, 10), diagonal="hist")
st.pyplot(plt.gcf())

st.subheader("Potential Unusual Employees")
unusual = filtered[(filtered["Productivity_Score"] < 55) | (filtered["Working_Hours"] < 34)]
st.dataframe(unusual, use_container_width=True)

st.subheader("Performance Summary")
avg = filtered["Productivity_Score"].mean()
if avg >= 75:
    st.success("Overall employee productivity is good.")
elif avg >= 60:
    st.warning("Overall employee productivity is moderate.")
else:
    st.error("Overall employee productivity needs improvement.")
