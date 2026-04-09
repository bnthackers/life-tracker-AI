import streamlit as st
import pandas as pd
from datetime import date
import os
import random
from groq import Groq

st.set_page_config(
    page_title="Life Tracker",
    layout="wide",import streamlit as st
import pandas as pd
from datetime import date
import os
import random
from groq import Groq

st.set_page_config(
    page_title="Life Tracker",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)

DAILY_BUDGET = 200

# INSANELY COOL CSS - MINIMALIST & CYBER
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=JetBrains+Mono:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* Dark cyber background */
    .main {
        background: linear-gradient(135deg, #0a0a0a 0%, #0f1419 50%, #0a0a0a 100%);
        color: #e0f7ff;
    }
    
    /* Content wrapper - NO PADDING */
    .wrapper {
        max-width: 1400px;
        margin: 0;
        padding: 0;
    }
    
    /* NO SPACE WASTING */
    .stContainer {
        padding: 0 !important;
    }
    
    .stColumn {
        padding: 0 !important;
    }
    
    /* Content area padding only */
    [data-testid="stAppViewContainer"] {
        padding: 0 !important;
    }
    
    /* Main content - tight spacing */
    .main-content {
        padding: 16px 20px;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* HEADER - Minimal spacing */
    .header {
        margin-bottom: 16px;
        text-align: center;
        padding: 12px 0;
    }
    
    .title {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00ffff 0%, #0099ff 50%, #6600ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        letter-spacing: -2px;
        font-family: 'Space Mono', monospace;
    }
    
    .subtitle {
        font-size: 0.8rem;
        color: #66ccff;
        margin-top: 4px;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    
    /* TOP SECTION - Compact */
    .top-section {
        display: grid;
        grid-template-columns: 1.5fr 1fr;
        gap: 12px;
        margin-bottom: 12px;
    }
    
    /* AI Chat Section */
    .ai-section {
        background: rgba(15, 30, 50, 0.6);
        border: 1px solid #0099ff;
        border-radius: 8px;
        padding: 12px;
        backdrop-filter: blur(10px);
    }
    
    .ai-section:hover {
        border-color: #00ffff;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.2);
    }
    
    .ai-header {
        font-size: 0.75rem;
        color: #00ffff;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
        font-weight: 700;
    }
    
    .ai-message {
        font-size: 0.85rem;
        line-height: 1.4;
        color: #e0f7ff;
        margin-bottom: 8px;
    }
    
    .chat-input {
        width: 100%;
        background: rgba(0, 0, 0, 0.8);
        border: 1px solid #0099ff;
        border-radius: 6px;
        padding: 10px 12px;
        color: #00ffff;
        font-size: 0.9rem;
        transition: all 0.3s;
    }
    
    .chat-input:focus {
        border-color: #00ffff;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
        outline: none;
    }
    
    /* Quick Stats Grid - Compact */
    .stats-section {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 8px;
    }
    
    .stat-mini {
        background: rgba(0, 99, 255, 0.1);
        border: 1px solid #0066ff;
        border-radius: 6px;
        padding: 10px;
        text-align: center;
        transition: all 0.3s;
    }
    
    .stat-mini:hover {
        background: rgba(0, 99, 255, 0.2);
        border-color: #00ffff;
        transform: translateY(-2px);
    }
    
    .stat-num {
        font-size: 1.4rem;
        font-weight: 700;
        color: #00ffff;
    }
    
    .stat-text {
        font-size: 0.65rem;
        color: #66ccff;
        text-transform: uppercase;
        margin-top: 2px;
    }
    
    /* MAIN GRID - Compact */
    .main-grid {
        display: grid;
        grid-template-columns: 0.9fr 1.1fr;
        gap: 12px;
        margin-bottom: 12px;
    }
    
    /* Panel - Minimal padding */
    .panel {
        background: rgba(10, 20, 40, 0.5);
        border: 1px solid #0099ff;
        border-radius: 8px;
        padding: 12px;
        backdrop-filter: blur(10px);
    }
    
    .panel:hover {
        border-color: #00ffff;
        background: rgba(10, 20, 40, 0.7);
    }
    
    .panel-title {
        font-size: 0.8rem;
        font-weight: 700;
        color: #00ffff;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 10px;
        padding-bottom: 6px;
        border-bottom: 1px solid #0099ff;
    }
    
    /* Form Group */
    .form-group {
        margin-bottom: 10px;
    }
    
    .input-label {
        font-size: 0.75rem;
        color: #66ccff;
        text-transform: uppercase;
        letter-spacing: 0.3px;
        margin-bottom: 4px;
        display: block;
    }
    
    .stRadio > label {
        color: #e0f7ff !important;
        font-size: 0.8rem !important;
        margin-right: 8px !important;
    }
    
    .stNumberInput input {
        background: rgba(0, 0, 0, 0.7) !important;
        border: 1px solid #0099ff !important;
        border-radius: 4px !important;
        padding: 6px 8px !important;
        color: #00ffff !important;
        font-size: 0.85rem !important;
        transition: all 0.3s !important;
    }
    
    .stNumberInput input:focus {
        border-color: #00ffff !important;
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.2) !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #0066ff 0%, #00ccff 100%);
        color: #000;
        border: 1px solid #00ffff;
        border-radius: 6px;
        padding: 8px 12px;
        font-weight: 700;
        font-size: 0.75rem;
        letter-spacing: 0.3px;
        width: 100%;
        transition: all 0.3s;
        text-transform: uppercase;
    }
    
    .stButton > button:hover {
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.4);
        transform: translateY(-2px);
    }
    
    /* Progress Cards */
    .progress-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 10px;
        margin-bottom: 16px;
    }
    
    .progress-item {
        background: rgba(0, 50, 100, 0.3);
        border: 1px solid #0066ff;
        border-radius: 10px;
        padding: 12px;
        text-align: center;
    }
    
    .progress-item:hover {
        background: rgba(0, 50, 100, 0.5);
        border-color: #00ffff;
    }
    
    .progress-icon {
        font-size: 1.6rem;
        margin-bottom: 4px;
    }
    
    .progress-val {
        font-size: 1.6rem;
        font-weight: 700;
        color: #00ffff;
    }
    
    .progress-label {
        font-size: 0.7rem;
        color: #66ccff;
        text-transform: uppercase;
    }
    
    /* Chart container */
    .chart-box {
        background: rgba(0, 30, 60, 0.3);
        border: 1px solid #0066ff;
        border-radius: 10px;
        padding: 12px;
    }
    
    .chart-title {
        font-size: 0.8rem;
        color: #66ccff;
        text-transform: uppercase;
        margin-bottom: 12px;
    }
    
    /* Bottom charts */
    .bottom-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
        margin-bottom: 30px;
    }
    
    /* Success msg */
    .success {
        background: rgba(0, 100, 50, 0.3);
        border: 1px solid #00ff66;
        border-radius: 8px;
        padding: 12px;
        color: #00ff99;
        font-size: 0.9rem;
        margin-bottom: 12px;
    }
    
    /* Minimal divider */
    hr {
        margin: 8px 0 !important;
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, #0099ff, transparent) !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        font-size: 0.75rem;
        color: #66ccff;
        margin-top: 12px;
        padding-top: 8px;
        border-top: 1px solid #0099ff;
    }
    
    /* Responsive */
    @media (max-width: 1024px) {
        .top-section, .main-grid, .bottom-grid {
            grid-template-columns: 1fr;
        }
    }
