import streamlit as st
import pandas as pd
from datetime import date, timedelta
import os
import random
from groq import Groq

# PAGE CONFIG
st.set_page_config(
    page_title="AI Life Tracker Pro",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)

DAILY_BUDGET = 200

# PREMIUM CSS - ULTRA MODERN
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Background */
    .main {
        background: linear-gradient(-45deg, #0f172a, #1a1f4b, #2d1b69, #1a1f4b);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: #e2e8f0;
        padding: 0;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Header */
    .header-section {
        background: linear-gradient(135deg, rgba(236, 72, 153, 0.1) 0%, rgba(168, 85, 247, 0.1) 100%);
        border: 1px solid rgba(236, 72, 153, 0.3);
        border-radius: 24px;
        padding: 32px;
        margin-bottom: 32px;
        backdrop-filter: blur(20px);
        box-shadow: 0 25px 50px rgba(236, 72, 153, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    .logo-section {
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 20px;
    }
    
    .logo-text {
        font-size: 2.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #ec4899 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* AI Message Box */
    .ai-box {
        background: rgba(15, 23, 42, 0.7);
        border-left: 4px solid #ec4899;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        font-size: 1.05rem;
        line-height: 1.7;
        color: #e2e8f0;
        box-shadow: 0 10px 30px rgba(236, 72, 153, 0.1);
    }
    
    /* Chat Input */
    .chat-box {
        display: flex;
        gap: 12px;
        margin-bottom: 24px;
    }
    
    .stTextInput input {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 2px solid rgba(99, 102, 241, 0.3) !important;
        border-radius: 14px !important;
        padding: 14px 18px !important;
        color: #e2e8f0 !important;
        font-size: 1rem !important;
        transition: all 0.3s !important;
    }
    
    .stTextInput input:focus {
        border-color: #ec4899 !important;
        background: rgba(30, 41, 59, 0.95) !important;
        box-shadow: 0 0 0 3px rgba(236, 72, 153, 0.1) !important;
    }
    
    /* Quick Stats - Animated */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 16px;
        margin-bottom: 32px;
    }
    
    .stat-card {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(168, 85, 247, 0.15) 100%);
        border: 2px solid rgba(99, 102, 241, 0.3);
        border-radius: 18px;
        padding: 20px;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        transition: left 0.5s;
    }
    
    .stat-card:hover {
        transform: translateY(-8px) scale(1.02);
        border-color: #ec4899;
        background: linear-gradient(135deg, rgba(236, 72, 153, 0.2) 0%, rgba(168, 85, 247, 0.2) 100%);
        box-shadow: 0 20px 50px rgba(236, 72, 153, 0.2);
    }
    
    .stat-card:hover::before {
        left: 100%;
    }
    
    .stat-value {
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(135deg, #ec4899 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 8px;
    }
    
    .stat-label {
        font-size: 0.85rem;
        color: #cbd5e1;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 1px;
    }
    
    /* Main Grid */
    .content-wrapper {
        display: grid;
        grid-template-columns: 1fr 1.2fr;
        gap: 24px;
        margin-bottom: 32px;
    }
    
    /* Card */
    .premium-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 20px;
        padding: 28px;
        backdrop-filter: blur(20px);
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.4s ease;
    }
    
    .premium-card:hover {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.95) 100%);
        border-color: rgba(148, 163, 184, 0.4);
        transform: translateY(-4px);
        box-shadow: 0 35px 80px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.15);
    }
    
    .card-title {
        font-size: 1.3rem;
        font-weight: 800;
        color: #00d4ff;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* Input Fields */
    .form-group {
        margin-bottom: 18px;
    }
    
    .form-label {
        font-size: 0.9rem;
        font-weight: 700;
        color: #cbd5e1;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
        display: block;
    }
    
    .stRadio > label {
        color: #cbd5e1 !important;
        font-weight: 600 !important;
        margin-right: 16px !important;
    }
    
    .stNumberInput input {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 2px solid rgba(99, 102, 241, 0.3) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        color: #e2e8f0 !important;
        font-weight: 600 !important;
        transition: all 0.3s !important;
    }
    
    .stNumberInput input:focus {
        border-color: #ec4899 !important;
        box-shadow: 0 0 0 3px rgba(236, 72, 153, 0.1) !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #ec4899 0%, #a855f7 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 14px 24px;
        font-weight: 700;
        font-size: 0.95rem;
        letter-spacing: 0.5px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 12px 30px rgba(236, 72, 153, 0.3);
        text-transform: uppercase;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 20px 50px rgba(236, 72, 153, 0.5);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    /* Today's Metrics */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 14px;
        margin-bottom: 24px;
    }
    
    .metric-item {
        background: linear-gradient(135deg, rgba(236, 72, 153, 0.1) 0%, rgba(99, 102, 241, 0.1) 100%);
        border: 2px solid rgba(236, 72, 153, 0.2);
        border-radius: 14px;
        padding: 16px;
        text-align: center;
        transition: all 0.3s;
    }
    
    .metric-item:hover {
        background: linear-gradient(135deg, rgba(236, 72, 153, 0.15) 0%, rgba(99, 102, 241, 0.15) 100%);
        border-color: rgba(236, 72, 153, 0.5);
        transform: translateY(-2px);
    }
    
    .metric-emoji {
        font-size: 2rem;
        margin-bottom: 8px;
    }
    
    .metric-num {
        font-size: 2.2rem;
        font-weight: 900;
        background: linear-gradient(135deg, #ec4899 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 4px;
    }
    
    .metric-text {
        font-size: 0.8rem;
        color: #94a3b8;
        text-transform: uppercase;
        font-weight: 700;
    }
    
    /* Charts */
    .chart-container {
        background: rgba(15, 23, 42, 0.5);
        border-radius: 14px;
        padding: 16px;
        margin-top: 16px;
    }
    
    /* Success Message */
    .success-msg {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        border-left: 4px solid #10b981;
        border-radius: 12px;
        padding: 16px;
        color: white;
        font-weight: 600;
        animation: slideIn 0.4s ease;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Divider */
    hr {
        margin: 24px 0 !important;
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.3), transparent) !important;
    }
    
    /* Footer */
    .footer-text {
        text-align: center;
        color: #94a3b8;
        font-size: 0.9rem;
        padding: 24px 0;
    }
    
    /* Responsive */
    @media (max-width: 1024px) {
        .content-wrapper {
            grid-template-columns: 1fr;
        }
    }
</style>
""", unsafe_allow_html=True)

# DATA FUNCTIONS
FILE = "data.csv"

def load_data():
    try:
        df = pd.read_csv(FILE)
        df['date'] = pd.to_datetime(df['date'])
        return df
    except:
        return pd.DataFrame(columns=["date","gym","study_hours","junk_food","spending"])

def save_data(df):
    df.to_csv(FILE, index=False)

# GROQ AI
@st.cache_resource
def get_groq_client():
    api_key = st.secrets.get('GROQ_API_KEY') or os.getenv('GROQ_API_KEY')
    if not api_key:
        return None
    try:
        return Groq(api_key=api_key)
    except:
        return None

def get_motivation(df, user_msg=""):
    client = get_groq_client()
    
    if df.empty:
        return "🎯 Ready to crush it? Log your first day and let's go! 💪"
    
    if not client:
        msgs = [
            "💪 You're building unstoppable momentum! Keep crushing it! 🔥",
            "⚡ Every day is a new opportunity to be better. Go get it! 🚀",
            "🎯 Small wins compound into EPIC results. You got this! 💯",
            "✨ Your dedication is inspiring. Push harder today! 🌟"
        ]
        return random.choice(msgs)
    
    try:
        recent = df.tail(7)
        gym = (recent["gym"] == "Yes").sum()
        study = recent["study_hours"].mean()
        junk = (recent["junk_food"] == "Yes").sum()
        
        msg = user_msg if user_msg else f"My stats: {gym}/7 gym, {study:.1f}h study, {junk}/7 junk days"
        
        prompt = f"""You're an ELITE performance coach. User: {msg}
Their week: Gym {gym}/7, Study {study:.1f}h/day, Junk {junk}/7

Give SHORT (1-2 sentences), ENERGETIC advice with emojis. Make them want to WIN! 🚀"""
        
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=120,
            temperature=0.9
        )
        return response.choices[0].message.content
    except:
        return "💪 You're doing amazing! Keep the momentum going! 🔥"

# LOAD DATA
df = load_data()

# LAYOUT
with st.container():
    # HEADER
    st.markdown('<div class="header-section">', unsafe_allow_html=True)
    
    st.markdown('''
    <div class="logo-section">
        <span class="logo-text">✨ AI LIFE TRACKER</span>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown(f'<div class="ai-box">{get_motivation(df)}</div>', unsafe_allow_html=True)
    
    # Chat
    st.markdown('<p style="color: #cbd5e1; font-weight: 700; font-size: 0.95rem; margin-bottom: 12px;">💬 Ask Coach Anything</p>', unsafe_allow_html=True)
    
    chat_col1, chat_col2 = st.columns([1, 0.12], gap="small")
    with chat_col1:
        user_msg = st.text_input("", placeholder="Get tips, motivation, or suggestions...", label_visibility="collapsed", key="chat")
    with chat_col2:
        if st.button("📤", key="send", help="Send"):
            if user_msg.strip():
                response = get_motivation(df, user_msg)
                st.markdown(f'<div class="ai-box" style="margin-top: 12px;">🤖: {response}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # STATS
    if not df.empty:
        recent = df.tail(7)
        st.markdown('<div class="stats-grid">', unsafe_allow_html=True)
        
        gym_stats = (recent["gym"] == "Yes").sum()
        study_stats = recent["study_hours"].mean()
        junk_stats = (recent["junk_food"] == "Yes").sum()
        spend_stats = recent["spending"].mean()
        
        st.markdown(f'''
        <div class="stat-card">
            <div class="stat-value">{gym_stats}/7</div>
            <div class="stat-label">💪 Gym Days</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{study_stats:.1f}h</div>
            <div class="stat-label">📚 Study Avg</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{junk_stats}/7</div>
            <div class="stat-label">🍕 Junk Days</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">₹{spend_stats:.0f}</div>
            <div class="stat-label">💰 Daily Avg</div>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # MAIN CONTENT
    col_left, col_right = st.columns([1, 1.2], gap="large")
    
    # LEFT: FORM
    with col_left:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown('<h3 class="card-title">✍️ Log Today</h3>', unsafe_allow_html=True)
        
        st.markdown('<div class="form-group">', unsafe_allow_html=True)
        st.markdown('<span class="form-label">💪 Gym?</span>', unsafe_allow_html=True)
        gym = st.radio("", ["Yes", "No"], horizontal=True, label_visibility="collapsed", key="gym_input")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="form-group">', unsafe_allow_html=True)
        st.markdown('<span class="form-label">📚 Study Hours</span>', unsafe_allow_html=True)
        study = st.number_input("", min_value=0.0, max_value=24.0, step=0.5, value=0.0, label_visibility="collapsed", key="study_input")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="form-group">', unsafe_allow_html=True)
        st.markdown('<span class="form-label">🍕 Junk Food?</span>', unsafe_allow_html=True)
        junk = st.radio("", ["Yes", "No"], horizontal=True, label_visibility="collapsed", key="junk_input")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="form-group">', unsafe_allow_html=True)
        st.markdown('<span class="form-label">💰 Spending (₹)</span>', unsafe_allow_html=True)
        spend = st.number_input("", min_value=0, max_value=10000, step=10, value=0, label_visibility="collapsed", key="spend_input")
        st.markdown('</div>', unsafe_allow_html=True)
        
        btn_col1, btn_col2 = st.columns(2, gap="small")
        with btn_col1:
            if st.button("💾 Save", key="save_btn"):
                today = date.today()
                existing = df[df['date'].dt.date == today] if not df.empty else pd.DataFrame()
                if not existing.empty:
                    df.loc[df['date'].dt.date == today, ['gym', 'study_hours', 'junk_food', 'spending']] = [gym, study, junk, spend]
                else:
                    new_entry = pd.DataFrame({"date": [today], "gym": [gym], "study_hours": [study], "junk_food": [junk], "spending": [spend]})
                    df = pd.concat([df, new_entry], ignore_index=True)
                save_data(df)
                st.success("✅ Saved! Keep crushing it! 🔥")
                st.balloons()
                st.rerun()
        
        with btn_col2:
            if st.button("🔄 Clear", key="clear_btn"):
                if st.session_state.get('confirm'):
                    df = pd.DataFrame(columns=["date","gym","study_hours","junk_food","spending"])
                    save_data(df)
                    st.success("Data cleared!")
                    st.rerun()
                else:
                    st.session_state.confirm = True
                    st.warning("Click again to confirm")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # RIGHT: STATS & CHARTS
    with col_right:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown('<h3 class="card-title">📊 Your Progress</h3>', unsafe_allow_html=True)
        
        if not df.empty:
            today_data = df[df['date'].dt.date == date.today()]
            
            if not today_data.empty:
                today = today_data.iloc[0]
                st.markdown('<p style="color: #cbd5e1; font-weight: 700; font-size: 0.9rem; margin-bottom: 12px;">Today\'s Results</p>', unsafe_allow_html=True)
                
                st.markdown('<div class="metrics-grid">', unsafe_allow_html=True)
                
                st.markdown(f'''
                <div class="metric-item">
                    <div class="metric-emoji">💪</div>
                    <div class="metric-num">{'✅' if today['gym'] == 'Yes' else '❌'}</div>
                    <div class="metric-text">Gym</div>
                </div>
                <div class="metric-item">
                    <div class="metric-emoji">📚</div>
                    <div class="metric-num">{today['study_hours']:.1f}</div>
                    <div class="metric-text">Hours</div>
                </div>
                <div class="metric-item">
                    <div class="metric-emoji">🍕</div>
                    <div class="metric-num">{'❌' if today['junk_food'] == 'Yes' else '✅'}</div>
                    <div class="metric-text">Junk</div>
                </div>
                <div class="metric-item">
                    <div class="metric-emoji">💰</div>
                    <div class="metric-num">₹{today['spending']}</div>
                    <div class="metric-text">Spent</div>
                </div>
                ''', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Chart
            recent = df.tail(7)
            if len(recent) > 0:
                st.markdown('<p style="color: #cbd5e1; font-weight: 700; font-size: 0.9rem; margin-top: 20px; margin-bottom: 12px;">7-Day Trend</p>', unsafe_allow_html=True)
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                study_data = recent[['date', 'study_hours']].set_index('date')
                st.line_chart(study_data, use_container_width=True, color="#ec4899")
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("📝 Log your first day to see progress!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # BOTTOM CHARTS
    if not df.empty and len(df) > 1:
        col_chart1, col_chart2 = st.columns(2, gap="large")
        
        with col_chart1:
            st.markdown('<div class="premium-card">', unsafe_allow_html=True)
            st.markdown('<h3 class="card-title">📈 Study Progression</h3>', unsafe_allow_html=True)
            study_full = df[['date', 'study_hours']].set_index('date')
            st.line_chart(study_full, use_container_width=True, color="#00d4ff")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_chart2:
            st.markdown('<div class="premium-card">', unsafe_allow_html=True)
            st.markdown('<h3 class="card-title">💸 Spending Pattern</h3>', unsafe_allow_html=True)
            spend_full = df[['date', 'spending']].set_index('date')
            st.bar_chart(spend_full, use_container_width=True, color="#10b981")
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # DATA TABLE
    if not df.empty:
        with st.expander("📊 View All Data", expanded=False):
            display_df = df.copy()
            display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d')
            display_df = display_df.sort_values('date', ascending=False)
            
            st.dataframe(
                display_df.style.format({'spending': '₹{:.0f}', 'study_hours': '{:.1f}h'}),
                use_container_width=True,
                hide_index=True
            )
            
            csv = display_df.to_csv(index=False)
            st.download_button("📥 Download Data", csv, "tracker_data.csv", "text/csv", use_container_width=True)

st.markdown("""
<div class="footer-text">
    🔥 Small Daily Wins = Extraordinary Results | Built with ❤️ | Keep Growing! 💪
</div>
""", unsafe_allow_html=True)
