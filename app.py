import streamlit as st
from supabase import create_client
import pandas as pd
from datetime import datetime, date
import time
import requests
from streamlit_lottie import st_lottie

# 1. DATABASE CONNECTION
# Replace with your actual Supabase credentials
URL = st.secrets["SUPABASE_URL"]
KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(URL, KEY)

# Load Lottie animations
@st.cache_resource
def load_lottie_url(url):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except:
        return None

# Animation URLs
lottie_blood = "https://lottie.host/5eef21a8-e43c-4ee8-b52e-cccd82e7c6f9/XqhKFXoRmK.json"
lottie_heart = "https://lottie.host/38c0e87e-f8f1-4b96-ba80-f4baa73a4558/K2kpZ8EAnm.json"
lottie_success = "https://lottie.host/a1c1fb24-3e71-4dc5-8da8-ef3ef4ea3e5f/hzHXrFZcKm.json"
lottie_loading = "https://lottie.host/a2c2c93c-7da6-47dd-b8ce-3dde0fa65f1e/hqCx0T4X8p.json"

# 2. PREMIUM UI/UX STYLING WITH ANIMATIONS & TRANSITIONS
st.set_page_config(page_title="LifeFlow Pro", page_icon="🩸", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* ===== ANIMATIONS ===== */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes slideInUp {
        from { opacity: 0; transform: translateY(40px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 20px rgba(220, 38, 38, 0.3); }
        50% { box-shadow: 0 0 30px rgba(220, 38, 38, 0.6); }
    }
    
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes rotateIn {
        from { 
            opacity: 0;
            transform: rotate(-10deg) scale(0.9);
        }
        to { 
            opacity: 1;
            transform: rotate(0) scale(1);
        }
    }
    
    /* ===== GLOBAL STYLES ===== */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@600;700&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #FEF2F2 0%, #FCE7E7 50%, #FFF5F7 100%);
        min-height: 100vh;
    }
    
    .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background: linear-gradient(135deg, #FEF2F2 0%, #FCE7E7 50%, #FFF5F7 100%);
    }
    
    /* ===== HIDE DEFAULTS ===== */
    #MainMenu, footer, header { visibility: hidden; }
    .viewerBadge_container__r5tak { display: none; }
    
    /* ===== CONTAINER STYLING ===== */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 3rem;
        max-width: 600px;
        margin: 0 auto;
    }
    
    /* ===== SECTION CONTAINERS WITH ANIMATION ===== */
    [data-testid="stVerticalBlock"] > div:nth-child(n) {
        animation: fadeIn 0.6s ease-out forwards;
        animation-fill-mode: both;
    }
    
    [data-testid="stVerticalBlock"] > div:nth-child(1) { animation-delay: 0.1s; }
    [data-testid="stVerticalBlock"] > div:nth-child(2) { animation-delay: 0.2s; }
    [data-testid="stVerticalBlock"] > div:nth-child(3) { animation-delay: 0.3s; }
    [data-testid="stVerticalBlock"] > div:nth-child(4) { animation-delay: 0.4s; }
    [data-testid="stVerticalBlock"] > div:nth-child(n+5) { animation-delay: 0.5s; }
    
    /* ===== CARD STYLING ===== */
    .stContainer, [data-testid="stVerticalBlock"] {
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 24px;
        margin-bottom: 20px;
        border: 1px solid rgba(220, 38, 38, 0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.06);
    }
    
    .stContainer:hover, [data-testid="stVerticalBlock"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 48px rgba(220, 38, 38, 0.15);
        border-color: rgba(220, 38, 38, 0.2);
    }
    
    /* ===== BUTTONS ===== */
    .stButton > button {
        width: 100%;
        border-radius: 16px;
        height: 48px;
        background: linear-gradient(135deg, #DC2626 0%, #991B1B 100%);
        color: white;
        font-weight: 700;
        font-size: 16px;
        border: none;
        box-shadow: 0 8px 16px rgba(220, 38, 38, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        letter-spacing: 0.5px;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 14px 28px rgba(220, 38, 38, 0.4);
        background: linear-gradient(135deg, #EF4444 0%, #B91C1C 100%);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(220, 38, 38, 0.2);
    }
    
    /* ===== INPUT FIELDS ===== */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input {
        border-radius: 14px;
        border: 2px solid #E5E7EB;
        background-color: #FAFAFA;
        padding: 14px 16px;
        font-size: 15px;
        font-family: 'Plus Jakarta Sans', sans-serif;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #DC2626;
        box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1), 0 2px 8px rgba(220, 38, 38, 0.2);
        background-color: #FFF;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #9CA3AF;
    }
    
    /* ===== TABS ===== */
    .stTabs [data-baseweb="tab-list"] {
        display: flex;
        justify-content: center;
        gap: 12px;
        background-color: rgba(220, 38, 38, 0.05);
        padding: 8px;
        border-radius: 16px;
        margin: 20px auto;
        max-width: fit-content;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
        color: #6B7280;
        border-radius: 12px;
        padding: 12px 24px;
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: linear-gradient(135deg, #DC2626 0%, #991B1B 100%);
        color: white !important;
        box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
    }
    
    /* ===== TYPOGRAPHY ===== */
    h1 {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 800;
        color: #1F2937;
        letter-spacing: -1px;
        animation: slideInLeft 0.6s ease-out;
    }
    
    h2 {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        color: #DC2626;
        animation: slideInLeft 0.6s ease-out 0.1s backwards;
    }
    
    h3 {
        font-weight: 700;
        color: #374151;
        animation: fadeIn 0.6s ease-out;
    }
    
    p, .stMarkdown {
        color: #4B5563;
        line-height: 1.8;
        font-weight: 500;
    }
    
    /* ===== METRICS ===== */
    [data-testid="stMetricValue"] {
        font-size: 2.2em;
        font-weight: 800;
        background: linear-gradient(135deg, #DC2626 0%, #991B1B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    [data-testid="stMetricLabel"] {
        font-weight: 600;
        color: #4B5563;
    }
    
    /* ===== PROGRESS BARS ===== */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #DC2626 0%, #991B1B 100%);
        border-radius: 10px;
        animation: slideInLeft 0.8s ease-out;
    }
    
    /* ===== SPINNERS & LOADING ===== */
    .stSpinner > div {
        border-color: rgba(220, 38, 38, 0.2);
        border-right-color: #DC2626;
    }
    
    /* ===== ALERTS & MESSAGES ===== */
    .stSuccess {
        background-color: rgba(34, 197, 94, 0.1) !important;
        border-left: 4px solid #22C55E !important;
        border-radius: 8px;
        animation: slideInUp 0.4s ease-out;
    }
    
    .stError {
        background-color: rgba(220, 38, 38, 0.1) !important;
        border-left: 4px solid #DC2626 !important;
        border-radius: 8px;
        animation: slideInUp 0.4s ease-out;
    }
    
    .stInfo {
        background-color: rgba(59, 130, 246, 0.1) !important;
        border-left: 4px solid #3B82F6 !important;
        border-radius: 8px;
        animation: slideInUp 0.4s ease-out;
    }
    
    .stWarning {
        background-color: rgba(251, 146, 60, 0.1) !important;
        border-left: 4px solid #FB923C !important;
        border-radius: 8px;
        animation: slideInUp 0.4s ease-out;
    }
    
    /* ===== DATAFRAME ===== */
    .stDataFrame {
        border-radius: 14px;
        overflow: hidden;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
    }
    
    /* ===== COLUMNS ===== */
    [data-testid="column"] {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FEF2F2 0%, #FCE7E7 100%);
    }
    
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        background: rgba(255, 255, 255, 0.8);
    }
    
    /* ===== DECORATIVE ELEMENTS ===== */
    .hero-section {
        background: linear-gradient(135deg, #DC2626 0%, #991B1B 100%);
        color: white;
        padding: 40px 20px;
        border-radius: 24px;
        text-align: center;
        box-shadow: 0 20px 60px rgba(220, 38, 38, 0.3);
        animation: rotateIn 0.6s ease-out;
    }
    
    .status-badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 13px;
        letter-spacing: 0.5px;
        animation: pulse 2s ease-in-out infinite;
    }
    
    .status-eligible {
        background-color: rgba(34, 197, 94, 0.2);
        color: #15803D;
    }
    
    .status-waiting {
        background-color: rgba(251, 146, 60, 0.2);
        color: #92400E;
    }
    
    .status-urgent {
        background-color: rgba(220, 38, 38, 0.2);
        color: #7F1D1D;
        animation: glow 2s ease-in-out infinite;
    }
    </style>
    """, unsafe_allow_html=True)
# 3. APP STATE MANAGEMENT
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'page_load' not in st.session_state:
    st.session_state.page_load = True

# --- UI COMPONENT: AUTH ---
def auth_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="margin-bottom: 10px; font-size: 3em;">🩸</h1>
            <h1 style="color: #DC2626; margin: 10px 0;">LifeFlow</h1>
            <p style="color: #6B7280; font-size: 18px; font-weight: 500;">Connecting Lives, Saving Lives</p>
        </div>
        """, unsafe_allow_html=True)
    
    with st.container():
        mode = st.tabs(["🔐 Sign In", "✨ Register"])
        
        with mode[0]:
            st.markdown("### Welcome Back")
            email = st.text_input("📧 Email Address", placeholder="you@example.com", key="login_email")
            pwd = st.text_input("🔒 Password", type="password", placeholder="••••••••", key="login_pwd")
            
            col1, col2 = st.columns(2)
            with col1:
                remember = st.checkbox("Remember me")
            with col2:
                st.markdown('<a href="#" style="color: #DC2626; text-decoration: none; font-weight: 600;">Forgot password?</a>', unsafe_allow_html=True)
            
            if st.button("🚀 Sign In to LifeFlow", key="login_btn", use_container_width=True):
                with st.spinner(""):
                    col_spinner = st.columns(3)
                    with col_spinner[1]:
                        st_lottie(load_lottie_url(lottie_loading), height=80, key="loading1")
                    time.sleep(1.5)
                st.session_state.logged_in = True
                st.session_state.user_role = "Admin" if "admin" in email.lower() else "Donor"
                st.toast("✅ Welcome back! Redirecting...", icon="✅")
                time.sleep(0.5)
                st.rerun()
        
        with mode[1]:
            st.markdown("### Join the LifeSaver Community")
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("👤 Full Name", placeholder="John Doe", key="reg_name")
            with col2:
                phone = st.text_input("📱 Phone", placeholder="+91-XXXXX-XXXXX", key="reg_phone")
            
            blood = st.selectbox("🩸 Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"], key="reg_blood")
            email_reg = st.text_input("📧 Email", placeholder="you@example.com", key="reg_email")
            
            if st.button("✨ Create LifeSaver Account", key="reg_btn", use_container_width=True):
                with st.spinner(""):
                    col_spinner = st.columns(3)
                    with col_spinner[1]:
                        st_lottie(load_lottie_url(lottie_loading), height=80, key="loading2")
                    time.sleep(1.5)
                st.balloons()
                st.toast("🎉 Welcome to LifeFlow! Your account is ready.", icon="🎉")
                time.sleep(0.5)
                st.session_state.logged_in = True
                st.session_state.user_role = "Donor"
                st.rerun()

