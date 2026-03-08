import streamlit as st
import pandas as pd
import os
import numpy as np


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
</style>
""", unsafe_allow_html=True)


# Initialize Session States
if 'nav' not in st.session_state:
    st.session_state.nav = "Home"
if 'manual_db' not in st.session_state:
    st.session_state.manual_db = []
if 'depts' not in st.session_state:
    st.session_state.depts = ["IT", "HR", "ACC", "DEV", "ADMIN", "Finance", "Sale", "Design", "Marketing"]


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
        ou_path = f"OU={group},OU=USER,OU={root_ou},{base_dn}"
        
        return {
            "DisplayName": clean_name,
            "DN": f"CN={clean_name},OU={group},OU=USER,OU={root_ou},{base_dn}",
            "sAMAccountName": sam,
            "userPrincipalName": f"{sam}@{domain}",
            "Database": f"MBX_{group}",
            "Group": f"Group_{group}",
            "Password": password,
            "OUPath": ou_path,
            "Status": "OK"
        }
    except Exception as e:
        return {
            "DisplayName": str(row.get(name_key, "Error")),
            "DN": "ERROR",
            "sAMAccountName": "ERROR",
            "userPrincipalName": "ERROR",
            "Database": "ERROR",
            "Group": str(group) if 'group' in locals() else "ERROR",
            "Password": password,
            "OUPath": "ERROR",
            "Status": f"Failed: {str(e)}"
        }


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

    with st.expander("🏢 Department Management"):
        new_dept = st.text_input("Add Department", key="dept_input", help="ឧ. IT_Support, Year4_Students")
        if st.button("Add Now", use_container_width=True):
            if new_dept and new_dept not in st.session_state.depts:
                st.session_state.depts.append(new_dept)
                st.toast(f"✅ Added {new_dept}")
        st.markdown(f"**Current:** {', '.join(st.session_state.depts)}")
    
    st.divider()
    if st.button("🏠 Home (ទំព័រដើម)", use_container_width=True):
        st.session_state.nav = "Home"
    if st.button("📁 Bulk Import (ការបញ្ចូលជាកញ្ចប់ File)", use_container_width=True):
        st.session_state.nav = "Bulk"
    if st.button("✍️ Manual Add Entry (ការបញ្ចូល User ម្តងមួយ)", use_container_width=True):
        st.session_state.nav = "Manual"


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


# === 4. PAGE: BULK IMPORT ===
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
            
            if st.button("🚀 PROCESS DATA", use_container_width=True):
                with st.spinner("Processing..."):
                    results = []
                    for idx, row in df_in.iterrows():
                        result = clean_and_generate(row, domain_val, base_dn_val, root_ou_val, default_pass)
                        results.append(result)
                    
                    final_df = pd.DataFrame(results)
                    success = len(final_df[final_df["Status"] == "OK"])
                    failed = len(final_df) - success
                    st.success(f"✅ Processed: {success} OK | {failed} Failed")
                    
                    if failed > 0:
                        st.warning("⚠️ Some rows have errors — check 'Status' column.")
                    
                    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
                    st.dataframe(final_df, use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True) # FIXED HERE: FROM st.markmarkdown TO st.markdown
                    
                    st.divider()
                    csv_data = final_df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
                    st.download_button(
                        "📥 DOWNLOAD CLEANED CSV FOR SERVER",
                        csv_data,
                        "Server_Import_Final.csv",
                        use_container_width=True
                    )
        except Exception as e:
            st.error(f"❌ File reading error: {str(e)}")


# === 5. PAGE: MANUAL ENTRY ===
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
                st.success(f"✅ Added: {name}")
            else:
                st.warning("⚠️ Please enter a name.")
        
        if c4.button("🗑️ Clear List", use_container_width=True):
            if st.session_state.manual_db:
                st.session_state.manual_db = []
                st.success("✅ List cleared!")
                st.rerun()

    if st.session_state.manual_db:
        st.divider()
        df_man = pd.DataFrame(st.session_state.manual_db)
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        st.table(df_man[["DisplayName", "sAMAccountName", "Group", "Database", "Status"]])
        st.markdown("</div>", unsafe_allow_html=True)
        
        csv_data = df_man.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
        st.download_button(
            "💾 EXPORT MANUAL LIST TO CSV",
            csv_data,
            "Manual_Export.csv",
            use_container_width=True
        )


# === 6. SERVER SCRIPTS ===
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

# ==== TAB 1: AD SCRIPT + HOW TO RUN ====
with t1:
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.code("""
# STEP 1: CREATE AD USERS WITH LOGGING
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

    st.markdown("""
    <div class='howto-step'>
        <b>🔧 How to run this AD script (Windows Server):</b><br>
        1. Copy the script above and save it as <code>Create-ADUsers.ps1</code> on your AD server (e.g. <code>C:\\Scripts\\Create-ADUsers.ps1</code>).<br>
        2. Open <b>Windows PowerShell</b> as <b>Administrator</b> on the Domain Controller.<br>
        3. Make sure the <b>ActiveDirectory</b> module is installed, then run: <code>Import-Module ActiveDirectory</code>.<br>
        4. If scripts are blocked, run: <code>Set-ExecutionPolicy RemoteSigned</code> (then press Y).<br>
        5. Ensure the CSV is located at <code>C:\\Data\\Server_Import_Final.csv</code> as shown above.<br>
        6. Navigate to the script folder: <code>cd C:\\Scripts</code>.<br>
        7. Run the script: <code>.\Create-ADUsers.ps1</code> and watch the console for SUCCESS / FAILED messages.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ==== TAB 2: EXCHANGE SCRIPT + HOW TO RUN ====
with t2:
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.code("""
# STEP 2: ENABLE MAILBOXES & ADD TO GROUPS
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

    st.markdown("""
    <div class='howto-step'>
        <b>📧 How to run this Exchange script:</b><br>
        1. Save the script above as <code>Enable-Mailboxes.ps1</code> on your Exchange Server (e.g. <code>C:\\Scripts\\Enable-Mailboxes.ps1</code>).<br>
        2. Open the <b>Exchange Management Shell</b> as <b>Administrator</b> (or a PowerShell window connected to Exchange).<br>
        3. Confirm the CSV file is at <code>C:\\Data\\Server_Import_Final.csv</code> and matches the exported columns.<br>
        4. Navigate to the script folder: <code>cd C:\\Scripts</code>.<br>
        5. If needed, allow scripts: <code>Set-ExecutionPolicy RemoteSigned</code> and press Y.<br>
        6. Run the script: <code>.\Enable-Mailboxes.ps1</code>.<br>
        7. Monitor the output: each user will show SUCCESS or FAILED with the error reason.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


st.markdown("""
<div class="footer">
    © 2026 SETEC Institute | Developed by <b>Eab Rithea</b> | MIS Year 3 | Professional Edition ✨
</div>
""", unsafe_allow_html=True)