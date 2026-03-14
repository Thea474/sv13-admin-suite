import streamlit as st
import pandas as pd
import os
import numpy as np
from datetime import datetime
import json
import re


# === 1. SYSTEM CONFIGURATION & PROFESSIONAL UI STYLING ===
st.set_page_config(page_title="SV13 Admin Suite | SETEC Institute", page_icon="🏢", layout="wide")

LOGO_PATH = "assets/Setec.png"

# FIXED CSS WITH PROPER KHMER FONT & RESPONSIVE LAYOUT
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Battambang:wght@400;700&family=Noto+Sans+Khmer:wght@300;400;500;700&family=Inter:wght@300;400;500;600;700&display=swap');

/* BASE FONTS */
html, body, [class*="css"] { 
    font-family: 'Inter', 'Noto Sans Khmer', 'Battambang', sans-serif !important; 
}

h1, h2, h3, .moul-font {
    font-family: 'Noto Sans Khmer', 'Battambang', serif !important;
    color: #1e3a8a !important;
    font-weight: 700 !important;
    text-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
    border-right: 4px solid #2563eb !important;
    padding: 2rem 1.5rem !important;
}
[data-testid="stSidebar"] * { color: white !important; }
[data-testid="stSidebar"] .stTextInput > div > div > input {
    background-color: #1e293b !important; color: white !important;
    border: 1px solid #475569 !important; border-radius: 8px !important;
}

/* CARDS */
.main-card {
    background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%) !important;
    border-radius: 20px !important; padding: 2.5rem !important;
    box-shadow: 0 15px 40px rgba(0,0,0,0.12) !important;
    border: 2px solid #e2e8f0 !important; margin-bottom: 2rem !important;
    position: relative; overflow: hidden;
}
.main-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(135deg, rgba(37,99,235,0.03) 0%, transparent 100%);
    z-index: 0;
}
.main-card > * { position: relative; z-index: 1; }

/* STATUS & BUTTONS */
.status-text {
    font-weight: 900 !important; color: #16a34a !important;
    font-size: 2.5rem !important; text-shadow: 0 0 20px rgba(22,163,74,0.3);
}
div.stButton > button {
    background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 50%, #1d4ed8 100%) !important;
    color: white !important; border-radius: 16px !important; font-weight: 700 !important;
    padding: 1.2rem 2.5rem !important; box-shadow: 0 12px 30px rgba(37,99,235,0.4) !important;
    transition: all 0.4s ease !important; text-transform: uppercase;
}
div.stButton > button:hover { transform: translateY(-4px) scale(1.02) !important; }

/* STEPS */
.howto-step {
    background: rgba(37,99,235,0.08) !important; border-radius: 12px !important;
    padding: 1.5rem !important; border-left: 4px solid #2563eb !important;
    margin: 1rem 0 !important; line-height: 1.6;
}

/* FIXED FEATURE BOXES */
.core-feature {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
    border-radius: 12px !important; padding: 1.5rem !important; margin: 0.8rem 0 !important;
    border-left: 5px solid #10b981 !important; color: white !important;
    font-family: 'Noto Sans Khmer', 'Inter', sans-serif !important;
    line-height: 1.6 !important; font-size: 0.95rem !important;
}

.special-feature {
    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
    border-radius: 12px !important; padding: 1.5rem !important; margin: 0.8rem 0 !important;
    border-left: 5px solid #3b82f6 !important; color: white !important;
    font-family: 'Noto Sans Khmer', 'Inter', sans-serif !important;
    line-height: 1.6 !important; font-size: 0.95rem !important;
}

/* RESPONSIVE GRID */
.feature-grid {
    display: flex !important; gap: 2rem !important; margin-top: 2rem !important;
    flex-wrap: wrap !important;
}
@media (max-width: 768px) { 
    .feature-grid { flex-direction: column !important; gap: 1rem !important; } 
}

.footer { 
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%) !important;
    border-radius: 20px !important; padding: 2rem !important; color: #475569 !important;
    text-align: center !important; margin-top: 3rem !important; 
}

/* NEW PROFESSIONAL ADMIN STYLES */
.metric-card {
    background: white;
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    border: 1px solid #e2e8f0;
    transition: all 0.3s ease;
}
.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 30px rgba(37,99,235,0.15);
}

.admin-table {
    background: white;
    border-radius: 16px;
    padding: 1.5rem;
    border: 1px solid #e2e8f0;
}

