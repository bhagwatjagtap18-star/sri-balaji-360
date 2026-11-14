import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime, timedelta
import urllib.parse
import time

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Sri Balaji 360 Growth OS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CREDENTIALS ---
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "https://whkvoyiwcsyhnvyauzyd.supabase.co").strip()
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "").strip()
GMB_REVIEW_LINK = st.secrets.get("GMB_REVIEW_LINK", "https://g.page/r/CcA7OAT6SREBEBM/review").strip()
ADMIN_USER = st.secrets.get("ADMIN_USER", "admin").strip()
ADMIN_PASS = st.secrets.get("ADMIN_PASS", "balaji@2026").strip()

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
        st.warning("● Add SUPABASE_KEY in Secrets")

    st.divider()
    custom_review_url = st.text_input("Direct Google Review Link:", value=GMB_REVIEW_LINK)

    menu = st.radio(
        "Navigation",
        [
            "Growth Overview",
            "Repair CRM & WhatsApp Review",
            "360 Content & 1-Tap Publisher",
            "GMB Review Reply Engine"
        ]
    )
    st.divider()
    st.markdown("**Quick Launchers:**")
    st.markdown("- [sribalajiinfotech.co.in](https://sribalajiinfotech.co.in)")
    st.markdown("- [Instagram Profile](https://www.instagram.com/)")
    st.markdown("- [Google Business Manager](https://business.google.com)")
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()

