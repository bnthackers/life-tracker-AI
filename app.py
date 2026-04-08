import streamlit as st
import pandas as pd
from datetime import date
import os
from openai import OpenAI

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="AI Life Tracker", layout="wide")

# ---------- CUSTOM CSS ----------
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        color: white;
    }
    .card {
        background: #1e293b;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        margin-bottom: 15px;
    }
    .stButton>button {
        border-radius: 10px;
        height: 45px;
        width: 100%;
        font-weight: bold;
        background: linear-gradient(90deg, #3b82f6, #06b6d4);
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- LOAD DATA ----------
FILE = "data.csv"

def load_data():
    try:
        return pd.read_csv(FILE)
    except:
        return pd.DataFrame(columns=["date", "gym", "study_hours", "junk_food", "spending"])

def save_data(df):
    df.to_csv(FILE, index=False)

# ---------- HEADER ----------
st.title("AI Life Tracker Dashboard")
st.caption("Track. Improve. Dominate your habits.")

df = load_data()

# ---------- INPUT SECTION ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("Daily Check-in")

col1, col2 = st.columns(2)

with col1:
    gym = st.selectbox("Gym", ["Yes", "No"])
    junk = st.selectbox("Junk Food", ["Yes", "No"])

with col2:
    study = st.number_input("Study Hours", min_value=0.0, step=0.5)
    spend = st.number_input("Money Spent (₹)", min_value=0)

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

st.markdown("</div>", unsafe_allow_html=True)

# ---------- DASHBOARD ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("Stats Overview")

if not df.empty:
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Spending", f"₹{int(df['spending'].sum())}")
    col2.metric("Study Hours", f"{float(df['study_hours'].sum())}")
    col3.metric("Entries", len(df))

    st.line_chart(df["study_hours"])
    st.bar_chart(df["spending"])

st.markdown("</div>", unsafe_allow_html=True)

# ---------- AI COACH ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("AI Coach")

client = None
if os.getenv("OPENAI_API_KEY"):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_ai_feedback(df):
    if df.empty:
        return "Start tracking first."

    recent = df.tail(5).to_dict(orient="records")

    prompt = f"""
    You are a strict, high-performance life coach.

    Data: {recent}

    Give short, sharp feedback and one action for tomorrow.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

if st.button("Get AI Feedback"):
    if client:
        st.write(get_ai_feedback(df))
    else:
        st.warning("Add API key to enable AI")

st.markdown("</div>", unsafe_allow_html=True)

# ---------- FOOTER ----------
st.caption("Built with Streamlit + AI")