</style>
""", unsafe_allow_html=True)

# DATA
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

# GROQ
@st.cache_resource
def get_groq_client():
    api_key = st.secrets.get('GROQ_API_KEY') or os.getenv('GROQ_API_KEY')
    if not api_key:
        return None
    try:
        return Groq(api_key=api_key)
    except:
        return None

def get_ai_msg(df, user_msg=""):
    client = get_groq_client()
    
    msgs = [
        "⚡ You're crushing it! Keep the fire going! 💯",
        "🎯 Every day counts. Push harder today!",
        "💪 Small wins lead to BIG results. Go!",
        "🔥 You got this! Stay focused and grind!",
        "🚀 Ready to start? Log your first day!"
    ]
    
    if df.empty:
        return random.choice(msgs)
    
    if not client:
        return random.choice(msgs)
    
    try:
        recent = df.tail(7)
        gym = (recent["gym"] == "Yes").sum()
        study = recent["study_hours"].mean()
        junk = (recent["junk_food"] == "Yes").sum()
        
        if user_msg.strip():
            prompt = f"""User wants: {user_msg}
Give SHORT motivation (1 sentence). Be epic!"""
        else:
            prompt = f"""Stats: Gym {gym}/7, Study {study:.1f}h, Junk {junk}/7
Give SHORT power message (1 sentence). Keep it under 10 words!"""
        
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=30,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return random.choice(msgs)

df = load_data()

# LAYOUT
st.markdown('<div class="wrapper">', unsafe_allow_html=True)

# HEADER
st.markdown('''
<div class="header">
    <h1 class="title">LIFE TRACKER</h1>
    <p class="subtitle">>> Build Habits. Track Progress. Dominate</p>
</div>
''', unsafe_allow_html=True)

# TOP SECTION
st.markdown('<div class="top-section">', unsafe_allow_html=True)

# AI Chat
with st.container():
    st.markdown('<div class="ai-section">', unsafe_allow_html=True)
    st.markdown('<div class="ai-header">⚡ AI Coach</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="ai-message">{get_ai_msg(df)}</div>', unsafe_allow_html=True)
    
    col_chat, col_btn = st.columns([1, 0.15], gap="small")
    with col_chat:
        user_input = st.text_input("", placeholder="Ask for tips...", label_visibility="collapsed", key="chat")
    with col_btn:
        if st.button("→", key="send"):
            if user_input.strip():
                response = get_ai_msg(df, user_input)
                st.markdown(f'<div class="ai-message" style="margin-top: 12px; color: #00ff99;">🤖: {response}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Quick Stats
st.markdown('<div class="stats-section">', unsafe_allow_html=True)

if not df.empty:
    recent = df.tail(7)
    gym_val = (recent["gym"] == "Yes").sum()
    study_val = recent["study_hours"].mean()
    junk_val = (recent["junk_food"] == "Yes").sum()
    spend_val = recent["spending"].mean()
    
    st.markdown(f'''
    <div class="stat-mini">
        <div class="stat-num">{gym_val}/7</div>
        <div class="stat-text">💪 Gym</div>
    </div>
    <div class="stat-mini">
        <div class="stat-num">{study_val:.1f}h</div>
        <div class="stat-text">📚 Study</div>
    </div>
    <div class="stat-mini">
        <div class="stat-num">{junk_val}</div>
        <div class="stat-text">🍕 Junk</div>
    </div>
    <div class="stat-mini">
        <div class="stat-num">₹{spend_val:.0f}</div>
        <div class="stat-text">💰 Spend</div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# MAIN GRID
st.markdown('<div class="main-grid">', unsafe_allow_html=True)

# LEFT - Form
with st.container():
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Log Entry</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="form-group">', unsafe_allow_html=True)
    st.markdown('<span class="input-label">💪 Gym?</span>', unsafe_allow_html=True)
    gym = st.radio("", ["Yes", "No"], horizontal=True, label_visibility="collapsed", key="gym")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="form-group">', unsafe_allow_html=True)
    st.markdown('<span class="input-label">📚 Study Hours</span>', unsafe_allow_html=True)
    study = st.number_input("", min_value=0.0, max_value=24.0, step=0.5, value=0.0, label_visibility="collapsed", key="study")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="form-group">', unsafe_allow_html=True)
    st.markdown('<span class="input-label">🍕 Junk Food?</span>', unsafe_allow_html=True)
    junk = st.radio("", ["Yes", "No"], horizontal=True, label_visibility="collapsed", key="junk")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="form-group">', unsafe_allow_html=True)
    st.markdown('<span class="input-label">💰 Spending</span>', unsafe_allow_html=True)
    spend = st.number_input("", min_value=0, max_value=10000, step=10, value=0, label_visibility="collapsed", key="spend")
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="small")
    with col1:
        if st.button("💾 SAVE", key="save"):
            today = date.today()
            existing = df[df['date'].dt.date == today] if not df.empty else pd.DataFrame()
            if not existing.empty:
                df.loc[df['date'].dt.date == today, ['gym', 'study_hours', 'junk_food', 'spending']] = [gym, study, junk, spend]
            else:
                new_entry = pd.DataFrame({"date": [today], "gym": [gym], "study_hours": [study], "junk_food": [junk], "spending": [spend]})
                df = pd.concat([df, new_entry], ignore_index=True)
            save_data(df)
            st.success("✓ SAVED")
            st.balloons()
            st.rerun()
    
    with col2:
        if st.button("🔄 CLEAR", key="clear"):
            if st.session_state.get('confirm'):
                df = pd.DataFrame(columns=["date","gym","study_hours","junk_food","spending"])
                save_data(df)
                st.success("Cleared!")
                st.rerun()
            else:
                st.session_state.confirm = True
                st.warning("Click again")
    
    st.markdown('</div>', unsafe_allow_html=True)

# RIGHT - Progress
with st.container():
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Progress</div>', unsafe_allow_html=True)
    
    if not df.empty:
        today_data = df[df['date'].dt.date == date.today()]
        
        if not today_data.empty:
            today = today_data.iloc[0]
            st.markdown('<div class="progress-grid">', unsafe_allow_html=True)
            
            st.markdown(f'''
            <div class="progress-item">
                <div class="progress-icon">💪</div>
                <div class="progress-val">{'✓' if today['gym'] == 'Yes' else '✗'}</div>
                <div class="progress-label">Gym</div>
            </div>
            <div class="progress-item">
                <div class="progress-icon">📚</div>
                <div class="progress-val">{today['study_hours']:.1f}</div>
                <div class="progress-label">Hours</div>
            </div>
            <div class="progress-item">
                <div class="progress-icon">🍕</div>
                <div class="progress-val">{'✗' if today['junk_food'] == 'Yes' else '✓'}</div>
                <div class="progress-label">Junk</div>
            </div>
            <div class="progress-item">
                <div class="progress-icon">💰</div>
                <div class="progress-val">₹{today['spending']}</div>
                <div class="progress-label">Spend</div>
            </div>
            ''', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        recent = df.tail(7)
        if len(recent) > 0:
            st.markdown('<div class="chart-box">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">7-Day Trend</div>', unsafe_allow_html=True)
            study_data = recent[['date', 'study_hours']].set_index('date')
            st.line_chart(study_data, use_container_width=True, color="#00ffff")
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("📊 Log your first entry!")
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# BOTTOM CHARTS
if not df.empty and len(df) > 1:
    st.markdown('<div class="bottom-grid">', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Study Chart</div>', unsafe_allow_html=True)
        study_full = df[['date', 'study_hours']].set_index('date')
        st.line_chart(study_full, use_container_width=True, color="#00ffff")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Spending Chart</div>', unsafe_allow_html=True)
        spend_full = df[['date', 'spending']].set_index('date')
        st.bar_chart(spend_full, use_container_width=True, color="#0099ff")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# DATA TABLE
if not df.empty:
    with st.expander("📊 View Data", expanded=False):
        display_df = df.copy()
        display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d')
        display_df = display_df.sort_values('date', ascending=False)
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        csv = display_df.to_csv(index=False)
        st.download_button("📥 Download", csv, "data.csv", "text/csv", use_container_width=True)

st.markdown('''
<div class="footer">
>> Stay Focused. Keep Grinding. Dominate 2024 🚀
</div>
''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
    initial_sidebar_state="collapsed",
    menu_items=None
)

DAILY_BUDGET = 200

# INSANELY COOL CSS - MINIMALIST & CYBER
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=JetBrains+Mono:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* Dark cyber background */
    .main {
        background: linear-gradient(135deg, #0a0a0a 0%, #0f1419 50%, #0a0a0a 100%);
        color: #e0f7ff;
    }
    
    /* Content wrapper */
    .wrapper {
        max-width: 1400px;
        margin: 0 auto;
        padding: 20px;
    }
    
    /* HEADER - Minimal & Striking */
    .header {
        margin-bottom: 40px;
        text-align: center;
    }
    
    .title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00ffff 0%, #0099ff 50%, #6600ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        letter-spacing: -2px;
        font-family: 'Space Mono', monospace;
    }
    
    .subtitle {
        font-size: 0.9rem;
        color: #66ccff;
        margin-top: 8px;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    
    /* TOP SECTION - AI + STATS IN ONE ROW */
    .top-section {
        display: grid;
        grid-template-columns: 1.5fr 1fr;
        gap: 20px;
        margin-bottom: 30px;
    }
    
    /* AI Chat Section */
    .ai-section {
        background: rgba(15, 30, 50, 0.6);
        border: 1px solid #0099ff;
        border-radius: 12px;
        padding: 20px;
        backdrop-filter: blur(10px);
    }
    
    .ai-section:hover {
        border-color: #00ffff;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.2);
    }
    
    .ai-header {
        font-size: 0.9rem;
        color: #00ffff;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 12px;
        font-weight: 700;
    }
    
    .ai-message {
        font-size: 0.95rem;
        line-height: 1.6;
        color: #e0f7ff;
        margin-bottom: 12px;
    }
    
    .chat-input {
        width: 100%;
        background: rgba(0, 0, 0, 0.8);
        border: 1px solid #0099ff;
        border-radius: 6px;
        padding: 10px 12px;
        color: #00ffff;
        font-size: 0.9rem;
        transition: all 0.3s;
    }
    
    .chat-input:focus {
        border-color: #00ffff;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
        outline: none;
    }
    
    /* Quick Stats Grid */
    .stats-section {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 12px;
    }
    
    .stat-mini {
        background: rgba(0, 99, 255, 0.1);
        border: 1px solid #0066ff;
        border-radius: 10px;
        padding: 14px;
        text-align: center;
        transition: all 0.3s;
    }
    
    .stat-mini:hover {
        background: rgba(0, 99, 255, 0.2);
        border-color: #00ffff;
        transform: translateY(-2px);
    }
    
    .stat-num {
        font-size: 1.8rem;
        font-weight: 700;
        color: #00ffff;
    }
    
    .stat-text {
        font-size: 0.75rem;
        color: #66ccff;
        text-transform: uppercase;
        margin-top: 4px;
    }
    
    /* MAIN GRID */
    .main-grid {
        display: grid;
        grid-template-columns: 0.9fr 1.1fr;
        gap: 20px;
        margin-bottom: 30px;
    }
    
    /* Panel */
    .panel {
        background: rgba(10, 20, 40, 0.5);
        border: 1px solid #0099ff;
        border-radius: 12px;
        padding: 20px;
        backdrop-filter: blur(10px);
    }
    
    .panel:hover {
        border-color: #00ffff;
        background: rgba(10, 20, 40, 0.7);
    }
    
    .panel-title {
        font-size: 1rem;
        font-weight: 700;
        color: #00ffff;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 16px;
        padding-bottom: 12px;
        border-bottom: 1px solid #0099ff;
    }
    
    /* Form Group */
    .form-group {
        margin-bottom: 14px;
    }
    
    .input-label {
        font-size: 0.8rem;
        color: #66ccff;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
        display: block;
    }
    
    .stRadio > label {
        color: #e0f7ff !important;
        font-size: 0.9rem !important;
        margin-right: 12px !important;
    }
    
    .stNumberInput input {
        background: rgba(0, 0, 0, 0.7) !important;
        border: 1px solid #0099ff !important;
        border-radius: 6px !important;
        padding: 8px 10px !important;
        color: #00ffff !important;
        font-size: 0.9rem !important;
        transition: all 0.3s !important;
    }
    
    .stNumberInput input:focus {
        border-color: #00ffff !important;
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.2) !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #0066ff 0%, #00ccff 100%);
        color: #000;
        border: 1px solid #00ffff;
        border-radius: 8px;
        padding: 10px 16px;
        font-weight: 700;
        font-size: 0.85rem;
        letter-spacing: 0.5px;
        width: 100%;
        transition: all 0.3s;
        text-transform: uppercase;
    }
    
    .stButton > button:hover {
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.4);
        transform: translateY(-2px);
    }
    
    /* Progress Cards */
    .progress-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 10px;
        margin-bottom: 16px;
    }
    
    .progress-item {
        background: rgba(0, 50, 100, 0.3);
        border: 1px solid #0066ff;
        border-radius: 10px;
        padding: 12px;
        text-align: center;
    }
    
    .progress-item:hover {
        background: rgba(0, 50, 100, 0.5);
        border-color: #00ffff;
    }
    
    .progress-icon {
        font-size: 1.6rem;
        margin-bottom: 4px;
    }
    
    .progress-val {
        font-size: 1.6rem;
        font-weight: 700;
        color: #00ffff;
    }
    
    .progress-label {
        font-size: 0.7rem;
        color: #66ccff;
        text-transform: uppercase;
    }
    
    /* Chart container */
    .chart-box {
        background: rgba(0, 30, 60, 0.3);
        border: 1px solid #0066ff;
        border-radius: 10px;
        padding: 12px;
    }
    
    .chart-title {
        font-size: 0.8rem;
        color: #66ccff;
        text-transform: uppercase;
        margin-bottom: 12px;
    }
    
    /* Bottom charts */
    .bottom-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
        margin-bottom: 30px;
    }
    
    /* Success msg */
    .success {
        background: rgba(0, 100, 50, 0.3);
        border: 1px solid #00ff66;
        border-radius: 8px;
        padding: 12px;
        color: #00ff99;
        font-size: 0.9rem;
        margin-bottom: 12px;
    }
    
    /* Minimal divider */
    hr {
        margin: 24px 0 !important;
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, #0099ff, transparent) !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        font-size: 0.85rem;
        color: #66ccff;
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid #0099ff;
    }
    
    /* Responsive */
    @media (max-width: 1024px) {
        .top-section, .main-grid, .bottom-grid {
            grid-template-columns: 1fr;
        }
    }
</style>
""", unsafe_allow_html=True)

