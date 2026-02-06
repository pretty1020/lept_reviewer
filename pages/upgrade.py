"""
LEPT AI Reviewer - Upgrade Page
Modern Techy Theme
"""

import streamlit as st

from components.auth import get_current_user
from components.alerts import show_email_warning, show_payment_pending_banner
from services.usage_tracker import get_user_status
from services.payment_handler import submit_payment_request, get_user_payment_status, get_plan_details
from utils.validators import validate_full_name, validate_email
from config.settings import (
    COLORS, PLAN_FREE, PLAN_PRO, PLAN_PREMIUM,
    PRO_PRICE, PREMIUM_PRICE, GCASH_NUMBER, GCASH_ACCOUNT_NAME,
    PAYMENT_PENDING, PAYMENT_APPROVED, PAYMENT_REJECTED
)


def render_upgrade_page():
    """Render the upgrade/payment page with modern techy theme."""
    user = get_current_user()
    
    if not user:
        st.error("Please log in to continue.")
        return
    
    email = user.get("email", "")
    status = get_user_status(user)
    payment_status = get_user_payment_status(email)
    
    # Header
    st.markdown(f"""
    <div style="padding: 2rem; 
                background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(99, 102, 241, 0.1) 100%);
                border-radius: 20px; margin-bottom: 1.5rem;
                border: 1px solid {COLORS['border']};">
        <h2 style="color: {COLORS['text']}; margin: 0; display: flex; align-items: center; gap: 0.5rem;">
            <span style="filter: drop-shadow(0 0 10px {COLORS['accent']});">💳</span>
            Payment & Receipt Upload
        </h2>
        <p style="color: {COLORS['text_muted']}; margin: 0.5rem 0 0 0;">
            Upgrade your plan to unlock more questions and premium features.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    show_email_warning()
    
    # Show pending payment status if any
    if payment_status.get("has_pending"):
        show_payment_pending_banner()
    
    # Section 1: Payment Tiers
    st.markdown(f"<h3 style='color: {COLORS['text']}; margin: 1.5rem 0 1rem 0;'>1️⃣ PAYMENT TIERS</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    free_details = get_plan_details(PLAN_FREE)
    pro_details = get_plan_details(PLAN_PRO)
    premium_details = get_plan_details(PLAN_PREMIUM)
    
    with col1:
        is_current = status["plan"] == PLAN_FREE
        border_color = COLORS['success'] if is_current else COLORS['border']
        current_badge = f'<span style="background: {COLORS["success"]}; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.7rem; margin-left: 0.5rem;">CURRENT</span>' if is_current else ""
        
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.8); padding: 1.5rem; border-radius: 16px; 
                    border: 2px solid {border_color}; height: 100%;">
            <h3 style="color: {COLORS['text_muted']}; margin: 0; font-size: 1.1rem;">{free_details['name']}{current_badge}</h3>
            <p style="font-size: 2.5rem; font-weight: 700; color: {COLORS['text']}; margin: 0.5rem 0;">Free</p>
            <p style="color: {COLORS['text_muted']}; margin: 0 0 1rem 0;">{free_details['questions']}</p>
            <ul style="list-style: none; padding: 0; margin: 0;">
                {''.join([f"<li style='padding: 0.3rem 0; color: {COLORS['text_muted']};'>✓ {f}</li>" for f in free_details['features']])}
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        is_current = status["plan"] == PLAN_PRO
        border_color = COLORS['success'] if is_current else COLORS['primary']
        current_badge = f'<span style="background: {COLORS["success"]}; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.7rem; margin-left: 0.5rem;">CURRENT</span>' if is_current else ""
        
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.8); padding: 1.5rem; border-radius: 16px; 
                    border: 2px solid {border_color}; height: 100%;
                    box-shadow: 0 0 20px rgba(99, 102, 241, 0.2);">
            <h3 style="color: {COLORS['primary']}; margin: 0; font-size: 1.1rem;">{pro_details['name']}{current_badge}</h3>
            <p style="font-size: 2.5rem; font-weight: 700; color: {COLORS['text']}; margin: 0.5rem 0;">₱{PRO_PRICE}</p>
            <p style="color: {COLORS['text_muted']}; margin: 0 0 1rem 0;">{pro_details['questions']}</p>
            <ul style="list-style: none; padding: 0; margin: 0;">
                {''.join([f"<li style='padding: 0.3rem 0; color: {COLORS['text_muted']};'>✓ {f}</li>" for f in pro_details['features']])}
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        is_current = status["plan"] == PLAN_PREMIUM
        border_color = COLORS['success'] if is_current else COLORS['accent']
        current_badge = f'<span style="background: {COLORS["success"]}; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.7rem; margin-left: 0.5rem;">CURRENT</span>' if is_current else ""
        
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.8); padding: 1.5rem; border-radius: 16px; 
                    border: 2px solid {border_color}; height: 100%; position: relative;
                    box-shadow: 0 0 30px rgba(139, 92, 246, 0.3);">
            <span style="background: linear-gradient(135deg, {COLORS['accent']} 0%, {COLORS['primary']} 100%); 
                         color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.7rem; 
                         position: absolute; top: -10px; right: 10px;">RECOMMENDED</span>
            <h3 style="color: {COLORS['accent']}; margin: 0; font-size: 1.1rem;">{premium_details['name']}{current_badge}</h3>
            <p style="font-size: 2.5rem; font-weight: 700; color: {COLORS['text']}; margin: 0.5rem 0;">₱{PREMIUM_PRICE}</p>
            <p style="color: {COLORS['text_muted']}; margin: 0 0 1rem 0;">{premium_details['questions']}</p>
            <ul style="list-style: none; padding: 0; margin: 0;">
                {''.join([f"<li style='padding: 0.3rem 0; color: {COLORS['text_muted']};'>✓ {f}</li>" for f in premium_details['features']])}
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Section 2: Payment Method
    st.markdown(f"<h3 style='color: {COLORS['text']}; margin: 1.5rem 0 1rem 0;'>2️⃣ PAYMENT METHOD</h3>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background: rgba(30, 41, 59, 0.8); padding: 1.5rem; border-radius: 16px; 
                border: 1px solid {COLORS['border']};">
        <h4 style="color: {COLORS['secondary']}; margin: 0 0 1rem 0;">💙 Pay via GCash</h4>
        <div style="background: rgba(6, 182, 212, 0.1); padding: 1.25rem; border-radius: 12px;
                    border: 1px solid rgba(6, 182, 212, 0.3);">
            <p style="margin: 0; font-size: 1rem; color: {COLORS['text_muted']};">
                <strong style="color: {COLORS['text']};">GCash Number:</strong> 
                <span style="font-size: 1.3rem; color: {COLORS['secondary']}; font-weight: 700;">{GCASH_NUMBER}</span>
            </p>
            <p style="margin: 0.5rem 0 0 0; color: {COLORS['text_muted']};">
                <strong style="color: {COLORS['text']};">Account Name:</strong> {GCASH_ACCOUNT_NAME}
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Section 3: Receipt Submission
    st.markdown(f"<h3 style='color: {COLORS['text']}; margin: 1.5rem 0 1rem 0;'>3️⃣ RECEIPT SUBMISSION</h3>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background: rgba(99, 102, 241, 0.1); padding: 1rem; border-radius: 12px; 
                border: 1px solid rgba(99, 102, 241, 0.3); margin-bottom: 1rem;">
        <p style="margin: 0; color: {COLORS['text']};">
            📧 After sending payment via GCash, upload your receipt below.
        </p>
        <p style="margin: 0.5rem 0 0 0; color: {COLORS['text_muted']}; font-size: 0.9rem;">
            <strong>Please specify which plan you're purchasing (PRO or PREMIUM)</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Section 4: Important Notice
    st.markdown(f"<h3 style='color: {COLORS['text']}; margin: 1.5rem 0 1rem 0;'>⚠️ IMPORTANT NOTICE</h3>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background: rgba(245, 158, 11, 0.1); padding: 1rem; border-radius: 12px; 
                border-left: 4px solid {COLORS['warning']};">
        <p style="margin: 0; color: {COLORS['text']};">
            ✅ Access will be activated after receipt validation.
        </p>
        <p style="margin: 0.5rem 0 0 0; color: {COLORS['text']};">
            ⏰ Please allow <strong>12-24 hours</strong> for processing.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Payment Form
    st.markdown(f"<h3 style='color: {COLORS['text']}; margin: 1.5rem 0 1rem 0;'>📝 Payment Details Form</h3>", unsafe_allow_html=True)
    
    with st.form("payment_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input(
                "Full Name *",
                placeholder="Juan Dela Cruz",
                help="Enter your full name as it appears on your GCash account"
            )
        
        with col2:
            form_email = st.text_input(
                "Email Address *",
                value=email,
                placeholder="your.email@example.com",
                help="Email for payment confirmation"
            )
        
        col1, col2 = st.columns(2)
        
        with col1:
            plan_selected = st.selectbox(
                "Plan to Purchase *",
                options=[PLAN_PRO, PLAN_PREMIUM],
                format_func=lambda x: f"{x} - ₱{PRO_PRICE}" if x == PLAN_PRO else f"{x} - ₱{PREMIUM_PRICE}"
            )
        
        with col2:
            gcash_ref = st.text_input(
                "GCash Reference Number (Optional)",
                placeholder="e.g., 1234567890",
                help="Reference number from your GCash transaction"
            )
        
        receipt_file = st.file_uploader(
            "Upload Receipt (Image/PDF) *",
            type=["png", "jpg", "jpeg", "pdf"],
            help="Upload a screenshot or PDF of your GCash payment receipt"
        )
        
        submitted = st.form_submit_button("📤 Submit Payment Request", use_container_width=True, type="primary")
        
        if submitted:
            # Validation
            if not full_name:
                st.error("Full name is required.")
            elif not form_email:
                st.error("Email address is required.")
            elif not receipt_file:
                st.error("Please upload your payment receipt.")
            else:
                valid_name, name_error = validate_full_name(full_name)
                valid_email, email_error = validate_email(form_email)
                
                if not valid_name:
                    st.error(name_error)
                elif not valid_email:
                    st.error(email_error)
                else:
                    # Submit payment
                    success, message = submit_payment_request(
                        email=form_email,
                        full_name=full_name,
                        plan_requested=plan_selected,
                        gcash_ref=gcash_ref,
                        receipt_file=receipt_file
                    )
                    
                    if success:
                        st.success(message)
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(message)
    
    # Payment History
    st.markdown(f"<h3 style='color: {COLORS['text']}; margin: 2rem 0 1rem 0;'>📜 Payment History</h3>", unsafe_allow_html=True)
    
    payments = payment_status.get("payments", [])
    
    if not payments:
        st.info("No payment history yet.")
    else:
        for payment in payments:
            status_colors = {
                PAYMENT_PENDING: (COLORS["warning"], "⏳ PENDING"),
                PAYMENT_APPROVED: (COLORS["success"], "✅ APPROVED"),
                PAYMENT_REJECTED: (COLORS["error"], "❌ REJECTED")
            }
            status_info = status_colors.get(payment.get("status"), (COLORS["text_muted"], "UNKNOWN"))
            
            st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.8); padding: 1rem; border-radius: 12px; 
                        border: 1px solid {COLORS['border']}; margin-bottom: 0.5rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong style="color: {COLORS['text']};">{payment.get('plan_requested')}</strong>
                        <span style="color: {COLORS['text_muted']}; margin-left: 0.5rem;">
                            {payment.get('created_at', 'N/A')}
                        </span>
                    </div>
                    <span style="background: {status_info[0]}33; color: {status_info[0]}; padding: 4px 12px; 
                                 border-radius: 10px; font-size: 0.8rem; font-weight: 600;">
                        {status_info[1]}
                    </span>
                </div>
                {f"<p style='margin: 0.5rem 0 0 0; color: {COLORS['text_muted']}; font-size: 0.85rem;'>Note: {payment.get('admin_notes')}</p>" if payment.get('admin_notes') else ""}
            </div>
            """, unsafe_allow_html=True)
