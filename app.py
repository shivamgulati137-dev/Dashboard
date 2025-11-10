import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os
import shutil
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="Urban Svamitva Dashboard - Ludhiana MCL",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional government dashboard appearance
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f4788;
        text-align: center;
        padding: 1rem 0;
        border-bottom: 3px solid #1f4788;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f4788;
    }
    .status-completed {
        color: #28a745;
        font-weight: bold;
    }
    .status-ontrack {
        color: #ffc107;
        font-weight: bold;
    }
    .status-behind {
        color: #dc3545;
        font-weight: bold;
    }
    .stButton>button {
        background-color: #1f4788;
        color: white;
        border-radius: 0.3rem;
    }
    .sidebar-credit {
        text-align: center;
        color: #6c757d;
        font-size: 0.85rem;
        padding: 1rem 0;
        margin-top: 2rem;
        border-top: 1px solid #e0e0e0;
    }
    .reload-section {
        padding: 1rem 0;
    }
    /* Mobile-friendly table styles */
    @media screen and (max-width: 768px) {
        .main-header {
            font-size: 1.5rem;
            padding: 0.5rem 0;
        }
        /* Make tables scrollable on mobile */
        div[data-testid="stDataFrame"] {
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
        }
        /* Optimize table cells for mobile */
        div[data-testid="stDataFrame"] table {
            font-size: 0.85rem;
            width: 100%;
        }
        div[data-testid="stDataFrame"] th,
        div[data-testid="stDataFrame"] td {
            padding: 0.4rem 0.3rem;
            white-space: nowrap;
        }
        /* Reduce column width on mobile */
        .stMetric {
            padding: 0.5rem;
        }
    }
    /* Optimize dataframe rendering */
    div[data-testid="stDataFrame"] {
        border-radius: 0.5rem;
    }
    /* Improve table performance */
    div[data-testid="stDataFrame"] table {
        border-collapse: collapse;
    }
    /* Optimize scrolling performance on mobile */
    @media screen and (max-width: 768px) {
        div[data-testid="stDataFrame"] {
            will-change: scroll-position;
            transform: translateZ(0);
            -webkit-transform: translateZ(0);
        }
        /* Reduce font size for better performance */
        div[data-testid="stDataFrame"] td,
        div[data-testid="stDataFrame"] th {
            font-size: 0.8rem;
        }
        /* Optimize metric cards for mobile */
        [data-testid="stMetricValue"] {
            font-size: 1.2rem;
        }
        [data-testid="stMetricLabel"] {
            font-size: 0.75rem;
        }
    }
    /* Reduce reflow/repaint */
    div[data-testid="stDataFrame"] {
        contain: layout style paint;
    }
    </style>
