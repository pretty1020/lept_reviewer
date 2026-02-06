"""
LEPT AI Reviewer - Authentication Components
OPTIMIZED: Session state based, minimal reruns
"""

import streamlit as st

from config.settings import EMAIL_SHARING_WARNING, COLORS
from services.usage_tracker import get_or_create_user, get_user_status, get_cached_user_status
from utils.validators import validate_email


def init_session_state():
    """Initialize session state variables - called once per session."""
    defaults = {
        "user": None,
        "user_status": None,
        "is_admin": False,
        "current_page": "home",
        "login_attempted": False,
        "generated_questions": None,
        "quiz_answers": {},
        "quiz_submitted": False,
        "selected_docs": [],
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value


def check_authentication() -> bool:
    """Check if user is authenticated - no DB query."""
    init_session_state()
    return st.session_state.user is not None


def show_login_form():
    """Display the login/registration form with modern techy theme."""
    
    # Hero Section - static HTML, no DB queries
    st.markdown(f"""
    <div style="text-align: center; padding: 3rem 1rem; margin-bottom: 2rem;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">
            🎓
        </div>
        <h1 style="font-size: 2.8rem; font-weight: 700; margin: 0;
                   background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 50%, {COLORS['accent']} 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   background-clip: text;">
            LEPT AI Reviewer
        </h1>
        <p style="color: {COLORS['secondary']}; font-size: 1.1rem; margin: 0.5rem 0 0 0; 
                  letter-spacing: 2px; text-transform: uppercase;">
            Philippine Edition
        </p>
        <p style="color: {COLORS['text_muted']}; font-size: 1rem; margin: 1rem 0 0 0; max-width: 600px; margin-left: auto; margin-right: auto;">
            AI-Powered Reviewer for the Philippine Licensure Examination for Professional Teachers
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Warning banner
    st.warning(EMAIL_SHARING_WARNING)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.8); backdrop-filter: blur(20px);
                    padding: 2rem; border-radius: 20px; 
                    border: 1px solid {COLORS['border']};">
            <h3 style="color: {COLORS['text']}; margin: 0 0 0.5rem 0; text-align: center;">
                🚀 Get Started
            </h3>
            <p style="color: {COLORS['text_muted']}; text-align: center; margin: 0 0 1.5rem 0;">
                Enter your email to begin your LEPT review journey
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Use form to prevent reruns on input change
        with st.form("login_form", clear_on_submit=False):
            email = st.text_input(
                "Email Address",
                placeholder="your.email@example.com",
                help="Your email will be used to track your progress and usage."
            )
            
            agree = st.checkbox(
                "I understand that my email will be used to track my usage and I will not share my account."
            )
            
            submit = st.form_submit_button("⚡ Start Reviewing", use_container_width=True, type="primary")
            
            if submit:
                if not agree:
                    st.error("Please agree to the terms to continue.")
                    return
                
                valid, msg = validate_email(email)
                if not valid:
                    st.error(msg)
                    return
                
                email = email.strip().lower()
                
                with st.spinner("Setting up your account..."):
                    user, message = get_or_create_user(email)
                
                if user:
                    st.session_state.user = user
                    st.session_state.user_status = get_user_status(user)
                    st.session_state.login_attempted = True
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
    
    # Features section - static HTML only
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style="text-align: center; padding: 1.5rem; background: rgba(30, 41, 59, 0.6);
                    border-radius: 16px; border: 1px solid {COLORS['border']};">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🎯</div>
            <h4 style="color: {COLORS['text']}; margin: 0 0 0.5rem 0;">AI-Powered</h4>
            <p style="color: {COLORS['text_muted']}; font-size: 0.9rem; margin: 0;">
                Smart questions generated from your own reviewers
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="text-align: center; padding: 1.5rem; background: rgba(30, 41, 59, 0.6);
                    border-radius: 16px; border: 1px solid {COLORS['border']};">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📄</div>
            <h4 style="color: {COLORS['text']}; margin: 0 0 0.5rem 0;">Your Materials</h4>
            <p style="color: {COLORS['text_muted']}; font-size: 0.9rem; margin: 0;">
                Upload PDF and DOCX for personalized practice
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="text-align: center; padding: 1.5rem; background: rgba(30, 41, 59, 0.6);
                    border-radius: 16px; border: 1px solid {COLORS['border']};">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📊</div>
            <h4 style="color: {COLORS['text']}; margin: 0 0 0.5rem 0;">Track Progress</h4>
            <p style="color: {COLORS['text_muted']}; font-size: 0.9rem; margin: 0;">
                Monitor usage and upgrade for unlimited access
            </p>
        </div>
        """, unsafe_allow_html=True)


def show_admin_login():
    """Display admin login form - uses form to prevent reruns."""
    st.markdown("### 🔐 Admin Access", unsafe_allow_html=True)
    
    with st.form("admin_login_form", clear_on_submit=True):
        password = st.text_input("Admin Password", type="password")
        submit = st.form_submit_button("Login as Admin")
        
        if submit:
            try:
                admin_password = st.secrets.get("admin", {}).get("password", "")
                if password == admin_password and admin_password:
                    st.session_state.is_admin = True
                    st.success("Admin access granted!")
                    st.rerun()
                else:
                    st.error("Invalid admin password.")
            except Exception:
                st.error("Admin authentication not configured.")


def logout_user():
    """Log out the current user - clears all session state."""
    keys_to_clear = ["user", "user_status", "is_admin", "generated_questions", 
                     "quiz_answers", "quiz_submitted", "selected_docs"]
    for key in keys_to_clear:
        if key in st.session_state:
            st.session_state[key] = None
    
    st.session_state.current_page = "home"
    st.rerun()


def logout_admin():
    """Log out admin (keep user session)."""
    st.session_state.is_admin = False
    st.rerun()


def get_current_user() -> dict:
    """Get the current user from session state - no DB query."""
    return st.session_state.get("user", None)


def is_admin() -> bool:
    """Check if current session has admin access - no DB query."""
    return st.session_state.get("is_admin", False)
