"""
LEPT AI Reviewer (PH) - Main Application Entry Point

AI-Powered Reviewer for the Philippine Licensure Examination for Professional Teachers
Modern Techy Theme - Optimized for Performance
"""

import streamlit as st
from pathlib import Path

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="LEPT AI Reviewer (PH)",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",  # Collapsed sidebar - navigation in main page
    menu_items={
        'About': "LEPT AI Reviewer (PH) - AI-Powered Reviewer for the Philippine Licensure Examination for Professional Teachers"
    }
)

# Import components and pages
from components.auth import init_session_state, check_authentication, show_login_form, get_current_user, is_admin, logout_user, logout_admin, show_admin_login
from services.usage_tracker import get_user_status
from pages.home import render_home_page
from pages.upload_reviewer import render_upload_page
from pages.practice_exam import render_practice_page
from pages.upgrade import render_upgrade_page
from pages.admin_panel import render_admin_page
from config.settings import COLORS, PLAN_FREE, PLAN_PRO, PLAN_PREMIUM, EMAIL_SHARING_WARNING


@st.cache_data(ttl=3600)
def load_css_file():
    """Load and cache CSS file content."""
    css_path = Path(__file__).parent / "assets" / "style.css"
    if css_path.exists():
        with open(css_path) as f:
            return f.read()
    return ""


