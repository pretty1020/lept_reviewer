"""
LEPT AI Reviewer - Alert and Notification Components
Modern Techy Theme
"""

import streamlit as st
from config.settings import COLORS, EMAIL_SHARING_WARNING


def show_email_warning():
    """Display the email sharing warning banner."""
    st.warning(EMAIL_SHARING_WARNING)


def show_upgrade_prompt(message: str = None):
    """Display an upgrade prompt."""
    if message is None:
        message = "You've used all your free questions. Upgrade to continue your LEPT review!"
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(139, 92, 246, 0.15) 100%); 
                padding: 1.5rem; border-radius: 16px; text-align: center; margin: 1rem 0;
                border: 2px solid {COLORS['warning']};">
        <h3 style="color: {COLORS['warning']}; margin: 0 0 0.5rem 0;">⚡ Upgrade Required</h3>
        <p style="color: {COLORS['text']}; margin: 0 0 1rem 0;">{message}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("💳 Upgrade Now", key="upgrade_prompt_btn", use_container_width=True, type="primary"):
        st.session_state.current_page = "upgrade"
        st.rerun()


def show_success_message(title: str, message: str):
    """Display a success message card."""
    st.markdown(f"""
    <div style="background: rgba(16, 185, 129, 0.15); padding: 1rem; border-radius: 12px; 
                border-left: 4px solid {COLORS['success']}; margin: 1rem 0;">
        <h4 style="color: {COLORS['success']}; margin: 0;">✓ {title}</h4>
        <p style="color: {COLORS['text']}; margin: 0.5rem 0 0 0;">{message}</p>
    </div>
    """, unsafe_allow_html=True)


def show_error_message(title: str, message: str):
    """Display an error message card."""
    st.markdown(f"""
    <div style="background: rgba(239, 68, 68, 0.15); padding: 1rem; border-radius: 12px; 
                border-left: 4px solid {COLORS['error']}; margin: 1rem 0;">
        <h4 style="color: {COLORS['error']}; margin: 0;">✗ {title}</h4>
        <p style="color: {COLORS['text']}; margin: 0.5rem 0 0 0;">{message}</p>
    </div>
    """, unsafe_allow_html=True)


def show_info_banner(message: str, icon: str = "ℹ️"):
    """Display an info banner."""
    st.markdown(f"""
    <div style="background: rgba(6, 182, 212, 0.15); padding: 1rem; border-radius: 12px; 
                text-align: center; margin: 1rem 0; border: 1px solid rgba(6, 182, 212, 0.3);">
        <span style="font-size: 1.5rem;">{icon}</span>
        <p style="color: {COLORS['text']}; margin: 0.5rem 0 0 0;">{message}</p>
    </div>
    """, unsafe_allow_html=True)


def show_payment_pending_banner():
    """Display a banner for pending payment status."""
    st.markdown(f"""
    <div style="background: rgba(245, 158, 11, 0.15); padding: 1rem; border-radius: 12px; 
                border: 1px solid rgba(245, 158, 11, 0.3); margin: 1rem 0;">
        <h4 style="color: {COLORS['warning']}; margin: 0;">⏳ Payment Pending</h4>
        <p style="color: {COLORS['text']}; margin: 0.5rem 0 0 0;">
            Your payment is being processed. Please allow 12-24 hours for validation.
        </p>
    </div>
    """, unsafe_allow_html=True)


def show_blocked_user_message():
    """Display message for blocked users."""
    st.markdown(f"""
    <div style="background: rgba(239, 68, 68, 0.15); padding: 2rem; border-radius: 16px; 
                text-align: center; margin: 2rem 0; border: 1px solid rgba(239, 68, 68, 0.3);">
        <span style="font-size: 3rem;">🚫</span>
        <h3 style="color: {COLORS['error']}; margin: 1rem 0 0.5rem 0;">Account Blocked</h3>
        <p style="color: {COLORS['text']};">
            Your account has been blocked. If you believe this is an error, 
            please contact support for assistance.
        </p>
    </div>
    """, unsafe_allow_html=True)


def show_premium_expired_banner():
    """Display banner for expired premium subscription."""
    st.markdown(f"""
    <div style="background: rgba(245, 158, 11, 0.15); padding: 1rem; border-radius: 12px; 
                border: 1px solid rgba(245, 158, 11, 0.3); margin: 1rem 0;">
        <h4 style="color: {COLORS['warning']}; margin: 0;">⏰ Premium Expired</h4>
        <p style="color: {COLORS['text']}; margin: 0.5rem 0 0 0;">
            Your Premium subscription has expired. Renew now to continue with unlimited access!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("💳 Renew Premium", key="renew_premium_btn", use_container_width=True, type="primary"):
        st.session_state.current_page = "upgrade"
        st.rerun()


def show_document_required_message():
    """Display message when no documents are available for practice."""
    st.markdown(f"""
    <div style="background: rgba(6, 182, 212, 0.1); padding: 2rem; border-radius: 16px; 
                text-align: center; margin: 2rem 0; border: 2px dashed {COLORS['secondary']};">
        <span style="font-size: 3rem; filter: drop-shadow(0 0 10px {COLORS['secondary']});">📄</span>
        <h3 style="color: {COLORS['text']}; margin: 1rem 0 0.5rem 0;">No Documents Available</h3>
        <p style="color: {COLORS['text_muted']};">
            Upload your reviewer documents first to generate practice questions.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("📄 Upload Reviewer", key="upload_redirect_btn", use_container_width=True, type="primary"):
        st.session_state.current_page = "upload"
        st.rerun()
