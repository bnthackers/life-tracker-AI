import streamlit as st
import pandas as pd
from datetime import date

# ---------- CONFIG ----------
st.set_page_config(page_title="AI Life Tracker", layout="wide")

DAILY_BUDGET = 200

# ---------- STYLE ----------
st.markdown("""
<style>
.main {background-color:#0f172a;color:white;}
.card {background:#1e293b;padding:18px;border-radius:12px;margin-bottom:16px;}
.section-title {font-size:20px;font-weight:600;margin-bottom:10px}
.bad {color:#ef4444;font-weight:600}
.good {color:#22c55e;font-weight:600}
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
<div style='padding:10px 0 20px 0;'>
    <h1 style='margin-bottom:5px;'>AI Life Tracker</h1>
    <p style='color:#94a3b8;'>Track habits. Stay disciplined. Improve daily.</p>
</div>
""", unsafe_allow_html=True)


# ---------- INPUT ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Daily Check-in</div>", unsafe_allow_html=True)

c1,c2,c3,c4 = st.columns(4)
with c1:
    gym = st.radio("Gym", ["Yes","No"], horizontal=True)
with c2:
    junk = st.radio("Junk Food", ["Yes","No"], horizontal=True)
with c3:
    study = st.number_input("Study (hrs)", min_value=0.0, step=0.5)
with c4:
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

# ---------- TODAY SUMMARY ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Today Summary</div>", unsafe_allow_html=True)

if not df.empty:
    today = df.iloc[-1]

    t1,t2,t3,t4 = st.columns(4)

    t1.metric("Gym", today["gym"])
    t2.metric("Junk", today["junk_food"])
    t3.metric("Study", f"{today['study_hours']} hrs")

    # Spending with budget logic
    spend_val = today['spending']
    if spend_val > DAILY_BUDGET:
        t4.markdown(f"**Spend: ₹{spend_val}**<br><span class='bad'>Over budget</span>", unsafe_allow_html=True)
    else:
        t4.markdown(f"**Spend: ₹{spend_val}**<br><span class='good'>Within budget</span>", unsafe_allow_html=True)

    # Budget progress bar
    progress = min(spend_val / DAILY_BUDGET, 1.0)
    st.progress(progress)
    st.caption(f"Budget used: ₹{spend_val} / ₹{DAILY_BUDGET}")

else:
    st.write("No data yet")

st.markdown("</div>", unsafe_allow_html=True)

# ---------- PROGRESS ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Progress Overview</div>", unsafe_allow_html=True)

if not df.empty:
    col1,col2 = st.columns(2)

    with col1:
        st.write("Study Trend")
        st.line_chart(df.set_index("date")["study_hours"])

        st.write("Gym Consistency")
        st.bar_chart(df["gym"].value_counts())

    with col2:
        st.write("Spending Trend")
        st.bar_chart(df.set_index("date")["spending"])

        st.write("Junk Food Pattern")
        st.bar_chart(df["junk_food"].value_counts())

st.markdown("</div>", unsafe_allow_html=True)

# ---------- HISTORY ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Last 7 Days</div>", unsafe_allow_html=True)

if not df.empty:
    st.dataframe(df.tail(7), use_container_width=True)

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
    spend_total = recent["spending"].sum()

    msg = ""

    if gym_missed >= 3:
        msg += "You are skipping gym too often. "
    else:
        msg += "Gym consistency is okay. "

    if avg_study < 2:
        msg += "Study is weak. "
    else:
        msg += "Study is improving. "

    if junk_days >= 3:
        msg += "Too much junk food. "

    if spend_total > DAILY_BUDGET * 5:
        msg += "You are overspending consistently. "

    msg += "\n\nTomorrow: Gym + 2hr study + no junk + spend under ₹200."

    return msg

if not df.empty:
    st.info(get_ai_feedback(df))

st.markdown("</div>", unsafe_allow_html=True)

# ---------- FOOTER ----------
st.caption("Stay consistent. Improve daily.")