def load_custom_css():
    """Load custom CSS styles for modern techy theme."""
    css_content = load_css_file()
    if css_content:
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    
    # Additional inline styles for the modern techy theme
    st.markdown(f"""
    <style>
    /* ========== HIDE STREAMLIT DEFAULTS ========== */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* ========== HIDE SIDEBAR ========== */
    [data-testid="stSidebar"] {{
        display: none !important;
    }}
    
    /* ========== DARK TECHY BACKGROUND ========== */
    .stApp {{
        background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 50%, #0F172A 100%);
        background-attachment: fixed;
    }}
    
    .stApp::before {{
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(ellipse at 20% 20%, rgba(99, 102, 241, 0.15) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 80%, rgba(6, 182, 212, 0.1) 0%, transparent 50%),
            radial-gradient(ellipse at 50% 50%, rgba(139, 92, 246, 0.05) 0%, transparent 70%);
        pointer-events: none;
        z-index: 0;
    }}
    
    .main .block-container {{
        position: relative;
        z-index: 1;
        padding-top: 1rem;
    }}
    
    /* ========== TYPOGRAPHY ========== */
    h1, h2, h3, h4, h5, h6 {{
        color: {COLORS['text']} !important;
    }}
    
    p, span, label {{
        color: {COLORS['text_muted']} !important;
    }}
    
    /* ========== BUTTONS ========== */
    .stButton > button {{
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }}
    
    .stButton > button[data-testid="baseButton-primary"] {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['accent']} 100%) !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4) !important;
    }}
    
    .stButton > button[data-testid="baseButton-primary"]:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.5) !important;
    }}
    
    .stButton > button[data-testid="baseButton-secondary"] {{
        background: {COLORS['background_light']} !important;
        border: 1px solid {COLORS['border']} !important;
        color: {COLORS['text']} !important;
    }}
    
    /* ========== INPUTS ========== */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {{
        background: {COLORS['background_light']} !important;
        border: 1px solid {COLORS['border']} !important;
        border-radius: 12px !important;
        color: {COLORS['text']} !important;
    }}
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {{
        border-color: {COLORS['primary']} !important;
        box-shadow: 0 0 0 3px {COLORS['glow']} !important;
    }}
    
    .stSelectbox > div > div {{
        background: {COLORS['background_light']} !important;
        border: 1px solid {COLORS['border']} !important;
        border-radius: 12px !important;
    }}
    
    /* ========== FILE UPLOADER ========== */
    .stFileUploader > div {{
        background: {COLORS['background_light']} !important;
        border: 2px dashed {COLORS['border']} !important;
        border-radius: 16px !important;
    }}
    
    .stFileUploader > div:hover {{
        border-color: {COLORS['primary']} !important;
    }}
    
    /* ========== TABS ========== */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background: {COLORS['background_light']};
        border-radius: 12px;
        padding: 4px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px;
        color: {COLORS['text_muted']} !important;
        background: transparent;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['accent']} 100%) !important;
        color: white !important;
    }}
    
    /* ========== EXPANDER ========== */
    .streamlit-expanderHeader {{
        background: {COLORS['background_light']} !important;
        border-radius: 12px !important;
        color: {COLORS['text']} !important;
    }}
    
    .streamlit-expanderContent {{
        background: {COLORS['background_light']} !important;
        border: 1px solid {COLORS['border']} !important;
    }}
    
    /* ========== ALERTS ========== */
    [data-testid="stAlert"] {{
        background: {COLORS['background_light']} !important;
        border-radius: 12px !important;
    }}
    
    /* ========== METRICS ========== */
    [data-testid="stMetric"] {{
        background: {COLORS['background_light']};
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid {COLORS['border']};
    }}
    
    [data-testid="stMetricValue"] {{
        color: {COLORS['primary']} !important;
    }}
    
    /* ========== FORM ========== */
    [data-testid="stForm"] {{
        background: {COLORS['background_light']};
        border: 1px solid {COLORS['border']};
        border-radius: 16px;
        padding: 1.5rem;
    }}
    
    /* ========== RADIO ========== */
    .stRadio label {{
        background: {COLORS['background_light']} !important;
        border: 1px solid {COLORS['border']} !important;
        border-radius: 10px !important;
        color: {COLORS['text']} !important;
    }}
    
    /* ========== CHECKBOX ========== */
    .stCheckbox label {{
        color: {COLORS['text']} !important;
    }}
    
    /* ========== SLIDER ========== */
    .stSlider > div > div > div {{
        background: linear-gradient(90deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%) !important;
    }}
    
    /* ========== CUSTOM SCROLLBAR ========== */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {COLORS['background']};
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {COLORS['surface']};
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: {COLORS['primary']};
    }}
    
    /* ========== NAVIGATION BAR ========== */
    .nav-bar {{
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        justify-content: center;
        margin-bottom: 1rem;
    }}
    
    /* ========== MOBILE RESPONSIVE ========== */
    @media (max-width: 768px) {{
        .main .block-container {{
            padding-left: 1rem;
            padding-right: 1rem;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)


def render_header_nav():
    """Render the header with navigation on the main page."""
    user = get_current_user()
    if not user:
        return
    
    status = get_user_status(user)
    
    plan_colors = {
        PLAN_FREE: COLORS["text_muted"],
        PLAN_PRO: COLORS["primary"],
        PLAN_PREMIUM: COLORS["accent"]
    }
    plan_color = plan_colors.get(status["plan"], COLORS["text_muted"])
    
    # Header with branding and user info
    col1, col2, col3 = st.columns([2, 4, 2])
    
    with col1:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 0.75rem;">
            <div style="font-size: 2rem; filter: drop-shadow(0 0 15px {COLORS['glow']});">🎓</div>
            <div>
                <h3 style="background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
                           -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                           margin: 0; font-size: 1.1rem; line-height: 1.2;">LEPT AI Reviewer</h3>
                <p style="color: {COLORS['text_muted']}; margin: 0; font-size: 0.65rem;
                          letter-spacing: 1px;">PHILIPPINE EDITION</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Navigation buttons - determine number of columns
        num_nav_items = 4  # Home, Practice, Upgrade, Admin Login
        if status["plan"] in [PLAN_PRO, PLAN_PREMIUM]:
            num_nav_items = 5  # Add Upload
        if is_admin():
            num_nav_items += 1  # Add Admin Panel
        
        nav_cols = st.columns(num_nav_items)
        
        nav_items = [
            ("🏠", "Home", "home"),
            ("🧠", "Practice", "practice"),
            ("💳", "Upgrade", "upgrade"),
        ]
        
        # Only show Upload for Pro/Premium
        if status["plan"] in [PLAN_PRO, PLAN_PREMIUM]:
            nav_items.insert(1, ("📄", "Upload", "upload"))
        
        # Add Admin Panel if already logged in as admin
        if is_admin():
            nav_items.append(("🛠️", "Admin Panel", "admin"))
        
        # Always show Admin Login button (unless already admin)
        if not is_admin():
            nav_items.append(("🔐", "Admin", "admin_login"))
        
        for i, (icon, label, page_key) in enumerate(nav_items):
            with nav_cols[i]:
                is_active = st.session_state.get("current_page") == page_key
                button_type = "primary" if is_active else "secondary"
                if st.button(f"{icon} {label}", key=f"nav_{page_key}", use_container_width=True, type=button_type):
                    st.session_state.current_page = page_key
                    st.rerun()
    
    with col3:
        # User info and logout
        st.markdown(f"""
        <div style="text-align: right;">
            <span style="background: {plan_color}33; color: {plan_color}; 
                         padding: 4px 12px; border-radius: 20px; font-size: 0.75rem;
                         font-weight: 600;">{status['plan']}</span>
            <span style="color: {COLORS['secondary']}; font-weight: 700; margin-left: 0.5rem;">
                {status['questions_display']} Q
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        logout_cols = st.columns([3, 1])
        with logout_cols[1]:
            if st.button("🚪", key="logout_btn", help="Logout"):
                if is_admin():
                    logout_admin()
                logout_user()
    
    # Separator
    st.markdown(f"""
    <hr style="border: none; height: 1px; background: linear-gradient(90deg, transparent, {COLORS['border']}, transparent); margin: 0.5rem 0 1rem 0;">
    """, unsafe_allow_html=True)
    
    # Warning for email sharing
    if status["plan"] == PLAN_FREE:
        st.markdown(f"""
        <div style="background: rgba(245, 158, 11, 0.1); padding: 0.5rem 1rem; border-radius: 8px;
                    border-left: 3px solid {COLORS['warning']}; margin-bottom: 1rem; font-size: 0.85rem;">
            <span style="color: {COLORS['warning']};">⚠️</span>
            <span style="color: {COLORS['text_muted']};">{EMAIL_SHARING_WARNING.replace('**', '')}</span>
        </div>
        """, unsafe_allow_html=True)


def render_admin_login_page():
    """Render a dedicated admin login page."""
    if is_admin():
        # Already logged in, redirect to admin panel
        st.session_state.current_page = "admin"
        st.rerun()
        return
    
    # Centered admin login card
    st.markdown(f"""
    <div style="max-width: 500px; margin: 2rem auto;">
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem; filter: drop-shadow(0 0 20px {COLORS['glow']});">🔐</div>
            <h1 style="background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                       font-size: 2rem; margin: 0;">Admin Login</h1>
            <p style="color: {COLORS['text_muted']}; margin-top: 0.5rem;">
                Enter your admin password to access the Admin Panel
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Login form in centered container
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"""
        <div style="background: {COLORS['surface']}; padding: 2rem; border-radius: 16px;
                    border: 1px solid {COLORS['border']}; box-shadow: 0 4px 20px rgba(0,0,0,0.3);">
        """, unsafe_allow_html=True)
        
        with st.form("admin_login_form_page"):
            admin_password = st.text_input(
                "Admin Password", 
                type="password", 
                key="admin_pwd_page",
                placeholder="Enter admin password..."
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            submit = st.form_submit_button("🔑 Login as Admin", use_container_width=True, type="primary")
            
            if submit:
                try:
                    correct_password = st.secrets.get("admin", {}).get("password", "")
                    if admin_password == correct_password and correct_password:
                        st.session_state.is_admin = True
                        st.success("✅ Admin access granted! Redirecting...")
                        st.session_state.current_page = "admin"
                        st.rerun()
                    else:
                        st.error("❌ Invalid admin password.")
                except Exception as e:
                    st.error("Admin authentication not configured.")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Back to home link
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← Back to Home", key="back_to_home", use_container_width=True):
            st.session_state.current_page = "home"
            st.rerun()


def main():
    """Main application entry point."""
    # Initialize session state
    init_session_state()
    
    # Load custom CSS
    load_custom_css()
    
    # Check authentication
    if not check_authentication():
        # Show login form for unauthenticated users
        show_login_form()
        return
    
    # Render header with navigation (on main page)
    render_header_nav()
    
    # Get current page and render
    current_page = st.session_state.get("current_page", "home")
    
    # Get user status to check plan
    user = get_current_user()
    status = get_user_status(user) if user else {"plan": PLAN_FREE}
    
    # Page routing (with restrictions for FREE users)
    if current_page == "home":
        render_home_page()
    elif current_page == "upload":
        # Only allow upload for Pro/Premium
        if status["plan"] in [PLAN_PRO, PLAN_PREMIUM]:
            render_upload_page()
        else:
            st.session_state.current_page = "upgrade"
            st.rerun()
    elif current_page == "practice":
        render_practice_page()
    elif current_page == "upgrade":
        render_upgrade_page()
    elif current_page == "admin_login":
        render_admin_login_page()  # Dedicated admin login page
    elif current_page == "admin":
        if is_admin():
            render_admin_page()
        else:
            # Not logged in as admin, show login page
            render_admin_login_page()
    else:
        # Default to home
        render_home_page()


if __name__ == "__main__":
    main()
