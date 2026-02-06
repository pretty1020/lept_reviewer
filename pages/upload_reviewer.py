"""
LEPT AI Reviewer - Upload Reviewer Page
OPTIMIZED: Lazy loading, cached queries
"""

import streamlit as st

from components.auth import get_current_user
from services.usage_tracker import get_cached_user_status, get_user_status
from config.settings import COLORS, PLAN_FREE, PLAN_PRO, PLAN_PREMIUM


def render_upload_page():
    """Render the document upload page - OPTIMIZED."""
    user = get_current_user()
    
    if not user:
        st.error("Please log in to continue.")
        return
    
    email = user.get("email")
    
    # Use cached status - NO DB query
    status = get_cached_user_status()
    if not status:
        status = get_user_status(user)
        st.session_state.user_status = status
    
    is_free_user = status["plan"] == PLAN_FREE
    
    # Show upgrade prompt for FREE users
    if is_free_user:
        render_free_user_upgrade_prompt()
        return
    
    # Header
    st.markdown(f"""
    <div style="padding: 2rem; 
                background: linear-gradient(135deg, rgba(6, 182, 212, 0.2) 0%, rgba(99, 102, 241, 0.1) 100%);
                border-radius: 20px; margin-bottom: 1.5rem;
                border: 1px solid {COLORS['border']};">
        <h2 style="color: {COLORS['text']}; margin: 0;">
            📄 Upload & Download Reviewers
        </h2>
        <p style="color: {COLORS['text_muted']}; margin: 0.5rem 0 0 0;">
            Upload your own reviewers or download admin resources for AI-generated questions.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2 = st.tabs(["📤 My Documents", "📥 Admin Library"])
    
    with tab1:
        render_user_documents_tab(email)
    
    with tab2:
        render_admin_documents_tab(email, status)


def render_free_user_upgrade_prompt():
    """Upgrade prompt for FREE users - static HTML, no DB queries."""
    st.markdown(f"""
    <div style="padding: 2rem; 
                background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(99, 102, 241, 0.15) 100%);
                border-radius: 20px; margin-bottom: 1.5rem;
                border: 1px solid {COLORS['accent']};">
        <h2 style="color: {COLORS['text']}; margin: 0;">
            📄 Upload & Download Reviewers
        </h2>
        <p style="color: {COLORS['text_muted']}; margin: 0.5rem 0 0 0;">
            <span style="background: {COLORS['warning']}; color: #000; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem;">PRO/PREMIUM</span>
            This feature requires an upgraded plan
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(30, 27, 75, 0.9) 100%);
                padding: 2.5rem; border-radius: 20px; text-align: center;
                border: 2px solid {COLORS['accent']}; margin-bottom: 1.5rem;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🔒✨</div>
        <h2 style="color: {COLORS['text']}; margin: 0 0 1rem 0; font-size: 1.8rem;">
            Unlock Upload & Download Features
        </h2>
        <p style="color: {COLORS['text_muted']}; margin: 0 0 1.5rem 0; font-size: 1.1rem;">
            Upgrade to <strong style="color: {COLORS['primary']};">PRO</strong> or 
            <strong style="color: {COLORS['accent']};">PREMIUM</strong> for powerful features!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="background: rgba(99, 102, 241, 0.1); padding: 1.5rem; border-radius: 16px;
                    border: 1px solid {COLORS['primary']};">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">📤</div>
            <h4 style="color: {COLORS['primary']}; margin: 0 0 0.5rem 0;">Upload Your Reviewers</h4>
            <p style="color: {COLORS['text_muted']}; margin: 0; font-size: 0.9rem;">
                Upload PDF/DOCX materials for <strong style="color: {COLORS['text']};">AI-powered questions</strong>.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: rgba(6, 182, 212, 0.1); padding: 1.5rem; border-radius: 16px;
                    border: 1px solid {COLORS['secondary']};">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">📥</div>
            <h4 style="color: {COLORS['secondary']}; margin: 0 0 0.5rem 0;">Download Admin Reviewers</h4>
            <p style="color: {COLORS['text_muted']}; margin: 0; font-size: 0.9rem;">
                Access our <strong style="color: {COLORS['text']};">curated reviewer library</strong>.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="background: rgba(139, 92, 246, 0.1); padding: 1.5rem; border-radius: 16px;
                    border: 1px solid {COLORS['accent']};">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🤖</div>
            <h4 style="color: {COLORS['accent']}; margin: 0 0 0.5rem 0;">AI-Generated Questions</h4>
            <p style="color: {COLORS['text_muted']}; margin: 0; font-size: 0.9rem;">
                Generate <strong style="color: {COLORS['text']};">context-aware questions</strong> using AI.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: rgba(16, 185, 129, 0.1); padding: 1.5rem; border-radius: 16px;
                    border: 1px solid {COLORS['success']};">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">📚</div>
            <h4 style="color: {COLORS['success']}; margin: 0 0 0.5rem 0;">More Questions</h4>
            <p style="color: {COLORS['text_muted']}; margin: 0; font-size: 0.9rem;">
                <strong>PRO: +75</strong> | <strong>PREMIUM: Unlimited</strong> for 30 days!
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("💳 Upgrade Now to Unlock All Features", key="upgrade_from_upload", use_container_width=True, type="primary"):
        st.session_state.current_page = "upgrade"
        st.rerun()
    
    st.markdown(f"""
    <p style="text-align: center; color: {COLORS['text_muted']}; margin-top: 1rem; font-size: 0.85rem;">
        Pay via GCash • Instant activation after admin approval
    </p>
    """, unsafe_allow_html=True)