# --- UI COMPONENT: ADMIN ---
def admin_page():
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1 style="font-size: 2.5em; margin-bottom: 10px;">🏥 Command Center</h1>
        <p style="font-size: 1.1em; opacity: 0.95;">Real-time Blood Donation Network</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Live Metrics Section
    st.markdown("<h2 style='margin-top: 30px;'>📊 Live Metrics</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🆘 Pending Requests", "5", "High Priority")
    with col2:
        st.metric("💪 Available Donors", "142", "+4 today")
    with col3:
        st.metric("✅ Fulfilled Today", "3", "100% Success")
    
    # Broadcast Section
    st.markdown("""
    <div style="margin-top: 30px; margin-bottom: 20px;">
        <h2 style="margin-bottom: 20px;">📢 Emergency Broadcast</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        bg_req = st.selectbox("🩸 Blood Group Needed", ["O-", "O+", "A-", "B+", "AB-", "B-", "A+", "AB+"], key="admin_bg")
    with col2:
        units = st.number_input("📦 Units Required", 1, 50, 3, key="admin_units")
    
    hospital = st.text_input("🏥 Hospital Name", "City General Hospital", key="admin_hospital")
    location = st.text_input("📍 Location", "Downtown Medical Center", key="admin_location")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚨 Send SMS Alert", use_container_width=True):
            with st.spinner(""):
                col_spinner = st.columns(3)
                with col_spinner[1]:
                    st_lottie(load_lottie_url(lottie_loading), height=60, key="admin_load")
                time.sleep(1.5)
            st.success(f"✅ Emergency alert sent to all {bg_req} donors in 10km radius!")
            st.balloons()
    
    with col2:
        if st.button("📧 Send Email Alert", use_container_width=True):
            with st.spinner("Sending..."):
                time.sleep(1)
            st.success("✅ Email notifications sent to premium donors")
    
    # Live Request Feed
    st.markdown("""
    <div style="margin-top: 30px; margin-bottom: 20px;">
        <h2>🔴 Live Request Feed</h2>
        <p style="color: #6B7280; font-size: 14px;">Real-time blood requests from hospitals</p>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        res = supabase.table("blood_requests").select("*").order('created_at', ascending=False).limit(5).execute()
        if res.data:
            df = pd.DataFrame(res.data)
            st.dataframe(df[['hospital_name', 'required_group', 'status']], use_container_width=True, hide_index=True)
        else:
            st.info("No active requests at the moment")
    except:
        st.info("💾 Live data connection loading...")
    
    # Statistics
    st.markdown("""
    <div style="margin-top: 30px; margin-bottom: 20px;">
        <h2>📈 Analytics</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Response Time", "4.2 min", "-15% improvement")
    with col2:
        st.metric("Success Rate", "98.5%", "↑ 2%")

# --- UI COMPONENT: DONOR ---
def donor_page():
    # Hero Section with Animation
    col_hero = st.columns(3)
    with col_hero[1]:
        st_lottie(load_lottie_url(lottie_heart), height=100)
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: #DC2626; margin-bottom: 10px;">🛡️ My Dashboard</h1>
        <p style="color: #6B7280; font-size: 16px;">Track your donation journey</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 90-Day Logic Engine
    last_donation = date(2026, 2, 10)
    days_passed = (date.today() - last_donation).days
    days_remaining = max(0, 90 - days_passed)
    
    # Eligibility Status Card
    with st.container():
        if days_passed >= 90:
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(74, 222, 128, 0.1));
                border-left: 4px solid #22C55E;
                padding: 20px;
                border-radius: 12px;
                margin-bottom: 20px;
            ">
                <h3 style="color: #15803D; margin: 0; display: flex; align-items: center;">
                    ✅ You're Eligible to Donate!
                </h3>
                <p style="color: #4B5563; margin: 10px 0 0 0;">
                    It's been <strong>{} days</strong> since your last donation. Your body has recovered fully.
                </p>
            </div>
            """.format(days_passed), unsafe_allow_html=True)
            
            if st.button("💪 Mark Yourself Available", use_container_width=True):
                col_spinner = st.columns(3)
                with col_spinner[1]:
                    st_lottie(load_lottie_url(lottie_success), height=100)
                st.balloons()
                st.toast("🎉 Status updated! Hospitals can now see you.", icon="🎉")
        else:
            progress_value = days_passed / 90
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, rgba(251, 146, 60, 0.1), rgba(253, 224, 71, 0.1));
                border-left: 4px solid #FB923C;
                padding: 20px;
                border-radius: 12px;
                margin-bottom: 20px;
            ">
                <h3 style="color: #92400E; margin: 0; display: flex; align-items: center;">
                    ⏳ Waiting Period
                </h3>
                <p style="color: #4B5563; margin: 10px 0 0 0;">
                    You can donate again in <strong>{} days</strong>
                </p>
            </div>
            """.format(days_remaining), unsafe_allow_html=True)
            
            st.progress(progress_value, text=f"{int(progress_value*100)}% recovered")
    
    # Donation History
    st.markdown("""
    <div style="margin-top: 30px; margin-bottom: 20px;">
        <h2>💝 Your Impact</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🩸 Total Donations", "7", "Lives Saved: 21")
    with col2:
        st.metric("❤️ Last Donation", "Feb 10, 2026", "90+ days ago")
    with col3:
        st.metric("🏆 Status", "Gold Donor", "Tier 2")
    
    # Nearby Emergencies
    st.markdown("""
    <div style="margin-top: 30px; margin-bottom: 20px;">
        <h2>🚨 Emergency Requests Near You</h2>
        <p style="color: #6B7280; font-size: 14px;">Blood requests from hospitals within 10km</p>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        res = supabase.table("blood_requests").select("location_lat, location_long").eq('status', 'pending').execute()
        if res.data:
            map_df = pd.DataFrame(res.data).rename(columns={'location_lat': 'lat', 'location_long': 'lon'})
            st.map(map_df, zoom=12)
        else:
            st.info("No emergency requests nearby right now")
    except:
        st.warning("📍 Map data loading...")
    
    # Recent Requests
    st.markdown("""
    <div style="margin-top: 30px; margin-bottom: 20px;">
        <h2>📋 Recent Requests</h2>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        res = supabase.table("blood_requests").select("*").eq('status', 'pending').limit(3).execute()
        if res.data:
            for request in res.data:
                st.markdown(f"""
                <div style="
                    background: rgba(255,255,255,0.7);
                    border-left: 4px solid #DC2626;
                    padding: 15px;
                    border-radius: 8px;
                    margin-bottom: 15px;
                ">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <p style="margin: 0; font-weight: 600; color: #1F2937;">{request.get('hospital_name', 'Unknown Hospital')}</p>
                            <p style="margin: 5px 0 0 0; color: #6B7280; font-size: 14px;">
                                🩸 {request.get('required_group', 'Unknown')} • 📍 {request.get('units', '2')} units
                            </p>
                        </div>
                        <button style="
                            background: linear-gradient(135deg, #DC2626 0%, #991B1B 100%);
                            color: white;
                            border: none;
                            padding: 8px 16px;
                            border-radius: 8px;
                            cursor: pointer;
                            font-weight: 600;
                            font-size: 12px;
                        ">Respond</button>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No pending requests at this moment")
    except:
        st.info("Loading requests...")

# --- MAIN ROUTER ---
if not st.session_state.logged_in:
    auth_page()
else:
    # Enhanced Sidebar with Animations
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 20px 0; margin-bottom: 30px;">
            <h2 style="font-size: 2em; margin: 0;">🩸</h2>
            <p style="color: #DC2626; font-weight: 700; margin: 10px 0 0 0;">LifeFlow</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, rgba(220, 38, 38, 0.1), rgba(185, 28, 28, 0.05));
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 20px;
            border-left: 4px solid #DC2626;
        ">
            <p style="margin: 0; font-weight: 600; color: #1F2937;">Role</p>
            <p style="margin: 5px 0 0 0; color: #DC2626; font-weight: 700; font-size: 16px;">
                {st.session_state.user_role}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⚙️ Settings", use_container_width=True):
                st.toast("Settings coming soon!", icon="⚡")
        with col2:
            if st.button("❓ Help", use_container_width=True):
                st.toast("Help center loading...", icon="❓")
        
        st.divider()
        
        if st.button("🚪 Sign Out", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_role = None
            st.toast("👋 Signed out successfully", icon="👋")
            time.sleep(0.5)
            st.rerun()
    
    # Page Content
    if st.session_state.user_role == "Admin":
        admin_page()
    else:
        donor_page()