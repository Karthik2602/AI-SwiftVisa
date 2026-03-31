import streamlit as st
import json
from visa_agent import screen_visa_eligibility
from chatbot_backend import visa_chatbot_response

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="SwiftVisa AI",
    page_icon="✈️",
    layout="wide"
)

# -------------------------------------------------
# CSS — Modern SaaS Dark Theme
# -------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

/* ─── GLOBAL RESET ─────────────────────────────── */
html, body, [data-testid="stAppViewContainer"] {
    background: #060b18 !important;
    font-family: 'Inter', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 0%, #0d1f4a 0%, #060b18 50%, #0a0d1a 100%) !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

.block-container {
    padding-top: 3rem;
    padding-left: 4rem;
    padding-right: 4rem;
    max-width: 1200px;
    margin: 0 auto;
}

/* ─── TYPOGRAPHY ────────────────────────────────── */
h1, h2, h3 {
    font-family: 'Sora', sans-serif !important;
    color: #f0f4ff !important;
    letter-spacing: -0.02em;
}

p, li, div, span, label {
    color: #94a3b8 !important;
}

/* ─── HERO SECTION ──────────────────────────────── */
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(99, 102, 241, 0.15);
    border: 1px solid rgba(99, 102, 241, 0.35);
    border-radius: 999px;
    padding: 5px 14px;
    font-size: 12px;
    font-family: 'Sora', sans-serif;
    font-weight: 500;
    color: #a5b4fc !important;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 20px;
}

.hero-title {
    font-family: 'Sora', sans-serif !important;
    font-size: 52px !important;
    font-weight: 700 !important;
    line-height: 1.15 !important;
    letter-spacing: -0.03em !important;
    background: linear-gradient(135deg, #e0e7ff 0%, #a5b4fc 50%, #818cf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 16px !important;
}

.hero-desc {
    font-size: 17px !important;
    line-height: 1.75 !important;
    color: #64748b !important;
    max-width: 560px;
    margin-bottom: 40px !important;
}

/* ─── FEATURE LIST ──────────────────────────────── */
.features-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px 32px;
    margin-bottom: 48px;
    max-width: 640px;
}

.feature-item {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 4px 0;
}

.feature-dot {
    width: 22px;
    height: 22px;
    min-width: 22px;
    border-radius: 50%;
    background: linear-gradient(135deg, #6366f1, #818cf8);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: 1px;
}

.feature-dot svg {
    width: 12px;
    height: 12px;
}

.feature-text {
    font-size: 14px !important;
    color: #cbd5e1 !important;
    line-height: 1.5;
}

/* ─── MODE CARDS ────────────────────────────────── */
.cards-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-top: 8px;
}

.mode-card {
    background: linear-gradient(145deg, rgba(15,23,42,0.9), rgba(20,30,55,0.7));
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 20px;
    padding: 32px 28px;
    position: relative;
    overflow: hidden;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    height: 100%;
}

.mode-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, #6366f1, #818cf8, #a5b4fc);
    opacity: 0;
    transition: opacity 0.3s;
}

.mode-card:hover {
    border-color: rgba(99, 102, 241, 0.5);
    transform: translateY(-4px);
    box-shadow: 0 20px 60px rgba(99, 102, 241, 0.15);
}

.mode-card:hover::before {
    opacity: 1;
}

.card-icon {
    width: 48px;
    height: 48px;
    border-radius: 14px;
    background: linear-gradient(135deg, rgba(99,102,241,0.25), rgba(129,140,248,0.1));
    border: 1px solid rgba(99,102,241,0.3);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    margin-bottom: 18px;
}

.card-title {
    font-family: 'Sora', sans-serif !important;
    font-size: 18px !important;
    font-weight: 600 !important;
    color: #e2e8f0 !important;
    margin-bottom: 10px !important;
}

.card-desc {
    font-size: 13.5px !important;
    color: #64748b !important;
    line-height: 1.7;
    margin-bottom: 22px !important;
}

.card-tag {
    display: inline-block;
    background: rgba(99, 102, 241, 0.12);
    border: 1px solid rgba(99, 102, 241, 0.25);
    border-radius: 6px;
    padding: 3px 9px;
    font-size: 11px;
    color: #a5b4fc !important;
    margin: 3px 3px 3px 0;
    font-weight: 500;
    letter-spacing: 0.02em;
}

/* ─── DIVIDER ───────────────────────────────────── */
.section-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99,102,241,0.3), transparent);
    margin: 40px 0;
}

