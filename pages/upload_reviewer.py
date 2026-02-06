"""
LEPT AI Reviewer - Upload Reviewer Page
Modern Techy Theme - PRO/PREMIUM Only
"""

import streamlit as st
import base64

from components.auth import get_current_user
from components.alerts import show_email_warning
from services.document_processor import extract_text_from_file, get_text_stats
from services.usage_tracker import get_user_status
from database.queries import (
    save_user_document, get_user_documents, delete_user_document,
    get_admin_documents, get_admin_document_content
)
from utils.file_utils import validate_file, get_file_icon
from config.settings import COLORS, PLAN_FREE, PLAN_PRO, PLAN_PREMIUM


def render_upload_page():
    """Render the document upload page with modern techy theme."""
    user = get_current_user()
    
    if not user:
        st.error("Please log in to continue.")
        return
    
    email = user.get("email")
    status = get_user_status(user)
    is_free_user = status["plan"] == PLAN_FREE
    
    # If somehow a FREE user gets here, redirect to upgrade
    if is_free_user:
        st.markdown(f"""
        <div style="background: rgba(239, 68, 68, 0.15); padding: 2rem; border-radius: 16px;
                    border: 2px solid {COLORS['error']}; text-align: center; margin-bottom: 1rem;">
            <div style="font-size: 3rem; margin-bottom: 0.75rem;">🔒</div>
            <h3 style="color: {COLORS['error']}; margin: 0 0 0.5rem 0;">PRO/PREMIUM Feature</h3>
            <p style="color: {COLORS['text_muted']}; margin: 0 0 1rem 0;">
                Uploading reviewers and downloading admin resources is available for PRO and PREMIUM users only.
            </p>
            <p style="color: {COLORS['text']}; margin: 0;">
                Upgrade now to unlock <strong style="color: {COLORS['primary']};">AI-generated questions</strong> from your own reviewers!
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("💳 Upgrade to Unlock", key="upgrade_from_upload", use_container_width=True, type="primary"):
            st.session_state.current_page = "upgrade"
            st.rerun()
        return
    
    # Header
    st.markdown(f"""
    <div style="padding: 2rem; 
                background: linear-gradient(135deg, rgba(6, 182, 212, 0.2) 0%, rgba(99, 102, 241, 0.1) 100%);
                border-radius: 20px; margin-bottom: 1.5rem;
                border: 1px solid {COLORS['border']};">
        <h2 style="color: {COLORS['text']}; margin: 0; display: flex; align-items: center; gap: 0.5rem;">
            <span style="filter: drop-shadow(0 0 10px {COLORS['secondary']});">📄</span>
            Upload & Download Reviewers
        </h2>
        <p style="color: {COLORS['text_muted']}; margin: 0.5rem 0 0 0;">
            Upload your own reviewers or download admin resources for AI-generated practice questions.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs for User Documents and Admin Documents
    tab1, tab2 = st.tabs(["📤 My Documents", "📥 Download Admin Reviewers"])
    
    with tab1:
        render_user_documents_tab(email)
    
    with tab2:
        render_admin_documents_tab(email, status)


def render_user_documents_tab(email: str):
    """Render the user's uploaded documents tab."""
    st.markdown(f"<h3 style='color: {COLORS['text']}; margin: 1rem 0;'>Upload New Document</h3>", unsafe_allow_html=True)
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a PDF or DOCX file",
        type=["pdf", "docx"],
        help="Upload your reviewer materials. Supported formats: PDF, DOCX",
        key="user_doc_upload"
    )
    
    if uploaded_file:
        # Validate file
        valid, error_msg = validate_file(uploaded_file)
        
        if not valid:
            st.error(error_msg)
        else:
            st.markdown(f"""
            <div style="background: rgba(6, 182, 212, 0.1); padding: 1rem; border-radius: 12px;
                        border: 1px solid rgba(6, 182, 212, 0.3); margin: 1rem 0;">
                <p style="color: {COLORS['text']}; margin: 0;">
                    📎 Selected: <strong>{uploaded_file.name}</strong> ({uploaded_file.size / 1024:.1f} KB)
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("📤 Upload & Process", key="process_upload_btn", use_container_width=True, type="primary"):
                with st.spinner("Extracting text from document..."):
                    success, result = extract_text_from_file(uploaded_file)
                
                if success:
                    # Save to database
                    file_type = uploaded_file.name.split('.')[-1].lower()
                    storage_path = f"@STAGE_USER_DOCS/{email}/{uploaded_file.name}"
                    
                    doc_id = save_user_document(
                        email=email,
                        filename=uploaded_file.name,
                        file_type=file_type,
                        storage_path=storage_path,
                        text_hash=None  # Could add hash of extracted text
                    )
                    
                    if doc_id:
                        st.success("✅ Document uploaded and processed successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to save document. Please try again.")
                else:
                    st.error(f"❌ {result}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display existing documents
    st.markdown(f"<h3 style='color: {COLORS['text']}; margin: 1rem 0;'>My Uploaded Documents</h3>", unsafe_allow_html=True)
    
    docs = get_user_documents(email)
    
    if not docs:
        st.markdown(f"""
        <div style="background: rgba(6, 182, 212, 0.1); padding: 2rem; border-radius: 16px; 
                    text-align: center; border: 2px dashed {COLORS['secondary']};">
            <span style="font-size: 3rem; filter: drop-shadow(0 0 10px {COLORS['secondary']});">📄</span>
            <p style="color: {COLORS['text_muted']}; margin: 1rem 0 0 0;">
                No documents uploaded yet. Upload your first reviewer above!
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for doc in docs:
            render_document_item(doc, email)


def render_admin_documents_tab(email: str, status: dict):
    """Render the admin-provided documents tab with download feature."""
    st.markdown(f"<h3 style='color: {COLORS['text']}; margin: 1rem 0;'>Admin Reviewer Library</h3>", unsafe_allow_html=True)
    
    can_use = status.get("can_use_admin_docs", False)
    user_plan = status.get("plan", PLAN_FREE)
    
    # Benefit highlight
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(99, 102, 241, 0.1) 100%); 
                padding: 1.25rem; border-radius: 16px;
                border: 1px solid rgba(139, 92, 246, 0.4); margin-bottom: 1.5rem;">
        <div style="display: flex; align-items: center; gap: 0.75rem;">
            <span style="font-size: 2rem; filter: drop-shadow(0 0 10px {COLORS['accent']});">📚</span>
            <div>
                <h4 style="color: {COLORS['accent']}; margin: 0;">✨ PRO/PREMIUM Exclusive!</h4>
                <p style="color: {COLORS['text']}; margin: 0.25rem 0 0 0; font-size: 0.95rem;">
                    Download curated admin reviewer materials and use them for <strong>AI-generated practice questions</strong>!
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    docs = get_admin_documents()
    
    if not docs:
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.6); padding: 2rem; border-radius: 16px; 
                    text-align: center; border: 1px solid {COLORS['border']};">
            <span style="font-size: 3rem;">📚</span>
            <p style="color: {COLORS['text_muted']}; margin: 1rem 0 0 0;">
                No admin reviewers available yet. Check back later!
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <p style="color: {COLORS['text_muted']}; margin-bottom: 1rem;">
            <strong style="color: {COLORS['secondary']};">{len(docs)}</strong> reviewer(s) available
        </p>
        """, unsafe_allow_html=True)
        
        for doc in docs:
            render_admin_document_item(doc, can_use, user_plan)


def render_document_item(doc: dict, email: str):
    """Render a single user document item."""
    filename = doc.get("filename", "Unknown")
    doc_id = doc.get("doc_id")
    created_at = doc.get("created_at")
    
    icon = get_file_icon(filename)
    
    st.markdown(f"""
    <div style="background: rgba(30, 41, 59, 0.8); padding: 1rem; border-radius: 12px; 
                border: 1px solid {COLORS['border']}; margin-bottom: 0.5rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
            <div>
                <span style="font-size: 1.3rem;">{icon}</span>
                <span style="margin-left: 0.5rem; font-weight: 500; color: {COLORS['text']};">{filename}</span>
            </div>
            <div style="font-size: 0.85rem; color: {COLORS['text_muted']};">
                {f"Uploaded: {created_at}" if created_at else ""}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("🗑️ Delete", key=f"delete_{doc_id}", use_container_width=True):
            delete_user_document(doc_id, email)
            st.success("Document deleted!")
            st.rerun()


