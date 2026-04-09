import streamlit as st
import pandas as pd
from datetime import date, timedelta
import os
import random
import json

# Try to import Groq
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Background */
    .main {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f4b 25%, #2d1b69 50%, #1a1f4b 75%, #0a0e27 100%);
        color: #e2e8f0;
        padding: 0 !important;
    }
    
    /* Container */
    .main-container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 20px;
    }
    
    /* AI Chat Section - Top */
    .ai-chat-section {
        background: linear-gradient(135deg, rgba(236, 72, 153, 0.1) 0%, rgba(168, 85, 247, 0.1) 100%);
        border: 1px solid rgba(236, 72, 153, 0.3);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 24px;
        backdrop-filter: blur(10px);
        box-shadow: 0 20px 60px rgba(236, 72, 153, 0.15);
    }
    
    .coach-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 16px;
    }
    
    .coach-title {
        font-size: 1.3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ec4899 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
    }
    
    .coach-message {
        background: rgba(15, 23, 42, 0.5);
        border-left: 4px solid #ec4899;
        padding: 16px;
        border-radius: 12px;
        font-size: 1rem;
        line-height: 1.6;
        color: #e2e8f0;
        margin-bottom: 16px;
    }
    
    /* Chat input area */
    .chat-input-area {
        display: flex;
        gap: 10px;
        align-items: flex-end;
    }
    
    /* Quick stats row */
    .quick-stats {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 12px;
        margin-top: 16px;
    }
    
    .stat-mini {
        background: rgba(99, 102, 241, 0.1);
        border: 1px solid rgba(99, 102, 241, 0.3);
        padding: 12px;
        border-radius: 12px;
        text-align: center;
    }
    
    .stat-mini-value {
        font-size: 1.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00d4ff 0%, #6366f1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .stat-mini-label {
        font-size: 0.75rem;
        color: #94a3b8;
        text-transform: uppercase;
        font-weight: 700;
        margin-top: 6px;
    }
    
    /* Main content grid */
    .content-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
        margin-bottom: 24px;
    }
    
    /* Glass card */
    .glass-card {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        background: rgba(30, 41, 59, 0.8);
        border-color: rgba(148, 163, 184, 0.4);
        transform: translateY(-2px);
    }
    
    .card-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #00d4ff;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Today's entry card */
    .entry-card {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
        border: 2px solid rgba(99, 102, 241, 0.3);
        border-radius: 16px;
        padding: 20px;
        transition: all 0.3s ease;
    }
    
    .entry-card:hover {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.25) 0%, rgba(139, 92, 246, 0.25) 100%);
        border-color: rgba(99, 102, 241, 0.6);
    }
    
    .input-field-group {
        margin-bottom: 14px;
    }
    
    .input-label {
        font-size: 0.8rem;
        font-weight: 700;
        color: #cbd5e1;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
        display: block;
    }
    
    .input-wrapper {
        display: flex;
        gap: 8px;
        align-items: center;
    }
    
    .input-value {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 8px;
        padding: 8px 12px;
        color: #e2e8f0;
        font-weight: 600;
        font-size: 0.95rem;
    }
    
    /* Metric box */
    .metric-box {
        background: rgba(99, 102, 241, 0.1);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 12px;
        padding: 14px;
        text-align: center;
        margin-bottom: 10px;
    }
    
    .metric-label {
        font-size: 0.75rem;
        color: #94a3b8;
        text-transform: uppercase;
        font-weight: 700;
        margin-bottom: 4px;
    }
    
    .metric-value {
        font-size: 1.6rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00d4ff 0%, #6366f1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #00d4ff 0%, #0099ff 50%, #6366f1 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 16px;
        font-size: 0.9rem;
        font-weight: 700;
        letter-spacing: 0.3px;
        transition: all 0.3s ease;
        box-shadow: 0 8px 20px rgba(0, 212, 255, 0.25);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 30px rgba(0, 212, 255, 0.4);
    }
    
    /* Number input */
    .stNumberInput input {
        background: rgba(15, 23, 42, 0.7) !important;
        border: 1px solid rgba(99, 102, 241, 0.3) !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        color: #e2e8f0 !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
    }
    
    .stNumberInput input:focus {
        border-color: #6366f1 !important;
    }
    
    /* Radio buttons */
    .stRadio > label {
        color: #cbd5e1 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }
    
    /* Charts */
    .stPlotlyChart, .stLineChart {
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Mobile responsive */
    @media (max-width: 1024px) {
        .content-grid {
            grid-template-columns: 1fr;
        }
    }
    
    /* No margin on elements */
    .stMarkdown {
        margin: 0 !important;
    }
    
    /* Divider */
    hr {
        margin: 16px 0 !important;
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, rgba(99, 102, 241, 0) 0%, rgba(99, 102, 241, 0.3) 50%, rgba(99, 102, 241, 0) 100%) !important;
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

# ---------- GROQ AI SETUP ----------
@st.cache_resource
def get_groq_client():
    if not GROQ_AVAILABLE:
        return None
    
    api_key = st.secrets.get('GROQ_API_KEY') or os.getenv('GROQ_API_KEY')
    if not api_key:
        return None
    
    try:
        return Groq(api_key=api_key)
    except:
        return None

def get_fallback_feedback(df):
    """Fallback feedback"""
    if df.empty:
        return "🎯 Start tracking to unlock personalized insights!"
    
    recent = df.tail(7)
    gym_days = (recent["gym"] == "Yes").sum()
    avg_study = recent["study_hours"].mean()
    junk_days = (recent["junk_food"] == "Yes").sum()
    
    feedbacks = [
        f"💪 You've crushed {gym_days}/7 gym sessions! Your study avg is {avg_study:.1f}h - keep that fire! 🔥",
        f"🎯 Amazing! {gym_days} gym days + {avg_study:.1f}h study = unstoppable momentum! Just cut {junk_days} junk days! 🚀",
        f"⚡ You're on 🔥! Gym: {gym_days}/7, Study: {avg_study:.1f}h. Tomorrow aim for {min(avg_study + 0.5, 5):.1f}h! 💪",
        f"✨ Building serious habits! Keep gym strong ({gym_days}/7), maintain study ({avg_study:.1f}h), you got this! 🎯",
    ]
    return random.choice(feedbacks)

def get_ai_coaching(df, user_message=""):
    """Get AI coaching from Groq"""
    client = get_groq_client()
    if not client or df.empty:
        return get_fallback_feedback(df)
    
    try:
        recent = df.tail(7)
        gym_days = (recent["gym"] == "Yes").sum()
        avg_study = recent["study_hours"].mean()
        junk_days = (recent["junk_food"] == "Yes").sum()
        avg_spending = recent["spending"].mean()
        
        context = f"""User's last 7 days: Gym {gym_days}/7, Study {avg_study:.1f}h/day, Junk {junk_days}/7, Spend ₹{avg_spending:.0f}/day"""
        
        prompt = f"""You are a world-class life coach. Be ENERGETIC, MOTIVATING, use emojis!
{context}

{f'User says: {user_message}' if user_message else 'Give a brief, motivating insight about their progress.'}

Keep it SHORT (1-2 sentences max) and ACTION-FOCUSED! 🚀"""
        
        message = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.8
        )
        
        return message.choices[0].message.content
    except:
        return get_fallback_feedback(df)

# ---------- LOAD DATA ----------
df = load_data()

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

# ---------- LAYOUT ----------
col_main = st.container()

with col_main:
    # ========== AI COACH SECTION (TOP) ==========
    st.markdown('<div class="ai-chat-section">', unsafe_allow_html=True)
    
    st.markdown('''
    <div class="coach-header">
        <span style="font-size: 1.8rem;">🤖</span>
        <h2 class="coach-title">Your AI Life Coach</h2>
    </div>
    ''', unsafe_allow_html=True)
    
    # Coach message
    coaching = get_ai_coaching(df)
    st.markdown(f'<div class="coach-message">{coaching}</div>', unsafe_allow_html=True)
    
    # Chat interface
    st.markdown('<h3 style="color: #cbd5e1; font-weight: 700; font-size: 0.95rem; margin-bottom: 12px;">💬 Chat with Coach</h3>', unsafe_allow_html=True)
    
    chat_col1, chat_col2 = st.columns([1, 0.15], gap="small")
    
    with chat_col1:
        user_input = st.text_input(
            "",
            placeholder="Ask for motivation, tips, or help with your goals...",
            label_visibility="collapsed",
            key="chat_input"
        )
    
    with chat_col2:
        if st.button("→", key="send_btn", help="Send message"):
            if user_input.strip():
                response = get_ai_coaching(df, user_input)
                st.markdown(f'<div class="coach-message">🤖: {response}</div>', unsafe_allow_html=True)
                st.rerun()
    
    # Quick stats
    if not df.empty:
        recent = df.tail(7)
        gym_days = (recent["gym"] == "Yes").sum()
        avg_study = recent["study_hours"].mean()
        junk_days = (recent["junk_food"] == "Yes").sum()
        avg_spending = recent["spending"].mean()
        
        st.markdown('<div class="quick-stats">', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4, gap="small")
        with col1:
            st.markdown(f'''
            <div class="stat-mini">
                <div class="stat-mini-value">{gym_days}/7</div>
                <div class="stat-mini-label">💪 Gym</div>
            </div>
            ''', unsafe_allow_html=True)
        with col2:
            st.markdown(f'''
            <div class="stat-mini">
                <div class="stat-mini-value">{avg_study:.1f}h</div>
                <div class="stat-mini-label">📚 Study</div>
            </div>
            ''', unsafe_allow_html=True)
        with col3:
            st.markdown(f'''
            <div class="stat-mini">
                <div class="stat-mini-value">{junk_days}/7</div>
                <div class="stat-mini-label">🍕 Junk</div>
            </div>
            ''', unsafe_allow_html=True)
        with col4:
            st.markdown(f'''
            <div class="stat-mini">
                <div class="stat-mini-value">₹{avg_spending:.0f}</div>
                <div class="stat-mini-label">💰 Spend</div>
            </div>
            ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # ========== MAIN CONTENT GRID ==========
    col1, col2 = st.columns(2, gap="medium")
    
    # ========== LEFT: TODAY'S ENTRY ==========
    with col1:
        st.markdown('<div class="glass-card entry-card">', unsafe_allow_html=True)
        st.markdown('<h3 class="card-title">📝 Log Your Day</h3>', unsafe_allow_html=True)
        
        st.markdown('<div class="input-field-group">', unsafe_allow_html=True)
        st.markdown('<span class="input-label">💪 Gym Today?</span>', unsafe_allow_html=True)
        gym = st.radio("", ["Yes","No"], horizontal=True, label_visibility="collapsed", key="gym")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="input-field-group">', unsafe_allow_html=True)
        st.markdown('<span class="input-label">📚 Study Hours</span>', unsafe_allow_html=True)
        study = st.number_input("", min_value=0.0, max_value=24.0, step=0.5, value=0.0, label_visibility="collapsed", key="study")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="input-field-group">', unsafe_allow_html=True)
        st.markdown('<span class="input-label">🍕 Junk Food?</span>', unsafe_allow_html=True)
        junk = st.radio("", ["Yes","No"], horizontal=True, label_visibility="collapsed", key="junk")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="input-field-group">', unsafe_allow_html=True)
        st.markdown('<span class="input-label">💰 Spending (₹)</span>', unsafe_allow_html=True)
        spend = st.number_input("", min_value=0, max_value=10000, step=10, value=0, label_visibility="collapsed", key="spend")
        st.markdown('</div>', unsafe_allow_html=True)
        
        col_btn1, col_btn2 = st.columns([1, 1], gap="small")
        with col_btn1:
            if st.button("💾 Save Entry", use_container_width=True, key="save"):
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
                st.rerun()
        
        with col_btn2:
            if st.button("🗑️ Clear All", use_container_width=True, key="clear"):
                if st.session_state.get('confirm'):
                    df = pd.DataFrame(columns=["date","gym","study_hours","junk_food","spending"])
                    save_data(df)
                    st.success("✅ Data cleared!")
                    st.rerun()
                else:
                    st.session_state.confirm = True
                    st.warning("⚠️ Click again to confirm")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ========== RIGHT: STATS ==========
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h3 class="card-title">📊 Your Progress</h3>', unsafe_allow_html=True)
        
        if not df.empty:
            today_data = df[df['date'].dt.date == date.today()]
            if not today_data.empty:
                today = today_data.iloc[0]
                st.markdown('<h4 style="color: #cbd5e1; font-weight: 700; font-size: 0.9rem; margin-bottom: 12px;">Today</h4>', unsafe_allow_html=True)
                
                col_t1, col_t2 = st.columns(2, gap="small")
                with col_t1:
                    st.markdown(f'''
                    <div class="metric-box">
                        <div class="metric-label">Gym</div>
                        <div class="metric-value">{'✅' if today['gym'] == 'Yes' else '❌'}</div>
                    </div>
                    ''', unsafe_allow_html=True)
                    st.markdown(f'''
                    <div class="metric-box">
                        <div class="metric-label">Study</div>
                        <div class="metric-value">{today['study_hours']:.1f}h</div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                with col_t2:
                    st.markdown(f'''
                    <div class="metric-box">
                        <div class="metric-label">Junk</div>
                        <div class="metric-value">{'❌' if today['junk_food'] == 'Yes' else '✅'}</div>
                    </div>
                    ''', unsafe_allow_html=True)
                    spend_status = "🔴" if today['spending'] > DAILY_BUDGET else "🟢"
                    st.markdown(f'''
                    <div class="metric-box">
                        <div class="metric-label">Spend {spend_status}</div>
                        <div class="metric-value">₹{today['spending']}</div>
                    </div>
                    ''', unsafe_allow_html=True)
            
            # 7-day chart
            recent = df.tail(7)
            if len(recent) > 0:
                st.markdown('<h4 style="color: #cbd5e1; font-weight: 700; font-size: 0.9rem; margin-top: 20px; margin-bottom: 12px;">7 Days Trend</h4>', unsafe_allow_html=True)
                
                study_data = recent[['date', 'study_hours']].set_index('date')
                st.line_chart(study_data, use_container_width=True, color="#00d4ff")
        else:
            st.info("📝 Log your first day to see progress!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # ========== BOTTOM: FULL WIDTH CHARTS ==========
    if not df.empty and len(df) > 1:
        col_chart1, col_chart2 = st.columns(2, gap="medium")
        
        with col_chart1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<h3 class="card-title">📈 Study Progression</h3>', unsafe_allow_html=True)
            study_data = df[['date', 'study_hours']].set_index('date')
            st.line_chart(study_data, use_container_width=True, color="#00d4ff")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_chart2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<h3 class="card-title">💸 Spending Pattern</h3>', unsafe_allow_html=True)
            spend_data = df[['date', 'spending']].set_index('date')
            st.bar_chart(spend_data, use_container_width=True, color="#ec4899")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # ========== DATA TABLE ==========
    if not df.empty and len(df) > 1:
        st.divider()
        with st.expander("📊 View All Data"):
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

st.divider()
st.markdown("""
<div style='text-align: center; padding: 16px 0;'>
    <p style='color: #94a3b8; font-size: 0.95rem; margin: 0;'>
        🔥 Small daily wins = Extraordinary results | Track • Analyze • Grow ✨
    </p>
</div>
""", unsafe_allow_html=True)
