import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime, timedelta
import urllib.parse

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Sri Balaji 360 Growth OS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CREDENTIALS (Streamlit Cloud Secrets se safely load hongi) ---
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "https://whkvoyiwcsyhnvyauzyd.supabase.co")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "")
GMB_REVIEW_LINK = st.secrets.get("GMB_REVIEW_LINK", "https://g.page/r/CcA7OAT6SREBEBM/review")
ADMIN_USER = st.secrets.get("ADMIN_USER", "admin")
ADMIN_PASS = st.secrets.get("ADMIN_PASS", "balaji@2026")

# --- AUTHENTICATION ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def login_screen():
    st.markdown("<h2 style='text-align:center; color:#38bdf8;'>Sri Balaji 360 Growth OS</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#94a3b8;'>Private Marketing, CRM & Local SEO Command Center</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        with st.form("login_form"):
            user = st.text_input("Username")
            pwd = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login to Command Center", use_container_width=True)
            if submit:
                if user == ADMIN_USER and pwd == ADMIN_PASS:
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Invalid Username or Password")

if not st.session_state.authenticated:
    login_screen()
    st.stop()

# --- SUPABASE CONNECTION ---
@st.cache_resource
def init_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

db_connected = False
supabase = None
if SUPABASE_URL.startswith("http") and len(SUPABASE_KEY) > 15:
    try:
        supabase = init_supabase()
        db_connected = True
    except Exception as e:
        st.error(f"Database Connection Error: {e}")

# --- SIDEBAR ---
with st.sidebar:
    st.title("Sri Balaji 360")
    st.caption("Pimple Saudagar • Wakad • PCMC")
    if db_connected:
        st.success("● Cloud Database Connected")
    else:
        st.warning("● Add SUPABASE_KEY in Streamlit Secrets")

    st.divider()
    custom_review_url = st.text_input("Direct Google Review Link:", value=GMB_REVIEW_LINK)

    menu = st.radio(
        "Navigation",
        [
            "Growth Overview",
            "Repair CRM & WhatsApp Review",
            "360 Content & API Publisher",
            "GMB Review Reply Engine"
        ]
    )
    st.divider()
    st.markdown("**Live Links:**")
    st.markdown("- [sribalajiinfotech.co.in](https://sribalajiinfotech.co.in)")
    st.markdown("- [Google Business Manager](https://business.google.com)")
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()

# --- 1. GROWTH OVERVIEW ---
if menu == "Growth Overview":
    st.header("Sri Balaji Infotech — 360 Growth Dashboard")
    total_repairs = 0
    total_rev = 0
    reviews_sent = 0

    if db_connected:
        try:
            res = supabase.table("repairs").select("*").execute()
            df = pd.DataFrame(res.data)
            if not df.empty:
                total_repairs = len(df)
                total_rev = df["amount"].sum()
                reviews_sent = df["review_sent"].sum()
        except Exception as e:
            st.error(f"Error loading overview: {e}")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Logged Repairs", total_repairs)
    c2.metric("Logged Revenue (₹)", f"₹{total_rev:,.0f}")
    c3.metric("WhatsApp Review Requests", int(reviews_sent))
    c4.metric("Website & SSL Status", "LIVE (HTTPS)")

    st.subheader("Weekly Local SEO Checklist (Top 3 Map Ranking)")
    st.info("""
    - **Step 1:** Log every completed laptop/MacBook repair in **Repair CRM** and send the 1-tap WhatsApp Warranty + Review link.
    - **Step 2:** Publish 2–3 repair case posts per week across **GMB + Instagram** using **360 Content Publisher** targeting *Pimple Saudagar, Wakad, and Thergaon*.
    - **Step 3:** Reply to every new Google review within 24 hours using local area + chip-level keywords.
    """)

# --- 2. REPAIR CRM & WHATSAPP REVIEW ---
elif menu == "Repair CRM & WhatsApp Review":
    st.header("Customer Repair CRM & 1-Tap Google Review Sender")

    with st.expander("Add New Completed / In-Progress Repair", expanded=True):
        with st.form("add_repair_form", clear_on_submit=True):
            col1, col2, col3 = st.columns(3)
            c_name = col1.text_input("Customer Name *", placeholder="e.g. Amit Sharma")
            c_phone = col2.text_input("WhatsApp Number (10 digits) *", placeholder="e.g. 9876543210")
            c_area = col3.selectbox("Customer Area", ["Pimple Saudagar", "Wakad", "Thergaon", "Rahatani", "Hinjewadi", "Pimpri-Chinchwad"])

            col4, col5, col6 = st.columns(3)
            c_device = col4.text_input("Laptop / MacBook Model *", placeholder="e.g. Dell Latitude 5410")
            c_issue = col5.text_input("Work Completed *", placeholder="e.g. No Power Dead Motherboard Repaired")
            c_amount = col6.number_input("Repair Amount (₹)", min_value=0, step=100, value=2500)

            col7, col8 = st.columns(2)
            c_warranty = col7.selectbox("Warranty Period", [30, 90, 180, 365], index=1)
            c_status = col8.selectbox("Status", ["Completed", "In Lab Diagnosis", "Delivered"])

            if st.form_submit_button("Save Repair Record", use_container_width=True):
                if not c_name or not c_phone or not c_device:
                    st.warning("Please enter Customer Name, Phone, and Device Model.")
                elif db_connected:
                    try:
                        supabase.table("repairs").insert({
                            "customer_name": c_name,
                            "phone": c_phone,
                            "area": c_area,
                            "device_model": c_device,
                            "issue_fixed": c_issue,
                            "amount": c_amount,
                            "warranty_days": c_warranty,
                            "status": c_status
                        }).execute()
                        st.success(f"Saved repair record for {c_name}!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Database Save Error: {e}")
                else:
                    st.error("Database not connected. Please add SUPABASE_KEY in Secrets.")

    st.subheader("Recent Customers & Instant 1-Tap Review Message")
    if db_connected:
        try:
            res = supabase.table("repairs").select("*").order("id", desc=True).limit(25).execute()
            if res.data:
                for row in res.data:
                    valid_till = (datetime.now() + timedelta(days=row["warranty_days"])).strftime("%d %b %Y")
                    phone_clean = "".join(filter(str.isdigit, str(row["phone"])))
                    if len(phone_clean) == 10:
                        phone_clean = "91" + phone_clean

                    review_target = custom_review_url.strip()

                    wa_text = (
                        f"Namaste *{row['customer_name']} ji!*\n"
                        f"Thank you for choosing *Laptop Repair Center - Sri Balaji Infotech (Pimple Saudagar)*.\n\n"
                        f"• *Device:* {row['device_model']}\n"
                        f"• *Service:* {row['issue_fixed']}\n"
                        f"• *Warranty:* {row['warranty_days']} Days (Valid till {valid_till})\n\n"
                        f"*Tap below to rate us 5-Star (★★★★★) on Google (takes 10 seconds):*\n"
                        f"{review_target}\n\n"
                        f"*Website:* https://sribalajiinfotech.co.in\n"
                        f"*Call / WhatsApp:* +91 77588 82128"
                    )
                    wa_url = f"https://wa.me/{phone_clean}?text={urllib.parse.quote(wa_text)}"

                    with st.container(border=True):
                        c1, c2, c3 = st.columns([2.5, 1.5, 1.5])
                        c1.markdown(f"**{row['customer_name']}** ({row['area']}) — `{row['phone']}`")
                        c1.caption(f"Device: {row['device_model']} | Work: {row['issue_fixed']}")
                        c2.markdown(f"**₹{row['amount']}** • {row['warranty_days']}d Warranty")
                        c2.caption(f"Status: {row['status']}")
                        c3.link_button("Send WhatsApp + Review", wa_url, use_container_width=True)
            else:
                st.info("No repair records yet. Add your first customer above!")
        except Exception as e:
            st.error(f"Database Fetch Error: {e}")

# --- 3. 360 CONTENT & API PUBLISHER ---
elif menu == "360 Content & API Publisher":
    st.header("360 Multi-Platform Content Publisher")
    col1, col2 = st.columns([1, 1.3])

    with col1:
        p_model = st.text_input("Device Model", "Apple MacBook Pro M1")
        p_service = st.selectbox("Repair Category", [
            "Chip-Level Motherboard Micro-Soldering",
            "Liquid / Water Damage Logic Board Revival",
            "Broken Laptop Hinge & Body Fabrication",
            "Original OEM Display / Retina Screen Replacement",
            "NVMe SSD, RAM Upgrade & Thermal Repasting"
        ])
        p_area = st.selectbox("Target Area Keyword", ["Pimple Saudagar", "Wakad", "Thergaon", "Rahatani", "Hinjewadi", "Pimpri-Chinchwad"])
        p_note = st.text_area("Technical Summary", "Schematic-driven motherboard fault diagnosis and IC replacement with 100% data safety and 90-day warranty.")
        gen_btn = st.button("Generate & Save 360 Campaign", use_container_width=True)

    with col2:
        gmb_text = (
            f"Precision Repair Completed: {p_model} — {p_service} in {p_area}!\n\n"
            f"At Laptop Repair Center - Sri Balaji Infotech, our certified technicians restored this {p_model}.\n"
            f"- {p_note}\n"
            f"- Free Diagnosis (₹0 Checkup) & 90-Day Warranty\n\n"
            f"Serving {p_area}, Pimple Saudagar, Wakad, Thergaon & PCMC.\n"
            f"Address: Shop No. A01, Sai Prem Park, Seven Star Lane, Mithila Nagari, Pimple Saudagar, Pune 411027\n"
            f"Call/WhatsApp: +91 77588 82128 | Website: https://sribalajiinfotech.co.in"
        )
        area_tag = p_area.replace(" ", "").replace("-", "")
        ig_text = (
            f"Precision Chip-Level Lab Work: {p_model} ({p_service}) restored back to 100% performance!\n\n"
            f"{p_note}\n\n"
            f"Location: Pimple Saudagar, Pune (Serving {p_area}, Wakad & PCMC)\n"
            f"WhatsApp +91 77588 82128 for ₹0 Free Diagnostic Checkup!\n"
            f"Website: https://sribalajiinfotech.co.in\n\n"
            f"#SriBalajiInfotech #PimpleSaudagar #{area_tag} #PuneLaptopRepair #MacBookRepairPune #ChipLevelRepair #PCMC"
        )

        if gen_btn and db_connected:
            try:
                supabase.table("marketing_posts").insert({
                    "device_model": p_model,
                    "service_type": p_service,
                    "area": p_area,
                    "gmb_post": gmb_text,
                    "ig_caption": ig_text
                }).execute()
                st.toast("Saved to Cloud Marketing Log!")
            except Exception as e:
                st.error(f"Save Error: {e}")

        st.subheader("1. Google Business Profile Post")
        st.code(gmb_text, language="text")
        st.subheader("2. Instagram Post / Reel Caption")
        st.code(ig_text, language="text")

# --- 4. GMB REVIEW REPLY ENGINE ---
elif menu == "GMB Review Reply Engine":
    st.header("Local SEO Google Review Reply Builder")
    r_name = st.text_input("Customer Name", "Rohan")
    r_service = st.text_input("Service Provided", "MacBook motherboard repair")
    r_area = st.selectbox("Area Mention", ["Pimple Saudagar", "Wakad", "Thergaon", "Rahatani", "Pimpri-Chinchwad"])

    reply_text = (
        f"Thank you so much, {r_name}, for your 5-star review! We are glad our certified technicians could assist you with your "
        f"{r_service} at Laptop Repair Center - Sri Balaji Infotech in Pimple Saudagar. Delivering transparent pricing, precision chip-level "
        f"diagnostics, and fast turnaround for customers across {r_area} and Pimpri-Chinchwad is always our top priority. "
        f"Reach us anytime at +91 77588 82128 or https://sribalajiinfotech.co.in!"
    )
    st.subheader("Copy & Paste in Google Business Reviews:")
    st.code(reply_text, language="text")