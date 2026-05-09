import streamlit as st
from supabase import create_client
import pandas as pd
from datetime import datetime, date

# 1. DATABASE CONNECTION
# Replace with your actual Supabase credentials
URL = "https://wtitwbjfdycckiimtuxg.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind0aXR3YmpmZHljY2tpaW10dXhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzgzNDE4ODUsImV4cCI6MjA5MzkxNzg4NX0.bzt4l0bI84n5T6sF70pmOl7EPy-GpwUERi69Q7bdzfk"
supabase = create_client(URL, KEY)

# 2. "THE BEST" MOBILE UI STYLING
st.set_page_config(page_title="LifeFlow Pro", page_icon="🩸", layout="centered")

st.markdown("""
    <style>
    /* Hide Default Headers */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Background & Font */
    .stApp { background-color: #F8F9FA; }
    
    /* Card Layouts */
    div[data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {
        background-color: white;
        padding: 25px;
        border-radius: 24px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.04);
        border: 1px solid #f0f0f0;
        margin-bottom: 20px;
    }

    /* High-End Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 18px;
        height: 3.8em;
        background: linear-gradient(135deg, #FF4B4B 0%, #AF1B1B 100%);
        color: white;
        font-weight: 700;
        font-size: 16px;
        border: none;
        box-shadow: 0 6px 20px rgba(211, 47, 47, 0.25);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(211, 47, 47, 0.35);
    }
    
    /* Modern Input Fields */
    .stTextInput>div>div>input {
        border-radius: 12px;
        border: 1px solid #E0E0E0;
        padding: 12px;
    }

    /* Custom Navigation Tabs */
    .stTabs [data-baseweb="tab-list"] {
        display: flex;
        justify-content: center;
        background-color: #eee;
        padding: 5px;
        border-radius: 15px;
        margin-bottom: 25px;
    }
    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
        border-radius: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. APP STATE MANAGEMENT
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None

# --- UI COMPONENT: AUTH ---
def auth_page():
    st.markdown("<h1 style='text-align: center; color: #D32F2F;'>🩸 LifeFlow</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>Connecting Life to Need</p>", unsafe_allow_html=True)
    
    with st.container():
        mode = st.tabs(["Login", "Register"])
        
        with mode[0]:
            email = st.text_input("Username / Email", placeholder="johndoe@example.com")
            pwd = st.text_input("Password", type="password", placeholder="••••••••")
            if st.button("Sign In to LifeFlow"):
                with st.spinner("Authenticating..."):
                    time.sleep(1)
                    st.session_state.logged_in = True
                    # Smart Role Selection for Demo
                    st.session_state.user_role = "Admin" if "admin" in email.lower() else "Donor"
                    st.rerun()
        
        with mode[1]:
            st.text_input("Full Name")
            st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
            st.text_input("Phone Number")
            if st.button("Create LifeSaver Account"):
                st.toast("Welcome to the community!")

# --- UI COMPONENT: ADMIN ---
def admin_page():
    st.markdown("<h2 style='color: #D32F2F;'>🏥 Command Center</h2>", unsafe_allow_html=True)
    
    # Live Metrics
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Pending Requests", "5", "Urgent")
    with c2:
        st.metric("Available Donors", "142", "+4 today")

    with st.container():
        st.subheader("📢 Broadcast Requirement")
        bg_req = st.selectbox("Select Blood Group Needed", ["O-", "O+", "A-", "B+", "AB-"])
        hospital = st.text_input("Hospital Name", "City General Hospital")
        if st.button("Send Instant SMS Alert"):
            st.toast("Connecting to SMS Gateway...")
            time.sleep(1.5)
            st.success(f"Emergency Alert broadcasted to all {bg_req} donors in a 10km radius!")

    st.subheader("Live Request Feed")
    try:
        res = supabase.table("blood_requests").select("*").order('created_at', ascending=False).execute()
        df = pd.DataFrame(res.data)
        st.dataframe(df[['hospital_name', 'required_group', 'status']], use_container_width=True)
    except:
        st.info("Waiting for live data connection...")

# --- UI COMPONENT: DONOR ---
def donor_page():
    st.markdown("<h2 style='color: #D32F2F;'>🛡️ My Profile</h2>", unsafe_allow_html=True)
    
    # 90-Day Logic Engine
    last_donation = date(2026, 2, 10) # Change this to test the logic
    days_passed = (date.today() - last_donation).days
    
    with st.container():
        if days_passed >= 90:
            st.markdown("<h3 style='color: #2E7D32;'>✅ You are Eligible!</h3>", unsafe_allow_html=True)
            st.write(f"It has been **{days_passed} days** since your last hero act.")
            if st.button("Set Available for Donation"):
                st.balloons()
                st.toast("Status updated on Hospital Dashboards!")
        else:
            st.markdown(f"<h3 style='color: #D32F2F;'>⏳ Waiting Period</h3>", unsafe_allow_html=True)
            st.write(f"You can donate again in **{90 - days_passed} days**.")
            st.progress(days_passed / 90)

    st.subheader("📍 Nearby Emergencies")
    # Interactive Map Logic
    try:
        res = supabase.table("blood_requests").select("location_lat, location_long").eq('status', 'pending').execute()
        map_df = pd.DataFrame(res.data).rename(columns={'location_lat': 'lat', 'location_long': 'lon'})
        st.map(map_df, zoom=11)
    except:
        st.warning("Map Data Unavailable")

# --- MAIN ROUTER ---
if not st.session_state.logged_in:
    auth_page()
else:
    # Minimalist Sidebar
    with st.sidebar:
        st.markdown(f"**Logged in as:**\n{st.session_state.user_role}")
        if st.button("Sign Out"):
            st.session_state.logged_in = False
            st.rerun()
    
    if st.session_state.user_role == "Admin":
        admin_page()
    else:
        donor_page()