/* ─── BUTTONS ───────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, #4f46e5, #6366f1) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 24px !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    letter-spacing: 0.02em !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
    cursor: pointer !important;
    width: 100%;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #4338ca, #4f46e5) !important;
    box-shadow: 0 6px 25px rgba(99, 102, 241, 0.45) !important;
    transform: translateY(-1px) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* ─── BACK BUTTON ───────────────────────────────── */
[data-testid="stButton"]:first-child > button {
    background: rgba(30, 41, 59, 0.6) !important;
    border: 1px solid rgba(99,102,241,0.25) !important;
    color: #94a3b8 !important;
    box-shadow: none !important;
    width: auto !important;
    padding: 7px 18px !important;
}

[data-testid="stButton"]:first-child > button:hover {
    background: rgba(30, 41, 59, 0.9) !important;
    border-color: rgba(99,102,241,0.5) !important;
    color: #e2e8f0 !important;
    transform: none !important;
    box-shadow: none !important;
}

/* ─── INPUTS ────────────────────────────────────── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div > div {
    background: rgba(15, 23, 42, 0.8) !important;
    border: 1px solid rgba(99, 102, 241, 0.25) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
    transition: border-color 0.2s;
}

.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: rgba(99, 102, 241, 0.6) !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
}

.stSelectbox > div > div > div:hover {
    border-color: rgba(99, 102, 241, 0.5) !important;
}

/* ─── PROGRESS BAR ──────────────────────────────── */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #4f46e5, #818cf8) !important;
    border-radius: 999px !important;
}

.stProgress > div > div {
    background: rgba(30, 41, 59, 0.5) !important;
    border-radius: 999px !important;
}

/* ─── CHAT AREA ─────────────────────────────────── */
.chat-wrapper {
    background: rgba(8, 14, 30, 0.6);
    border: 1px solid rgba(99, 102, 241, 0.15);
    border-radius: 20px;
    padding: 28px 24px;
    max-height: 520px;
    overflow-y: auto;
    margin-bottom: 24px;
    scrollbar-width: thin;
    scrollbar-color: rgba(99,102,241,0.3) transparent;
}

.chat-wrapper::-webkit-scrollbar {
    width: 5px;
}
.chat-wrapper::-webkit-scrollbar-track {
    background: transparent;
}
.chat-wrapper::-webkit-scrollbar-thumb {
    background: rgba(99,102,241,0.3);
    border-radius: 999px;
}

.chat-row-user {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 16px;
}

.chat-row-bot {
    display: flex;
    justify-content: flex-start;
    margin-bottom: 16px;
    align-items: flex-start;
    gap: 10px;
}

