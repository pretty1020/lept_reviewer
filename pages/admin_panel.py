"""
LEPT AI Reviewer - Admin Panel Page
Modern Techy Theme
"""

import streamlit as st
from datetime import datetime

from components.auth import is_admin, show_admin_login
from services.payment_handler import process_payment_approval, process_payment_rejection
from database.queries import (
    get_all_users, get_pending_payments, get_all_payments,
    get_admin_documents, save_admin_document, delete_admin_document,
    update_admin_document_downloadable, get_admin_actions,
    block_user, adjust_user_quota, log_admin_action,
    delete_user, change_user_plan
)
from database.connection import test_connection
from services.document_processor import extract_text_from_file
from config.settings import (
    COLORS, PLAN_FREE, PLAN_PRO, PLAN_PREMIUM,
    PAYMENT_PENDING, PAYMENT_APPROVED, PAYMENT_REJECTED,
    ACTION_USER_BLOCKED, ACTION_USER_UNBLOCKED, ACTION_QUOTA_ADJUSTED, 
    ACTION_UPLOAD_ADMIN_DOC, ACTION_USER_DELETED, ACTION_PLAN_CHANGED, ACTION_DELETE_ADMIN_DOC
)


def render_admin_page():
    """Render the admin panel page with modern techy theme."""
    if not is_admin():
        st.warning("Admin access required.")
        show_admin_login()
        return
    
    # Header
    st.markdown(f"""
    <div style="padding: 2rem; 
                background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(99, 102, 241, 0.1) 100%);
                border-radius: 20px; margin-bottom: 1.5rem;
                border: 1px solid {COLORS['border']};">
        <h2 style="color: {COLORS['text']}; margin: 0; display: flex; align-items: center; gap: 0.5rem;">
            <span style="filter: drop-shadow(0 0 10px {COLORS['error']});">🛠️</span>
            Admin Panel
        </h2>
        <p style="color: {COLORS['text_muted']}; margin: 0.5rem 0 0 0;">
            Manage users, payments, and reviewer documents.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Admin tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "👥 Users", 
        "💳 Payments", 
        "📚 Admin Reviewers",
        "📊 Audit Logs",
        "⚙️ Settings"
    ])
    
    with tab1:
        render_users_tab()
    
    with tab2:
        render_payments_tab()
    
    with tab3:
        render_admin_docs_tab()
    
    with tab4:
        render_audit_logs_tab()
    
    with tab5:
        render_settings_tab()


def render_users_tab():
    """Render the users management tab."""
    st.markdown(f"<h3 style='color: {COLORS['text']}; margin-bottom: 1rem;'>All Users</h3>", unsafe_allow_html=True)
    
    users = get_all_users()
    
    if not users:
        st.info("No users found.")
        return
    
    # Summary stats
    col1, col2, col3, col4 = st.columns(4)
    
    total_users = len(users)
    free_users = len([u for u in users if u.get("plan_type") == PLAN_FREE])
    pro_users = len([u for u in users if u.get("plan_type") == PLAN_PRO])
    premium_users = len([u for u in users if u.get("plan_type") == PLAN_PREMIUM])
    
    with col1:
        st.metric("Total Users", total_users)
    with col2:
        st.metric("Free Users", free_users)
    with col3:
        st.metric("Pro Users", pro_users)
    with col4:
        st.metric("Premium Users", premium_users)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # User list
    for user in users:
        email = user.get("email", "N/A")
        ip = user.get("ip_address", "N/A")
        plan = user.get("plan_type", PLAN_FREE)
        questions = user.get("questions_remaining", 0)
        is_blocked = user.get("is_blocked", False)
        expiry = user.get("premium_expiry")
        
        plan_colors = {
            PLAN_FREE: COLORS["text_muted"],
            PLAN_PRO: COLORS["primary"],
            PLAN_PREMIUM: COLORS["accent"]
        }
        plan_color = plan_colors.get(plan, COLORS["text_muted"])
        
        blocked_icon = "🚫 " if is_blocked else ""
        
        with st.expander(f"{blocked_icon}{email} - {plan}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Email:** {email}")
                st.markdown(f"**IP Address:** {ip}")
                st.markdown(f"**Plan:** <span style='color: {plan_color}'>{plan}</span>", unsafe_allow_html=True)
                st.markdown(f"**Questions Remaining:** {questions}")
                if expiry:
                    st.markdown(f"**Premium Expiry:** {expiry}")
            
            with col2:
                st.markdown("**Actions:**")
                
                # Change Plan
                plan_options = [PLAN_FREE, PLAN_PRO, PLAN_PREMIUM]
                current_index = plan_options.index(plan) if plan in plan_options else 0
                new_plan = st.selectbox(
                    "Change Plan:",
                    options=plan_options,
                    index=current_index,
                    key=f"plan_{email}"
                )
                
                if st.button("💳 Update Plan", key=f"update_plan_{email}"):
                    change_user_plan(email, new_plan)
                    log_admin_action("admin", ACTION_PLAN_CHANGED, f"Changed plan to {new_plan} for {email}")
                    st.success(f"Plan updated to {new_plan}!")
                    st.rerun()
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Block/Unblock
                if is_blocked:
                    if st.button(f"✅ Unblock User", key=f"unblock_{email}"):
                        block_user(email, False)
                        log_admin_action("admin", ACTION_USER_UNBLOCKED, f"Unblocked user {email}")
                        st.success("User unblocked!")
                        st.rerun()
                else:
                    if st.button(f"🚫 Block User", key=f"block_{email}"):
                        block_user(email, True)
                        log_admin_action("admin", ACTION_USER_BLOCKED, f"Blocked user {email}")
                        st.success("User blocked!")
                        st.rerun()
                
                # Adjust quota
                new_quota = st.number_input(
                    "Adjust Quota:",
                    min_value=0,
                    max_value=10000,
                    value=questions,
                    key=f"quota_{email}"
                )
                
                if st.button("📊 Update Quota", key=f"update_quota_{email}"):
                    adjust_user_quota(email, new_quota)
                    log_admin_action("admin", ACTION_QUOTA_ADJUSTED, f"Quota set to {new_quota} for {email}")
                    st.success("Quota updated!")
                    st.rerun()
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Delete User (with confirmation)
                st.markdown(f"<p style='color: {COLORS['error']};'><strong>Danger Zone:</strong></p>", unsafe_allow_html=True)
                delete_confirm = st.checkbox(f"I confirm to delete this user", key=f"confirm_delete_{email}")
                
                if delete_confirm:
                    if st.button(f"🗑️ Delete User", key=f"delete_{email}", type="primary"):
                        delete_user(email)
                        log_admin_action("admin", ACTION_USER_DELETED, f"Deleted user {email}")
                        st.success(f"User {email} deleted!")
                        st.rerun()


def render_payments_tab():
    """Render the payments management tab."""
    # Pending payments section
    st.markdown(f"<h3 style='color: {COLORS['text']}; margin-bottom: 1rem;'>⏳ Pending Payments</h3>", unsafe_allow_html=True)
    
    pending = get_pending_payments()
    
    if not pending:
        st.success("No pending payments to review.")
    else:
        st.warning(f"{len(pending)} payment(s) awaiting review")
        
        for payment in pending:
            render_payment_card(payment, is_pending=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # All payments
    st.markdown(f"<h3 style='color: {COLORS['text']}; margin-bottom: 1rem;'>📜 All Payments</h3>", unsafe_allow_html=True)
    
    all_payments = get_all_payments()
    
    if not all_payments:
        st.info("No payment history.")
    else:
        for payment in all_payments:
            if payment.get("status") != PAYMENT_PENDING:
                render_payment_card(payment, is_pending=False)


def render_payment_card(payment: dict, is_pending: bool = True):
    """Render a payment card for admin review."""
    payment_id = payment.get("payment_id")
    full_name = payment.get("full_name", "N/A")
    email = payment.get("email", "N/A")
    plan = payment.get("plan_requested", "N/A")
    gcash_ref = payment.get("gcash_ref", "N/A")
    status = payment.get("status", PAYMENT_PENDING)
    created_at = payment.get("created_at", "N/A")
    
    status_colors = {
        PAYMENT_PENDING: COLORS["warning"],
        PAYMENT_APPROVED: COLORS["success"],
        PAYMENT_REJECTED: COLORS["error"]
    }
    status_color = status_colors.get(status, COLORS["text_muted"])
    
    with st.expander(f"{'⏳' if is_pending else '📄'} {full_name} - {plan} ({status})"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**Name:** {full_name}")
            st.markdown(f"**Email:** {email}")
            st.markdown(f"**Plan:** {plan}")
            st.markdown(f"**GCash Ref:** {gcash_ref}")
            st.markdown(f"**Submitted:** {created_at}")
            st.markdown(f"**Status:** <span style='color: {status_color}'>{status}</span>", unsafe_allow_html=True)
            
            if payment.get("admin_notes"):
                st.markdown(f"**Admin Notes:** {payment.get('admin_notes')}")
        
        with col2:
            st.info("Receipt stored in Snowflake stage")
        
        if is_pending:
            st.markdown("---")
            st.markdown("**Admin Actions:**")
            
            admin_notes = st.text_input("Notes:", key=f"notes_{payment_id}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("✅ Approve", key=f"approve_{payment_id}", use_container_width=True, type="primary"):
                    success, msg = process_payment_approval(payment_id, payment, admin_notes)
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
            
            with col2:
                if st.button("❌ Reject", key=f"reject_{payment_id}", use_container_width=True):
                    success, msg = process_payment_rejection(payment_id, payment, admin_notes)
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)


def render_admin_docs_tab():
    """Render the admin documents management tab."""
    st.markdown(f"<h3 style='color: {COLORS['text']}; margin-bottom: 1rem;'>Upload Admin Reviewer</h3>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background: rgba(99, 102, 241, 0.1); padding: 1rem; border-radius: 12px;
                border: 1px solid {COLORS['primary']}; margin-bottom: 1rem;">
        <p style="margin: 0; color: {COLORS['text']};">
            📚 Admin reviewers will be available for PRO/PREMIUM users to download and use for AI-generated questions.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose a PDF or DOCX file",
        type=["pdf", "docx"],
        key="admin_doc_upload"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        category = st.selectbox(
            "Category:",
            options=["General Education", "Professional Education", "Specialization", "Review Materials", "Practice Tests"],
            key="admin_doc_category"
        )
    with col2:
        is_downloadable = st.checkbox("Allow download for PRO/PREMIUM users", value=True)
    
    if uploaded_file:
        st.markdown(f"""
        <div style="background: rgba(6, 182, 212, 0.1); padding: 0.75rem 1rem; border-radius: 10px; margin: 0.5rem 0;">
            <p style="margin: 0; color: {COLORS['text']};">
                📎 Selected: <strong>{uploaded_file.name}</strong> ({uploaded_file.size / 1024:.1f} KB)
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📤 Upload Admin Reviewer", use_container_width=True, type="primary"):
            with st.spinner("Processing document..."):
                # Read file content
                file_content = uploaded_file.getvalue()
                
                # Extract text from file
                success, extracted_text = extract_text_from_file(uploaded_file)
                
                storage_path = f"@STAGE_ADMIN_DOCS/{uploaded_file.name}"
                file_type = uploaded_file.name.split('.')[-1].lower()
                
                doc_id = save_admin_document(
                    filename=uploaded_file.name,
                    file_type=file_type,
                    storage_path=storage_path,
                    is_downloadable=is_downloadable,
                    uploaded_by="admin",
                    file_content=file_content,
                    extracted_text=extracted_text if success else None,
                    category=category
                )
                
                if doc_id:
                    log_admin_action("admin", ACTION_UPLOAD_ADMIN_DOC, f"Uploaded {uploaded_file.name} (Category: {category})")
                    st.success(f"✅ Admin reviewer uploaded successfully! Text extracted: {'Yes' if success else 'No'}")
                    st.rerun()
                else:
                    st.error("Failed to save document.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Existing admin documents
    st.markdown(f"<h3 style='color: {COLORS['text']}; margin-bottom: 1rem;'>Existing Admin Reviewers</h3>", unsafe_allow_html=True)
    
    docs = get_admin_documents()
    
    if not docs:
        st.info("No admin reviewers uploaded yet.")
    else:
        st.markdown(f"<p style='color: {COLORS['text_muted']};'>{len(docs)} reviewer(s) uploaded</p>", unsafe_allow_html=True)
        
        for doc in docs:
            doc_id = doc.get("doc_id")
            filename = doc.get("filename", "Unknown")
            is_downloadable = doc.get("is_downloadable", False)
            category = doc.get("category", "General")
            has_text = doc.get("extracted_text") is not None
            
            st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.8); padding: 1rem; border-radius: 12px; 
                        border: 1px solid {COLORS['border']}; margin-bottom: 0.5rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                    <div>
                        <strong style="color: {COLORS['text']};">{filename}</strong>
                        <span style="background: {COLORS['primary']}33; color: {COLORS['primary']}; 
                                     padding: 2px 8px; border-radius: 10px; font-size: 0.75rem; margin-left: 0.5rem;">
                            {category}
                        </span>
                        <span style="color: {'#10B981' if has_text else '#F59E0B'}; font-size: 0.75rem; margin-left: 0.5rem;">
                            {'✅ Text Ready' if has_text else '⚠️ No Text'}
                        </span>
                    </div>
                    <div>
                        <span style="color: {COLORS['success'] if is_downloadable else COLORS['warning']}; font-size: 0.85rem;">
                            {'📥 Downloadable' if is_downloadable else '🔒 View Only'}
                        </span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                toggle_label = "🔓 Make Downloadable" if not is_downloadable else "🔒 Remove Download"
                if st.button(toggle_label, key=f"toggle_{doc_id}"):
                    update_admin_document_downloadable(doc_id, not is_downloadable)
                    st.rerun()
            
            with col2:
                pass  # Space for future actions
            
            with col3:
                if st.button("🗑️ Delete", key=f"delete_admin_{doc_id}"):
                    delete_admin_document(doc_id)
                    log_admin_action("admin", ACTION_DELETE_ADMIN_DOC, f"Deleted {filename}")
                    st.success("Deleted!")
                    st.rerun()


def render_audit_logs_tab():
    """Render the audit logs tab."""
    st.markdown(f"<h3 style='color: {COLORS['text']}; margin-bottom: 1rem;'>Admin Actions Log</h3>", unsafe_allow_html=True)
    
    actions = get_admin_actions(limit=50)
    
    if not actions:
        st.info("No admin actions logged yet.")
        return
    
    for action in actions:
        action_type = action.get("action_type", "Unknown")
        admin_user = action.get("admin_user", "N/A")
        details = action.get("details", "")
        action_time = action.get("action_time", "N/A")
        
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.8); padding: 0.75rem 1rem; border-radius: 10px; 
                    border-left: 3px solid {COLORS['primary']}; margin-bottom: 0.5rem;">
            <div style="display: flex; justify-content: space-between;">
                <strong style="color: {COLORS['text']};">{action_type}</strong>
                <span style="color: {COLORS['text_muted']}; font-size: 0.85rem;">{action_time}</span>
            </div>
            <p style="margin: 0.25rem 0 0 0; color: {COLORS['text_muted']}; font-size: 0.9rem;">
                By: {admin_user} | {details}
            </p>
        </div>
        """, unsafe_allow_html=True)


def render_settings_tab():
    """Render admin settings tab."""
    st.markdown(f"<h3 style='color: {COLORS['text']}; margin-bottom: 1rem;'>Database Management</h3>", unsafe_allow_html=True)
    
    st.warning("⚠️ These actions are for database management. Use with caution!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.8); padding: 1.5rem; border-radius: 16px;
                    border: 1px solid {COLORS['border']};">
            <h4 style="color: {COLORS['text']}; margin: 0 0 0.5rem 0;">🔌 Test Connection</h4>
            <p style="color: {COLORS['text_muted']}; margin: 0 0 1rem 0; font-size: 0.9rem;">
                Test Snowflake database connection.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Test Connection", key="test_conn_btn", use_container_width=True):
            with st.spinner("Testing connection..."):
                success, result = test_connection()
            if success:
                st.success(f"Connected! Snowflake version: {result}")
            else:
                st.error(f"Connection failed: {result}")
    
    with col2:
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.8); padding: 1.5rem; border-radius: 16px;
                    border: 1px solid {COLORS['border']};">
            <h4 style="color: {COLORS['text']}; margin: 0 0 0.5rem 0;">📊 System Info</h4>
            <p style="color: {COLORS['text_muted']}; margin: 0; font-size: 0.9rem;">
                Free Limit: 10 questions<br>
                Pro Bonus: +75 questions<br>
                Premium: 30 days unlimited
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background: rgba(30, 41, 59, 0.8); padding: 1.5rem; border-radius: 16px;
                border: 1px solid {COLORS['border']};">
        <h4 style="color: {COLORS['text']}; margin: 0 0 1rem 0;">💰 Pricing Configuration</h4>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
            <div>
                <p style="color: {COLORS['text_muted']}; margin: 0;">Pro Plan</p>
                <p style="color: {COLORS['primary']}; font-size: 1.5rem; font-weight: 700; margin: 0;">₱99</p>
            </div>
            <div>
                <p style="color: {COLORS['text_muted']}; margin: 0;">Premium Plan</p>
                <p style="color: {COLORS['accent']}; font-size: 1.5rem; font-weight: 700; margin: 0;">₱499</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