""", unsafe_allow_html=True)

# File paths
VILLAGES_DATA = "villages_data.csv"
PROGRESS_DATA = "progress_data.csv"
RESPONSIBILITY_DATA = "responsibility_data.csv"
REMARKS_DATA = "remarks_data.csv"

# Initialize data files if they don't exist
def initialize_data_files():
    """Create sample data files if they don't exist"""
    
    if not os.path.exists(VILLAGES_DATA):
        sample_villages = {
            'Village_Name': ['Village A', 'Village B', 'Village C', 'Village D', 'Village E', 
                           'Village F', 'Village G', 'Village H', 'Village I', 'Village J',
                           'Village K', 'Village L', 'Village M', 'Village N', 'Village O'],
            'Municipal_Zone': ['A', 'A', 'B', 'B', 'B', 'C', 'C', 'C', 'D', 'D', 'A', 'B', 'C', 'D', 'A'],
            'Current_Phase': ['Card Issuance', 'Map 3', 'Objections Hearing', 'Pasting', 'Map 2 awaited',
                            'Ground Truthing Pending', 'Map 1 awaited', 'Drone Survey Pending', 'Notification', 'Drone Survey Pending',
                            'Map 3', 'Pasting', 'Map 2 awaited', 'Ground Truthing Pending', 'Objections Hearing'],
            'Status': ['Completed', 'On Track', 'On Track', 'Behind Schedule', 'On Track',
                      'On Track', 'Behind Schedule', 'On Track', 'On Track', 'On Track',
                      'On Track', 'Behind Schedule', 'On Track', 'On Track', 'On Track'],
            'Last_Updated': pd.to_datetime(['2024-01-15', '2024-01-10', '2024-01-08', '2024-01-05',
                                           '2024-01-12', '2024-01-07', '2024-01-03', '2024-01-09',
                                           '2024-01-11', '2024-01-06', '2024-01-13', '2024-01-04',
                                           '2024-01-14', '2024-01-02', '2024-01-01']),
            'HDM_JDM': ['Mr. Sharma', 'Mr. Sharma', 'Mr. Kumar', 'Mr. Kumar', 'Mr. Kumar',
                        'Ms. Patel', 'Ms. Patel', 'Ms. Patel', 'Mr. Singh', 'Mr. Singh',
                        'Mr. Sharma', 'Mr. Kumar', 'Ms. Patel', 'Mr. Singh', 'Mr. Sharma'],
            'ATP_MTP': ['Mr. Verma', 'Mr. Verma', 'Ms. Reddy', 'Ms. Reddy', 'Ms. Reddy',
                       'Mr. Gupta', 'Mr. Gupta', 'Mr. Gupta', 'Ms. Iyer', 'Ms. Iyer',
                       'Mr. Verma', 'Ms. Reddy', 'Mr. Gupta', 'Ms. Iyer', 'Mr. Verma'],
            'ARRO_Officer': ['Mr. Joshi', 'Mr. Joshi', 'Mr. Rao', 'Mr. Rao', 'Mr. Rao',
                            'Ms. Desai', 'Ms. Desai', 'Ms. Desai', 'Mr. Nair', 'Mr. Nair',
                            'Mr. Joshi', 'Mr. Rao', 'Ms. Desai', 'Mr. Nair', 'Mr. Joshi'],
            'Total_Properties': [250, 180, 320, 150, 280, 200, 170, 220, 190, 240, 260, 210, 230, 160, 270],
            'Survey_Date': pd.to_datetime(['2023-01-15', '2023-02-20', '2023-03-10', '2023-04-05',
                                          '2023-05-12', '2023-06-18', '2023-07-22', '2023-08-15',
                                          '2023-09-08', '2023-10-20', '2023-11-05', '2023-12-10',
                                          '2023-01-25', '2023-02-28', '2023-03-15']),
            'Notification_Date': pd.to_datetime(['2022-12-01', '2023-01-15', '2023-02-20', '2023-03-10',
                                                 '2023-04-05', '2023-05-12', '2023-06-18', '2023-07-22',
                                                 '2023-08-15', '2023-09-08', '2023-10-20', '2023-11-05',
                                                 '2023-12-10', '2022-12-15', '2023-01-20']),
            'Drone_Survey_Date': pd.to_datetime(['2023-01-20', '2023-02-25', '2023-03-15', '2023-04-10',
                                                 '2023-05-18', '2023-06-23', '2023-07-27', '2023-08-20',
                                                 '2023-09-13', '2023-10-25', '2023-11-10', '2023-12-15',
                                                 '2023-01-30', '2023-03-05', '2023-03-20']),
            'Map1_Date': pd.to_datetime(['2023-02-15', '2023-03-20', '2023-04-15', '2023-05-10',
                                        '2023-06-18', '2023-07-25', None, '2023-09-15', None, '2023-11-20',
                                        '2023-12-05', None, None, None, None]),
            'Ground_Truthing_Date': pd.to_datetime(['2023-03-01', '2023-04-05', '2023-05-01', '2023-05-28',
                                                   '2023-07-05', None, None, None, None, None,
                                                   None, None, None, None, None]),
            'Map2_Date': pd.to_datetime(['2023-04-01', '2023-05-10', None, None, None,
                                        None, None, None, None, None, None, None, None, None, None]),
            'Pasting_Start_Date': pd.to_datetime(['2023-06-01', None, None, None, None,
                                                 None, None, None, None, None, None, None, None, None, None]),
            'Objections_Date': pd.to_datetime(['2023-09-01', None, None, None, None,
                                              None, None, None, None, None, None, None, None, None, None]),
            'Map3_Date': pd.to_datetime(['2023-10-01', None, None, None, None,
                                        None, None, None, None, None, None, None, None, None, None]),
            'Cards_Issued_Date': pd.to_datetime(['2023-11-15', None, None, None, None,
                                                None, None, None, None, None, None, None, None, None, None])
        }
        df = pd.DataFrame(sample_villages)
        df.to_csv(VILLAGES_DATA, index=False)
    
    if not os.path.exists(PROGRESS_DATA):
        sample_progress = {
            'Phase': ['Notification', 'Drone Survey Pending', 'Map 1 awaited', 'Ground Truthing Pending', 'Map 2 awaited',
                     'Pasting', 'Objections Hearing', 'Map 3', 'Card Issuance'],
            'Completed': [15, 15, 13, 11, 9, 7, 5, 3, 1],
            'Target': [15, 15, 15, 15, 15, 15, 15, 15, 15],
            'Avg_Duration_Days': [0, 25, 15, 30, 20, 90, 45, 30, 45],
            'Responsible_Department': ['DC Administration', 'Survey of India', 'Survey of India',
                                      'Property Tax Dept (HDM/JDM)', 'Survey of India', 'ATP/MTP',
                                      'ARRO', 'Survey of India', 'DC Administration'],
            'Primary_Contact': ['DC Office', 'SOI Regional Office', 'SOI Regional Office',
                               'Property Tax HOD', 'SOI Regional Office', 'ATP Coordinator',
                               'ARRO Office', 'SOI Regional Office', 'DC Office']
        }
        df = pd.DataFrame(sample_progress)
        df.to_csv(PROGRESS_DATA, index=False)
    
    if not os.path.exists(RESPONSIBILITY_DATA):
        sample_responsibility = {
            'Phase': ['Notification', 'Drone Survey Pending', 'Map 1 awaited', 'Ground Truthing Pending', 'Map 2 awaited',
                     'Pasting', 'Objections Hearing', 'Map 3', 'Card Issuance'],
            'Responsible_Department': ['DC Administration', 'Survey of India', 'Survey of India',
                                      'Property Tax Dept (HDM/JDM)', 'Survey of India', 'ATP/MTP',
                                      'ARRO', 'Survey of India', 'DC Administration'],
            'Primary_Contact': ['DC Office', 'SOI Regional Office', 'SOI Regional Office',
                               'Property Tax HOD', 'SOI Regional Office', 'ATP Coordinator',
                               'ARRO Office', 'SOI Regional Office', 'DC Office'],
            'Contact_Info': ['dc.ludhiana@punjab.gov.in', 'soi.ludhiana@nic.in', 'soi.ludhiana@nic.in',
                            'proptax.ludhiana@punjab.gov.in', 'soi.ludhiana@nic.in', 'atp.ludhiana@punjab.gov.in',
                            'arro.ludhiana@punjab.gov.in', 'soi.ludhiana@nic.in', 'dc.ludhiana@punjab.gov.in']
        }
        df = pd.DataFrame(sample_responsibility)
        df.to_csv(RESPONSIBILITY_DATA, index=False)
    
    if not os.path.exists(REMARKS_DATA):
        # Create empty remarks file with headers
        remarks_columns = ['Date', 'Official_Name', 'Department', 'Phase', 'Village', 'Remarks', 'Help_Required', 'Status', 'Response']
        df = pd.DataFrame(columns=remarks_columns)
        df.to_csv(REMARKS_DATA, index=False)

