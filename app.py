import streamlit as st
import pandas as pd
from datetime import date, timedelta
import os
import random

# Try to import Groq, with fallback
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    st.warning("⚠️ Groq library not installed. Using fallback feedback mode. Run: pip install groq")

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="✨ AI Life Tracker",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)

DAILY_BUDGET = 200

# ---------- ULTRA MODERN 2026 CSS ----------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main background - beautiful gradient */
    .main {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f4b 25%, #2d1b69 50%, #1a1f4b 75%, #0a0e27 100%);
        color: #e2e8f0;
        min-height: 100vh;
    }
    
    /* Glass morphism effect */
    .glass-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 24px;
        padding: 28px;
        margin-bottom: 24px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .glass-card:hover {
        background: rgba(30, 41, 59, 0.85);
        border-color: rgba(148, 163, 184, 0.4);
        transform: translateY(-2px);
        box-shadow: 0 30px 80px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.15);
    }
    
    /* Gradient text */
    .gradient-text {
        background: linear-gradient(135deg, #00d4ff 0%, #0099ff 25%, #6366f1 50%, #ec4899 75%, #f59e0b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    
    /* Main title */
    .main-title {
        font-size: 3.5rem;
        font-weight: 900;
        margin-bottom: 8px;
        letter-spacing: -1px;
        text-align: center;
    }
    
    .subtitle {
        font-size: 1.1rem;
        text-align: center;
        color: #94a3b8;
        margin-bottom: 40px;
        font-weight: 500;
    }
    
    /* Input section styling */
    .input-card {
        background: transparent;
        border: none;
        border-radius: 0;
        padding: 0;
        backdrop-filter: none;
        transition: none;
    }
    
    .input-card:hover {
        background: transparent;
        border-color: transparent;
    }
    
    /* Input labels */
    .input-label {
        font-size: 0.85rem;
        font-weight: 700;
        color: #cbd5e1;
        margin-bottom: 8px;
        display: block;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Toggle buttons */
    .toggle-group {
        display: flex;
        gap: 10px;
        margin-bottom: 20px;
    }
    
    /* Number input styling - COMPACT */
    .stNumberInput input {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(99, 102, 241, 0.4) !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        color: #e2e8f0 !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        height: 38px !important;
    }
    
    .stNumberInput input:hover {
        border-color: rgba(99, 102, 241, 0.7) !important;
        background: rgba(15, 23, 42, 0.8) !important;
    }
    
    .stNumberInput input:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.1) !important;
    }
    
    /* Button styling - COMPACT */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #00d4ff 0%, #0099ff 50%, #6366f1 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 16px;
        font-size: 0.95rem;
        font-weight: 700;
        letter-spacing: 0.3px;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 8px 20px rgba(0, 212, 255, 0.25);
        text-transform: uppercase;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 30px rgba(0, 212, 255, 0.4);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Metric display */
    .metric-showcase {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(59, 130, 246, 0.1) 100%);
        border: 2px solid rgba(16, 185, 129, 0.3);
        border-radius: 20px;
        padding: 24px;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-showcase:hover {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(59, 130, 246, 0.15) 100%);
        border-color: rgba(16, 185, 129, 0.6);
        transform: translateY(-4px);
    }
    
    .metric-label {
        font-size: 0.85rem;
        text-transform: uppercase;
        color: #94a3b8;
        font-weight: 700;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00d4ff 0%, #6366f1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 8px;
    }
    
    .metric-subtitle {
        font-size: 0.9rem;
        color: #cbd5e1;
        font-weight: 500;
    }
    
    /* Stat boxes */
    .stat-box {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
        border: 2px solid rgba(99, 102, 241, 0.3);
        border-radius: 18px;
        padding: 20px;
        text-align: center;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .stat-box:hover {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.3) 0%, rgba(139, 92, 246, 0.3) 100%);
        border-color: rgba(99, 102, 241, 0.6);
        transform: translateY(-6px);
    }
    
    .stat-value {
        font-size: 2.2rem;
        font-weight: 900;
        color: #00d4ff;
        margin-bottom: 4px;
    }
    
    .stat-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        color: #94a3b8;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    
    /* AI Coach section */
    .ai-coach-box {
        background: linear-gradient(135deg, rgba(236, 72, 153, 0.15) 0%, rgba(168, 85, 247, 0.15) 100%);
        border: 2px solid rgba(236, 72, 153, 0.4);
        border-radius: 24px;
        padding: 32px;
        margin-bottom: 24px;
        backdrop-filter: blur(10px);
        box-shadow: 0 20px 60px rgba(236, 72, 153, 0.2);
    }
    
    .coach-title {
        font-size: 1.4rem;
        font-weight: 800;
        margin-bottom: 16px;
        background: linear-gradient(135deg, #ec4899 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .coach-message {
        font-size: 1.05rem;
        line-height: 1.8;
        color: #e2e8f0;
        font-weight: 500;
    }
    
    /* Success message */
    .success-toast {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        border: 2px solid rgba(16, 185, 129, 0.5);
        border-radius: 16px;
        padding: 20px;
        color: white;
        font-weight: 600;
        margin-bottom: 20px;
        animation: slideIn 0.4s ease;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Loading animation */
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.6;
        }
    }
    
    .loading {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5rem;
        }
        
        .subtitle {
            font-size: 1rem;
        }
        
        .input-card {
            padding: 20px;
        }
        
        .metric-value {
            font-size: 1.8rem;
        }
    }
    
    /* Radio buttons */
    .stRadio > label {
        color: #cbd5e1 !important;
        font-weight: 600 !important;
    }
    
    /* Hide default dividers */
    hr {
        margin: 8px 0 !important;
    }
    
    /* Tighter spacing */
    .stColumn {
        gap: 8px !important;
    }
    
    /* Reduce margins */
    .stMarkdown {
        margin-bottom: 4px !important;
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
    if not GROQ_AVAILABLE:
        return None
    
    api_key = st.secrets.get('GROQ_API_KEY') or os.getenv('GROQ_API_KEY')
    if not api_key:
        return None
    
    try:
        return Groq(api_key=api_key)
    except Exception as e:
        st.warning(f"⚠️ Could not connect to Groq: {str(e)}")
        return None

def get_fallback_feedback(df):
    """Fallback feedback when API is not available"""
    if df.empty:
        return "🎯 Start tracking to get personalized feedback!"
    
    recent = df.tail(7)
    gym_days = (recent["gym"] == "Yes").sum()
    junk_days = (recent["junk_food"] == "Yes").sum()
    avg_study = recent["study_hours"].mean()
    avg_spending = recent["spending"].mean()
    
    feedbacks = [
        f"💪 Amazing! You crushed {gym_days} gym sessions this week. Keep that fire burning! Your study average is {avg_study:.1f}h - that's solid progress!",
        f"🎯 Brilliant consistency! {gym_days}/7 gym days is incredible. You're averaging {avg_study:.1f}h of study. Just watch those junk food days ({junk_days}) - try to cut 1 next week!",
        f"⚡ You're on 🔥! Study time: {avg_study:.1f}h/day, Spending: ₹{avg_spending:.0f}/day. Gym: {gym_days}/7. Tomorrow: Aim for 1 more hour of study!",
        f"✨ Wow! You're building serious habits. {gym_days} gym days, {avg_study:.1f}h study avg. Junk food: {junk_days} days - reduce by 1 for next level! 🚀",
    ]
    
    return random.choice(feedbacks)

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
        
        prompt = f"""You are an incredibly encouraging and motivating life coach. Be enthusiastic and use emojis!
        
Here's their data from the past 7 days:
- Gym: {gym_days} days out of {total_days} ({gym_percentage:.0f}%)
- Average study hours: {avg_study:.1f} hours/day
- Junk food days: {junk_days} out of {total_days}
- Average daily spending: ₹{avg_spending:.0f} (Budget: ₹200)

Give ENERGETIC, MOTIVATING feedback in 2-3 sentences with emojis! Be honest but encouraging. End with one specific action for tomorrow. Make them feel pumped up!"""
        
        message = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.8
        )
        
        return message.choices[0].message.content
    
    except:
        return get_fallback_feedback(df)