# DATA
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

# GROQ
@st.cache_resource
def get_groq_client():
    api_key = st.secrets.get('GROQ_API_KEY') or os.getenv('GROQ_API_KEY')
    if not api_key:
        return None
    try:
        return Groq(api_key=api_key)
    except:
        return None

def get_ai_msg(df, user_msg=""):
    client = get_groq_client()
    
    if df.empty:
        return "🚀 Ready to start? Log your first day and let's build momentum!"
    
    if not client:
        msgs = [
            "⚡ You're crushing it! Keep the fire going! 💯",
            "🎯 Every day counts. Push harder today!",
            "💪 Small wins lead to BIG results. Go!",
            "🔥 You got this! Stay focused and grind!"
        ]
        return random.choice(msgs)
    
    try:
        recent = df.tail(7)
        gym = (recent["gym"] == "Yes").sum()
        study = recent["study_hours"].mean()
        junk = (recent["junk_food"] == "Yes").sum()
        
        msg = user_msg if user_msg else f"Gym: {gym}/7, Study: {study:.1f}h, Junk: {junk}/7"
        
        prompt = f"""Short power message! User: {msg}
Stats: Gym {gym}/7, Study {study:.1f}h, Junk {junk}/7
Keep it under 15 words. Be epic! 🚀"""
        
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50,
            temperature=0.9
        )
        return response.choices[0].message.content
    except:
        return "💯 Keep pushing! You're getting stronger every day!"