.chat-avatar {
    width: 32px;
    height: 32px;
    min-width: 32px;
    border-radius: 50%;
    background: linear-gradient(135deg, #4f46e5, #818cf8);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    margin-top: 2px;
}

.chat-bubble-user {
    background: linear-gradient(135deg, #4f46e5, #6366f1);
    color: #fff !important;
    padding: 12px 18px;
    border-radius: 18px 18px 4px 18px;
    max-width: 68%;
    font-size: 14px !important;
    line-height: 1.65 !important;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.25);
    word-wrap: break-word;
}

.chat-bubble-bot {
    background: rgba(20, 30, 55, 0.85);
    border: 1px solid rgba(99, 102, 241, 0.18);
    color: #cbd5e1 !important;
    padding: 12px 18px;
    border-radius: 18px 18px 18px 4px;
    max-width: 68%;
    font-size: 14px !important;
    line-height: 1.65 !important;
    word-wrap: break-word;
}

.chat-empty {
    text-align: center;
    padding: 60px 20px;
    color: #334155 !important;
    font-size: 14px !important;
}

.chat-empty-icon {
    font-size: 40px;
    display: block;
    margin-bottom: 12px;
    opacity: 0.5;
}

/* ─── STEP HEADER ───────────────────────────────── */
.step-header {
    background: rgba(15, 23, 42, 0.5);
    border: 1px solid rgba(99, 102, 241, 0.15);
    border-radius: 14px;
    padding: 16px 22px;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    gap: 14px;
}

.step-number {
    width: 36px;
    height: 36px;
    min-width: 36px;
    border-radius: 50%;
    background: linear-gradient(135deg, #4f46e5, #818cf8);
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Sora', sans-serif;
    font-weight: 700;
    font-size: 15px;
    color: #fff !important;
}

.step-label {
    font-family: 'Sora', sans-serif !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    color: #e2e8f0 !important;
}

/* ─── RESULT CARD ───────────────────────────────── */
.result-card {
    background: linear-gradient(145deg, rgba(16,24,44,0.9), rgba(20,30,56,0.7));
    border: 1px solid rgba(99, 102, 241, 0.25);
    border-radius: 20px;
    padding: 32px;
    margin-bottom: 20px;
}

.result-title {
    font-family: 'Sora', sans-serif !important;
    font-size: 22px !important;
    font-weight: 700 !important;
    color: #e2e8f0 !important;
    margin-bottom: 8px !important;
}

/* ─── ALERTS ────────────────────────────────────── */
.stAlert {
    border-radius: 12px !important;
    border: none !important;
    background: rgba(245, 158, 11, 0.08) !important;
}

/* ─── SUCCESS BOX (dark green override) ─────────── */
[data-testid="stAlert"][data-baseweb="notification"] {
    background: rgba(6, 78, 59, 0.55) !important;
    border: 1px solid rgba(16, 185, 129, 0.35) !important;
    border-radius: 14px !important;
}

[data-testid="stAlert"][data-baseweb="notification"] p,
[data-testid="stAlert"][data-baseweb="notification"] div,
[data-testid="stAlert"][data-baseweb="notification"] span {
    color: #6ee7b7 !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    line-height: 1.7 !important;
}

/* ─── WARNING BOX ─────────────────────────────── */
div[data-testid="stAlert"] {
    border-radius: 12px !important;
}

/* ─── AI DISCLAIMER ─────────────────────────────── */
.ai-disclaimer {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(99, 102, 241, 0.07);
    border: 1px solid rgba(99, 102, 241, 0.18);
    border-radius: 8px;
    padding: 5px 12px;
    font-size: 11.5px;
    color: #6366f1 !important;
    font-style: italic;
    letter-spacing: 0.01em;
}

/* ─── CONFIDENCE BAR CUSTOM ─────────────────────── */
.conf-bar-wrap {
    background: rgba(30,41,59,0.5);
    border-radius: 999px;
    height: 10px;
    width: 100%;
    overflow: hidden;
    margin: 10px 0 6px;
}

.conf-bar-fill {
    height: 100%;
    border-radius: 999px;
    transition: width 0.6s ease;
}

/* ─── MISSING DOCS CARD ──────────────────────────── */
.missing-doc-item {
    display: flex;
    align-items: center;
    gap: 10px;
    background: rgba(239, 68, 68, 0.07);
    border: 1px solid rgba(239, 68, 68, 0.2);
    border-radius: 10px;
    padding: 10px 14px;
    margin-bottom: 8px;
}

.missing-doc-label {
    font-size: 13.5px !important;
    color: #fca5a5 !important;
    font-weight: 500;
}

/* ─── RISK METER ─────────────────────────────────── */
.risk-card {
    background: rgba(15,23,42,0.6);
    border: 1px solid rgba(99,102,241,0.18);
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 16px;
}

.risk-label {
    font-family: 'Sora', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #64748b !important;
    margin-bottom: 10px !important;
}

.risk-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 8px;
}

.risk-factor {
    font-size: 13px !important;
    color: #94a3b8 !important;
}

.risk-badge {
    font-size: 11px;
    font-weight: 600;
    padding: 2px 10px;
    border-radius: 999px;
    letter-spacing: 0.04em;
}

.risk-ok   { background: rgba(16,185,129,0.15); color: #6ee7b7 !important; border: 1px solid rgba(16,185,129,0.3); }
.risk-warn { background: rgba(245,158,11,0.15);  color: #fcd34d !important; border: 1px solid rgba(245,158,11,0.3); }
.risk-bad  { background: rgba(239,68,68,0.15);   color: #fca5a5 !important; border: 1px solid rgba(239,68,68,0.3); }

/* ─── NEXT STEPS ─────────────────────────────────── */
.next-step-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px 0;
    border-bottom: 1px solid rgba(99,102,241,0.1);
}

.next-step-num {
    width: 26px;
    height: 26px;
    min-width: 26px;
    border-radius: 50%;
    background: linear-gradient(135deg, #4f46e5, #818cf8);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 700;
    color: #fff !important;
    font-family: 'Sora', sans-serif;
}

.next-step-text {
    font-size: 13.5px !important;
    color: #94a3b8 !important;
    line-height: 1.6;
    padding-top: 3px;
}

/* ─── SIDEBAR HIDE ──────────────────────────────── */
[data-testid="stSidebar"] { display: none; }

/* ─── DIVIDER ───────────────────────────────────── */
hr {
    border-color: rgba(99, 102, 241, 0.15) !important;
    margin: 32px 0 !important;
}

/* ─── STEP NAV BACK BUTTON ─────────────────────────── */
/* Back buttons sit in col_nav1 — style them ghost */
div[data-testid="column"]:first-child .stButton > button {
    background: rgba(30, 41, 59, 0.5) !important;
    border: 1px solid rgba(99, 102, 241, 0.2) !important;
    color: #94a3b8 !important;
    box-shadow: none !important;
    font-size: 13px !important;
}

div[data-testid="column"]:first-child .stButton > button:hover {
    background: rgba(30, 41, 59, 0.9) !important;
    border-color: rgba(99, 102, 241, 0.45) !important;
    color: #e2e8f0 !important;
    transform: none !important;
    box-shadow: none !important;
}

/* ─── LABEL FONT ─────────────────────────────────── */
.stTextInput label, .stNumberInput label, .stSelectbox label {
    font-family: 'Sora', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #94a3b8 !important;
    letter-spacing: 0.03em !important;
    text-transform: uppercase !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# SESSION STATE  +  REFRESH PERSISTENCE
# -------------------------------------------------
_qp = st.query_params

if "mode" not in st.session_state:
    st.session_state.mode = _qp.get("mode", None)

if "step" not in st.session_state:
    try:
        st.session_state.step = int(_qp.get("step", 1))
    except (ValueError, TypeError):
        st.session_state.step = 1

if "personal" not in st.session_state:
    st.session_state.personal = {}
if "travel" not in st.session_state:
    st.session_state.travel = {}
if "financial" not in st.session_state:
    st.session_state.financial = {}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def _sync_params():
    if st.session_state.mode:
        st.query_params["mode"] = st.session_state.mode
        st.query_params["step"] = str(st.session_state.step)
    else:
        st.query_params.clear()

_sync_params()

# -------------------------------------------------
# HOME PAGE
# -------------------------------------------------
if st.session_state.mode is None:

    # Badge
    st.markdown('<div class="hero-badge">✦ AI-Powered Visa Intelligence</div>', unsafe_allow_html=True)

    # Title
    st.markdown('<h1 class="hero-title">SwiftVisa AI</h1>', unsafe_allow_html=True)

    # Description
    st.markdown("""
    <p class="hero-desc">
        Your intelligent visa companion — analyze eligibility, decode policies, and
        prepare the right documents with AI-driven precision. No guesswork, just clarity.
    </p>
    """, unsafe_allow_html=True)

    # Features
    features = [
        "Real-time eligibility results",
        "AI reasoning via official policies",
        "Confidence score transparency",
        "Smart approval improvement tips",
    ]

    check_svg = '<svg viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M2 6l3 3 5-5" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'

    items_html = "".join([
        f'<div class="feature-item"><div class="feature-dot">{check_svg}</div><span class="feature-text">{f}</span></div>'
        for f in features
    ])

    st.markdown(f'<div class="features-grid">{items_html}</div>', unsafe_allow_html=True)

    # Cards
    st.markdown('<div class="cards-row">', unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
        <div class="mode-card">
            <div class="card-icon">🧾</div>
            <div class="card-title">Visa Eligibility Checker</div>
            <div class="card-desc">
                Submit your profile through a guided 5-step form and receive a
                detailed AI verdict with confidence scoring and actionable feedback.
            </div>
            <div>
                <span class="card-tag">Eligibility Decision</span>
                <span class="card-tag">Confidence Score</span>
                <span class="card-tag">Document Checklist</span>
                <span class="card-tag">Policy References</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("Start Eligibility Check →", key="btn_elig"):
            st.session_state.mode = "eligibility"
            st.session_state.step = 1
            st.query_params["mode"] = "eligibility"
            st.query_params["step"] = "1"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="mode-card">
            <div class="card-icon">💬</div>
            <div class="card-title">Visa Chatbot Assistant</div>
            <div class="card-desc">
                Ask anything about visa requirements, documentation, country-specific
                rules, or visa types — and get instant, accurate AI responses.
            </div>
            <div>
                <span class="card-tag">Visa Requirements</span>
                <span class="card-tag">Document Guidance</span>
                <span class="card-tag">Country Rules</span>
                <span class="card-tag">Visa Types</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("Open Chatbot →", key="btn_chat"):
            st.session_state.mode = "chatbot"
            st.session_state.step = 1
            st.query_params["mode"] = "chatbot"
            st.query_params["step"] = "1"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# -------------------------------------------------
# BACK BUTTON
# -------------------------------------------------
if st.button("← Back to Home"):
    st.session_state.mode = None
    st.session_state.step = 1
    st.query_params.clear()
    st.rerun()

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
@st.cache_data
def load_data():
    with open("countries_visa_types.json") as f:
        return json.load(f)

visa_data = load_data()
countries = list(visa_data.keys())

# -------------------------------------------------
# CHATBOT MODE
# -------------------------------------------------
if st.session_state.mode == "chatbot":

    st.markdown('<h2 style="font-family:Sora,sans-serif;color:#e2e8f0;font-size:28px;font-weight:700;margin-bottom:6px;">💬 Visa Assistant</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#64748b;font-size:14px;margin-bottom:28px;">Ask any question about visas, requirements, documents, or country-specific rules.</p>', unsafe_allow_html=True)

    # Chat history display
    if st.session_state.chat_history:
        chat_html = '<div class="chat-wrapper">'
        for role, msg in st.session_state.chat_history:
            # Sanitize newlines for HTML
            msg_html = msg.replace("\n", "<br>")
            if role == "You":
                chat_html += f'<div class="chat-row-user"><div class="chat-bubble-user">{msg_html}</div></div>'
            else:
                chat_html += f'''
                <div class="chat-row-bot">
                    <div class="chat-avatar">✦</div>
                    <div class="chat-bubble-bot">{msg_html}</div>
                </div>'''
        chat_html += '</div>'
        st.markdown(chat_html, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="chat-wrapper">
            <div class="chat-empty">
                <span class="chat-empty-icon">✈️</span>
                No messages yet. Ask your first visa question below!
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Input
    user_query = st.text_input("", placeholder="e.g. What documents do I need for a Schengen tourist visa?", label_visibility="collapsed")

    if st.button("Send Message →") and user_query:
        with st.spinner("Thinking..."):
            answer = visa_chatbot_response(user_query)
        st.session_state.chat_history.append(("You", user_query))
        st.session_state.chat_history.append(("Bot", answer))
        st.rerun()

# -------------------------------------------------
# ELIGIBILITY MODE
# -------------------------------------------------
elif st.session_state.mode == "eligibility":

    st.markdown('<h2 style="font-family:Sora,sans-serif;color:#e2e8f0;font-size:28px;font-weight:700;margin-bottom:6px;">🧾 Visa Eligibility Checker</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#64748b;font-size:14px;margin-bottom:28px;">Complete the form below to receive your AI-powered visa eligibility assessment.</p>', unsafe_allow_html=True)

    steps = [
        "Personal Information",
        "Travel Details",
        "Financial Background",
        "Review Application",
        "AI Decision"
    ]

    # Progress bar
    st.progress(st.session_state.step / 5)
    st.markdown(f"""
    <div class="step-header">
        <div class="step-number">{st.session_state.step}</div>
        <div class="step-label">{steps[st.session_state.step - 1]}</div>
    </div>
    """, unsafe_allow_html=True)

    # STEP 1
    if st.session_state.step == 1:
        st.markdown('<p style="font-size:12px;color:#475569;margin-bottom:16px;">Fields marked <span style="color:#f87171;">*</span> are required.</p>', unsafe_allow_html=True)
        col_a, col_b = st.columns(2, gap="large")
        with col_a:
            age = st.number_input("Age *", 18, 80)
            nationality = st.text_input("Nationality *")
        with col_b:
            marital_status = st.selectbox("Marital Status *", ["Single", "Married", "Divorced"])
            passport_validity = st.number_input("Passport Validity (months) *", 0, 120)

        st.write("")
        col_nav1, col_nav2, col_nav3 = st.columns([1, 3, 1])
        with col_nav3:
            if st.button("Continue →", key="s1"):
                st.session_state.personal = {
                    "age": age,
                    "nationality": nationality,
                    "marital_status": marital_status,
                    "passport_validity": passport_validity
                }
                st.session_state.step = 2
                st.query_params["step"] = "2"
                st.rerun()

    # STEP 2
    elif st.session_state.step == 2:
        st.markdown('<p style="font-size:12px;color:#475569;margin-bottom:16px;">Fields marked <span style="color:#f87171;">*</span> are required.</p>', unsafe_allow_html=True)
        col_a, col_b = st.columns(2, gap="large")
        with col_a:
            destination_country = st.selectbox("Destination Country *", countries)
            visa_type = st.selectbox("Visa Type *", visa_data[destination_country])
        with col_b:
            purpose = st.text_input("Purpose of Visit *")
            travel_duration = st.number_input("Travel Duration (months) *", 1, 60)

        previous_travel = st.selectbox("Previous International Travel", ["Yes", "No"])

        st.write("")
        col_nav1, col_nav2, col_nav3 = st.columns([1, 3, 1])
        with col_nav1:
            if st.button("← Back", key="back2"):
                st.session_state.step = 1
                st.query_params["step"] = "1"
                st.rerun()
        with col_nav3:
            if st.button("Continue →", key="s2"):
                st.session_state.travel = {
                    "country": destination_country,
                    "visa_type": visa_type,
                    "purpose": purpose,
                    "travel_duration": travel_duration,
                    "travel_history": previous_travel
                }
                st.session_state.step = 3
                st.query_params["step"] = "3"
                st.rerun()

    # STEP 3
    elif st.session_state.step == 3:
        st.markdown('<p style="font-size:12px;color:#475569;margin-bottom:16px;">Fields marked <span style="color:#f87171;">*</span> are required.</p>', unsafe_allow_html=True)
        col_a, col_b = st.columns(2, gap="large")
        with col_a:
            education = st.selectbox("Education Level *", ["High School", "Bachelor's", "Master's", "PhD"])
            employment = st.selectbox("Employment Status *", ["Student", "Employed", "Self-employed", "Unemployed"])
        with col_b:
            income = st.number_input("Annual Income (USD) *", min_value=0)
            bank_balance = st.number_input("Bank Balance (USD) *", min_value=0)

        financial_proof = st.selectbox("Financial Proof Available *", ["Yes", "No"])

        st.write("")
        col_nav1, col_nav2, col_nav3 = st.columns([1, 3, 1])
        with col_nav1:
            if st.button("← Back", key="back3"):
                st.session_state.step = 2
                st.query_params["step"] = "2"
                st.rerun()
        with col_nav3:
            if st.button("Continue →", key="s3"):
                st.session_state.financial = {
                    "education": education,
                    "employment": employment,
                    "income": income,
                    "bank_balance": bank_balance,
                    "financial_proof": financial_proof
                }
                st.session_state.step = 4
                st.query_params["step"] = "4"
                st.rerun()

    # STEP 4
    elif st.session_state.step == 4:
        data = {
            **st.session_state.personal,
            **st.session_state.travel,
            **st.session_state.financial
        }

        summary = f"""
A {data['age']}-year-old applicant from {data['nationality']} is planning to travel to {data['country']} to apply for a {data['visa_type']} visa for the purpose of {data['purpose']}, with an intended stay of around {data['travel_duration']} months. 

The applicant has completed {data['education']} education and is currently {data['employment']}, having {data.get('experience', 0)} years of work experience. Financially, the applicant reports an annual income of ${data['income']} and maintains a bank balance of ${data['bank_balance']}. However, financial proof availability is marked as {data['financial_proof']}, and sponsor support is {data.get('sponsor', 'No')}.

In terms of background, the applicant has {data['travel_history']} previous international travel experience, possesses an English proficiency level of {data.get('english', 'Basic')}, and has a criminal record status of {data.get('criminal_record', 'No')}. The passport validity is {data['passport_validity']} months.
"""
        st.markdown('<div class="result-card"><div class="result-title">Application Summary</div></div>', unsafe_allow_html=True)
        st.markdown(f'<p style="color:#94a3b8;font-size:14px;line-height:1.8;">{summary.strip()}</p>', unsafe_allow_html=True)
        st.write("")
        col_nav1, col_nav2, col_nav3 = st.columns([1, 3, 1])
        with col_nav1:
            if st.button("← Back", key="back4"):
                st.session_state.step = 3
                st.query_params["step"] = "3"
                st.rerun()
        with col_nav3:
            if st.button("Submit →", key="s4"):
                st.session_state.step = 5
                st.query_params["step"] = "5"
                st.rerun()

    # STEP 5
    elif st.session_state.step == 5:
        data = {
            **st.session_state.personal,
            **st.session_state.travel,
            **st.session_state.financial
        }

        with st.spinner("Analyzing your visa profile with AI..."):
            output, confidence = screen_visa_eligibility(str(data))

        # ── AI Result (dark green box) ──
        st.success(output["result"])

        # AI disclaimer — placed right below result, subtle
        st.markdown(
            '<div style="margin-top:8px;margin-bottom:24px;">'
            '<span class="ai-disclaimer">🤖 AI-generated result — predictions may not be 100% accurate. '
            'Always verify with official embassy guidelines.</span></div>',
            unsafe_allow_html=True
        )

        st.markdown("---")

        # ── Row 1: Confidence + Risk Factors ──
        col_a, col_b = st.columns([1, 1], gap="large")

        with col_a:
            # Dynamic confidence bar colour
            conf_int = int(confidence)
            if conf_int >= 70:
                bar_color = "linear-gradient(90deg, #059669, #10b981)"
                conf_label_color = "#6ee7b7"
                conf_tier = "High Confidence"
            elif conf_int >= 45:
                bar_color = "linear-gradient(90deg, #d97706, #f59e0b)"
                conf_label_color = "#fcd34d"
                conf_tier = "Moderate Confidence"
            else:
                bar_color = "linear-gradient(90deg, #dc2626, #ef4444)"
                conf_label_color = "#fca5a5"
                conf_tier = "Low Confidence"

            st.markdown(f"""
            <div class="risk-card">
                <div class="risk-label">📊 Confidence Score</div>
                <div style="display:flex;align-items:baseline;gap:10px;margin-bottom:4px;">
                    <span style="font-family:Sora,sans-serif;font-size:36px;font-weight:700;color:{conf_label_color};">{confidence:.1f}%</span>
                    <span style="font-size:12px;color:#475569;">{conf_tier}</span>
                </div>
                <div class="conf-bar-wrap">
                    <div class="conf-bar-fill" style="width:{conf_int}%;background:{bar_color};"></div>
                </div>
                <p style="font-size:12px;color:#475569;margin-top:6px;">
                    Score reflects the AI's estimated probability of visa approval based on your profile.
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col_b:
            # Risk factor breakdown
            passport_status = "ok" if data["passport_validity"] >= 6 else "bad"
            financial_status = "ok" if data["financial_proof"] == "Yes" else "warn"
            income_status = "ok" if data["income"] >= 10000 else ("warn" if data["income"] >= 4000 else "bad")
            balance_status = "ok" if data["bank_balance"] >= 3000 else ("warn" if data["bank_balance"] >= 1000 else "bad")
            employment_status = "ok" if data["employment"] in ["Employed", "Self-employed"] else "warn"

            def badge(status, ok_label, warn_label, bad_label):
                labels = {"ok": ok_label, "warn": warn_label, "bad": bad_label}
                return f'<span class="risk-badge risk-{status}">{labels[status]}</span>'

            st.markdown(f"""
            <div class="risk-card">
                <div class="risk-label">🔍 Profile Risk Factors</div>
                <div class="risk-row">
                    <span class="risk-factor">Passport Validity</span>
                    {badge(passport_status, "✓ Valid", "⚠ Expiring", "✗ Insufficient")}
                </div>
                <div class="risk-row">
                    <span class="risk-factor">Financial Proof</span>
                    {badge(financial_status, "✓ Available", "⚠ Missing", "✗ Not Provided")}
                </div>
                <div class="risk-row">
                    <span class="risk-factor">Annual Income</span>
                    {badge(income_status, "✓ Strong", "⚠ Borderline", "✗ Low")}
                </div>
                <div class="risk-row">
                    <span class="risk-factor">Bank Balance</span>
                    {badge(balance_status, "✓ Sufficient", "⚠ Low", "✗ Insufficient")}
                </div>
                <div class="risk-row" style="border:none;margin:0;">
                    <span class="risk-factor">Employment</span>
                    {badge(employment_status, "✓ Stable", "⚠ Review Needed", "✗ Unemployed")}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # ── Row 2: Suggestions + Missing Docs ──
        col_c, col_d = st.columns([1, 1], gap="large")

        with col_c:
            suggestions = []
            if data["passport_validity"] < 6:
                suggestions.append("🛂 Renew your passport — validity must be at least 6 months from travel date.")
            if data["financial_proof"] == "No":
                suggestions.append("💳 Gather financial proof: bank statements, salary slips, or ITR copies.")
            if data["income"] < 10000:
                suggestions.append("💼 A stronger income profile significantly improves approval odds.")
            if data["bank_balance"] < 3000:
                suggestions.append("🏦 Maintain a minimum bank balance of $3,000 before applying.")
            if data["employment"] == "Unemployed":
                suggestions.append("📋 Provide a strong cover letter explaining financial support sources.")
            if data["travel_history"] == "No":
                suggestions.append("🌐 No prior travel history — attach stronger ties-to-home documents.")
            if data["travel_duration"] > 6:
                suggestions.append("📅 Long stay duration increases scrutiny — justify the length clearly.")

            st.markdown('<div class="risk-label" style="font-family:Sora,sans-serif;font-size:13px;font-weight:600;text-transform:uppercase;letter-spacing:0.06em;color:#64748b;margin-bottom:12px;">📌 Improvement Suggestions</div>', unsafe_allow_html=True)

            if suggestions:
                for s in suggestions:
                    st.warning(s)
            else:
                st.markdown('<p style="color:#6ee7b7;font-size:14px;background:rgba(6,78,59,0.3);border:1px solid rgba(16,185,129,0.25);border-radius:10px;padding:12px 16px;">✅ Your profile looks strong! No major red flags detected.</p>', unsafe_allow_html=True)

        with col_d:
            # Documents: split into present vs potentially missing
            all_docs = [
                ("Valid Passport", data["passport_validity"] >= 6),
                ("Bank Statements (3 months)", data["financial_proof"] == "Yes"),
                ("Employment / Income Proof", data["employment"] in ["Employed", "Self-employed"]),
                ("Completed Visa Application Form", True),
                ("Travel Itinerary / Flight Booking", True),
                ("Passport-size Photographs", True),
                ("Travel Insurance", data["travel_duration"] > 1),
                ("Accommodation Proof / Hotel Booking", True),
            ]

            st.markdown('<div class="risk-label" style="font-family:Sora,sans-serif;font-size:13px;font-weight:600;text-transform:uppercase;letter-spacing:0.06em;color:#64748b;margin-bottom:12px;">📂 Document Checklist</div>', unsafe_allow_html=True)

            for doc_name, is_likely_available in all_docs:
                if is_likely_available:
                    st.markdown(
                        f'<div style="display:flex;align-items:center;gap:10px;padding:8px 12px;background:rgba(16,185,129,0.06);border:1px solid rgba(16,185,129,0.15);border-radius:9px;margin-bottom:6px;">'
                        f'<span style="color:#6ee7b7;font-size:14px;">✓</span>'
                        f'<span style="font-size:13px;color:#94a3b8;">{doc_name}</span></div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f'<div class="missing-doc-item">'
                        f'<span style="color:#f87171;font-size:14px;">✗</span>'
                        f'<span class="missing-doc-label">{doc_name} — likely missing</span></div>',
                        unsafe_allow_html=True
                    )

        st.markdown("---")

        # ── Next Steps ──
        st.markdown('<div class="risk-label" style="font-family:Sora,sans-serif;font-size:13px;font-weight:600;text-transform:uppercase;letter-spacing:0.06em;color:#64748b;margin-bottom:12px;">🗺️ Recommended Next Steps</div>', unsafe_allow_html=True)

        next_steps = [
            ("Verify requirements", f"Visit the official embassy website of {data['country']} to confirm current visa requirements."),
            ("Gather documents", "Collect all documents listed above. Certified translations may be required for non-English documents."),
            ("Book appointment", "Schedule your visa appointment or biometrics session well in advance — slots fill fast."),
            ("Submit application", "Apply through the official visa portal or authorised VFS centre in your city."),
            ("Track status", "Use your application reference number to monitor processing status online."),
        ]

        ns_html = ""
        for i, (title, desc) in enumerate(next_steps, 1):
            ns_html += f"""
            <div class="next-step-item">
                <div class="next-step-num">{i}</div>
                <div class="next-step-text"><strong style="color:#e2e8f0;font-size:13.5px;">{title}</strong><br>{desc}</div>
            </div>"""

        st.markdown(ns_html, unsafe_allow_html=True)

        # Final disclaimer at very bottom
        st.markdown("""
        <div style="margin-top:32px;padding:14px 20px;background:rgba(99,102,241,0.05);border:1px solid rgba(99,102,241,0.12);border-radius:12px;text-align:center;">
            <span style="font-size:12px;color:#475569;">
                ⚠️ <em>SwiftVisa AI uses large language models to estimate visa eligibility. 
                Results are indicative only and should not be treated as legal advice. 
                Final decisions rest solely with the respective embassy or immigration authority.</em>
            </span>
        </div>
        """, unsafe_allow_html=True)