"""
LEPT AI Reviewer (PH) - Main Application Entry Point
OPTIMIZED: Single connection, cached queries, minimal reruns
"""

import streamlit as st
from pathlib import Path

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="LEPT AI Reviewer (PH)",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': "LEPT AI Reviewer (PH) - AI-Powered Reviewer for Philippine LEPT"
    }
)

# Import components - minimal imports at top level
from components.auth import init_session_state, check_authentication, show_login_form, get_current_user, is_admin, logout_user, logout_admin
from config.settings import COLORS, PLAN_FREE, PLAN_PRO, PLAN_PREMIUM, EMAIL_SHARING_WARNING


@st.cache_data(ttl=3600, show_spinner=False)
def load_css_file():
    """Load and cache CSS file content."""
    css_path = Path(__file__).parent / "assets" / "style.css"
    if css_path.exists():
        with open(css_path) as f:
            return f.read()
    return ""


def load_custom_css():
    """Load custom CSS styles - cached CSS file + inline styles."""
    css_content = load_css_file()
    
    # Combined CSS string (cached file + inline)
    inline_css = f"""
    /* ========== HIDE STREAMLIT DEFAULTS ========== */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* ========== HIDE SIDEBAR ========== */
    [data-testid="stSidebar"] {{display: none !important;}}
    
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
            radial-gradient(ellipse at 80% 80%, rgba(6, 182, 212, 0.1) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }}
    
    .main .block-container {{
        position: relative;
        z-index: 1;
        padding-top: 1rem;
    }}
    
    /* ========== TYPOGRAPHY ========== */
    h1, h2, h3, h4, h5, h6 {{color: {COLORS['text']} !important;}}
    p, span, label {{color: {COLORS['text_muted']} !important;}}
    
    /* ========== BUTTONS ========== */
    .stButton > button {{
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }}
    
    .stButton > button[data-testid="baseButton-primary"] {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['accent']} 100%) !important;
        border: none !important;
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
    
    /* ========== ALERTS ========== */
    [data-testid="stAlert"] {{
        background: {COLORS['background_light']} !important;
        border-radius: 12px !important;
    }}
    
    /* ========== FORM ========== */
    [data-testid="stForm"] {{
        background: {COLORS['background_light']};
        border: 1px solid {COLORS['border']};
        border-radius: 16px;
        padding: 1.5rem;
    }}
    
    /* ========== MOBILE RESPONSIVE ========== */
    @media (max-width: 768px) {{
        .main .block-container {{
            padding-left: 1rem;
            padding-right: 1rem;
        }}
    }}
    """
    
    st.markdown(f"<style>{css_content}{inline_css}</style>", unsafe_allow_html=True)