df = load_data()

# LAYOUT
st.markdown('<div class="wrapper">', unsafe_allow_html=True)

# HEADER
st.markdown('''
<div class="header">
    <h1 class="title">LIFE TRACKER</h1>
    <p class="subtitle">>> Build Habits. Track Progress. Dominate</p>
</div>
''', unsafe_allow_html=True)

# TOP SECTION
st.markdown('<div class="top-section">', unsafe_allow_html=True)

# AI Chat
with st.container():
    st.markdown('<div class="ai-section">', unsafe_allow_html=True)
    st.markdown('<div class="ai-header">⚡ AI Coach</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="ai-message">{get_ai_msg(df)}</div>', unsafe_allow_html=True)
    
    col_chat, col_btn = st.columns([1, 0.15], gap="small")
    with col_chat:
        user_input = st.text_input("", placeholder="Ask for tips...", label_visibility="collapsed", key="chat")
    with col_btn:
        if st.button("→", key="send"):
            if user_input.strip():
                response = get_ai_msg(df, user_input)
                st.markdown(f'<div class="ai-message" style="margin-top: 12px; color: #00ff99;">🤖: {response}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Quick Stats
st.markdown('<div class="stats-section">', unsafe_allow_html=True)

if not df.empty:
    recent = df.tail(7)
    gym_val = (recent["gym"] == "Yes").sum()
    study_val = recent["study_hours"].mean()
    junk_val = (recent["junk_food"] == "Yes").sum()
    spend_val = recent["spending"].mean()
    
    st.markdown(f'''
    <div class="stat-mini">
        <div class="stat-num">{gym_val}/7</div>
        <div class="stat-text">💪 Gym</div>
    </div>
    <div class="stat-mini">
        <div class="stat-num">{study_val:.1f}h</div>
        <div class="stat-text">📚 Study</div>
    </div>
    <div class="stat-mini">
        <div class="stat-num">{junk_val}</div>
        <div class="stat-text">🍕 Junk</div>
    </div>
    <div class="stat-mini">
        <div class="stat-num">₹{spend_val:.0f}</div>
        <div class="stat-text">💰 Spend</div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# MAIN GRID
st.markdown('<div class="main-grid">', unsafe_allow_html=True)

# LEFT - Form
with st.container():
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Log Entry</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="form-group">', unsafe_allow_html=True)
    st.markdown('<span class="input-label">💪 Gym?</span>', unsafe_allow_html=True)
    gym = st.radio("", ["Yes", "No"], horizontal=True, label_visibility="collapsed", key="gym")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="form-group">', unsafe_allow_html=True)
    st.markdown('<span class="input-label">📚 Study Hours</span>', unsafe_allow_html=True)
    study = st.number_input("", min_value=0.0, max_value=24.0, step=0.5, value=0.0, label_visibility="collapsed", key="study")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="form-group">', unsafe_allow_html=True)
    st.markdown('<span class="input-label">🍕 Junk Food?</span>', unsafe_allow_html=True)
    junk = st.radio("", ["Yes", "No"], horizontal=True, label_visibility="collapsed", key="junk")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="form-group">', unsafe_allow_html=True)
    st.markdown('<span class="input-label">💰 Spending</span>', unsafe_allow_html=True)
    spend = st.number_input("", min_value=0, max_value=10000, step=10, value=0, label_visibility="collapsed", key="spend")
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="small")
    with col1:
        if st.button("💾 SAVE", key="save"):
            today = date.today()
            existing = df[df['date'].dt.date == today] if not df.empty else pd.DataFrame()
            if not existing.empty:
                df.loc[df['date'].dt.date == today, ['gym', 'study_hours', 'junk_food', 'spending']] = [gym, study, junk, spend]
            else:
                new_entry = pd.DataFrame({"date": [today], "gym": [gym], "study_hours": [study], "junk_food": [junk], "spending": [spend]})
                df = pd.concat([df, new_entry], ignore_index=True)
            save_data(df)
            st.success("✓ SAVED")
            st.balloons()
            st.rerun()
    
    with col2:
        if st.button("🔄 CLEAR", key="clear"):
            if st.session_state.get('confirm'):
                df = pd.DataFrame(columns=["date","gym","study_hours","junk_food","spending"])
                save_data(df)
                st.success("Cleared!")
                st.rerun()
            else:
                st.session_state.confirm = True
                st.warning("Click again")
    
    st.markdown('</div>', unsafe_allow_html=True)

# RIGHT - Progress
with st.container():
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Progress</div>', unsafe_allow_html=True)
    
    if not df.empty:
        today_data = df[df['date'].dt.date == date.today()]
        
        if not today_data.empty:
            today = today_data.iloc[0]
            st.markdown('<div class="progress-grid">', unsafe_allow_html=True)
            
            st.markdown(f'''
            <div class="progress-item">
                <div class="progress-icon">💪</div>
                <div class="progress-val">{'✓' if today['gym'] == 'Yes' else '✗'}</div>
                <div class="progress-label">Gym</div>
            </div>
            <div class="progress-item">
                <div class="progress-icon">📚</div>
                <div class="progress-val">{today['study_hours']:.1f}</div>
                <div class="progress-label">Hours</div>
            </div>
            <div class="progress-item">
                <div class="progress-icon">🍕</div>
                <div class="progress-val">{'✗' if today['junk_food'] == 'Yes' else '✓'}</div>
                <div class="progress-label">Junk</div>
            </div>
            <div class="progress-item">
                <div class="progress-icon">💰</div>
                <div class="progress-val">₹{today['spending']}</div>
                <div class="progress-label">Spend</div>
            </div>
            ''', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        recent = df.tail(7)
        if len(recent) > 0:
            st.markdown('<div class="chart-box">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">7-Day Trend</div>', unsafe_allow_html=True)
            study_data = recent[['date', 'study_hours']].set_index('date')
            st.line_chart(study_data, use_container_width=True, color="#00ffff")
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("📊 Log your first entry!")
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# BOTTOM CHARTS
if not df.empty and len(df) > 1:
    st.markdown('<div class="bottom-grid">', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Study Chart</div>', unsafe_allow_html=True)
        study_full = df[['date', 'study_hours']].set_index('date')
        st.line_chart(study_full, use_container_width=True, color="#00ffff")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Spending Chart</div>', unsafe_allow_html=True)
        spend_full = df[['date', 'spending']].set_index('date')
        st.bar_chart(spend_full, use_container_width=True, color="#0099ff")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# DATA TABLE
if not df.empty:
    with st.expander("📊 View Data", expanded=False):
        display_df = df.copy()
        display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d')
        display_df = display_df.sort_values('date', ascending=False)
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        csv = display_df.to_csv(index=False)
        st.download_button("📥 Download", csv, "data.csv", "text/csv", use_container_width=True)

st.markdown('''
<div class="footer">
>> Stay Focused. Keep Grinding. Dominate 2024 🚀
</div>
''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
