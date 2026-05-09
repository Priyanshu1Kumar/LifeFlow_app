import streamlit as st
from supabase import create_client
import pandas as pd
from datetime import datetime, date

# 1. DATABASE CONNECTION
# Replace with your actual Supabase credentials
URL = "https://wtitwbjfdycckiimtuxg.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind0aXR3YmpmZHljY2tpaW10dXhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzgzNDE4ODUsImV4cCI6MjA5MzkxNzg4NX0.bzt4l0bI84n5T6sF70pmOl7EPy-GpwUERi69Q7bdzfk"
supabase = create_client(URL, KEY)

# 2. PROFESSIONAL UI STYLING
st.set_page_config(page_title="LifeFlow Pro", page_icon="🩸", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 12px; height: 3.5em; background: linear-gradient(90deg, #ff4b4b, #d32f2f); color: white; border: none; font-weight: bold; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #f0f2f6; border-radius: 10px 10px 0 0; padding: 10px 20px; }
    .stMetric { background-color: #f8f9fa; padding: 15px; border-radius: 15px; border: 1px solid #eee; }
    </style>
    """, unsafe_allow_html=True)

# 3. SESSION STATE FOR LOGIN
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None

# --- PAGE: LOGIN/REGISTER ---
def auth_page():
    st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>🩸 LifeFlow</h1>", unsafe_allow_html=True)
    mode = st.radio("Select Mode", ["Login", "Register"], horizontal=True)
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if mode == "Register":
        role = st.selectbox("I am a...", ["Donor", "Hospital Admin"])
        blood = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
        if st.button("Create Account"):
            st.success("Account created! Please Login.")
    else:
        if st.button("Sign In"):
            st.session_state.logged_in = True
            st.session_state.user_role = "Admin" if "admin" in email.lower() else "Donor"
            st.rerun()

# --- PAGE: ADMIN DASHBOARD ---
def admin_page():
    st.title("🏥 Hospital Command Center")
    
    # Stats Row
    c1, c2, c3 = st.columns(3)
    c1.metric("Active Requests", "4", "Urgent")
    c2.metric("Nearby Donors", "24", "+2")
    c3.metric("Success Rate", "98%", "🏆")

    # Broadcast Feature
    with st.expander("📢 Post Emergency Requirement", expanded=True):
        group = st.selectbox("Required Blood Group", ["O-", "O+", "A-", "B+", "AB-"])
        units = st.number_input("Units Required", 1, 10)
        if st.button("Broadcast SMS Alert to Donors"):
            with st.spinner("Notifying nearby donors..."):
                st.toast(f"SMS Alerts sent to 14 {group} donors!")
                st.success("Alert Broadcasted via LifeFlow Network")

    # Data Feed
    st.subheader("Recent Activity")
    res = supabase.table("blood_requests").select("*").order('created_at', ascending=False).execute()
    df = pd.DataFrame(res.data)
    if not df.empty:
        st.dataframe(df[['hospital_name', 'required_group', 'status']], use_container_width=True)

# --- PAGE: DONOR PORTAL ---
def donor_page():
    st.title("🛡️ My Donor Profile")
    
    # 90-Day Logic
    # In real app, fetch this from Supabase based on logged-in user
    last_donation = date(2026, 3, 1) 
    days_passed = (date.today() - last_donation).days
    
    if days_passed >= 90:
        st.balloons()
        st.success(f"✅ Eligible! It has been {days_passed} days since your last donation.")
        if st.button("Ready to Donate: Notify Nearby Hospitals"):
            st.info("Your availability has been shared with local blood banks.")
    else:
        st.warning(f"⏳ Safety First: You can donate in {90 - days_passed} days.")
        st.progress(days_passed / 90)

    # Interactive Map
    st.subheader("Nearby Emergency Centers")
    res = supabase.table("blood_requests").select("location_lat, location_long").eq('status', 'pending').execute()
    map_df = pd.DataFrame(res.data).rename(columns={'location_lat': 'lat', 'location_long': 'lon'})
    if not map_df.empty:
        st.map(map_df)

# --- MAIN NAVIGATION ---
if not st.session_state.logged_in:
    auth_page()
else:
    st.sidebar.title("LifeFlow Navigation")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
    
    if st.session_state.user_role == "Admin":
        admin_page()
    else:
        donor_page()