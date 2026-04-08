import streamlit as st
import pandas as pd
from datetime import date

# ---------- CONFIG ----------
st.set_page_config(page_title="AI Life Tracker", layout="wide")

# ---------- CLEAN MODERN UI ----------
st.markdown("""
<style>
.main {
    background-color: #0f172a;
    color: white;
}
.card {
    background: #1e293b;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 20px;
}
h1, h2, h3 {
    color: #f8fafc;
}
.stButton>button {
    background-color: #22c55e;
    color: white;
    border-radius: 8px;
    height: 45px;
    font-weight: 600;
}
.metric {
    font-size: 20px;
    font-weight: bold;
}
.label {
    color: #94a3b8;
}
</style>
""", unsafe_allow_html=True)

# ---------- DATA ----------
FILE = "data.csv"

def load_data():
    try:
        return pd.read_csv(FILE)
    except:
        return pd.DataFrame(columns=["date", "gym", "study_hours", "junk_food", "spending"])

def save_data(df):
    df.to_csv(FILE, index=False)

df = load_data()

# ---------- HEADER ----------
st.title("AI Life Tracker")
st.write("Simple daily tracking with clear insights")

# ---------- INPUT ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("Daily Check-in")

col1, col2, col3, col4 = st.columns(4)

with col1:
    gym = st.radio("Gym", ["Yes", "No"], horizontal=True)

with col2:
    junk = st.radio("Junk Food", ["Yes", "No"], horizontal=True)

with col3:
    study = st.number_input("Study (hrs)", min_value=0.0, step=0.5)

with col4:
    spend = st.number_input("Spend (₹)", min_value=0)

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
    st.success("Saved")

st.markdown("</div>", unsafe_allow_html=True)

# ---------- SUMMARY ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("Today Summary")

if not df.empty:
    today = df.iloc[-1]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Gym", today["gym"])
    col2.metric("Junk Food", today["junk_food"])
    col3.metric("Study", f"{today['study_hours']} hrs")
    col4.metric("Spend", f"₹{today['spending']}")

st.markdown("</div>", unsafe_allow_html=True)

# ---------- HISTORY ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("Last 7 Days")

if not df.empty:
    st.dataframe(df.tail(7), use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------- CHARTS ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("Progress")

if not df.empty:
    st.write("Study Trend")
    st.line_chart(df["study_hours"])

    st.write("Spending Trend")
    st.bar_chart(df["spending"])

st.markdown("</div>", unsafe_allow_html=True)

# ---------- AI STYLE FEEDBACK ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("AI Coach")


def get_ai_feedback(df):
    if df.empty:
        return "Start tracking first"

    recent = df.tail(5)

    gym_missed = (recent["gym"] == "No").sum()
    avg_study = recent["study_hours"].mean()
    junk_days = (recent["junk_food"] == "Yes").sum()

    msg = ""

    if gym_missed >= 3:
        msg += "Gym consistency is poor. "
    else:
        msg += "Gym consistency is okay. "

    if avg_study < 2:
        msg += "Study hours are low. "
    else:
        msg += "Study is improving. "

    if junk_days >= 3:
        msg += "Too much junk food. "

    msg += "\n\nTomorrow: Go to gym, study more, eat clean, spend wisely."

    return msg

if st.button("Get Feedback"):
    st.write(get_ai_feedback(df))

st.markdown("</div>", unsafe_allow_html=True)

# ---------- FOOTER ----------
st.caption("Keep improving daily")