# --- 1. GROWTH OVERVIEW ---
if menu == "Growth Overview":
    st.header("Sri Balaji Infotech — 360 Growth Dashboard")
    total_repairs = 0
    total_rev = 0
    posts_count = 0

    if db_connected:
        try:
            res = supabase.table("repairs").select("*").execute()
            df = pd.DataFrame(res.data)
            if not df.empty:
                total_repairs = len(df)
                total_rev = df["amount"].sum()

            p_res = supabase.table("marketing_posts").select("id").execute()
            posts_count = len(p_res.data) if p_res.data else 0
        except Exception as e:
            st.error(f"Error loading overview: {e}")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Logged Repairs", total_repairs)
    c2.metric("Logged Revenue (₹)", f"₹{total_rev:,.0f}")
    c3.metric("360 Campaigns Created", posts_count)
    c4.metric("Domain & SSL Status", "app.sribalajiinfotech.co.in")

    st.subheader("Daily 5-Minute Local Growth Routine")
    st.info("""
    - **Step 1 (After Repair):** Log customer in **Repair CRM** and tap **Send WhatsApp + Review** (takes 10 seconds).
    - **Step 2 (3x Per Week):** Upload a photo of a repaired motherboard/MacBook in **360 Content & 1-Tap Publisher**, save to cloud (auto-updates your website with photo!), and post to **Instagram + Google Business Profile**.
    - **Step 3 (Within 24h):** Reply to every new Google review using **GMB Review Reply Engine** with Pimple Saudagar / Wakad keywords.
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

# --- 3. 360 CONTENT & 1-TAP PUBLISHER ---
elif menu == "360 Content & 1-Tap Publisher":
    st.header("360 Multi-Platform 1-Tap Content Publisher")
    col1, col2 = st.columns([1, 1.35])

    SERVICE_TEMPLATES = {
        "Chip-Level Motherboard Micro-Soldering (Dead / No Power)": "Schematic-driven motherboard fault diagnosis, power rail short removal, and IC micro-soldering with 100% data safety and 90-day warranty.",
        "Deep Motherboard Servicing, Thermal Repasting & Fan Cleaning": "Complete internal dust and oxidation cleaning, high-conductivity thermal paste application, and cooling fan servicing to eliminate overheating and lag.",
        "NVMe SSD, RAM Upgrade & OS Speed Optimization": "High-speed NVMe SSD and DDR4/DDR5 RAM upgrade with seamless OS migration and zero data loss for 5x faster boot and multitasking.",
        "Liquid / Water Damage Logic Board Revival": "Ultrasonic logic board cleaning, corroded circuit track restoration, and power IC replacement to revive water-damaged laptops without motherboard replacement.",
        "BIOS Programming & No-Display / Boot Loop Fix": "Chip-level EC/Main BIOS flashing, display power circuit repair, and GPU/RAM rail troubleshooting to resolve black screen and boot loop issues.",
        "Charging IC, USB-C Port & Power Jack Replacement": "Precision micro-soldering of charging IC, Mosfets, and damaged Type-C / DC power jack to restore stable battery charging.",
        "Broken Laptop Hinge & Body Panel Fabrication": "Heavy-duty brass nut reinforcement, hinge alignment, and palmrest/bottom panel fabrication for smooth and durable lid movement.",
        "Original OEM Display / Retina Screen Replacement": "Brand-new Full HD / Retina / Touch display panel replacement with true color calibration and scratch-free installation.",
        "MacBook Flexgate / Display Backlight IC Repair": "Micro-soldering backlight driver IC and display flex cable restoration for MacBook Pro & Air without expensive full screen replacement.",
        "Original Laptop / MacBook Battery Replacement": "Genuine high-cycle OEM battery replacement with power calibration and battery health verification.",
        "Backlit Keyboard & Trackpad Replacement": "Precision replacement of faulty or liquid-damaged laptop keyboard and multi-touch trackpad with full key testing.",
        "Gaming Laptop Overheating & GPU Thermal Servicing": "Dual-fan heatsink cleaning, VRM thermal pad replacement, and high-grade thermal compound repasting for peak gaming FPS stability.",
        "SSD / Hard Drive Data Recovery & Backup": "Safe sector-level data extraction and backup from crashed laptops, dead motherboards, or corrupted drives.",
        "Audio IC, Speaker & Wi-Fi Card Repair": "Internal speaker replacement, audio codec IC repair, and dual-band Wi-Fi/Bluetooth module restoration.",
        "Custom Service (Enter Your Own Title Below)": "Complete hardware diagnosis and precision chip-level repair completed with genuine components and 90-day warranty."
    }

    with col1:
        p_photo = st.file_uploader("Upload Repair Photo (Auto-Publishes to Website)", type=["jpg", "jpeg", "png", "webp"])
        if p_photo:
            st.image(p_photo, caption="Ready to publish to Website, Instagram & GMB", use_container_width=True)

        p_model = st.text_input("Device Model", "Dell Inspiron 3521")
        selected_cat = st.selectbox("Repair Category (15 Options)", list(SERVICE_TEMPLATES.keys()))
        if selected_cat == "Custom Service (Enter Your Own Title Below)":
            p_service = st.text_input("Custom Repair Title", "Custom Motherboard & Hardware Repair")
        else:
            p_service = selected_cat

        p_area = st.selectbox("Target Area Keyword", ["Pimple Saudagar", "Wakad", "Thergaon", "Rahatani", "Hinjewadi", "Pimpri-Chinchwad"])
        p_note = st.text_area("Technical Summary (Auto-filled — Edit if needed)", value=SERVICE_TEMPLATES[selected_cat], height=110)
        save_btn = st.button("Save Campaign & Publish Photo to Website", use_container_width=True)

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
            f"#SriBalajiInfotech #PimpleSaudagar #{area_tag} #PuneLaptopRepair #MacBookRepairPune #ChipLevelRepair #PCMC #LaptopServicePune #MotherboardRepair"
        )

        wa_promo_text = (
            f"*Recent Lab Repair — Sri Balaji Infotech (Pimple Saudagar)*\n\n"
            f"• *Device:* {p_model}\n"
            f"• *Work Done:* {p_service}\n"
            f"• *Details:* {p_note}\n\n"
            f"Facing laptop, MacBook, or motherboard issues? Visit us for *₹0 Free Checkup & 90-Day Warranty*!\n"
            f"*Website:* https://sribalajiinfotech.co.in\n"
            f"*Call / WhatsApp:* +91 77588 82128"
        )
        wa_share_url = f"https://wa.me/?text={urllib.parse.quote(wa_promo_text)}"

        if save_btn and db_connected:
            try:
                uploaded_img_url = ""
                if p_photo is not None:
                    ext = p_photo.name.split(".")[-1].lower()
                    file_path = f"repair_{int(time.time())}.{ext}"
                    supabase.storage.from_("repair-photos").upload(
                        file_path,
                        p_photo.getvalue(),
                        file_options={"content-type": p_photo.type}
                    )
                    uploaded_img_url = f"{SUPABASE_URL}/storage/v1/object/public/repair-photos/{file_path}"

                supabase.table("marketing_posts").insert({
                    "device_model": p_model,
                    "service_type": p_service,
                    "area": p_area,
                    "gmb_post": gmb_text,
                    "ig_caption": ig_text,
                    "image_url": uploaded_img_url
                }).execute()
                st.success("Campaign & Photo published live to your Website!")
            except Exception as e:
                st.error(f"Save Error: {e}")

        tab_ig, tab_gmb, tab_wa = st.tabs(["1. Instagram Post", "2. Google Business (GMB)", "3. WhatsApp Status / Share"])

        with tab_ig:
            st.caption("Tap the top-right Copy icon inside the box below, then tap Open Instagram:")
            st.code(ig_text, language="text")
            st.link_button("Open Instagram to Post", "https://www.instagram.com/", use_container_width=True)

        with tab_gmb:
            st.caption("Tap the top-right Copy icon inside the box below, then tap Open Google Business:")
            st.code(gmb_text, language="text")
            st.link_button("Open Google Business Profile", "https://business.google.com/", use_container_width=True)

        with tab_wa:
            st.caption("Share directly to your WhatsApp Status or customer broadcast list in 1 tap:")
            st.code(wa_promo_text, language="text")
            st.link_button("1-Tap Share on WhatsApp", wa_share_url, use_container_width=True)

    if db_connected:
        st.divider()
        st.subheader("Recent Saved 360 Campaigns")
        try:
            hist = supabase.table("marketing_posts").select("created_at, device_model, service_type, area").order("id", desc=True).limit(5).execute()
            if hist.data:
                st.dataframe(pd.DataFrame(hist.data), use_container_width=True, hide_index=True)
        except Exception:
            pass

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