def render_admin_document_item(doc: dict, can_use: bool, user_plan: str):
    """Render an admin document item with download button."""
    filename = doc.get("filename", "Unknown")
    doc_id = doc.get("doc_id")
    category = doc.get("category", "General")
    is_downloadable = doc.get("is_downloadable", True)
    file_type = doc.get("file_type", "pdf")
    
    icon = get_file_icon(filename)
    
    # Style based on access
    border_color = COLORS['accent'] if can_use else COLORS['border']
    glow = f"box-shadow: 0 0 15px rgba(139, 92, 246, 0.2);" if can_use else ""
    
    st.markdown(f"""
    <div style="background: rgba(30, 41, 59, 0.8); padding: 1rem; border-radius: 12px; 
                border: 1px solid {border_color}; margin-bottom: 0.75rem; {glow}">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
            <div>
                <span style="font-size: 1.5rem;">{icon}</span>
                <span style="margin-left: 0.5rem; font-weight: 600; color: {COLORS['text']};">{filename}</span>
                <span style="background: {COLORS['primary']}33; color: {COLORS['primary']}; 
                             padding: 2px 10px; border-radius: 10px; font-size: 0.75rem; margin-left: 0.5rem;">
                    {category}
                </span>
            </div>
            <div>
                <span style="font-size: 0.85rem; color: {COLORS['success'] if can_use else COLORS['warning']};">
                    {'✅ Available' if can_use else '🔒 PRO/PREMIUM Only'}
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if can_use and is_downloadable:
        col1, col2 = st.columns([3, 1])
        with col2:
            # Get file content and create download button
            doc_data = get_admin_document_content(doc_id)
            if doc_data and doc_data.get("content"):
                # Determine mime type
                mime_types = {
                    "pdf": "application/pdf",
                    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                }
                mime_type = mime_types.get(file_type, "application/octet-stream")
                
                st.download_button(
                    label="📥 Download",
                    data=doc_data["content"],
                    file_name=filename,
                    mime=mime_type,
                    key=f"download_{doc_id}",
                    use_container_width=True
                )
            else:
                if st.button(f"📥 Download", key=f"download_{doc_id}", use_container_width=True):
                    st.warning("File content not available. Please contact admin.")
    elif can_use and not is_downloadable:
        st.caption("📖 This reviewer is available for AI questions but not for download")
    else:
        st.markdown(f"""
        <p style="color: {COLORS['warning']}; font-size: 0.85rem; margin: 0.25rem 0 0 0;">
            ⚠️ Upgrade to PRO or PREMIUM to download and use this reviewer!
        </p>
        """, unsafe_allow_html=True)