# ---------- LOAD DATA ----------
df = load_data()

# ---------- HEADER ----------
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<h1 class="main-title gradient-text">✨ AI Life Tracker</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Track. Grow. Transform. Your life, optimized daily.</p>', unsafe_allow_html=True)

# ---------- INPUT SECTION ----------
st.markdown('<h2 style="color: #00d4ff; font-weight: 800; margin-bottom: 16px;">📝 Today\'s Check-in</h2>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4, gap="small")

with col1:
    st.markdown('<span class="input-label">💪 Gym?</span>', unsafe_allow_html=True)
    gym = st.radio("", ["Yes","No"], horizontal=True, label_visibility="collapsed", key="gym_input")

with col2:
    st.markdown('<span class="input-label">📚 Study (h)</span>', unsafe_allow_html=True)
    study = st.number_input("", min_value=0.0, step=0.5, value=0.0, label_visibility="collapsed", key="study_input")

with col3:
    st.markdown('<span class="input-label">🍕 Junk?</span>', unsafe_allow_html=True)
    junk = st.radio("", ["Yes","No"], horizontal=True, label_visibility="collapsed", key="junk_input")

with col4:
    st.markdown('<span class="input-label">💰 Spend (₹)</span>', unsafe_allow_html=True)
    spend = st.number_input("", min_value=0, value=0, label_visibility="collapsed", key="spend_input")

st.markdown('<br>', unsafe_allow_html=True)

btn_col1, btn_col2, btn_col3 = st.columns([3, 0.5, 0.5], gap="small")

with btn_col1:
    if st.button("💾 SAVE", use_container_width=True, key="save_btn"):
        today = date.today()
        existing = df[df['date'].dt.date == today] if not df.empty else pd.DataFrame()
        
        if not existing.empty:
            df.loc[df['date'].dt.date == today, ['gym', 'study_hours', 'junk_food', 'spending']] = [gym, study, junk, spend]
        else:
            new_entry = pd.DataFrame({
                "date": [today],
                "gym": [gym],
                "study_hours": [study],
                "junk_food": [junk],
                "spending": [spend]
            })
            df = pd.concat([df, new_entry], ignore_index=True)
        
        save_data(df)
        st.success("✅ Saved!")
        st.balloons()

with btn_col2:
    if st.button("↻", use_container_width=True, help="Reset form", key="reset_form"):
        st.rerun()

with btn_col3:
    if st.button("🗑️", use_container_width=True, help="Reset all data", key="reset_all"):
        if st.session_state.get('confirm_reset'):
            df = pd.DataFrame(columns=["date","gym","study_hours","junk_food","spending"])
            save_data(df)
            st.success("✅ All data reset!")
            st.session_state.confirm_reset = False
        else:
            st.session_state.confirm_reset = True
            st.warning("⚠️ Click again to confirm")

st.divider()

# ---------- TODAY SUMMARY ----------
if not df.empty:
    today_data = df[df['date'].dt.date == date.today()]
    
    if not today_data.empty:
        today = today_data.iloc[0]
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h2 style="color: #00d4ff; font-weight: 800;">📊 Today\'s Summary</h2>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4, gap="medium")
        
        with col1:
            st.markdown(f"""
            <div class="metric-showcase">
                <div class="metric-label">Gym</div>
                <div class="metric-value">{'✅' if today['gym'] == 'Yes' else '❌'}</div>
                <div class="metric-subtitle">{today['gym']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-showcase">
                <div class="metric-label">Study</div>
                <div class="metric-value">{today['study_hours']:.1f}</div>
                <div class="metric-subtitle">hours</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-showcase">
                <div class="metric-label">Junk</div>
                <div class="metric-value">{'❌' if today['junk_food'] == 'Yes' else '✅'}</div>
                <div class="metric-subtitle">{today['junk_food']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            spend_status = "Over 🔴" if today['spending'] > DAILY_BUDGET else "Good 🟢"
            st.markdown(f"""
            <div class="metric-showcase">
                <div class="metric-label">Spending</div>
                <div class="metric-value">₹{today['spending']}</div>
                <div class="metric-subtitle">{spend_status}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# ---------- 7-DAY STATS ----------
if len(df) > 0:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 style="color: #00d4ff; font-weight: 800;">📈 Last 7 Days Highlights</h2>', unsafe_allow_html=True)
    
    recent = df.tail(7)
    
    gym_days = (recent["gym"] == "Yes").sum()
    avg_study = recent["study_hours"].mean()
    junk_days = (recent["junk_food"] == "Yes").sum()
    avg_spending = recent["spending"].mean()
    total_spending = recent["spending"].sum()
    
    col1, col2, col3, col4 = st.columns(4, gap="medium")
    
    with col1:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-value">{gym_days}/7</div>
            <div class="stat-label">💪 Gym Days</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-value">{avg_study:.1f}h</div>
            <div class="stat-label">📚 Study Avg</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-value">{junk_days}/7</div>
            <div class="stat-label">🍕 Junk Days</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-value">₹{avg_spending:.0f}</div>
            <div class="stat-label">💰 Daily Avg</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Charts
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        st.markdown('<h3 style="color: #cbd5e1; font-weight: 700; margin-bottom: 16px;">📚 Study Progress</h3>', unsafe_allow_html=True)
        study_data = recent[['date', 'study_hours']].set_index('date')
        st.line_chart(study_data, use_container_width=True, color="#00d4ff")
    
    with col2:
        st.markdown('<h3 style="color: #cbd5e1; font-weight: 700; margin-bottom: 16px;">💸 Spending Pattern</h3>', unsafe_allow_html=True)
        spend_data = recent[['date', 'spending']].set_index('date')
        st.bar_chart(spend_data, use_container_width=True, color="#ec4899")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- AI COACH ----------
st.markdown('<div class="ai-coach-box">', unsafe_allow_html=True)
st.markdown('<h2 class="coach-title">🤖 Your AI Coach Says...</h2>', unsafe_allow_html=True)

with st.spinner("🔮 Coach is analyzing your brilliance..."):
    feedback = get_ai_feedback(df)

st.markdown(f'<p class="coach-message">{feedback}</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------- DETAILED ANALYTICS ----------
if len(df) > 1:
    with st.expander("📊 Detailed Analytics & History", expanded=False):
        st.markdown("### 📋 All Your Data")
        
        display_df = df.copy()
        display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d')
        display_df = display_df.sort_values('date', ascending=False)
        
        st.dataframe(
            display_df.style.format({
                'spending': '₹{:.0f}',
                'study_hours': '{:.1f}h'
            }),
            use_container_width=True,
            hide_index=True
        )
        
        csv = display_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Your Data (CSV)",
            data=csv,
            file_name=f"my_life_tracker_{date.today()}.csv",
            mime="text/csv",
            use_container_width=True
        )

# ---------- FOOTER ----------
st.divider()
st.markdown("""
<div style='text-align: center; padding: 20px 0;'>
    <p style='color: #94a3b8; font-size: 0.95rem; margin: 0;'>
        <strong>🔥 Remember:</strong> Small daily wins compound into extraordinary results.
    </p>
    <p style='color: #64748b; font-size: 0.85rem; margin: 8px 0 0 0;'>
        Track • Analyze • Grow • Repeat ✨
    </p>
</div>
""", unsafe_allow_html=True)
