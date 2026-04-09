import streamlit as st
import pandas as pd
from datetime import date, timedelta
from groq import Groq
import os

# ---------- CONFIG ----------
st.set_page_config(
    page_title="AI Life Tracker",
    layout="wide",
    initial_sidebar_state="expanded"
)

DAILY_BUDGET = 200

# ---------- ENHANCED CSS ----------
st.markdown("""
<style>
    /* Main background and text */
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1a1f35 100%);
        color: #e2e8f0;
    }
    
    /* Cards styling */
    .card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 24px;
        border-radius: 16px;
        margin-bottom: 20px;
        border: 1px solid #334155;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    /* Section titles */
    .section-title {
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 16px;
        background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    }
    
    /* Success/Status indicators */
    .success-box {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 16px;
        border-radius: 12px;
        margin: 8px 0;
        font-weight: 600;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        padding: 16px;
        border-radius: 12px;
        margin: 8px 0;
        font-weight: 600;
    }
    
    .info-box {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        padding: 16px;
        border-radius: 12px;
        margin: 8px 0;
        font-weight: 600;
    }
    
    /* Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 50px;
        font-weight: 600;
        font-size: 16px;
        border: none;
        transition: all 0.3s ease;
        background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
        color: white;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(96, 165, 250, 0.4);
    }
    
    /* Input styling */
    .stNumberInput input, .stRadio {
        border-radius: 8px !important;
    }
    
    /* Sidebar */
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    }
    
    /* Charts */
    .stPlotlyChart {
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* AI Coach section */
    .ai-coach {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 24px;
        border-radius: 16px;
        color: white;
        font-size: 16px;
        line-height: 1.6;
        box-shadow: 0 8px 32px rgba(245, 87, 108, 0.3);
        border-left: 6px solid #f5576c;
    }
    
    /* Mobile friendly */
    @media (max-width: 768px) {
        .card {
            padding: 16px;
            margin-bottom: 16px;
        }
        
        .section-title {
            font-size: 18px;
        }
        
        .stButton > button {
            height: 44px;
            font-size: 14px;
        }
    }
    
    /* Metric display */
    .metric-display {
        text-align: center;
        padding: 16px;
        background: #334155;
        border-radius: 12px;
        margin: 8px 0;
    }
    
    .metric-label {
        font-size: 12px;
        text-transform: uppercase;
        color: #94a3b8;
        font-weight: 600;
        letter-spacing: 1px;
    }
    
    .metric-value {
        font-size: 32px;
        font-weight: 700;
        color: #f1f5f9;
        margin-top: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ---------- DATA MANAGEMENT ----------
FILE = "data.csv"

def load_data():
    try:
        df = pd.read_csv(FILE)
        df['date'] = pd.to_datetime(df['date'])
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=["date","gym","study_hours","junk_food","spending"])

def save_data(df):
    df.to_csv(FILE, index=False)

# ---------- GROQ AI SETUP (FREE!) ----------
@st.cache_resource
def get_groq_client():
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        st.warning("⚠️ GROQ_API_KEY not set. Get it FREE at: https://console.groq.com/keys")
        return None
    return Groq(api_key=api_key)

def get_ai_feedback(df):
    """Get personalized AI feedback from Groq (FREE!)"""
    if df.empty:
        return "Start tracking first! 📊 Every entry helps the AI understand your patterns."
    
    client = get_groq_client()
    if not client:
        return get_fallback_feedback(df)
    
    try:
        recent = df.tail(7)
        
        gym_days = (recent["gym"] == "Yes").sum()
        avg_study = recent["study_hours"].mean()
        junk_days = (recent["junk_food"] == "Yes").sum()
        avg_spending = recent["spending"].mean()
        
        total_days = len(recent)
        gym_percentage = (gym_days / total_days * 100) if total_days > 0 else 0
        
        prompt = f"""You are an encouraging life coach analyzing someone's weekly progress. 
        
Here's their data from the past 7 days:
- Gym: {gym_days} days out of {total_days} ({gym_percentage:.0f}%)
- Average study hours: {avg_study:.1f} hours/day
- Junk food days: {junk_days} out of {total_days}
- Average daily spending: ₹{avg_spending:.0f} (Budget: ₹200)

Provide personalized, motivating feedback in 2-3 sentences. Be genuinely encouraging but honest about areas to improve. End with one specific, actionable tip for tomorrow. Keep it concise and energetic!"""
        
        message = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )
        
        return message.choices[0].message.content
    
    except Exception as e:
        st.warning(f"⚠️ AI Coach error: {str(e)}")
        return get_fallback_feedback(df)

def get_fallback_feedback(df):
    """Fallback feedback when API is not available"""
    if df.empty:
        return "📊 Start tracking to get personalized feedback!"
    
    recent = df.tail(7)
    gym_days = (recent["gym"] == "Yes").sum()
    junk_days = (recent["junk_food"] == "Yes").sum()
    avg_study = recent["study_hours"].mean()
    
    feedbacks = [
        f"💪 Great start! You've done gym {gym_days} times this week. Keep the momentum going!",
        f"🎯 Nice consistency! You're averaging {avg_study:.1f} hours of study daily. That's solid progress!",
        f"🍎 You had junk food {junk_days} days this week. Try to reduce that by 1 day next week!",
        f"⚡ You're building amazing habits! Gym: {gym_days}/7, Study: {avg_study:.1f}h avg. Keep it up!"
    ]
    
    import random
    return random.choice(feedbacks)

# ---------- LOAD DATA ----------
df = load_data()

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("<h2 style='color: #60a5fa;'>⚙️ Settings</h2>", unsafe_allow_html=True)
    
    if st.button("🔄 Reset All Data", use_container_width=True):
        if st.session_state.get('confirm_reset'):
            df = pd.DataFrame(columns=["date","gym","study_hours","junk_food","spending"])
            save_data(df)
            st.success("✅ All data has been reset!")
            st.session_state.confirm_reset = False
        else:
            st.session_state.confirm_reset = True
            st.warning("Click Reset again to confirm deletion of all data")
    
    st.divider()
    
    st.markdown("### 📊 Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Days", len(df))
    with col2:
        st.metric("Total Spent", f"₹{df['spending'].sum():.0f}")
    
    st.divider()
    st.caption("💡 Tip: Consistency beats motivation. Small wins compound into big results!")

# ---------- HEADER ----------
st.markdown("""
<div style='text-align: center; padding: 20px 0;'>
    <h1 style='background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-size: 48px; margin-bottom: 8px;'>
        🎯 AI Life Tracker
    </h1>
    <p style='color: #94a3b8; font-size: 18px;'>Track habits. Get AI insights. Transform your life.</p>
</div>
""", unsafe_allow_html=True)

# ---------- INPUT SECTION ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h2 class='section-title'>📝 Daily Check-in</h2>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    gym = st.radio("💪 Gym", ["Yes","No"], horizontal=False, key="gym_radio")

with col2:
    study = st.number_input("📚 Study (hrs)", min_value=0.0, step=0.5, key="study_input")

with col3:
    junk = st.radio("🍕 Junk Food", ["Yes","No"], horizontal=False, key="junk_radio")

with col4:
    spend = st.number_input("💰 Spending (₹)", min_value=0, key="spend_input")

st.divider()

if st.button("💾 Save Today's Entry", use_container_width=True, key="save_btn"):
    today = date.today()
    
    # Check if today's entry already exists
    existing = df[df['date'].dt.date == today] if not df.empty else pd.DataFrame()
    
    if not existing.empty:
        # Update existing entry
        df.loc[df['date'].dt.date == today, ['gym', 'study_hours', 'junk_food', 'spending']] = [gym, study, junk, spend]
    else:
        # Add new entry
        new_entry = pd.DataFrame({
            "date": [today],
            "gym": [gym],
            "study_hours": [study],
            "junk_food": [junk],
            "spending": [spend]
        })
        df = pd.concat([df, new_entry], ignore_index=True)
    
    save_data(df)
    st.success("✅ Today's data saved successfully!")
    st.balloons()

st.markdown("</div>", unsafe_allow_html=True)

# ---------- TODAY SUMMARY ----------
if not df.empty:
    today_data = df[df['date'].dt.date == date.today()]
    
    if not today_data.empty:
        today = today_data.iloc[0]
        
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h2 class='section-title'>📊 Today's Summary</h2>", unsafe_allow_html=True)
        
        tcol1, tcol2, tcol3, tcol4 = st.columns(4)
        
        with tcol1:
            st.markdown(f"""
            <div class='metric-display'>
                <div class='metric-label'>Gym</div>
                <div class='metric-value'>{'✅' if today['gym'] == 'Yes' else '❌'}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with tcol2:
            st.markdown(f"""
            <div class='metric-display'>
                <div class='metric-label'>Study</div>
                <div class='metric-value'>{today['study_hours']:.1f}h</div>
            </div>
            """, unsafe_allow_html=True)
        
        with tcol3:
            st.markdown(f"""
            <div class='metric-display'>
                <div class='metric-label'>Junk Food</div>
                <div class='metric-value'>{'❌' if today['junk_food'] == 'Yes' else '✅'}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with tcol4:
            spend_status = "🔴 Over" if today['spending'] > DAILY_BUDGET else "🟢 Good"
            st.markdown(f"""
            <div class='metric-display'>
                <div class='metric-label'>Spending</div>
                <div class='metric-value'>₹{today['spending']}</div>
                <div style='color: #94a3b8; font-size: 12px; margin-top: 8px;'>{spend_status}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# ---------- LAST 7 DAYS STATS ----------
if len(df) > 0:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='section-title'>📈 Last 7 Days Stats</h2>", unsafe_allow_html=True)
    
    recent = df.tail(7)
    
    gym_days = (recent["gym"] == "Yes").sum()
    avg_study = recent["study_hours"].mean()
    junk_days = (recent["junk_food"] == "Yes").sum()
    avg_spending = recent["spending"].mean()
    total_spending = recent["spending"].sum()
    
    mcol1, mcol2, mcol3, mcol4 = st.columns(4)
    
    with mcol1:
        st.markdown(f"""
        <div class='metric-card'>
            <div style='font-size: 14px; opacity: 0.9;'>GYM DAYS</div>
            <div style='font-size: 36px; font-weight: 700; margin-top: 8px;'>{gym_days}/7</div>
        </div>
        """, unsafe_allow_html=True)
    
    with mcol2:
        st.markdown(f"""
        <div class='metric-card' style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);'>
            <div style='font-size: 14px; opacity: 0.9;'>AVG STUDY</div>
            <div style='font-size: 36px; font-weight: 700; margin-top: 8px;'>{avg_study:.1f}h</div>
        </div>
        """, unsafe_allow_html=True)
    
    with mcol3:
        st.markdown(f"""
        <div class='metric-card' style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);'>
            <div style='font-size: 14px; opacity: 0.9;'>JUNK DAYS</div>
            <div style='font-size: 36px; font-weight: 700; margin-top: 8px;'>{junk_days}/7</div>
        </div>
        """, unsafe_allow_html=True)
    
    with mcol4:
        st.markdown(f"""
        <div class='metric-card' style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: #1a202c;'>
            <div style='font-size: 14px; opacity: 0.85;'>AVG SPEND</div>
            <div style='font-size: 36px; font-weight: 700; margin-top: 8px;'>₹{avg_spending:.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ---------- CHARTS ----------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='section-title'>📊 Progress Charts</h2>", unsafe_allow_html=True)
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.subheader("Study Hours Trend")
        study_chart_data = recent[['date', 'study_hours']].set_index('date')
        st.line_chart(study_chart_data, use_container_width=True)
    
    with chart_col2:
        st.subheader("Daily Spending")
        spending_chart_data = recent[['date', 'spending']].set_index('date')
        st.bar_chart(spending_chart_data, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- AI COACH SECTION ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h2 class='section-title'>🤖 Your AI Coach</h2>", unsafe_allow_html=True)

with st.spinner("🤔 Coach is analyzing your progress..."):
    feedback = get_ai_feedback(df)

st.markdown(f"""
<div class='ai-coach'>
    {feedback}
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------- DETAILED ANALYTICS ----------
if len(df) > 1:
    with st.expander("📋 Detailed Analytics & History"):
        st.markdown("### All Data")
        
        # Display dataframe with styling
        display_df = df.copy()
        display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d')
        
        st.dataframe(
            display_df.style.format({
                'spending': '₹{:.0f}',
                'study_hours': '{:.1f}h'
            }),
            use_container_width=True
        )
        
        # Download CSV
        csv = display_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Data as CSV",
            data=csv,
            file_name=f"life_tracker_{date.today()}.csv",
            mime="text/csv"
        )
        
        # Weekly Summary
        st.markdown("### Weekly Summary")
        
        if len(df) >= 7:
            weeks = []
            for i in range(0, len(df), 7):
                week_data = df.iloc[i:i+7]
                start_date = week_data['date'].min().strftime('%Y-%m-%d')
                
                week_summary = {
                    'Week Starting': start_date,
                    'Gym Days': (week_data['gym'] == 'Yes').sum(),
                    'Avg Study (hrs)': week_data['study_hours'].mean(),
                    'Junk Days': (week_data['junk_food'] == 'Yes').sum(),
                    'Total Spent': f"₹{week_data['spending'].sum():.0f}"
                }
                weeks.append(week_summary)
            
            st.dataframe(weeks, use_container_width=True)

# ---------- FOOTER ----------
st.divider()
st.markdown("""
<div style='text-align: center; color: #94a3b8; padding: 20px 0;'>
    <p style='margin: 0;'>✨ <strong>Consistency beats motivation.</strong> Small wins compound into amazing results.</p>
    <p style='margin: 8px 0; font-size: 12px;'>Track daily • Get AI insights • Transform your life 🚀</p>
</div>
""", unsafe_allow_html=True)