@st.cache_data
def load_villages_data():
    """Load villages data from CSV"""
    try:
        df = pd.read_csv(VILLAGES_DATA)
        # Convert date columns to datetime
        date_columns = ['Last_Updated', 'Survey_Date', 'Notification_Date', 'Drone_Survey_Date',
                       'Map1_Date', 'Ground_Truthing_Date', 'Map2_Date', 'Pasting_Start_Date',
                       'Objections_Date', 'Map3_Date', 'Cards_Issued_Date']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce', format='mixed')
        return df
    except Exception as e:
        st.error(f"Error loading villages data: {str(e)}")
        return pd.DataFrame()

@st.cache_data
def load_progress_data():
    """Load progress data from CSV"""
    try:
        return pd.read_csv(PROGRESS_DATA)
    except Exception as e:
        st.error(f"Error loading progress data: {str(e)}")
        return pd.DataFrame()

@st.cache_data
def load_responsibility_data():
    """Load responsibility data from CSV"""
    try:
        df = pd.read_csv(RESPONSIBILITY_DATA)
        # Remove empty rows (rows where all values are NaN or empty)
        df = df.dropna(how='all')
        # Also remove rows where Phase is empty or NaN
        if 'Phase' in df.columns:
            df = df[df['Phase'].notna()]
            df = df[df['Phase'].astype(str).str.strip() != '']
        return df
    except Exception as e:
        st.error(f"Error loading responsibility data: {str(e)}")
        return pd.DataFrame()

@st.cache_data
def load_remarks_data():
    """Load remarks data from CSV"""
    try:
        df = pd.read_csv(REMARKS_DATA)
        # Convert Date column to datetime
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce', format='mixed')
        return df
    except Exception as e:
        st.error(f"Error loading remarks data: {str(e)}")
        return pd.DataFrame()

def save_remarks_data(df):
    """Save remarks data to CSV"""
    try:
        df.to_csv(REMARKS_DATA, index=False)
        load_remarks_data.clear()
        return True
    except PermissionError:
        # Try workaround: save to temp file, then rename
        try:
            temp_file = REMARKS_DATA + '.tmp'
            df.to_csv(temp_file, index=False)
            
            if os.path.exists(REMARKS_DATA):
                try:
                    os.remove(REMARKS_DATA)
                except:
                    pass
            
            shutil.move(temp_file, REMARKS_DATA)
            load_remarks_data.clear()
            return True
        except Exception as e2:
            st.error(f"❌ **Permission Denied**: Cannot save remarks. Please close {REMARKS_DATA} if it's open in another program.")
            return False
    except Exception as e:
        st.error(f"❌ **Error saving remarks**: {str(e)}")
        return False

