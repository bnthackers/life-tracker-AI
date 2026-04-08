import streamlit as st
import pandas as pd
from datetime import date

# ---------- CONFIG ----------
st.set_page_config(page_title="AI Life Tracker", layout="wide")

DAILY_BUDGET = 200

# ---------- MOBILE FRIENDLY CSS ----------
st.markdown("""
<style>
.main {background-color:#0f172a;color:white;}
.card {background:#1e293b;padding:16px;border-radius:12px;margin-bottom:16px;}
.section-title {font-size:18px;font-weight:600;margin-bottom:8px}

/* Make everything stack nicely on small screens */
@media (max-width: 768px) {
    .block-container {padding-left: 1rem; padding-right: 1rem;}
}

/* Buttons full width on mobile */
.stButton>button {
    width: 100%;
    border-radius: 8px;
    height: 44px;
    background-color: #22c55e;
    color: white;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ---------- DATA ----------
FILE = "data.csv"

def load_data():
    try:
        return pd.read_csv(FILE)
    except:
        return pd.DataFrame(columns=["date","gym","study_hours","junk_food","spending"])

def save_data(df):
    df.to_csv(FILE, index=False)

# ---------- LOAD ----------
df = load_data()

# ---------- SIDEBAR ----------
if st.sidebar.button("Reset All Data"):
    df = pd.DataFrame(columns=["date","gym","study_hours","junk_food","spending"])
    df.to_csv(FILE, index=False)
    st.sidebar.success("Data reset!")

# ---------- HEADER ----------
st.markdown("""
<div style='padding:10px 0 15px 0;'>
    <h2>AI Life Tracker</h2>
    <p style='color:#94a3b8;'>Track habits. Improve daily.</p>
</div>
""", unsafe_allow_html=True)

# ---------- INPUT ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Daily Check-in</div>", unsafe_allow_html=True)

# Stack-friendly layout
col1, col2 = st.columns(2)

with col1:
    gym = st.radio("Gym", ["Yes","No"], horizontal=True)
    junk = st.radio("Junk Food", ["Yes","No"], horizontal=True)

with col2:
    study = st.number_input("Study (hrs)", min_value=0.0, step=0.5)
    spend = st.number_input("Spend (₹)", min_value=0)

if st.button("Save Today"):
    new = pd.DataFrame({
        "date":[date.today()],
        "gym":[gym],
        "study_hours":[study],
        "junk_food":[junk],
        "spending":[spend]
    })
    df = pd.concat([df,new], ignore_index=True)
    save_data(df)
    st.success("Saved")

st.markdown("</div>", unsafe_allow_html=True)

# ---------- TODAY ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Today Summary</div>", unsafe_allow_html=True)

if not df.empty:
    today = df.iloc[-1]

    t1, t2 = st.columns(2)
    t3, t4 = st.columns(2)

    t1.metric("Gym", today["gym"])
    t2.metric("Junk", today["junk_food"])
    t3.metric("Study", f"{today['study_hours']} hrs")

    spend_val = today['spending']
    if spend_val > DAILY_BUDGET:
        t4.markdown(f"**₹{spend_val}** 🔴 Over")
    else:
        t4.markdown(f"**₹{spend_val}** 🟢 OK")

st.markdown("</div>", unsafe_allow_html=True)

# ---------- PROGRESS ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Progress</div>", unsafe_allow_html=True)

if not df.empty:
    st.write("Study")
    st.line_chart(df.set_index("date")["study_hours"], use_container_width=True)

    st.write("Spending")
    st.bar_chart(df.set_index("date")["spending"], use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------- AI FEEDBACK ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>AI Coach</div>", unsafe_allow_html=True)


def get_ai_feedback(df):
    if df.empty:
        return "Start tracking first"

    recent = df.tail(5)

    gym_missed = (recent["gym"] == "No").sum()
    avg_study = recent["study_hours"].mean()
    junk_days = (recent["junk_food"] == "Yes").sum()

    msg = ""

    if gym_missed >= 3:
        msg += "Skip gym too much. "
    else:
        msg += "Gym okay. "

    if avg_study < 2:
        msg += "Study low. "
    else:
        msg += "Study good. "

    if junk_days >= 3:
        msg += "Too much junk. "

    msg += "\n\nTomorrow: Gym + Study + No junk + Spend < 200"

    return msg

if not df.empty:
    st.info(get_ai_feedback(df))

st.markdown("</div>", unsafe_allow_html=True)

# ---------- FOOTER ----------
st.caption("Consistency > Motivation")
