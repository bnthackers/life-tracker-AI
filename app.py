import streamlit as st
import pandas as pd
from datetime import date
import os
from openai import OpenAI

# ---------- CONFIG ----------
st.set_page_config(page_title="AI Life Tracker", layout="centered")

st.title("AI Life Tracker")

# ---------- LOAD DATA ----------
FILE = "data.csv"

def load_data():
    try:
        return pd.read_csv(FILE)
    except:
        return pd.DataFrame(columns=["date", "gym", "study_hours", "junk_food", "spending"])

def save_data(df):
    df.to_csv(FILE, index=False)

df = load_data()

# ---------- INPUT SECTION ----------
st.subheader("Daily Check-in")

gym = st.selectbox("Did you go to gym?", ["Yes", "No"])
study = st.number_input("Study hours", min_value=0.0, step=0.5)
junk = st.selectbox("Did you eat junk food?", ["Yes", "No"])
spend = st.number_input("Money spent today (₹)", min_value=0)

if st.button("Save Today"):
    new_data = pd.DataFrame({
        "date": [date.today()],
        "gym": [gym],
        "study_hours": [study],
        "junk_food": [junk],
        "spending": [spend]
    })

    df = pd.concat([df, new_data], ignore_index=True)
    save_data(df)
    st.success("Saved successfully!")

# ---------- DASHBOARD ----------
st.subheader("Dashboard")

if not df.empty:
    st.write("Total Spending:", int(df["spending"].sum()))
    st.write("Total Study Hours:", float(df["study_hours"].sum()))

    st.dataframe(df.tail(7))

# ---------- AI COACH ----------
st.subheader("AI Coach")

client = None
if os.getenv("OPENAI_API_KEY"):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_ai_feedback(df):
    if df.empty:
        return "No data yet. Start tracking first."

    recent = df.tail(5).to_dict(orient="records")

    prompt = f"""
    Act like a strict but helpful personal coach.

    User data (last 5 days):
    {recent}

    Give:
    - Short feedback
    - What is going wrong
    - Clear action for tomorrow

    Keep it under 100 words.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {e}"

if st.button("Get AI Feedback"):
    if client:
        feedback = get_ai_feedback(df)
        st.write(feedback)
    else:
        st.warning("Add your OpenAI API key to enable AI feedback.")