def save_villages_data(df):
    """Save villages data to CSV"""
    try:
        # Try to save directly first
        df.to_csv(VILLAGES_DATA, index=False)
        # Clear the specific cached function
        load_villages_data.clear()
        return True
    except PermissionError:
        # Try workaround: save to temp file, then rename
        try:
            
            # Create a temporary file in the same directory
            temp_file = VILLAGES_DATA + '.tmp'
            df.to_csv(temp_file, index=False)
            
            # Try to replace the original file
            if os.path.exists(VILLAGES_DATA):
                # On Windows, we need to remove the old file first
                try:
                    os.remove(VILLAGES_DATA)
                except:
                    pass
            
            # Rename temp file to original
            shutil.move(temp_file, VILLAGES_DATA)
            load_villages_data.clear()
            return True
        except Exception as e2:
            # If workaround also fails, show detailed error
            file_path = os.path.abspath(VILLAGES_DATA)
            st.error(f"""
            ❌ **Permission Denied Error**
            
            The file `villages_data.csv` cannot be saved.
            
            **File Location:** `{file_path}`
            
            **Possible Causes:**
            1. The file is open in Excel, Notepad, or another program
            2. Another Streamlit instance has the file locked
            3. Antivirus software is scanning the file
            4. You don't have write permissions
            
            **Solutions:**
            1. ✅ Close Excel/Notepad if `villages_data.csv` is open
            2. ✅ Close any other Streamlit instances
            3. ✅ Check Task Manager for processes using the file
            4. ✅ Right-click the file → Properties → Uncheck "Read-only" if checked
            5. ✅ Run Streamlit as Administrator (if permission issue)
            
            **Quick Fix:**
            - Close all programs
            - Click the 🔄 Reload button
            - Try updating again
            """)
            return False
    except Exception as e:
        st.error(f"❌ **Error saving data**: {str(e)}\n\nPlease check if the file is open in another program and try again.")
        return False

def get_status_color(status):
    """Get color code for status"""
    color_map = {
        'Completed': '#28a745',
        'On Track': '#ffc107',
        'Behind Schedule': '#dc3545'
    }
    return color_map.get(status, '#6c757d')

def get_phase_order():
    """Get ordered list of phases"""
    return ['Notification', 'Drone Survey Pending', 'Map 1 awaited', 'Ground Truthing Pending', 'Map 2 awaited',
            'Pasting', 'Objections Hearing', 'Map 3', 'Card Issuance']

# Initialize data files
initialize_data_files()

# Main header
st.markdown('<div class="main-header">Urban Svamitva Scheme Dashboard - Ludhiana MCL</div>', unsafe_allow_html=True)

# Reload button and developer credit in sidebar
with st.sidebar:
    st.markdown("### 🔄 Data Refresh")
    st.markdown("---")
    
    # Reload button section
    if st.button("🔄 Reload Data", use_container_width=True, type="primary", help="Reload all data from CSV files"):
        # Clear all cached data
        load_villages_data.clear()
        load_progress_data.clear()
        load_responsibility_data.clear()
        load_remarks_data.clear()
        st.rerun()
    
    st.caption("💡 Click to refresh data after changes")
    
    st.markdown("---")
    
    # Developer credit - centered and styled
    st.markdown("""
    <div class="sidebar-credit">
        <strong>Dashboard Developed by</strong><br>
        <span style="color: #1f4788; font-weight: bold;">Shivam Gulati</span><br>
        <span style="font-size: 0.8rem;">Land Revenue Fellow</span>
    </div>
    """, unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview", "👥 Responsibility Matrix", 
    "💬 Remarks & Help Required", "💾 Data Management"
])

# Load data
villages_df = load_villages_data()
progress_df = load_progress_data()
responsibility_df = load_responsibility_data()
remarks_df = load_remarks_data()

