"""
LEPT AI Reviewer - Sidebar Navigation Component
Modern Techy Theme
"""

import streamlit as st

from components.auth import get_current_user, is_admin, logout_user, logout_admin, show_admin_login
from services.usage_tracker import get_user_status
from config.settings import EMAIL_SHARING_WARNING, COLORS, PLAN_FREE, PLAN_PRO, PLAN_PREMIUM


def render_sidebar():
    """Render the main navigation sidebar with modern techy theme."""
    with st.sidebar:
        # App branding
        st.markdown(f"""
        <div style="text-align: center; padding: 1.5rem 0; margin-bottom: 1rem;
                    border-bottom: 1px solid {COLORS['border']};">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;
                        filter: drop-shadow(0 0 20px {COLORS['glow']});">🎓</div>
            <h2 style="background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                       margin: 0; font-size: 1.3rem;">LEPT AI Reviewer</h2>
            <p style="color: {COLORS['text_muted']}; margin: 0; font-size: 0.75rem;
                      letter-spacing: 1px;">PHILIPPINE EDITION</p>
        </div>
        """, unsafe_allow_html=True)
        
        user = get_current_user()
        
        if user:
            # User info section
            status = get_user_status(user)
            
            plan_colors = {
                PLAN_FREE: COLORS["text_muted"],
                PLAN_PRO: COLORS["primary"],
                PLAN_PREMIUM: COLORS["accent"]
            }
            plan_color = plan_colors.get(status["plan"], COLORS["text_muted"])
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(6, 182, 212, 0.1) 100%);
                        padding: 1rem; border-radius: 12px; margin-bottom: 1rem;
                        border: 1px solid {COLORS['border']};">
                <p style="margin: 0; font-size: 0.8rem; color: {COLORS['text_muted']};">Logged in as</p>
                <p style="margin: 0; font-weight: 600; color: {COLORS['text']}; 
                          word-wrap: break-word; font-size: 0.9rem;">{user.get('email', 'N/A')}</p>
                <hr style="border-color: {COLORS['border']}; margin: 0.75rem 0;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: {COLORS['text_muted']}; font-size: 0.8rem;">Plan</span>
                    <span style="background: {plan_color}33; color: {plan_color}; 
                                 padding: 2px 10px; border-radius: 20px; font-size: 0.75rem;
                                 font-weight: 600;">{status['plan']}</span>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.5rem;">
                    <span style="color: {COLORS['text_muted']}; font-size: 0.8rem;">Questions</span>
                    <span style="color: {COLORS['secondary']}; font-weight: 700;">{status['questions_display']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if status.get("expiry_display"):
                st.info(f"⏰ {status['expiry_display']}")
            
            # Navigation menu
            st.markdown(f"<p style='color: {COLORS['text_muted']}; font-size: 0.75rem; letter-spacing: 1px; margin: 1rem 0 0.5rem 0;'>NAVIGATION</p>", unsafe_allow_html=True)
            
            # Navigation buttons with icons
            nav_items = [
                ("🏠", "Home", "home"),
                ("📄", "Upload Reviewer", "upload"),
                ("🧠", "Practice Exam", "practice"),
                ("💳", "Upgrade", "upgrade"),
            ]
            
            for icon, label, page_key in nav_items:
                is_active = st.session_state.get("current_page") == page_key
                button_type = "primary" if is_active else "secondary"
                
                if st.button(f"{icon} {label}", key=f"nav_{page_key}", use_container_width=True,
                           type=button_type):
                    st.session_state.current_page = page_key
                    st.rerun()
            
            # Admin panel (only show if admin)
            if is_admin():
                st.markdown(f"<p style='color: {COLORS['text_muted']}; font-size: 0.75rem; letter-spacing: 1px; margin: 1.5rem 0 0.5rem 0;'>ADMIN</p>", unsafe_allow_html=True)
                
                if st.button("🛠️ Admin Panel", key="nav_admin", use_container_width=True):
                    st.session_state.current_page = "admin"
                    st.rerun()
                
                if st.button("🚪 Exit Admin", key="exit_admin", use_container_width=True):
                    logout_admin()
            else:
                # Admin login option (collapsed)
                with st.expander("🔐 Admin Access"):
                    show_admin_login()
            
            # Warning banner
            st.markdown("<br>", unsafe_allow_html=True)
            st.warning(EMAIL_SHARING_WARNING)
            
            # Logout button
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚪 Logout", key="logout_btn", use_container_width=True):
                logout_user()
        
        else:
            st.info("Please log in to access the reviewer.")
        
        # Footer
        st.markdown(f"""
        <div style="text-align: center; color: {COLORS['text_muted']}; font-size: 0.7rem;
                    margin-top: 2rem; padding-top: 1rem; border-top: 1px solid {COLORS['border']};">
            <p style="margin: 0;">LEPT AI Reviewer (PH)</p>
            <p style="margin: 0;">© 2024 All rights reserved</p>
        </div>
        """, unsafe_allow_html=True)


def get_current_page() -> str:
    """Get the currently selected page."""
    return st.session_state.get("current_page", "home")


def set_current_page(page: str):
    """Set the current page."""
    st.session_state.current_page = page
