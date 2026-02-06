"""
LEPT AI Reviewer - Home Page
OPTIMIZED: Session state caching, no DB queries
"""

import streamlit as st

from components.auth import get_current_user
from services.usage_tracker import get_cached_user_status, get_user_status
from config.settings import (
    COLORS, APP_NAME, APP_DESCRIPTION, PLAN_FREE, PLAN_PRO, PLAN_PREMIUM,
    EDUCATION_LEVELS, ELEMENTARY_SPECIALIZATIONS, SECONDARY_SPECIALIZATIONS,
    EXAM_COMPONENTS
)


def render_home_page():
    """Render the home page - OPTIMIZED."""
    user = get_current_user()
    
    if not user:
        st.error("Please log in to continue.")
        return
    
    # Use cached status - NO DB query
    status = get_cached_user_status()
    if not status:
        status = get_user_status(user)
        st.session_state.user_status = status
    is_free_user = status["plan"] == PLAN_FREE
    
    # Header with gradient
    st.markdown(f"""
    <div style="text-align: center; padding: 2.5rem 1rem; 
                background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(6, 182, 212, 0.15) 50%, rgba(139, 92, 246, 0.1) 100%);
                border-radius: 20px; margin-bottom: 2rem;
                border: 1px solid {COLORS['border']};
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2), inset 0 0 60px rgba(99, 102, 241, 0.05);">
        <h1 style="color: {COLORS['text']}; margin: 0; font-size: 2.2rem; font-weight: 700;">
            Welcome to <span style="background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
                                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                {APP_NAME}
            </span>
        </h1>
        <p style="color: {COLORS['text_muted']}; margin: 0.5rem 0 0 0; font-size: 1rem;">
            {APP_DESCRIPTION}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Payment pending check - lazy load
    if "payment_status_checked" not in st.session_state:
        st.session_state.payment_status_checked = False
    
    if not st.session_state.payment_status_checked:
        # Only check on first load, not every rerun
        from services.payment_handler import get_user_payment_status
        payment_status = get_user_payment_status(user.get("email"))
        st.session_state.has_pending_payment = payment_status.get("has_pending", False)
        st.session_state.payment_status_checked = True
    
    if st.session_state.get("has_pending_payment", False):
        from components.alerts import show_payment_pending_banner
        show_payment_pending_banner()
    
    st.markdown(f"<h3 style='color: {COLORS['text']}; margin-bottom: 1rem;'>📊 Your Dashboard</h3>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    plan_colors = {
        PLAN_FREE: COLORS["text_muted"],
        PLAN_PRO: COLORS["primary"],
        PLAN_PREMIUM: COLORS["accent"]
    }
    plan_color = plan_colors.get(status["plan"], COLORS["text_muted"])
    
    with col1:
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.8); padding: 1.25rem; border-radius: 16px; 
                    text-align: center; border: 1px solid {COLORS['border']};">
            <p style="margin: 0; font-size: 0.8rem; color: {COLORS['text_muted']};">Current Plan</p>
            <p style="margin: 0.25rem 0 0 0; font-size: 1.5rem; font-weight: 700; color: {plan_color};">{status['plan']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.8); padding: 1.25rem; border-radius: 16px; 
                    text-align: center; border: 1px solid {COLORS['border']};">
            <p style="margin: 0; font-size: 0.8rem; color: {COLORS['text_muted']};">Questions Left</p>
            <p style="margin: 0.25rem 0 0 0; font-size: 1.5rem; font-weight: 700; color: {COLORS['secondary']};">{status['questions_display']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        expiry_text = status.get('expiry_display') or "N/A"
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.8); padding: 1.25rem; border-radius: 16px; 
                    text-align: center; border: 1px solid {COLORS['border']};">
            <p style="margin: 0; font-size: 0.8rem; color: {COLORS['text_muted']};">Subscription</p>
            <p style="margin: 0.25rem 0 0 0; font-size: 1.5rem; font-weight: 700; color: {COLORS['warning']};">{expiry_text}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        access_text = "Full" if status.get('can_use_admin_docs') else "Limited"
        access_color = COLORS['success'] if status.get('can_use_admin_docs') else COLORS['error']
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.8); padding: 1.25rem; border-radius: 16px; 
                    text-align: center; border: 1px solid {COLORS['border']};">
            <p style="margin: 0; font-size: 0.8rem; color: {COLORS['text_muted']};">Reviewer Access</p>
            <p style="margin: 0.25rem 0 0 0; font-size: 1.5rem; font-weight: 700; color: {access_color};">{access_text}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Admin Reviewer Highlight for FREE users
    if is_free_user:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(99, 102, 241, 0.15) 100%);
                    padding: 1.25rem; border-radius: 16px; margin-bottom: 1.5rem;
                    border: 2px solid {COLORS['accent']};
                    box-shadow: 0 0 20px rgba(139, 92, 246, 0.2);">
            <div style="display: flex; align-items: flex-start; gap: 1rem; flex-wrap: wrap;">
                <div style="font-size: 2.5rem; filter: drop-shadow(0 0 15px {COLORS['accent']});">📚✨</div>
                <div style="flex: 1; min-width: 200px;">
                    <h4 style="color: {COLORS['accent']}; margin: 0 0 0.5rem 0;">
                        PRO/PREMIUM Users Can Download Admin Reviewers!
                    </h4>
                    <p style="color: {COLORS['text']}; margin: 0; font-size: 0.95rem;">
                        Upgrade now to access our <strong style="color: {COLORS['secondary']};">curated reviewer library</strong> - 
                        download high-quality materials prepared by our team and use them for 
                        <strong style="color: {COLORS['primary']};">AI-generated practice questions</strong>!
                    </p>
                    <div style="margin-top: 0.75rem;">
                        <span style="background: {COLORS['success']}33; color: {COLORS['success']}; padding: 4px 10px; 
                                     border-radius: 20px; font-size: 0.8rem; margin-right: 0.5rem;">📥 Download Files</span>
                        <span style="background: {COLORS['primary']}33; color: {COLORS['primary']}; padding: 4px 10px; 
                                     border-radius: 20px; font-size: 0.8rem; margin-right: 0.5rem;">🤖 AI Questions</span>
                        <span style="background: {COLORS['accent']}33; color: {COLORS['accent']}; padding: 4px 10px; 
                                     border-radius: 20px; font-size: 0.8rem;">📄 Upload Your Own</span>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Navigation cards
    st.markdown(f"<h3 style='color: {COLORS['text']}; margin-bottom: 1rem;'>🚀 Quick Actions</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Upload card - different for FREE vs PRO/PREMIUM
        if is_free_user:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(30, 41, 59, 0.8) 100%);
                        padding: 1.5rem; border-radius: 16px; 
                        border: 1px solid {COLORS['warning']}; margin-bottom: 1rem; min-height: 180px;
                        transition: all 0.3s ease;">
                <div style="font-size: 2.5rem; margin-bottom: 0.75rem;
                            filter: drop-shadow(0 0 15px {COLORS['warning']});">🔒</div>
                <h3 style="color: {COLORS['warning']}; margin: 0 0 0.5rem 0; font-size: 1.2rem;">Upload & Download Reviewers (PRO+)</h3>
                <p style="color: {COLORS['text_muted']}; margin: 0; font-size: 0.9rem;">
                    Upgrade to <strong style="color: {COLORS['primary']};">PRO</strong> or 
                    <strong style="color: {COLORS['accent']};">PREMIUM</strong> to upload your own reviewers 
                    and <strong style="color: {COLORS['success']};">download admin resources</strong>!
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("💳 Upgrade Now", key="home_upload_btn", use_container_width=True, type="primary"):
                st.session_state.current_page = "upgrade"
                st.rerun()
        else:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(6, 182, 212, 0.15) 0%, rgba(30, 41, 59, 0.8) 100%);
                        padding: 1.5rem; border-radius: 16px; 
                        border: 1px solid {COLORS['border']}; margin-bottom: 1rem; min-height: 180px;
                        transition: all 0.3s ease;">
                <div style="font-size: 2.5rem; margin-bottom: 0.75rem;
                            filter: drop-shadow(0 0 15px {COLORS['secondary']});">📄</div>
                <h3 style="color: {COLORS['text']}; margin: 0 0 0.5rem 0; font-size: 1.2rem;">Upload & Download Reviewers</h3>
                <p style="color: {COLORS['text_muted']}; margin: 0; font-size: 0.9rem;">
                    Upload your PDF/DOCX reviewers and download admin resources for AI-powered practice!
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("📄 Go to Upload", key="home_upload_btn", use_container_width=True, type="primary"):
                st.session_state.current_page = "upload"
                st.rerun()
    
    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(30, 41, 59, 0.8) 100%);
                    padding: 1.5rem; border-radius: 16px; 
                    border: 1px solid {COLORS['border']}; margin-bottom: 1rem; min-height: 180px;
                    transition: all 0.3s ease;">
            <div style="font-size: 2.5rem; margin-bottom: 0.75rem;
                        filter: drop-shadow(0 0 15px {COLORS['primary']});">🧠</div>
            <h3 style="color: {COLORS['text']}; margin: 0 0 0.5rem 0; font-size: 1.2rem;">Practice Exam</h3>
            <p style="color: {COLORS['text_muted']}; margin: 0; font-size: 0.9rem;">
                {'FREE: 15 preset questions (uses quota) | PRO/PREMIUM: AI-generated questions!' if is_free_user else 'AI-generated LEPT questions from your uploaded reviewers!'}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🧠 Start Practice", key="home_practice_btn", use_container_width=True, type="primary"):
            st.session_state.current_page = "practice"
            st.rerun()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(30, 41, 59, 0.8) 100%);
                    padding: 1.5rem; border-radius: 16px; 
                    border: 1px solid {COLORS['border']}; margin-bottom: 1rem; min-height: 180px;">
            <div style="font-size: 2.5rem; margin-bottom: 0.75rem;
                        filter: drop-shadow(0 0 15px {COLORS['accent']});">💳</div>
            <h3 style="color: {COLORS['text']}; margin: 0 0 0.5rem 0; font-size: 1.2rem;">Upgrade Plan</h3>
            <p style="color: {COLORS['text_muted']}; margin: 0; font-size: 0.9rem;">
                Unlock AI questions, upload reviewers, download admin resources via GCash!
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("💳 View Plans", key="home_upgrade_btn", use_container_width=True):
            st.session_state.current_page = "upgrade"
            st.rerun()
    
    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(30, 41, 59, 0.8) 100%);
                    padding: 1.5rem; border-radius: 16px; 
                    border: 1px solid {COLORS['border']}; margin-bottom: 1rem; min-height: 180px;">
            <div style="font-size: 2.5rem; margin-bottom: 0.75rem;
                        filter: drop-shadow(0 0 15px {COLORS['success']});">📚</div>
            <h3 style="color: {COLORS['text']}; margin: 0 0 0.5rem 0; font-size: 1.2rem;">2026 LEPT Structure</h3>
            <p style="color: {COLORS['text_muted']}; margin: 0; font-size: 0.9rem;">
                GenEd (20%) + ProfEd (40%) + Specialization (40%) - Updated for 2026!
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="padding: 0.5rem; background: rgba(30, 41, 59, 0.6); border-radius: 8px; 
                    text-align: center; color: {COLORS['text_muted']}; font-size: 0.85rem;">
            BEEd | BSEd | 10+ Specializations
        </div>
        """, unsafe_allow_html=True)
    
    # 2026 LEPT Exam Structure Section
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color: {COLORS['text']}; margin-bottom: 1rem;'>📋 2026 PRC LEPT Exam Structure</h3>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background: rgba(30, 41, 59, 0.8); padding: 1.5rem; border-radius: 16px; 
                border: 1px solid {COLORS['border']}; margin-bottom: 1rem;">
        <div style="display: flex; flex-wrap: wrap; gap: 1rem;">
            <div style="flex: 1; min-width: 200px; background: rgba(99, 102, 241, 0.1); padding: 1rem; 
                        border-radius: 12px; border-left: 4px solid {COLORS['primary']};">
                <h5 style="color: {COLORS['primary']}; margin: 0 0 0.5rem 0;">📚 GenEd (20%)</h5>
                <p style="color: {COLORS['text_muted']}; margin: 0; font-size: 0.85rem;">
                    English, Filipino, Math, Science, Social Studies
                </p>
            </div>
            <div style="flex: 1; min-width: 200px; background: rgba(6, 182, 212, 0.1); padding: 1rem; 
                        border-radius: 12px; border-left: 4px solid {COLORS['secondary']};">
                <h5 style="color: {COLORS['secondary']}; margin: 0 0 0.5rem 0;">👩‍🏫 ProfEd (40%)</h5>
                <p style="color: {COLORS['text_muted']}; margin: 0; font-size: 0.85rem;">
                    Teaching Principles, Child Development, Curriculum
                </p>
            </div>
            <div style="flex: 1; min-width: 200px; background: rgba(139, 92, 246, 0.1); padding: 1rem; 
                        border-radius: 12px; border-left: 4px solid {COLORS['accent']};">
                <h5 style="color: {COLORS['accent']}; margin: 0 0 0.5rem 0;">🎯 Specialization (40%)</h5>
                <p style="color: {COLORS['text_muted']}; margin: 0; font-size: 0.85rem;">
                    Your specific major/field of study
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Education Levels
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.8); padding: 1.25rem; border-radius: 16px; 
                    border: 1px solid {COLORS['border']};">
            <h4 style="color: {COLORS['primary']}; margin: 0 0 0.75rem 0;">🎒 Elementary Education (BEEd)</h4>
            <ul style="color: {COLORS['text_muted']}; margin: 0.5rem 0 0 0; padding-left: 1.25rem; font-size: 0.85rem;">
                <li>Early Childhood Education (ECE)</li>
                <li>Special Needs Education (SNE)</li>
                <li>General Education</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.8); padding: 1.25rem; border-radius: 16px; 
                    border: 1px solid {COLORS['border']};">
            <h4 style="color: {COLORS['secondary']}; margin: 0 0 0.75rem 0;">🏫 Secondary Education (BSEd)</h4>
            <p style="color: {COLORS['text_muted']}; margin: 0; font-size: 0.9rem;"><strong>10 Specializations:</strong></p>
            <ul style="color: {COLORS['text_muted']}; margin: 0.5rem 0 0 0; padding-left: 1.25rem; font-size: 0.85rem;">
                <li>English, Filipino, Math, Science, Social Studies</li>
                <li>Values Education, TLE, TVTE, PE, Culture & Arts</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Features section
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color: {COLORS['text']}; margin-bottom: 1rem;'>✨ Features</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style="text-align: center; padding: 1.5rem; background: rgba(30, 41, 59, 0.6);
                    border-radius: 16px; border: 1px solid {COLORS['border']};">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🎯</div>
            <h4 style="color: {COLORS['text']}; margin: 0 0 0.5rem 0;">Smart Questions</h4>
            <p style="color: {COLORS['text_muted']}; font-size: 0.85rem; margin: 0;">
                FREE: Quality preset questions | PRO+: AI-generated from your reviewers.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="text-align: center; padding: 1.5rem; background: rgba(30, 41, 59, 0.6);
                    border-radius: 16px; border: 1px solid {COLORS['border']};">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">📱</div>
            <h4 style="color: {COLORS['text']}; margin: 0 0 0.5rem 0;">Mobile-Friendly</h4>
            <p style="color: {COLORS['text_muted']}; font-size: 0.85rem; margin: 0;">
                Study anywhere with our responsive design that works on all devices.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="text-align: center; padding: 1.5rem; background: rgba(30, 41, 59, 0.6);
                    border-radius: 16px; border: 1px solid {COLORS['border']};">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">📖</div>
            <h4 style="color: {COLORS['text']}; margin: 0 0 0.5rem 0;">2026 LEPT Ready</h4>
            <p style="color: {COLORS['text_muted']}; font-size: 0.85rem; margin: 0;">
                Updated with the latest PRC LEPT guidelines effective 2026.
            </p>
        </div>
        """, unsafe_allow_html=True)