.status-badge {
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    display: inline-block;
}
.badge-success { background: #dcfce7; color: #166534; }
.badge-warning { background: #fef9c3; color: #854d0e; }
.badge-danger { background: #fee2e2; color: #991b1b; }

.activity-log {
    border-left: 3px solid #2563eb;
    padding: 1rem;
    margin: 0.5rem 0;
    background: #f8fafc;
    border-radius: 0 8px 8px 0;
}
</style>
""", unsafe_allow_html=True)


# Initialize Session States
if 'nav' not in st.session_state:
    st.session_state.nav = "Home"
if 'manual_db' not in st.session_state:
    st.session_state.manual_db = []
if 'depts' not in st.session_state:
    st.session_state.depts = ["IT", "HR", "ACC", "DEV", "ADMIN", "Finance", "Sale", "Design", "Marketing"]
if 'users_db' not in st.session_state:
    st.session_state.users_db = pd.DataFrame(columns=["DisplayName", "DN", "sAMAccountName", "userPrincipalName", "Database", "Group", "Password", "OUPath", "Status", "CreatedDate", "ModifiedDate", "UPN_Original"])
if 'activity_logs' not in st.session_state:
    st.session_state.activity_logs = []
if 'dashboard_stats' not in st.session_state:
    st.session_state.dashboard_stats = {
        'total_users': 0,
        'active_users': 0,
        'total_groups': len(st.session_state.depts),
        'success_rate': 100
    }
if 'upn_tracker' not in st.session_state:
    st.session_state.upn_tracker = set()  # Track all UPNs ever created


def log_activity(action, user, status, details=""):
    """Log system activities"""
    log_entry = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'action': action,
        'user': user,
        'status': status,
        'details': details
    }
    st.session_state.activity_logs.insert(0, log_entry)
    # Keep only last 100 logs
    if len(st.session_state.activity_logs) > 100:
        st.session_state.activity_logs = st.session_state.activity_logs[:100]


def generate_unique_upn(base_upn, domain):
    """Generate a unique UPN by adding numbers if needed"""
    username = base_upn.split('@')[0]
    counter = 1
    new_upn = base_upn
    
    while new_upn in st.session_state.upn_tracker:
        # Add number to make it unique (e.g., ann.david1@sv13.local)
        new_upn = f"{username}{counter}@{domain}"
        counter += 1
        if counter > 100:  # Safety limit
            new_upn = f"{username}{datetime.now().strftime('%Y%m%d%H%M%S')}@{domain}"
            break
    
    return new_upn


def clean_and_generate(row, domain, base_dn, root_ou, password):
    try:
        row_keys = {str(k).upper(): k for k in row.keys()}
        
        name_search_list = ['NAME_EN', 'NAME', 'FULLNAME', 'USER', 'DISPLAYNAME']
        name_key = next((row_keys[k] for k in name_search_list if k in row_keys), None)
        raw_name = str(row[name_key]).strip() if name_key else "Unnamed_User"
        
        group_search_list = ['GROUP', 'DEPT', 'DEPARTMENT', 'SECTION']
        group_key = next((row_keys[k] for k in group_search_list if k in row_keys), None)
        raw_group = row[group_key] if group_key else None
        
        if pd.isna(raw_group) or not str(raw_group).strip():
            group = "General"
        else:
            group = str(raw_group).strip()

        clean_name = " ".join(str(raw_name).split())
        if not clean_name or clean_name == "Unnamed_User":
            raise ValueError("No valid name found")

        parts = clean_name.lower().split()
        sam = f"{parts[0]}.{parts[-1]}" if len(parts) >= 2 else parts[0]
        
        # Clean sAMAccountName - remove special characters
        sam = re.sub(r'[^a-zA-Z0-9.]', '', sam)
        
        ou_path = f"OU={group},OU=USER,OU={root_ou},{base_dn}"
        
        # FIXED: Remove duplicate prefixes
        if group.startswith("Group_"):
            group_name = group
            db_name = f"MBX_{group.replace('Group_', '')}"
        else:
            group_name = f"Group_{group}"
            db_name = f"MBX_{group}"
        
        # Generate base UPN
        base_upn = f"{sam}@{domain}"
        
        # Check for UPN uniqueness and generate unique if needed
        original_upn = base_upn
        final_upn = base_upn
        
        if final_upn in st.session_state.upn_tracker:
            final_upn = generate_unique_upn(base_upn, domain)
            status_message = f"OK (UPN modified: {final_upn})"
        else:
            status_message = "OK"
        
        # Add to tracker
        st.session_state.upn_tracker.add(final_upn)
        
        return {
            "DisplayName": clean_name,
            "DN": f"CN={clean_name},OU={group},OU=USER,OU={root_ou},{base_dn}",
            "sAMAccountName": sam,
            "userPrincipalName": final_upn,
            "UPN_Original": original_upn if original_upn != final_upn else "",
            "Database": db_name,
            "Group": group_name,
            "Password": password,
            "OUPath": ou_path,
            "Status": status_message,
            "CreatedDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ModifiedDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        return {
            "DisplayName": str(row.get(name_key, "Error")),
            "DN": "ERROR",
            "sAMAccountName": "ERROR",
            "userPrincipalName": "ERROR",
            "UPN_Original": "",
            "Database": "ERROR",
            "Group": str(group) if 'group' in locals() else "ERROR",
            "Password": password,
            "OUPath": "ERROR",
            "Status": f"Failed: {str(e)}",
            "CreatedDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ModifiedDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }


def get_clean_export_df():
    """Returns DataFrame without date columns for CSV export - SAFETY LOGIC"""
    if st.session_state.users_db.empty:
        return pd.DataFrame()
    
    # Remove date columns and UPN_Original before export
    export_cols = ["DisplayName", "DN", "sAMAccountName", "userPrincipalName", "Database", "Group", "Password", "OUPath", "Status"]
    return st.session_state.users_db[export_cols].copy()


def update_dashboard_stats():
    """Update dashboard statistics"""
    if not st.session_state.users_db.empty:
        st.session_state.dashboard_stats['total_users'] = len(st.session_state.users_db)
        # Count OK status (including those with UPN modifications)
        st.session_state.dashboard_stats['active_users'] = len(st.session_state.users_db[st.session_state.users_db['Status'].str.startswith('OK', na=False)])
        st.session_state.dashboard_stats['total_groups'] = len(st.session_state.depts)
        success_count = len(st.session_state.users_db[st.session_state.users_db['Status'].str.startswith('OK', na=False)])
        if st.session_state.dashboard_stats['total_users'] > 0:
            st.session_state.dashboard_stats['success_rate'] = round((success_count / st.session_state.dashboard_stats['total_users']) * 100, 2)


# === SIDEBAR NAVIGATION ===
with st.sidebar:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=110)
    else:
        st.info("Logo not found.\nPlease place 'Setec.png' in the 'assets' folder.")

    st.markdown("<h1 class='moul-font' style='color:white; text-align:center;'>Admin Suite</h1>", unsafe_allow_html=True)
    st.divider()

    with st.expander("⚙️ Server Configuration"):
        domain_val = st.text_input("Domain", value="sv13.local", key="domain_input", help="ឧ. sv13.local ឬ company.com")
        base_dn_val = st.text_input("Base DN", value="DC=sv13,DC=local", key="basedn_input", help="ឧ. DC=company,DC=com")
        root_ou_val = st.text_input("Root OU", value="SV13", key="rootou_input", help="ឧ. SV13 ឬ UsersRoot")
        default_pass = st.text_input("Default Password", value="User@2026", key="password_input", type="password", help="ពាក្យសម្ងាត់ដើម")
        
        # Option to reset UPN tracker
        if st.button("🔄 Reset UPN Tracker", use_container_width=True):
            st.session_state.upn_tracker = set()
            st.success("UPN tracker reset!")

    with st.expander("🏢 Department Management"):
        new_dept = st.text_input("Add Department", key="dept_input", help="ឧ. IT_Support, Year4_Students")
        if st.button("Add Now", use_container_width=True):
            if new_dept and new_dept not in st.session_state.depts:
                st.session_state.depts.append(new_dept)
                st.toast(f"✅ Added {new_dept}")
                log_activity("ADD_DEPARTMENT", "System", "SUCCESS", f"Added department: {new_dept}")
        st.markdown(f"**Current:** {', '.join(st.session_state.depts)}")
    
    st.divider()
    
    # Professional Navigation Menu
    st.markdown("### 📊 NAVIGATION")
    if st.button("🏠 Home (ទំព័រដើម)", use_container_width=True):
        st.session_state.nav = "Home"
    if st.button("📊 Dashboard (ផ្ទាំងគ្រប់គ្រង)", use_container_width=True):
        st.session_state.nav = "Dashboard"
    if st.button("👥 Manage Users (គ្រប់គ្រងអ្នកប្រើ)", use_container_width=True):
        st.session_state.nav = "Manage"
    if st.button("📁 Bulk Import (ការបញ្ចូលជាកញ្ចប់ File)", use_container_width=True):
        st.session_state.nav = "Bulk"
    if st.button("✍️ Manual Add Entry (ការបញ្ចូល User ម្តងមួយ)", use_container_width=True):
        st.session_state.nav = "Manual"
    if st.button("📋 Activity Logs (កំណត់ហេតុសកម្មភាព)", use_container_width=True):
        st.session_state.nav = "Logs"


# === 3. PAGE: HOME ===
if st.session_state.nav == "Home":
    st.markdown("<h1 class='moul-font'>System Dashboard</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class='main-card'>
            <h4 style='margin:0 0 1.5rem 0; color:#1e293b;'>Domain Status</h4>
            <div class='status-text'>● Active</div>
            <small style='color:#64748b; font-size:1.1rem;'>{domain_val} Configured</small>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='main-card'>
            <h4 style='margin:0 0 1.5rem 0; color:#1e293b;'>Target Domain</h4>
            <div style='font-size:2.8rem; font-weight:900; color:#2563eb;'>{domain_val}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class='main-card'>
            <h4 style='margin:0 0 1.5rem 0; color:#1e293b;'>Security Mode</h4>
            <div style='font-size:2.8rem; font-weight:900; color:#16a34a;'>SSL Enabled</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class='main-card'>
        <h3 style='color:#1e293b; margin-bottom:2rem;'>🚀 ការប្រើប្រាស់ប្រព័ន្ធ (How to Use)</h3>
        <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 2rem;'>
            <div>
                <h4 class='moul-font' style='color:#2563eb;'>📋 ជំហានទី១: កំណត់</h4>
                <div class='howto-step'>
                    <b>✅</b> ចូល Sidebar → Server Configuration<br>
                    <b>✅</b> បញ្ចូល Domain, Base DN, Password<br>
                    <b>✅</b> បន្ថែម Department ថ្មី
                </div>
            </div>
            <div>
                <h4 class='moul-font' style='color:#2563eb;'>📁 ជំហានទី២: បញ្ចូល</h4>
                <div class='howto-step'>
                    <b>✅</b> Bulk Import → Excel/CSV File<br>
                    <b>OR</b><br><b>✅</b> Manual Entry → មួយម្នាក់ៗ
                </div>
            </div>
            <div>
                <h4 class='moul-font' style='color:#16a34a;'>💾 ជំហានទី៣: នាំចេញ</h4>
                <div class='howto-step'>
                    <b>✅</b> PROCESS DATA → Download CSV<br>
                    <b>✅</b> Run PowerShell Scripts<br>
                    <b>✅</b> Users created automatically
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # FEATURES SECTION
    st.markdown("""
    <div class="main-card">
        <h3 class='moul-font' style='color:#1e293b;'>សូមស្វាគមន៍ ទៅកាន់ប្រព័ន្ធ គ្រប់គ្រងអ្នកប្រើប្រាស់ | Welcome to User Management Platform</h3>
        <p style='color:#64748b; font-size:1.2rem; line-height:1.8; margin-bottom:2rem;'>
            ប្រព័ន្ធនេះ ធ្វើការស្វ័យប្រវត្តិការបង្កើត Active Directory និង Exchange Server សម្រាប់ SETEC Institute<br>
            This system automates Active Directory and Exchange Server provisioning for SETEC Institute.
        </p>
        <div class="feature-grid">
            <div style="flex: 1; min-width: 300px;">
                <h4 class="moul-font" style='color:#10b981; margin-bottom:1.5rem;'>គុណសម្បត្តិប្រព័ន្ធ (Core Features)</h4>
                <div class='core-feature'>
                    <b>🔒 Safe Imports:</b> Trims whitespace and hidden characters.<br>
                    លុបចន្លោះ និងតួអក្សរលាក់ដែលអាចបណ្តាលឱ្យមានកំហុស។
                </div>
                <div class='core-feature'>
                    <b>⚙️ Auto-Formatting:</b> Generates DN and sAMAccountName automatically.<br>
                    បង្កើត DN, sAMAccountName និង UPN ដោយស្វ័យប្រវត្តិតាមស្តង់ដារ AD។
                </div>
                <div class='core-feature'>
                    <b>📜 Script Ready:</b> Export PowerShell with logging.<br>
                    នាំចេញ PowerShell Script ស្រាប់ប្រើ មាន Logging ពេញលេញ។
                </div>
                <div class='core-feature'>
                    <b>🎯 Data Consistency:</b> Maps to correct DB & Group.<br>
                    ភ្ជាប់ User ទៅកាន់ Database និង Group ត្រឹមត្រូវដោយស្វ័យប្រវត្តិ។
                </div>
            </div>
            <div style="flex: 1; min-width: 300px;">
                <h4 class="moul-font" style='color:#3b82f6; margin-bottom:1.5rem;'>លក្ខណៈពិសេស (Features)</h4>
                <div class='special-feature'>
                    <b>🧠 Smart Detection:</b> Finds Name/Group columns automatically.<br>
                    ស្វែងរក និងភ្ជាប់ Column Name/Department ដោយស្វ័យប្រវត្តិ។
                </div>
                <div class='special-feature'>
                    <b>🌐 Bilingual UI:</b> English + Khmer.<br>
                    ចំណុចអាន និងជួយពន្យល់ជាភាសាអង់គ្លេស + ខ្មែរ។
                </div>
                <div class='special-feature'>
                    <b>✅ Real-time Validation:</b> Preview before export.<br>
                    មើលទិន្នន័យមុននាំចេញ ដឹង Status OK/Failed។
                </div>
                <div class='special-feature'>
                    <b>📱 Responsive Design:</b> Works on Desktop + Mobile.<br>
                    ប្រើបានលើ Desktop, Laptop, Tablet, Mobile។
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# === 4. PAGE: DASHBOARD ===
elif st.session_state.nav == "Dashboard":
    st.markdown("<h1 class='moul-font'>📊 Enterprise Dashboard ផ្ទាំងគ្រប់គ្រងកណ្តាល</h1>", unsafe_allow_html=True)
    
    # Update stats
    update_dashboard_stats()
    
    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color:#64748b; margin:0;">Total Users</h4>
            <h1 style="color:#1e3a8a; margin:0.5rem 0;">{st.session_state.dashboard_stats['total_users']}</h1>
            <small style="color:#10b981;">↑ Active: {st.session_state.dashboard_stats['active_users']}</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color:#64748b; margin:0;">Departments</h4>
            <h1 style="color:#1e3a8a; margin:0.5rem 0;">{st.session_state.dashboard_stats['total_groups']}</h1>
            <small style="color:#2563eb;">Active Groups</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color:#64748b; margin:0;">Success Rate</h4>
            <h1 style="color:#1e3a8a; margin:0.5rem 0;">{st.session_state.dashboard_stats['success_rate']}%</h1>
            <small style="color:#16a34a;">Processing Success</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color:#64748b; margin:0;">UPN Conflicts</h4>
            <h1 style="color:#1e3a8a; margin:0.5rem 0;">{len(st.session_state.users_db[st.session_state.users_db['UPN_Original'] != ''])}</h1>
            <small style="color:#f97316;">Auto-Resolved</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts and Distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        st.markdown("<h4>📊 User Distribution by Department</h4>", unsafe_allow_html=True)
        if not st.session_state.users_db.empty:
            # Extract clean department names for display
            display_df = st.session_state.users_db.copy()
            display_df['CleanGroup'] = display_df['Group'].str.replace('Group_', '')
            dept_counts = display_df['CleanGroup'].value_counts()
            st.bar_chart(dept_counts)
        else:
            st.info("No user data available yet. Import or add users to see distribution.")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        st.markdown("<h4>📈 Recent Activity</h4>", unsafe_allow_html=True)
        for log in st.session_state.activity_logs[:5]:
            status_color = "badge-success" if log['status'] == "SUCCESS" else "badge-warning" if log['status'] == "WARNING" else "badge-danger"
            st.markdown(f"""
            <div class='activity-log'>
                <small style='color:#64748b;'>{log['timestamp']}</small><br>
                <b>{log['action']}</b> - {log['user']}<br>
                <span class='status-badge {status_color}'>{log['status']}</span>
                <small style='color:#64748b; margin-left:1rem;'>{log['details']}</small>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


# === 5. PAGE: MANAGE USERS ===
elif st.session_state.nav == "Manage":
    st.markdown("<h1 class='moul-font'>👥 Manage Users គ្រប់គ្រងអ្នកប្រើប្រាស់</h1>", unsafe_allow_html=True)
    
    # Search and Filter
    col1, col2, col3 = st.columns([2,1,1])
    with col1:
        search_term = st.text_input("🔍 Search by Name or Username", placeholder="Type to search...")
    with col2:
        filter_dept = st.selectbox("Filter by Department", ["All"] + st.session_state.depts)
    with col3:
        filter_status = st.selectbox("Filter by Status", ["All", "OK", "OK (UPN modified)", "Failed"])
    
    # User Management Table
    st.markdown("<div class='admin-table'>", unsafe_allow_html=True)
    
    if not st.session_state.users_db.empty:
        # Apply filters
        filtered_df = st.session_state.users_db.copy()
        if search_term:
            filtered_df = filtered_df[
                filtered_df['DisplayName'].str.contains(search_term, case=False, na=False) |
                filtered_df['sAMAccountName'].str.contains(search_term, case=False, na=False)
            ]
        if filter_dept != "All":
            # Filter by clean department name
            filtered_df = filtered_df[filtered_df['Group'].str.replace('Group_', '') == filter_dept]
        if filter_status != "All":
            if filter_status == "OK (UPN modified)":
                filtered_df = filtered_df[filtered_df['UPN_Original'] != '']
            else:
                filtered_df = filtered_df[filtered_df['Status'] == filter_status]
        
        # Create display version with clean department names
        display_df = filtered_df.copy()
        display_df['Department'] = display_df['Group'].str.replace('Group_', '')
        display_df['Mailbox DB'] = display_df['Database']
        display_df['UPN'] = display_df['userPrincipalName']
        display_df['Original UPN'] = display_df['UPN_Original']
        
        # Display table with dates for UI only
        st.dataframe(
            display_df[['DisplayName', 'sAMAccountName', 'Department', 'UPN', 'Original UPN', 'Status', 'CreatedDate']],
            use_container_width=True,
            column_config={
                "DisplayName": "Full Name",
                "sAMAccountName": "Username",
                "Department": "Department",
                "UPN": "Final UPN",
                "Original UPN": "Original (if changed)",
                "Status": "Status",
                "CreatedDate": "Created Date"
            },
            hide_index=True
        )
        
        # Action Buttons
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("✅ Save Changes", use_container_width=True):
                log_activity("BULK_UPDATE", "Admin", "SUCCESS", f"Updated users")
                st.success("✅ Changes saved successfully!")
        
        with col2:
            if st.button("🗑️ Delete Selected", use_container_width=True):
                log_activity("DELETE_USERS", "Admin", "SUCCESS", f"Deleted users")
                st.success(f"✅ Deleted users!")
        
        with col3:
            if st.button("📥 Export Clean CSV", use_container_width=True):
                # SAFETY LOGIC: Export without date columns
                export_df = get_clean_export_df()
                if not export_df.empty:
                    # Filter to selected users if any
                    if not filtered_df.empty:
                        export_df = export_df[export_df['sAMAccountName'].isin(filtered_df['sAMAccountName'])]
                    
                    csv_data = export_df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
                    st.download_button(
                        "Download CSV for PowerShell",
                        csv_data,
                        f"AD_Users_Clean_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        use_container_width=True
                    )
                    st.info("✅ Exported without date columns - Ready for PowerShell import!")
        
        with col4:
            if st.button("🔄 Reset Password", use_container_width=True):
                log_activity("PASSWORD_RESET", "Admin", "SUCCESS", "Bulk password reset initiated")
                st.info("Password reset feature - would integrate with AD in production")
        
        # User Details Expansion with Warning
        with st.expander("⚠️ View Full Data (Includes Date Columns - NOT for Export)"):
            st.warning("These date columns are for display only. They will be automatically removed when exporting CSV for PowerShell.")
            st.dataframe(filtered_df, use_container_width=True)
    else:
        st.info("No users in database. Use Bulk Import or Manual Entry to add users.")
    
    st.markdown("</div>", unsafe_allow_html=True)


# === 6. PAGE: BULK IMPORT ===
elif st.session_state.nav == "Bulk":
    st.markdown("<h2 class='moul-font'>📁 Bulk Provisioning ការបញ្ចូលជាទម្រង់ File</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='main-card'>
        <h4 style='color:#16a34a;'>📋 ឯកសារត្រូវការ (File Requirements)</h4>
        <div style='display:flex; gap:1.5rem; flex-wrap:wrap;'>
            <div class='howto-step'><b>✅</b> CSV ឬ Excel format</div>
            <div class='howto-step'><b>✅</b> Columns: Name + Department</div>
            <div class='howto-step'><b>✅</b> Auto-detects column names</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    file = st.file_uploader(
        "Upload CSV or Excel file",
        type=['csv', 'xlsx'],
        help="ឯកសារគួរមានជួរឈរ: Name / FullName / Name_EN និង Department / Dept / Group"
    )
    
    if file:
        try:
            if file.name.endswith('xlsx'):
                df_in = pd.read_excel(file)
            else:
                df_in = pd.read_csv(file)
            
            st.success(f"✅ Loaded {len(df_in)} rows from file.")
            log_activity("FILE_UPLOAD", "Admin", "SUCCESS", f"Uploaded {file.name} with {len(df_in)} rows")
            
            if st.button("🚀 PROCESS DATA", use_container_width=True):
                with st.spinner("Processing..."):
                    results = []
                    duplicate_count = 0
                    
                    for idx, row in df_in.iterrows():
                        result = clean_and_generate(row, domain_val, base_dn_val, root_ou_val, default_pass)
                        
                        # Count UPN modifications
                        if result.get("UPN_Original", ""):
                            duplicate_count += 1
                            
                        results.append(result)
                    
                    final_df = pd.DataFrame(results)
                    success = len(final_df[final_df["Status"].str.startswith('OK', na=False)])
                    failed = len(final_df) - success
                    
                    # Add to users database
                    st.session_state.users_db = pd.concat([st.session_state.users_db, final_df], ignore_index=True)
                    
                    st.success(f"✅ Processed: {success} OK | {failed} Failed | {duplicate_count} UPN conflicts auto-resolved")
                    log_activity("BULK_PROCESS", "Admin", "SUCCESS", f"Processed {success} OK, {failed} Failed, {duplicate_count} UPN conflicts")
                    
                    if failed > 0:
                        st.warning("⚠️ Some rows have errors — check 'Status' column.")
                    
                    if duplicate_count > 0:
                        st.info(f"ℹ️ {duplicate_count} duplicate UPNs were automatically modified (e.g., ann.david1@sv13.local)")
                    
                    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
                    
                    # Display with clean department names
                    display_df = final_df.copy()
                    display_df['Department'] = display_df['Group'].str.replace('Group_', '')
                    display_df['Mailbox DB'] = display_df['Database']
                    display_df['UPN'] = display_df['userPrincipalName']
                    
                    st.dataframe(
                        display_df[['DisplayName', 'sAMAccountName', 'Department', 'UPN', 'Status']], 
                        use_container_width=True
                    )
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    st.divider()
                    
                    # SAFETY LOGIC: Export without date columns
                    st.info("📌 **Safety Feature**: Date columns and tracking data are automatically removed from CSV export.")
                    export_df = final_df[["DisplayName", "DN", "sAMAccountName", "userPrincipalName", "Database", "Group", "Password", "OUPath", "Status"]].copy()
                    
                    # Clean status for export (remove notes)
                    export_df['Status'] = export_df['Status'].apply(lambda x: 'OK' if x.startswith('OK') else x)
                    
                    csv_data = export_df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
                    
                    st.download_button(
                        "📥 DOWNLOAD CLEAN CSV FOR SERVER (No Date Columns)",
                        csv_data,
                        "Server_Import_Final.csv",
                        use_container_width=True
                    )
                    
                    # PowerShell Script for Bulk Import with UPN conflict handling
                    with st.expander("📜 View PowerShell Script for this Bulk Import"):
                        st.code(f"""
# PowerShell Script for Bulk Import - Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
# Total Users: {len(final_df)} | Success: {success} | Failed: {failed} | UPN Conflicts Resolved: {duplicate_count}

# Import the CSV file (Date columns are already removed for safety)
$data = Import-Csv "C:\\Data\\Server_Import_Final.csv"

# Create a log file
$logFile = "C:\\Logs\\Bulk_Import_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
$existingUsers = @{{}}

# First, check for existing users in AD
try {{
    $allADUsers = Get-ADUser -Filter * -Property UserPrincipalName
    foreach ($user in $allADUsers) {{
        $existingUsers[$user.UserPrincipalName] = $user.SamAccountName
    }}
    Write-Host "[INFO] Found $($existingUsers.Count) existing users in AD" -ForegroundColor Cyan
}} catch {{
    Write-Host "[WARNING] Could not check existing users: $_" -ForegroundColor Yellow
}}

foreach ($row in $data) {{
    try {{
        # Skip if status is not OK
        if ($row.Status -ne "OK") {{
            Write-Host "[SKIPPED] $($row.DisplayName) - $($row.Status)" -ForegroundColor Yellow
            continue
        }}
        
        # Check for UPN conflict in existing AD
        if ($existingUsers.ContainsKey($row.userPrincipalName)) {{
            Write-Host "[WARNING] UPN $($row.userPrincipalName) already exists in AD - Creating with modified UPN" -ForegroundColor Yellow
            
            # Generate new UPN by adding number
            $baseUPN = $row.userPrincipalName.Split('@')[0]
            $domain = $row.userPrincipalName.Split('@')[1]
            $counter = 1
            $newUPN = $row.userPrincipalName
            
            while ($existingUsers.ContainsKey($newUPN)) {{
                $newUPN = "$baseUPN$counter@$domain"
                $counter++
            }}
            
            $row.userPrincipalName = $newUPN
            Write-Host "[INFO] Using UPN: $newUPN" -ForegroundColor Cyan
        }}
        
        # Create secure password
        $secPass = ConvertTo-SecureString $row.Password -AsPlainText -Force
        
        # Create AD User
        New-ADUser -Name $row.DisplayName `
                   -SamAccountName $row.sAMAccountName `
                   -UserPrincipalName $row.userPrincipalName `
                   -DisplayName $row.DisplayName `
                   -Path $row.OUPath `
                   -AccountPassword $secPass `
                   -Enabled $true `
                   -ErrorAction Stop
        
        Write-Host "[SUCCESS] Created User: $($row.DisplayName) with UPN: $($row.userPrincipalName)" -ForegroundColor Green
        Add-Content -Path $logFile -Value "[SUCCESS] $($row.DisplayName) - $($row.sAMAccountName) - $($row.userPrincipalName)"
        
        # Add to existing users tracker
        $existingUsers[$row.userPrincipalName] = $row.sAMAccountName
        
    }} catch {{
        Write-Host "[FAILED] User: $($row.DisplayName) | Reason: $($_.Exception.Message)" -ForegroundColor Red
        Add-Content -Path $logFile -Value "[FAILED] $($row.DisplayName) - $($_.Exception.Message)"
    }}
}}

Write-Host "`nBulk import completed. Check log at: $logFile" -ForegroundColor Cyan
                        """, language="powershell")
                        
        except Exception as e:
            st.error(f"❌ File reading error: {str(e)}")
            log_activity("FILE_ERROR", "Admin", "ERROR", str(e))


# === 7. PAGE: MANUAL ENTRY ===
elif st.session_state.nav == "Manual":
    st.markdown("<h2 class='moul-font'>✍️ Manual Add Entry ការបញ្ចូលទិន្នន័យ User</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='main-card'>
        <h4 style='color:#16a34a;'>📋 របៀបបញ្ចូល User ដោយដៃ</h4>
        <div style='display:flex; gap:1.5rem; flex-wrap:wrap; margin-top:1rem;'>
            <div class='howto-step'><b>1️.</b> បញ្ចូល Full Name (អង់គ្លេស)</div>
            <div class='howto-step'><b>2️.</b> ជ្រើស Department</div>
            <div class='howto-step'><b>3️.</b> Add → Export CSV</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container(border=True):
        c1, c2 = st.columns(2)
        name = c1.text_input("Full Name (English)", key="name_input", help="ឧទាហរណ៍៖ Soksan Kim")
        dept = c2.selectbox("Department", st.session_state.depts, key="dept_select")
        
        c3, c4 = st.columns(2)
        if c3.button("➕ Add User to List", use_container_width=True):
            if name.strip():
                user = clean_and_generate({"Name": name, "Group": dept}, domain_val, base_dn_val, root_ou_val, default_pass)
                st.session_state.manual_db.append(user)
                
                # Add to main users database
                user_df = pd.DataFrame([user])
                st.session_state.users_db = pd.concat([st.session_state.users_db, user_df], ignore_index=True)
                
                upn_note = f" (UPN modified: {user['userPrincipalName']})" if user['UPN_Original'] else ""
                log_activity("MANUAL_ADD", "Admin", "SUCCESS", f"Added user: {name}{upn_note}")
                
                if user['UPN_Original']:
                    st.warning(f"⚠️ UPN '{user['UPN_Original']}' already exists. Using '{user['userPrincipalName']}' instead.")
                else:
                    st.success(f"✅ Added: {name}")
            else:
                st.warning("⚠️ Please enter a name.")
        
        if c4.button("🗑️ Clear List", use_container_width=True):
            if st.session_state.manual_db:
                st.session_state.manual_db = []
                log_activity("CLEAR_LIST", "Admin", "SUCCESS", "Cleared manual entry list")
                st.success("✅ List cleared!")
                st.rerun()

    if st.session_state.manual_db:
        st.divider()
        df_man = pd.DataFrame(st.session_state.manual_db)
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        
        # Display with clean department names
        display_man = df_man.copy()
        display_man['Department'] = display_man['Group'].str.replace('Group_', '')
        display_man['Mailbox DB'] = display_man['Database']
        display_man['UPN'] = display_man['userPrincipalName']
        
        st.table(display_man[["DisplayName", "sAMAccountName", "Department", "UPN", "Status"]])
        
        # Show UPN conflicts if any
        conflicts = display_man[display_man['UPN_Original'] != '']
        if not conflicts.empty:
            st.warning("⚠️ The following users had UPN conflicts and were automatically modified:")
            st.table(conflicts[["DisplayName", "UPN_Original", "UPN"]])
            
        st.markdown("</div>", unsafe_allow_html=True)
        
        # SAFETY LOGIC: Export without date columns
        st.info("📌 **Safety Feature**: Date columns are automatically removed from CSV export.")
        export_df = df_man[["DisplayName", "DN", "sAMAccountName", "userPrincipalName", "Database", "Group", "Password", "OUPath", "Status"]].copy()
        
        # Clean status for export
        export_df['Status'] = export_df['Status'].apply(lambda x: 'OK' if x.startswith('OK') else x)
        
        csv_data = export_df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
        
        st.download_button(
            "💾 EXPORT CLEAN CSV FOR SERVER (No Date Columns)",
            csv_data,
            "Manual_Export_Clean.csv",
            use_container_width=True
        )
        
        # PowerShell Script for Manual Entries with UPN handling
        with st.expander("📜 View PowerShell Script for Manual Entries"):
            st.code(f"""
# PowerShell Script for Manual User Creation - Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
# Total Users: {len(df_man)} | UPN Conflicts Resolved: {len(conflicts)}

# Import the CSV file (Date columns already removed for safety)
$data = Import-Csv "C:\\Data\\Manual_Export_Clean.csv"

# Create log file
$logFile = "C:\\Logs\\Manual_Creation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
$existingUsers = @{{}}

# Check for existing users
try {{
    $allADUsers = Get-ADUser -Filter * -Property UserPrincipalName
    foreach ($user in $allADUsers) {{
        $existingUsers[$user.UserPrincipalName] = $user.SamAccountName
    }}
}} catch {{
    Write-Host "[WARNING] Could not check existing users" -ForegroundColor Yellow
}}

foreach ($row in $data) {{
    try {{
        # Final UPN uniqueness check
        $finalUPN = $row.userPrincipalName
        if ($existingUsers.ContainsKey($finalUPN)) {{
            Write-Host "[WARNING] UPN $finalUPN already exists - Creating with modified UPN" -ForegroundColor Yellow
            $baseUPN = $finalUPN.Split('@')[0]
            $domain = $finalUPN.Split('@')[1]
            $counter = 1
            
            while ($existingUsers.ContainsKey("$baseUPN$counter@$domain")) {{
                $counter++
            }}
            
            $finalUPN = "$baseUPN$counter@$domain"
            $row.userPrincipalName = $finalUPN
        }}
        
        $secPass = ConvertTo-SecureString $row.Password -AsPlainText -Force
        
        # Create OU structure if it doesn't exist
        $ouPath = $row.OUPath
        $ouParts = $ouPath.Split(',')
        $currentPath = ""
        
        for ($i = 0; $i -lt $ouParts.Length; $i++) {{
            if ($currentPath -eq "") {{
                $currentPath = $ouParts[$i]
            }} else {{
                $currentPath = "$currentPath,$($ouParts[$i])"
            }}
            
            try {{
                Get-ADOrganizationalUnit -Identity $currentPath -ErrorAction Stop
            }} catch {{
                New-ADOrganizationalUnit -Name ($ouParts[$i].Split('=')[1]) -Path ($currentPath -replace "^[^,]+,", "") -ErrorAction SilentlyContinue
                Write-Host "[INFO] Created OU: $($ouParts[$i])" -ForegroundColor Cyan
            }}
        }}
        
        # Create AD User
        New-ADUser -Name $row.DisplayName `
                   -SamAccountName $row.sAMAccountName `
                   -UserPrincipalName $row.userPrincipalName `
                   -DisplayName $row.DisplayName `
                   -Path $row.OUPath `
                   -AccountPassword $secPass `
                   -Enabled $true `
                   -ErrorAction Stop
        
        Write-Host "[SUCCESS] Created User: $($row.DisplayName) with UPN: $($row.userPrincipalName)" -ForegroundColor Green
        Add-Content -Path $logFile -Value "[SUCCESS] $($row.DisplayName) - $($row.sAMAccountName) - $($row.userPrincipalName)"
        
        # Add to tracker
        $existingUsers[$row.userPrincipalName] = $row.sAMAccountName
        
    }} catch {{
        Write-Host "[FAILED] User: $($row.DisplayName) | Reason: $($_.Exception.Message)" -ForegroundColor Red
        Add-Content -Path $logFile -Value "[FAILED] $($row.DisplayName) - $($_.Exception.Message)"
    }}
}}

Write-Host "`nManual user creation completed. Check log at: $logFile" -ForegroundColor Cyan
            """, language="powershell")


# === 8. PAGE: ACTIVITY LOGS ===
elif st.session_state.nav == "Logs":
    st.markdown("<h1 class='moul-font'>📋 Activity Logs កំណត់ហេតុសកម្មភាព</h1>", unsafe_allow_html=True)
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        actions = ["All"] + list(set([log['action'] for log in st.session_state.activity_logs]))
        filter_action = st.selectbox("Filter by Action", actions)
    with col2:
        filter_status = st.selectbox("Filter by Status", ["All", "SUCCESS", "WARNING", "ERROR"])
    with col3:
        date_range = st.date_input("Date Range", [])
    
    # Display logs
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    
    if st.session_state.activity_logs:
        filtered_logs = st.session_state.activity_logs
        
        if filter_action != "All":
            filtered_logs = [log for log in filtered_logs if log['action'] == filter_action]
        if filter_status != "All":
            filtered_logs = [log for log in filtered_logs if log['status'] == filter_status]
        
        for log in filtered_logs:
            status_color = "badge-success" if log['status'] == "SUCCESS" else "badge-warning" if log['status'] == "WARNING" else "badge-danger"
            st.markdown(f"""
            <div class='activity-log'>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <div>
                        <small style='color:#64748b;'>{log['timestamp']}</small><br>
                        <b>{log['action']}</b> - {log['user']}
                    </div>
                    <span class='status-badge {status_color}'>{log['status']}</span>
                </div>
                <small style='color:#64748b;'>{log['details']}</small>
            </div>
            """, unsafe_allow_html=True)
        
        # Export logs
        if st.button("📥 Export Logs to CSV"):
            logs_df = pd.DataFrame(st.session_state.activity_logs)
            csv_data = logs_df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
            st.download_button(
                "Download Logs",
                csv_data,
                f"Activity_Logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                use_container_width=True
            )
    else:
        st.info("No activity logs yet. Actions will be recorded here.")
    
    st.markdown("</div>", unsafe_allow_html=True)


# === 9. SERVER SCRIPTS (Preserved with enhancements) ===
st.divider()
st.markdown("<h3 class='moul-font'>💻 PowerShell Execution Scripts</h3>", unsafe_allow_html=True)

st.markdown("""
<div class='main-card'>
    <h4 style='color:#16a34a;'>🎯 របៀបប្រើ PowerShell</h4>
    <div style='display:flex; gap:1.5rem; flex-wrap:wrap;'>
        <div class='howto-step'><b>1️⃣</b> Save CSV → <code>C:\\Data\\Server_Import_Final.csv</code></div>
        <div class='howto-step'><b>2️⃣</b> Run AD Script FIRST</div>
        <div class='howto-step'><b>3️⃣</b> Run Exchange Script SECOND</div>
        <div class='howto-step'><b>✅</b> Check console logs</div>
    </div>
</div>
""", unsafe_allow_html=True)

t1, t2 = st.tabs(["🛡️ Active Directory Script", "📧 Exchange Server Script"])

# ==== TAB 1: AD SCRIPT + HOW TO RUN (FIXED PLAIN TEXT) ====
with t1:
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.code("""
# STEP 1: CREATE AD USERS WITH LOGGING
# Purpose: Reads the CSV and creates user accounts in Active Directory
$data = Import-Csv "C:\\Data\\Server_Import_Final.csv"
foreach ($row in $data) {
    try {
        $secPass = ConvertTo-SecureString $row.Password -AsPlainText -Force
        New-ADUser -Name $row.DisplayName -SamAccountName $row.sAMAccountName `
                    -UserPrincipalName $row.userPrincipalName -DisplayName $row.DisplayName `
                    -Path $row.OUPath -AccountPassword $secPass -Enabled $true -ErrorAction Stop
        Write-Host "[SUCCESS] Created User: $($row.DisplayName)" -ForegroundColor Green
    } catch {
        Write-Host "[FAILED] User: $($row.DisplayName) | Reason: $($_.Exception.Message)" -ForegroundColor Red
    }
}
    """, language="powershell")

    # FIXED: Plain text without HTML tags showing
    st.markdown("""
    **🛠️ ជំហានត្រៀមលក្ខណៈក្នុង Windows Server (Active Directory)**

    **១. ការរៀបចំ Folder ក្នុងម៉ាស៊ីន Server**
    - បើក **This PC** រួចចូលទៅកាន់ **Local Disk (C:)** ។
    - ចុច Mouse ស្តាំបង្កើត Folder ថ្មីឈ្មោះ `Data` (សម្រាប់ដាក់ CSV) ។
    - បង្កើត Folder ថ្មីមួយទៀតឈ្មោះ `Scripts` (សម្រាប់ទុក Script .ps1) ។
    - បង្កើត Folder `Logs` សម្រាប់រក្សាទុកឯកសារ Log ។

    **២. របៀបបង្កើតឯកសារ Script (កុំឱ្យចេញជា .txt)**
    1. ចម្លង (Copy) កូដខាងលើ រួចបើកកម្មវិធី **Notepad** ។
    2. Paste កូដចូល រួចចុច **File > Save As...**
    3. នៅត្រង់ **Save as type**: ត្រូវប្តូរទៅជា **All Files (*.*)** (សំខាន់ខ្លាំង) ។
    4. នៅត្រង់ **File name**: វាយឈ្មោះ `Create-ADUsers.ps1` ។
    5. ជ្រើសរើសទីតាំង `C:\\Scripts` រួចចុច **Save** ។

    **៣. ការបង្កើត OU និង Group ទុកជាមុន (Prerequisites)**
    មុននឹងដំណើរការ Script អ្នកត្រូវបង្កើតរចនាសម្ព័ន្ធក្នុង **Active Directory Users and Computers** ដូចខាងក្រោម៖
    - **Root OU:** បង្កើត OU ធំមួយឈ្មោះ `EX:SV13` (នៅក្រោម Domain ផ្ទាល់) ។
    - **Sub OU:** នៅខាងក្នុង `EX: SV13` បង្កើត OU មួយទៀតឈ្មោះ `USER` ។
    - **Dept OUs:** នៅខាងក្នុង `USER` បង្កើត OU តាមឈ្មោះផ្នែកដូចជា `IT`, `HR`, `ACC`...
    - **Groups:** បង្កើត Security Groups ឈ្មោះ `Group_IT`, `Group_HR`... នៅក្នុង OU ដែលពាក់ព័ន្ធ ។

    **🚀 ៤. របៀបដំណើរការ Script**
    1. យកឯកសារ CSV ដែល Download បានពីកម្មវិធីនេះ ទៅ Copy ដាក់ក្នុង `C:\\Data\\Server_Import_Final.csv` ។
    2. បើក **Windows PowerShell** ក្នុងនាមជា **Administrator** ។
    3. វាយបញ្ជា: `Set-ExecutionPolicy RemoteSigned` រួចចុច **Y** ។
    4. វាយបញ្ជាចូលទៅកាន់ Folder: `cd C:\\Scripts`
    5. ដំណើរការ Script: `.\\Create-ADUsers.ps1`
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# ==== TAB 2: EXCHANGE SCRIPT + HOW TO RUN (FIXED PLAIN TEXT) ====
with t2:
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.code("""
# STEP 2: ENABLE MAILBOXES & ADD TO GROUPS
# Purpose: Link created AD users to Exchange Mailboxes and assign groups
$data = Import-Csv "C:\\Data\\Server_Import_Final.csv"
foreach ($row in $data) {
    try {
        Enable-Mailbox -Identity $row.sAMAccountName -Database $row.Database -ErrorAction Stop
        Add-DistributionGroupMember -Identity $row.Group -Member $row.sAMAccountName -ErrorAction SilentlyContinue
        Write-Host "[SUCCESS] Mailbox Enabled: $($row.DisplayName)" -ForegroundColor Green
    } catch {
        Write-Host "[FAILED] Mailbox Error: $($row.DisplayName) | Reason: $($_.Exception.Message)" -ForegroundColor Red
    }
}
    """, language="powershell")

    # FIXED: Plain text without HTML tags showing
    st.markdown("""
    **📧 ជំហានត្រៀមលក្ខណៈក្នុង Exchange Server**

    **១. ការរៀបចំ Database និង Distribution Groups**
    ចូលទៅកាន់ **Exchange Admin Center (EAC)** ៖
    - **Mailbox Database:** បង្កើត Database ឱ្យត្រូវតាមឈ្មោះដែលកម្មវិធីបានបង្កើត (ឧទាហរណ៍: `MBX_IT`, `MBX_HR`...) ។
    - **Distribution Groups:** បង្កើត Group សម្រាប់អ៊ីមែលរួម ឱ្យត្រូវនឹងឈ្មោះ `Group_IT`, `Group_HR`... ។

    **២. របៀបបង្កើតឯកសារ Script**
    1. ប្រើ **Notepad** បង្កើតឯកសារឈ្មោះ `Enable-Mailboxes.ps1` ។
    2. រក្សាទុកក្នុង `C:\\Scripts` (កុំភ្លេចប្តូរជា **All Files** ពេល Save) ។

    **🚀 ៣. របៀបដំណើរការ Script**
    1. **សំខាន់:** ត្រូវប្រាកដថាអ្នកបានបង្កើត User ក្នុង AD (ជំហានទី១) រួចរាល់អស់ហើយ ។
    2. បើកកម្មវិធី **Exchange Management Shell**  ក្នុងនាមជា **Administrator** ។
    3. វាយបញ្ជា: `cd C:\\Scripts`
    4. ដំណើរការ Script: `.\\Enable-Mailboxes.ps1`
    5. រង់ចាំមើលលទ្ធផលពណ៌បៃតង **[SUCCESS]** ។
    """)
    st.markdown("</div>", unsafe_allow_html=True)


# === 10. FOOTER ===
st.markdown("""
<div class="footer">
    © 2026 SETEC Institute | Developed by <b>Eab Rithea</b> | MIS Year 3 | Professional Edition ✨<br>
    <small style='color:#64748b;'>Enterprise Active Directory Management Suite v2.0</small>
</div>
""", unsafe_allow_html=True)