# TAB 1: OVERVIEW
with tab1:
    st.header("Dashboard Overview")
    
    if not villages_df.empty:
        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        total_villages = len(villages_df)
        survey_completed = len(villages_df[villages_df['Current_Phase'].isin(['Map 1 awaited', 'Ground Truthing Pending', 'Map 2 awaited', 'Pasting', 'Objections Hearing', 'Map 3', 'Card Issuance'])])
        map2_awaited = len(villages_df[villages_df['Current_Phase'] == 'Map 2 awaited'])
        ground_truthing = len(villages_df[villages_df['Current_Phase'] == 'Ground Truthing Pending'])
        
        with col1:
            st.metric("Total Villages", total_villages)
        with col2:
            st.metric("Survey Completed", survey_completed)
        with col3:
            st.metric("Map 2 awaited", map2_awaited)
        with col4:
            st.metric("Ground Truthing Pending", ground_truthing)
        
        st.markdown("---")
        
        # Village Progress Table
        st.markdown("### 🏘️ Village Progress Details")
        
        # Mobile-friendly view toggle
        col_view1, col_view2 = st.columns([1, 4])
        with col_view1:
            compact_view = st.checkbox("📱 Compact View", help="Optimized view for mobile devices")
        
        display_columns = ['Village_Name', 'Municipal_Zone', 'Current_Phase', 'Status',
                          'Last_Updated']
        
        # Format dates for display
        display_df = villages_df[display_columns].copy()
        display_df['Last_Updated'] = display_df['Last_Updated'].dt.strftime('%Y-%m-%d')
        
        # Reset index to start from 1 instead of 0
        display_df = display_df.reset_index(drop=True)
        display_df.index = display_df.index + 1
        display_df.index.name = 'S.No.'
        
        # Color code status
        def style_status(val):
            color = get_status_color(val)
            return f'color: {color}; font-weight: bold'
        
        styled_df = display_df.style.map(style_status, subset=['Status'])
        
        # Optimize for mobile: use container width and adjust height based on view
        table_height = 300 if compact_view else 400
        st.dataframe(
            styled_df,
            use_container_width=True,
            height=table_height,
            hide_index=False
        )
        
        # Export functionality
        col1, col2 = st.columns(2)
        with col1:
            csv = villages_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export to CSV",
                data=csv,
                file_name=f"village_progress_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        with col2:
            # Excel export would require openpyxl
            st.info("💡 For Excel export, install openpyxl: pip install openpyxl")
        
        st.markdown("---")
        
        # Charts row 1
        col1, col2 = st.columns(2)
        
        with col1:
            # Progress by Phase Chart
            phase_counts = villages_df['Current_Phase'].value_counts().reset_index()
            phase_counts.columns = ['Phase', 'Count']
            # Order phases
            phase_order = get_phase_order()
            phase_counts['Phase'] = pd.Categorical(phase_counts['Phase'], categories=phase_order, ordered=True)
            phase_counts = phase_counts.sort_values('Phase')
            
            fig_phase = px.bar(
                phase_counts,
                x='Phase',
                y='Count',
                title='Villages in Each Phase',
                color='Count',
                color_continuous_scale='Blues'
            )
            fig_phase.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_phase, width='stretch')
        
        with col2:
            # Zone Distribution Chart
            zone_counts = villages_df['Municipal_Zone'].value_counts().reset_index()
            zone_counts.columns = ['Zone', 'Count']
            
            fig_zone = px.pie(
                zone_counts,
                values='Count',
                names='Zone',
                title='Municipal Zone Distribution',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig_zone, width='stretch')
        
        st.markdown("---")
        
        # Charts row 2
        col1, col2 = st.columns(2)
        
        with col1:
            # Status Distribution
            status_counts = villages_df['Status'].value_counts().reset_index()
            status_counts.columns = ['Status', 'Count']
            status_colors = [get_status_color(s) for s in status_counts['Status']]
            
            fig_status = px.bar(
                status_counts,
                x='Status',
                y='Count',
                title='Status Distribution',
                color='Status',
                color_discrete_map={
                    'Completed': '#28a745',
                    'On Track': '#ffc107',
                    'Behind Schedule': '#dc3545'
                }
            )
            st.plotly_chart(fig_status, width='stretch')
        
        with col2:
            # Zone vs Status Heatmap
            zone_status = pd.crosstab(villages_df['Municipal_Zone'], villages_df['Status'])
            
            fig_heatmap = px.imshow(
                zone_status.values,
                labels=dict(x="Status", y="Zone", color="Count"),
                x=zone_status.columns,
                y=zone_status.index,
                title='Zone vs Status Distribution',
                color_continuous_scale='RdYlGn'
            )
            st.plotly_chart(fig_heatmap, width='stretch')

