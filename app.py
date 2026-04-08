import streamlit as st
import pandas as pd
from datetime import date

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="AI Life Tracker", layout="wide")

# ---------- MODERN UI CSS ----------
st.markdown("""
<style>
html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}

.main {
    background: linear-gradient(135deg, #0f172a, #020617);
}

.card {
    background: rgba(30, 41, 59, 0.6);
    backdrop-filter: blur(12px);
    border-radius: 20px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    margin-bottom: 20px;
}

.title {
    font-size: 40px;
    font-weight: 700;
    background: linear-gradient(90deg, #38bdf8, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    color: #94a3b8;
    margin-bottom: 20px;
}

.stButton>button {
    background: linear-gradient(90deg, #6366f1, #22c55e);
    color: white;
    border-radius: 12px;
    height: 48px;
    font-weight: 600;
    border: none;
}

.metric-card {
    background: rgba(15, 23, 42, 0.7);
    padding: 15px;
    border-radius: 15px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.08);
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
st.markdown("<div class='title'>AI Life Tracker</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Build discipline. Track progress. Upgrade your life.</div>", unsafe_allow_html=True)

# ---------- INPUT ----------
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
    st.success("Saved successfully")

st.markdown("</div>", unsafe_allow_html=True)

# ---------- DASHBOARD ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("Performance Overview")

if not df.empty:
    col1, col2, col3 = st.columns(3)

    col1.markdown(f"""
    <div class='metric-card'>
        <h3>₹{int(df['spending'].sum())}</h3>
        <p>Total Spending</p>
    </div>
    """, unsafe_allow_html=True)

    col2.markdown(f"""
    <div class='metric-card'>
        <h3>{float(df['study_hours'].sum())}</h3>
        <p>Study Hours</p>
    </div>
    """, unsafe_allow_html=True)

    col3.markdown(f"""
    <div class='metric-card'>
        <h3>{len(df)}</h3>
        <p>Days Tracked</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Study Trend")
    st.line_chart(df["study_hours"])

    st.markdown("### Spending Trend")
    st.bar_chart(df["spending"])

st.markdown("</div>", unsafe_allow_html=True)

# ---------- AI STYLE FEEDBACK (FREE) ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("AI Coach")


def get_ai_feedback(df):
    if df.empty:
        return "Start tracking first."

    recent = df.tail(5)

    gym_missed = (recent["gym"] == "No").sum()
    avg_study = recent["study_hours"].mean()
    junk_days = (recent["junk_food"] == "Yes").sum()

    message = ""

    if gym_missed >= 3:
        message += "You are losing discipline in gym. "
    else:
        message += "Gym consistency is improving. "

    if avg_study < 2:
        message += "Your focus is weak. "
    else:
        message += "You are building focus. "

    if junk_days >= 3:
        message += "Your diet is hurting performance. "

    message += "\n\nTomorrow: Train hard, stay focused, spend less, and stay disciplined."

    return message

if st.button("Get Feedback"):
    st.write(get_ai_feedback(df))

st.markdown("</div>", unsafe_allow_html=True)

# ---------- FOOTER ----------
st.markdown("---")
st.caption("Designed for discipline and growth")
