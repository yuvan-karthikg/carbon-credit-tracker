import streamlit as st
import pandas as pd
import os

data_file = "carbon_credits.csv"
if not os.path.exists(data_file):
    df = pd.DataFrame(columns=["Date", "Activity", "Credits", "Type"])
    df.to_csv(data_file, index=False)

st.title("🌱 Carbon Credit Tracker")

st.sidebar.header("Log a New Carbon Credit Transaction")
date = st.sidebar.date_input("Date")
activity = st.sidebar.text_input("Activity (e.g., EV usage, Renewable Energy, Reforestation)")
credits = st.sidebar.number_input("Credits (kg CO₂ offset)", min_value=0.0, format="%.2f")
t_type = st.sidebar.radio("Type", ["Earned", "Spent"])

if st.sidebar.button("Log Transaction"):
    new_data = pd.DataFrame([[date, activity, credits, t_type]], columns=["Date", "Activity", "Credits", "Type"])
    df = pd.read_csv(data_file)
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(data_file, index=False)
    st.sidebar.success("Transaction Logged!")


df = pd.read_csv(data_file)
st.write("### Transaction History")
st.dataframe(df)


st.write("### Carbon Credits Overview")
earned_credits = df[df["Type"] == "Earned"]["Credits"].sum()
spent_credits = df[df["Type"] == "Spent"]["Credits"].sum()

st.metric("Total Earned Credits", f"{earned_credits} kg CO₂")
st.metric("Total Spent Credits", f"{spent_credits} kg CO₂")

st.write("### Breakdown by Activity")
activity_data = df.groupby("Activity")["Credits"].sum()
st.bar_chart(activity_data)
