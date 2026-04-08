import streamlit as st
import pandas as pd
from datetime import date

# ---------- CONFIG ----------
st.set_page_config(page_title="AI Life Tracker", layout="wide")

# ---------- STYLE ----------
st.markdown("""
<style>
.main {background-color:#0f172a;color:white;}
.card {background:#1e293b;padding:18px;border-radius:12px;margin-bottom:16px;}
.stButton>button {background:#22c55e;color:white;border-radius:8px;height:44px;font-weight:600;}
.small {color:#94a3b8;font-size:12px}
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

# ---------- HEADER ----------
st.title("AI Life Tracker")
st.caption("Simple. Clear. Daily discipline.")

# ---------- INPUT ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("Daily Check-in")

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

# ---------- TODAY ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("Today Summary")

if not df.empty:
    today = df.iloc[-1]
    t1,t2,t3,t4 = st.columns(4)
    t1.metric("Gym", today["gym"])
    t2.metric("Junk", today["junk_food"])
    t3.metric("Study", f"{today['study_hours']} hrs")
    t4.metric("Spend", f"₹{today['spending']}")
else:
    st.write("No data yet")

st.markdown("</div>", unsafe_allow_html=True)

# ---------- PROGRESS (FIXED) ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("Progress Overview")

if not df.empty:
    p1,p2 = st.columns(2)

    with p1:
        st.write("Study Trend")
        st.line_chart(df.set_index("date")["study_hours"])

        st.write("Gym Consistency")
        gym_counts = df["gym"].value_counts()
        st.bar_chart(gym_counts)

    with p2:
        st.write("Spending Trend")
        st.bar_chart(df.set_index("date")["spending"])

        st.write("Junk Food Pattern")
        junk_counts = df["junk_food"].value_counts()
        st.bar_chart(junk_counts)

st.markdown("</div>", unsafe_allow_html=True)

# ---------- HISTORY ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("Last 7 Days")

if not df.empty:
    st.dataframe(df.tail(7), use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------- AI FEEDBACK (AUTO FIXED) ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("AI Coach")


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
        msg += "Gym discipline is okay. "

    if avg_study < 2:
        msg += "Study is weak. "
    else:
        msg += "Study is improving. "

    if junk_days >= 3:
        msg += "Too much junk food. "

    if spend_total > 2000:
        msg += "Spending is high. "

    msg += "\n\nTomorrow: Gym + 2hr study + no junk + controlled spending."

    return msg

# AUTO SHOW (no need button)
if not df.empty:
    st.info(get_ai_feedback(df))

st.markdown("</div>", unsafe_allow_html=True)

# ---------- FOOTER ----------
st.caption("Consistency beats motivation")