def render_header_nav():
    """Render the header with navigation - no DB queries."""
    user = get_current_user()
    if not user:
        return
    
    # Get status from session state (no DB query)
    from services.usage_tracker import get_cached_user_status
    status = get_cached_user_status()
    if not status:
        from services.usage_tracker import get_user_status
        status = get_user_status(user)
        st.session_state.user_status = status
    
    user_plan = status["plan"]
    plan_color = COLORS["accent"] if user_plan == PLAN_PREMIUM else (COLORS["primary"] if user_plan == PLAN_PRO else COLORS["text_muted"])
    
    # Header
    col1, col2, col3 = st.columns([2, 4, 2])
    
    with col1:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 0.75rem;">
            <div style="font-size: 2rem;">🎓</div>
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
        admin_logged = is_admin()
        num_nav_items = 6 if admin_logged else 5
        nav_cols = st.columns(num_nav_items)
        
        nav_items = [
            ("🏠", "Home", "home"),
            ("📄", "Upload", "upload"),
            ("🧠", "Practice", "practice"),
            ("💳", "Upgrade", "upgrade"),
        ]
        
        if admin_logged:
            nav_items.append(("🛠️", "Admin", "admin"))
        else:
            nav_items.append(("🔐", "Admin", "admin_login"))
        
        for i, (icon, label, page_key) in enumerate(nav_items):
            with nav_cols[i]:
                is_active = st.session_state.get("current_page") == page_key
                btn_type = "primary" if is_active else "secondary"
                if st.button(f"{icon} {label}", key=f"nav_{page_key}", use_container_width=True, type=btn_type):
                    st.session_state.current_page = page_key
                    st.rerun()
    
    with col3:
        st.markdown(f"""
        <div style="text-align: right;">
            <span style="background: {plan_color}33; color: {plan_color}; 
                         padding: 4px 12px; border-radius: 20px; font-size: 0.75rem;
                         font-weight: 600;">{user_plan}</span>
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
    
    # Warning for FREE users only
    if user_plan == PLAN_FREE:
        st.markdown(f"""
        <div style="background: rgba(245, 158, 11, 0.1); padding: 0.5rem 1rem; border-radius: 8px;
                    border-left: 3px solid {COLORS['warning']}; margin-bottom: 1rem; font-size: 0.85rem;">
            <span style="color: {COLORS['warning']};">⚠️</span>
            <span style="color: {COLORS['text_muted']};">{EMAIL_SHARING_WARNING.replace('**', '')}</span>
        </div>
        """, unsafe_allow_html=True)


def render_admin_login_page():
    """Render admin login page - form prevents reruns."""
    if is_admin():
        st.session_state.current_page = "admin"
        st.rerun()
        return
    
    st.markdown(f"""
    <div style="max-width: 500px; margin: 2rem auto; text-align: center;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🔐</div>
        <h1 style="background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   font-size: 2rem; margin: 0;">Admin Login</h1>
        <p style="color: {COLORS['text_muted']}; margin-top: 0.5rem;">
            Enter your admin password to access the Admin Panel
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("admin_login_form_page", clear_on_submit=True):
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
                        st.success("✅ Admin access granted!")
                        st.session_state.current_page = "admin"
                        st.rerun()
                    else:
                        st.error("❌ Invalid admin password.")
                except Exception:
                    st.error("Admin authentication not configured.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← Back to Home", key="back_to_home", use_container_width=True):
            st.session_state.current_page = "home"
            st.rerun()


def render_debug_info():
    """Render debug info (remove in production)."""
    from database.connection import get_query_count
    query_count = get_query_count()
    if query_count > 0:
        st.markdown(f"""
        <div style="position: fixed; bottom: 10px; right: 10px; 
                    background: rgba(0,0,0,0.8); color: white; 
                    padding: 5px 10px; border-radius: 5px; font-size: 11px; z-index: 9999;">
            DB Queries: {query_count}
        </div>
        """, unsafe_allow_html=True)


def main():
    """Main application entry point - OPTIMIZED."""
    # Initialize session state ONCE
    init_session_state()
    
    # Load CSS ONCE (cached)
    load_custom_css()
    
    # Check authentication (no DB query - session state only)
    if not check_authentication():
        show_login_form()
        return
    
    # Render header navigation
    render_header_nav()
    
    # Get current page from session state
    current_page = st.session_state.get("current_page", "home")
    
    # Page routing - LAZY IMPORTS to reduce startup time
    if current_page == "home":
        from pages.home import render_home_page
        render_home_page()
    elif current_page == "upload":
        from pages.upload_reviewer import render_upload_page
        render_upload_page()
    elif current_page == "practice":
        from pages.practice_exam import render_practice_page
        render_practice_page()
    elif current_page == "upgrade":
        from pages.upgrade import render_upgrade_page
        render_upgrade_page()
    elif current_page == "admin_login":
        render_admin_login_page()
    elif current_page == "admin":
        if is_admin():
            from pages.admin_panel import render_admin_page
            render_admin_page()
        else:
            render_admin_login_page()
    else:
        from pages.home import render_home_page
        render_home_page()
    
    # Debug info (comment out in production)
    # render_debug_info()


if __name__ == "__main__":
    main()