def render_user_documents_tab(email: str):
    """Render user documents tab - OPTIMIZED with lazy loading."""
    st.markdown(f"<h3 style='color: {COLORS['text']}; margin: 1rem 0;'>Upload New Document</h3>", unsafe_allow_html=True)
    
    # File uploader - only import processing when file is uploaded
    uploaded_file = st.file_uploader(
        "Choose a PDF or DOCX file",
        type=["pdf", "docx"],
        help="Supported: PDF, DOCX",
        key="user_doc_upload"
    )
    
    if uploaded_file:
        # Lazy import validation
        from utils.file_utils import validate_file
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
            
            # Use form to prevent reruns
            with st.form("upload_form", clear_on_submit=True):
                upload_submit = st.form_submit_button("📤 Upload & Process", use_container_width=True, type="primary")
                
                if upload_submit:
                    with st.spinner("Processing document..."):
                        from services.document_processor import extract_text_from_file
                        from database.queries import save_user_document
                        from database.cached_queries import invalidate_user_docs_cache
                        
                        success, extracted_text = extract_text_from_file(uploaded_file)
                    
                    # Always try to save the document, even if text extraction had issues
                    file_type = uploaded_file.name.split('.')[-1].lower()
                    storage_path = f"@STAGE_USER_DOCS/{email}/{uploaded_file.name}"
                    
                    # Save with extracted text (may be placeholder text if extraction failed)
                    doc_id = save_user_document(
                        email=email,
                        filename=uploaded_file.name,
                        file_type=file_type,
                        storage_path=storage_path,
                        extracted_text=extracted_text if success else None
                    )
                    
                    if doc_id:
                        invalidate_user_docs_cache(email)
                        if success and not extracted_text.startswith("["):
                            st.success(f"✅ Document uploaded! Extracted {len(extracted_text)} characters of text.")
                        else:
                            st.success("✅ Document uploaded! (Limited text extraction)")
                        st.rerun()
                    else:
                        st.error("Failed to save document. Please try again.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color: {COLORS['text']}; margin: 1rem 0;'>My Uploaded Documents</h3>", unsafe_allow_html=True)
    
    # Lazy load documents only when tab is viewed
    if "user_docs_loaded" not in st.session_state:
        st.session_state.user_docs_loaded = {}
    
    if email not in st.session_state.user_docs_loaded or st.session_state.user_docs_loaded.get(email) is None:
        if st.button("🔄 Load My Documents", key="load_user_docs"):
            from database.queries import get_user_documents
            docs = get_user_documents(email)
            st.session_state.user_docs_loaded[email] = docs
            st.rerun()
        return
    
    docs = st.session_state.user_docs_loaded.get(email, [])
    
    if not docs:
        st.markdown(f"""
        <div style="background: rgba(6, 182, 212, 0.1); padding: 2rem; border-radius: 16px; 
                    text-align: center; border: 2px dashed {COLORS['secondary']};">
            <span style="font-size: 3rem;">📄</span>
            <p style="color: {COLORS['text_muted']}; margin: 1rem 0 0 0;">
                No documents uploaded yet.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for doc in docs:
            render_document_item(doc, email)


def render_admin_documents_tab(email: str, status: dict):
    """Render admin documents tab - OPTIMIZED with lazy loading."""
    st.markdown(f"<h3 style='color: {COLORS['text']}; margin: 1rem 0;'>Admin Reviewer Library</h3>", unsafe_allow_html=True)
    
    can_use = status.get("can_use_admin_docs", False)
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(99, 102, 241, 0.1) 100%); 
                padding: 1.25rem; border-radius: 16px;
                border: 1px solid rgba(139, 92, 246, 0.4); margin-bottom: 1.5rem;">
        <h4 style="color: {COLORS['accent']}; margin: 0;">✨ PRO/PREMIUM Exclusive!</h4>
        <p style="color: {COLORS['text']}; margin: 0.25rem 0 0 0; font-size: 0.95rem;">
            Download curated materials for <strong>AI-generated questions</strong>!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Lazy load admin docs
    if "admin_docs_loaded" not in st.session_state:
        st.session_state.admin_docs_loaded = None
    
    if st.session_state.admin_docs_loaded is None:
        if st.button("🔄 Load Admin Library", key="load_admin_docs"):
            from database.queries import get_admin_documents
            st.session_state.admin_docs_loaded = get_admin_documents()
            st.rerun()
        return
    
    docs = st.session_state.admin_docs_loaded or []
    
    if not docs:
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.6); padding: 2rem; border-radius: 16px; 
                    text-align: center; border: 1px solid {COLORS['border']};">
            <span style="font-size: 3rem;">📚</span>
            <p style="color: {COLORS['text_muted']}; margin: 1rem 0 0 0;">
                No admin reviewers available yet.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"<p style='color: {COLORS['text_muted']};'><strong>{len(docs)}</strong> reviewer(s) available</p>", unsafe_allow_html=True)
        
        for doc in docs:
            render_admin_document_item(doc, can_use)


def render_document_item(doc: dict, email: str):
    """Render a single user document item."""
    from utils.file_utils import get_file_icon
    
    filename = doc.get("filename", "Unknown")
    doc_id = doc.get("doc_id")
    created_at = doc.get("created_at", "")
    icon = get_file_icon(filename)
    
    st.markdown(f"""
    <div style="background: rgba(30, 41, 59, 0.8); padding: 1rem; border-radius: 12px; 
                border: 1px solid {COLORS['border']}; margin-bottom: 0.5rem;">
        <span style="font-size: 1.3rem;">{icon}</span>
        <span style="margin-left: 0.5rem; font-weight: 500; color: {COLORS['text']};">{filename}</span>
        <span style="font-size: 0.8rem; color: {COLORS['text_muted']}; float: right;">{created_at}</span>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("🗑️", key=f"delete_{doc_id}", help="Delete"):
            from database.queries import delete_user_document
            from database.cached_queries import invalidate_user_docs_cache
            
            delete_user_document(doc_id, email)
            invalidate_user_docs_cache(email)
            st.session_state.user_docs_loaded[email] = None  # Force reload
            st.success("Deleted!")
            st.rerun()


def render_admin_document_item(doc: dict, can_use: bool):
    """Render an admin document item with download."""
    from utils.file_utils import get_file_icon
    
    filename = doc.get("filename", "Unknown")
    doc_id = doc.get("doc_id")
    category = doc.get("category", "General")
    is_downloadable = doc.get("is_downloadable", True)
    file_type = doc.get("file_type", "pdf")
    icon = get_file_icon(filename)
    
    border_color = COLORS['accent'] if can_use else COLORS['border']
    
    st.markdown(f"""
    <div style="background: rgba(30, 41, 59, 0.8); padding: 1rem; border-radius: 12px; 
                border: 1px solid {border_color}; margin-bottom: 0.75rem;">
        <span style="font-size: 1.5rem;">{icon}</span>
        <span style="margin-left: 0.5rem; font-weight: 600; color: {COLORS['text']};">{filename}</span>
        <span style="background: {COLORS['primary']}33; color: {COLORS['primary']}; 
                     padding: 2px 10px; border-radius: 10px; font-size: 0.75rem; margin-left: 0.5rem;">
            {category}
        </span>
        <span style="float: right; font-size: 0.85rem; color: {COLORS['success'] if can_use else COLORS['warning']};">
            {'✅ Available' if can_use else '🔒 PRO/PREMIUM'}
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    if can_use and is_downloadable:
        col1, col2 = st.columns([3, 1])
        with col2:
            # Only fetch content when download button is clicked
            download_key = f"download_admin_{doc_id}"
            if st.button("📥 Download", key=download_key, use_container_width=True):
                from database.queries import get_admin_document_content
                
                with st.spinner("Preparing download..."):
                    doc_data = get_admin_document_content(doc_id)
                
                if doc_data and doc_data.get("content"):
                    st.session_state[f"download_data_{doc_id}"] = doc_data
                    st.rerun()
                else:
                    st.warning("File not available.")
            
            # Show actual download button if data is loaded
            if f"download_data_{doc_id}" in st.session_state:
                doc_data = st.session_state[f"download_data_{doc_id}"]
                mime_types = {
                    "pdf": "application/pdf",
                    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                }
                st.download_button(
                    label="💾 Save File",
                    data=doc_data["content"],
                    file_name=doc_data["filename"],
                    mime=mime_types.get(file_type, "application/octet-stream"),
                    key=f"save_{doc_id}"
                )
    elif can_use and not is_downloadable:
        st.caption("📖 Available for AI questions but not download")