# TAB 2: RESPONSIBILITY MATRIX
with tab2:
    st.header("Phase-wise Responsibility Matrix")
    
    if not responsibility_df.empty:
        st.subheader("Phase Responsibilities")
        
        # Filter out Notification and Card Issuance
        filtered_responsibility_df = responsibility_df[
            (responsibility_df['Phase'] != 'Notification') & 
            (responsibility_df['Phase'] != 'Card Issuance')
        ]
        
        # Display responsibility matrix - optimized for mobile
        st.dataframe(
            filtered_responsibility_df,
            use_container_width=True,
            hide_index=True
        )
        
        st.markdown("---")
        
        # Contact Directory by Zone
        st.subheader("Contact Directory by Municipal Zone")
        
        if not villages_df.empty:
            # Get unique contacts by zone - filter out NaN values
            zone_contacts = {}
            
            # Filter out NaN zones before sorting
            valid_zones = [zone for zone in villages_df['Municipal_Zone'].unique() 
                          if pd.notna(zone) and str(zone).strip() != '']
            
            for zone in sorted(valid_zones):
                zone_data = villages_df[villages_df['Municipal_Zone'] == zone]
                # Filter out NaN values from contact lists
                hdm_jdm_list = [c for c in zone_data['HDM_JDM'].unique().tolist() 
                               if pd.notna(c) and str(c).strip() != '']
                atp_mtp_list = [c for c in zone_data['ATP_MTP'].unique().tolist() 
                               if pd.notna(c) and str(c).strip() != '']
                
                zone_contacts[zone] = {
                    'HDM/JDM': hdm_jdm_list,
                    'ATP/MTP': atp_mtp_list
                }
            
            # Display contacts in columns
            cols = st.columns(4)
            
            for idx, zone in enumerate(sorted(zone_contacts.keys())):
                with cols[idx % 4]:
                    with st.expander(f"Zone {zone}", expanded=True):
                        st.write("**Property Tax:**")
                        for contact in zone_contacts[zone]['HDM/JDM']:
                            st.write(f"- {contact}")
                        
                        st.write("**ATP/MTP:**")
                        for contact in zone_contacts[zone]['ATP/MTP']:
                            st.write(f"- {contact}")
        
        st.markdown("---")
        
        # One Point of Contact - DC Office
        st.subheader("One Point of Contact (DC Office)")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
            **Name:** Shivam Gulati  
            **Designation:** Land Revenue Fellow  
            **Contact:** 62844-12362
            """)
        with col2:
            st.info("📞 DC Office")
        
        st.markdown("---")
        
        # One Point of Contact - MCL
        st.subheader("One Point of Contact (MCL)")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
            **Name:** Nirvaan  
            **Designation:** ATP HQ  
            **Contact:** 95927-35111
            """)
        with col2:
            st.info("📞 MCL Office")

# TAB 3: REMARKS & HELP REQUIRED
with tab3:
    st.header("Remarks & Help Required")
    st.markdown("Officials can submit remarks and request help from higher officials regarding their responsibilities.")
    
    st.markdown("---")
    
    # Submit new remark/help request
    st.subheader("📝 Submit New Remark / Help Request")
    
    with st.form("remarks_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            official_name = st.text_input("Official Name *", placeholder="Enter your name")
            department = st.selectbox("Department *", [
                "DC Administration",
                "Survey of India",
                "Property Tax Dept (HDM/JDM)",
                "ATP/MTP",
                "ARRO",
                "Other"
            ])
            phase = st.selectbox("Phase (if applicable)", ['All'] + get_phase_order())
        
        with col2:
            village_list = ['All']
            if not villages_df.empty:
                village_list.extend(villages_df['Village_Name'].dropna().unique().tolist())
            village = st.selectbox("Village (if applicable)", village_list)
            help_required = st.selectbox("Type of Help Required", [
                "General Query",
                "Technical Support",
                "Resource Requirement",
                "Coordination Needed",
                "Approval Required",
                "Other"
            ])
        
        remarks = st.text_area("Remarks / Help Required Details *", 
                              placeholder="Please describe your remarks or the help you need...",
                              height=150)
        
        submitted = st.form_submit_button("Submit Remark / Help Request", type="primary")
        
        if submitted:
            if official_name and department and remarks:
                new_remark = {
                    'Date': datetime.now(),
                    'Official_Name': official_name,
                    'Department': department,
                    'Phase': phase if phase != 'All' else '',
                    'Village': village if village != 'All' else '',
                    'Remarks': remarks,
                    'Help_Required': help_required,
                    'Status': 'Pending',
                    'Response': ''
                }
                
                current_remarks_df = load_remarks_data()
                new_df = pd.concat([current_remarks_df, pd.DataFrame([new_remark])], ignore_index=True)
                
                if save_remarks_data(new_df):
                    st.success("✅ Your remark/help request has been submitted successfully!")
                    st.rerun()
            else:
                st.error("Please fill in all required fields (marked with *)")
    
    st.markdown("---")
    
    # Display existing remarks
    st.subheader("📋 Submitted Remarks & Help Requests")
    
    current_remarks_df = load_remarks_data()
    
    if not current_remarks_df.empty:
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_department = st.selectbox("Filter by Department", 
                                            ['All'] + current_remarks_df['Department'].unique().tolist() if 'Department' in current_remarks_df.columns else ['All'])
        with col2:
            filter_status = st.selectbox("Filter by Status", 
                                        ['All'] + current_remarks_df['Status'].unique().tolist() if 'Status' in current_remarks_df.columns else ['All'])
        with col3:
            filter_help = st.selectbox("Filter by Help Type", 
                                      ['All'] + current_remarks_df['Help_Required'].unique().tolist() if 'Help_Required' in current_remarks_df.columns else ['All'])
        
        # Apply filters
        filtered_remarks = current_remarks_df.copy()
        if filter_department != 'All':
            filtered_remarks = filtered_remarks[filtered_remarks['Department'] == filter_department]
        if filter_status != 'All':
            filtered_remarks = filtered_remarks[filtered_remarks['Status'] == filter_status]
        if filter_help != 'All':
            filtered_remarks = filtered_remarks[filtered_remarks['Help_Required'] == filter_help]
        
        # Display remarks
        if not filtered_remarks.empty:
            # Format date for display
            display_remarks = filtered_remarks.copy()
            if 'Date' in display_remarks.columns:
                display_remarks['Date'] = display_remarks['Date'].dt.strftime('%Y-%m-%d %H:%M')
            
            # Reorder columns for better display
            display_columns = ['Date', 'Official_Name', 'Department', 'Phase', 'Village', 'Help_Required', 'Remarks', 'Status', 'Response']
            available_columns = [col for col in display_columns if col in display_remarks.columns]
            display_remarks = display_remarks[available_columns]
            
            st.dataframe(display_remarks, use_container_width=True, height=400)
            
            # Export functionality
            csv = filtered_remarks.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export Remarks to CSV",
                data=csv,
                file_name=f"remarks_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.info("No remarks match the selected filters.")
    else:
        st.info("No remarks submitted yet. Use the form above to submit your first remark or help request.")
    
    st.markdown("---")
    
    # Response section for higher officials
    st.subheader("💼 Response from Higher Officials")
    st.markdown("Higher officials can provide responses to submitted remarks.")
    
    if not current_remarks_df.empty:
        pending_remarks = current_remarks_df[current_remarks_df['Status'] == 'Pending'] if 'Status' in current_remarks_df.columns else current_remarks_df
        
        if not pending_remarks.empty:
            remark_options = {idx: f"{row['Official_Name']} - {row['Department']} - {row['Date'].strftime('%Y-%m-%d') if pd.notna(row['Date']) else 'N/A'}" 
                            for idx, row in pending_remarks.iterrows()}
            
            selected_remark_idx = st.selectbox("Select Remark to Respond", 
                                                options=list(remark_options.keys()),
                                                format_func=lambda x: remark_options[x])
            
            col1, col2 = st.columns(2)
            with col1:
                response_status = st.selectbox("Status", ['Pending', 'In Progress', 'Resolved', 'Referred'])
            with col2:
                response_text = st.text_area("Response", placeholder="Enter your response...")
            
            if st.button("Submit Response"):
                current_remarks_df.loc[selected_remark_idx, 'Status'] = response_status
                current_remarks_df.loc[selected_remark_idx, 'Response'] = response_text
                
                if save_remarks_data(current_remarks_df):
                    st.success("✅ Response submitted successfully!")
                    st.rerun()
        else:
            st.info("No pending remarks to respond to.")

# TAB 4: DATA MANAGEMENT
with tab4:
    st.header("Data Management")
    
    # Warning about file access
    st.info("⚠️ **Important**: Make sure `villages_data.csv` is NOT open in Excel or any other program when updating data. Close the file first to avoid permission errors.")
    
    st.subheader("Manual Village Data Update")
    
    # Add new village form
    with st.expander("Add New Village", expanded=False):
        with st.form("add_village_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_village_name = st.text_input("Village Name *")
                new_zone = st.selectbox("Municipal Zone *", ['A', 'B', 'C', 'D'])
                new_phase = st.selectbox("Current Phase *", get_phase_order())
                new_status = st.selectbox("Status *", ['Completed', 'On Track', 'Behind Schedule'])
            
            with col2:
                new_hdm_jdm = st.text_input("Property Tax")
                new_atp_mtp = st.text_input("ATP/MTP")
                new_last_updated = st.date_input("Last Updated", value=datetime.now().date())
            
            submitted = st.form_submit_button("Add Village")
            
            if submitted:
                if new_village_name and new_zone and new_phase and new_status:
                    new_row = {
                        'Village_Name': new_village_name,
                        'Municipal_Zone': new_zone,
                        'Current_Phase': new_phase,
                        'Status': new_status,
                        'Last_Updated': pd.to_datetime(new_last_updated),
                        'HDM_JDM': new_hdm_jdm if new_hdm_jdm else '',
                        'ATP_MTP': new_atp_mtp if new_atp_mtp else '',
                        'ARRO_Officer': '',
                        'Total_Properties': 0,
                        'Survey_Date': None,
                        'Notification_Date': None,
                        'Drone_Survey_Date': None,
                        'Map1_Date': None,
                        'Ground_Truthing_Date': None,
                        'Map2_Date': None,
                        'Pasting_Start_Date': None,
                        'Objections_Date': None,
                        'Map3_Date': None,
                        'Cards_Issued_Date': None
                    }
                    
                    villages_df = load_villages_data()
                    new_df = pd.concat([villages_df, pd.DataFrame([new_row])], ignore_index=True)
                    
                    if save_villages_data(new_df):
                        st.success(f"Village '{new_village_name}' added successfully!")
                        st.rerun()
                else:
                    st.error("Please fill in all required fields (marked with *)")
    
    st.markdown("---")
    
    # Update existing village
    st.subheader("Update Existing Village")
    
    if not villages_df.empty:
        village_list = villages_df['Village_Name'].tolist()
        selected_village = st.selectbox("Select Village to Update", village_list)
        
        if selected_village:
            village_data = villages_df[villages_df['Village_Name'] == selected_village].iloc[0]
            
            col1, col2 = st.columns(2)
            
            with col1:
                updated_phase = st.selectbox("Current Phase", get_phase_order(), 
                                            index=get_phase_order().index(village_data['Current_Phase']) if village_data['Current_Phase'] in get_phase_order() else 0)
                updated_status = st.selectbox("Status", ['Completed', 'On Track', 'Behind Schedule'],
                                            index=['Completed', 'On Track', 'Behind Schedule'].index(village_data['Status']) if village_data['Status'] in ['Completed', 'On Track', 'Behind Schedule'] else 1)
                updated_zone = st.selectbox("Municipal Zone", ['A', 'B', 'C', 'D'],
                                          index=['A', 'B', 'C', 'D'].index(village_data['Municipal_Zone']) if village_data['Municipal_Zone'] in ['A', 'B', 'C', 'D'] else 0)
            
            with col2:
                updated_hdm = st.text_input("Property Tax", value=str(village_data['HDM_JDM']) if pd.notna(village_data['HDM_JDM']) else '')
                updated_atp = st.text_input("ATP/MTP", value=str(village_data['ATP_MTP']) if pd.notna(village_data['ATP_MTP']) else '')
            
            if st.button("Update Village"):
                villages_df.loc[villages_df['Village_Name'] == selected_village, 'Current_Phase'] = updated_phase
                villages_df.loc[villages_df['Village_Name'] == selected_village, 'Status'] = updated_status
                villages_df.loc[villages_df['Village_Name'] == selected_village, 'Municipal_Zone'] = updated_zone
                villages_df.loc[villages_df['Village_Name'] == selected_village, 'HDM_JDM'] = updated_hdm
                villages_df.loc[villages_df['Village_Name'] == selected_village, 'ATP_MTP'] = updated_atp
                villages_df.loc[villages_df['Village_Name'] == selected_village, 'Last_Updated'] = pd.to_datetime(datetime.now())
                
                if save_villages_data(villages_df):
                    st.success(f"Village '{selected_village}' updated successfully!")
                    st.rerun()
    
    st.markdown("---")
    
    # Bulk CSV Upload
    st.subheader("Bulk CSV Upload")
    
    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
    
    if uploaded_file is not None:
        try:
            uploaded_df = pd.read_csv(uploaded_file)
            
            st.write("Preview of uploaded data:")
            st.dataframe(uploaded_df.head())
            
            if st.button("Replace Existing Data"):
                # Validate required columns
                required_columns = ['Village_Name', 'Municipal_Zone', 'Current_Phase', 'Status']
                if all(col in uploaded_df.columns for col in required_columns):
                    # Convert date columns
                    date_columns = ['Last_Updated', 'Survey_Date', 'Notification_Date', 'Drone_Survey_Date',
                                   'Map1_Date', 'Ground_Truthing_Date', 'Map2_Date', 'Pasting_Start_Date',
                                   'Objections_Date', 'Map3_Date', 'Cards_Issued_Date']
                    for col in date_columns:
                        if col in uploaded_df.columns:
                            uploaded_df[col] = pd.to_datetime(uploaded_df[col], errors='coerce', format='mixed')
                    
                    if save_villages_data(uploaded_df):
                        st.success("Data uploaded successfully!")
                        st.rerun()
                else:
                    st.error(f"CSV must contain these columns: {', '.join(required_columns)}")
        
        except Exception as e:
            st.error(f"Error reading CSV file: {str(e)}")
    
    st.markdown("---")
    
    # Current data stats
    st.subheader("Current Data Statistics")
    
    if not villages_df.empty:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Villages", len(villages_df))
        
        with col2:
            st.metric("Columns", len(villages_df.columns))
        
        with col3:
            st.metric("Data Last Updated", villages_df['Last_Updated'].max().strftime('%Y-%m-%d') if pd.notna(villages_df['Last_Updated'].max()) else 'N/A')
        
        st.info("💡 Data is automatically saved to CSV files. Make sure you have write permissions.")

