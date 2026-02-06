"""
LEPT AI Reviewer - Practice Exam Page
OPTIMIZED: Session state caching, minimal DB queries
"""

import streamlit as st

from components.auth import get_current_user
from services.usage_tracker import get_user_status, can_generate_questions, use_questions, get_cached_user_status
from utils.ip_utils import get_client_ip
from config.settings import (
    COLORS, EXAM_COMPONENTS, DIFFICULTY_LEVELS, QUESTIONS_PER_BATCH,
    PLAN_FREE, PLAN_PRO, PLAN_PREMIUM,
    EDUCATION_LEVELS, ELEMENTARY_SPECIALIZATIONS, SECONDARY_SPECIALIZATIONS
)


def render_practice_page():
    """Render the practice exam page - OPTIMIZED."""
    user = get_current_user()
    
    if not user:
        st.error("Please log in to continue.")
        return
    
    email = user.get("email")
    
    # Use cached status from session state - NO DB query
    status = get_cached_user_status()
    if not status:
        status = get_user_status(user)
        st.session_state.user_status = status
    
    is_free_user = status["plan"] == PLAN_FREE
    questions_remaining = user.get("questions_remaining", 0)
    
    # Header
    st.markdown(f"""
    <div style="padding: 2rem; 
                background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(6, 182, 212, 0.1) 100%);
                border-radius: 20px; margin-bottom: 1.5rem;
                border: 1px solid {COLORS['border']};">
        <h2 style="color: {COLORS['text']}; margin: 0; display: flex; align-items: center; gap: 0.5rem;">
            <span>🧠</span> Practice Exam
        </h2>
        <p style="color: {COLORS['text_muted']}; margin: 0.5rem 0 0 0;">
            Configure your exam settings below and click <strong style="color: {COLORS['secondary']};">Generate Practice Questions</strong> to start.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if user can generate questions - no DB query, uses user dict
    can_gen, reason = can_generate_questions(user)
    
    # Display stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        questions_color = COLORS['error'] if questions_remaining <= 0 else (COLORS['warning'] if questions_remaining <= 5 else COLORS['secondary'])
        display_questions = "Unlimited" if status["plan"] == PLAN_PREMIUM and status.get("expiry_display") != "Expired" else str(questions_remaining)
        st.markdown(f"""
        <div style="background: rgba(6, 182, 212, 0.15); padding: 1.25rem; border-radius: 16px; 
                    text-align: center; border: 1px solid {COLORS['border']};">
            <p style="margin: 0; font-size: 0.85rem; color: {COLORS['text_muted']};">Questions Left</p>
            <p style="margin: 0.25rem 0 0 0; font-size: 2rem; font-weight: 700; color: {questions_color};">
                {display_questions}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        plan_color = COLORS['accent'] if status['plan'] == PLAN_PREMIUM else (COLORS['primary'] if status['plan'] == PLAN_PRO else COLORS['text_muted'])
        st.markdown(f"""
        <div style="background: rgba(99, 102, 241, 0.15); padding: 1.25rem; border-radius: 16px; 
                    text-align: center; border: 1px solid {COLORS['border']};">
            <p style="margin: 0; font-size: 0.85rem; color: {COLORS['text_muted']};">Current Plan</p>
            <p style="margin: 0.25rem 0 0 0; font-size: 2rem; font-weight: 700; color: {plan_color};">
                {status['plan']}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        question_source = "AI Generated" if not is_free_user else "Preset Questions"
        source_color = COLORS['success'] if not is_free_user else COLORS['warning']
        st.markdown(f"""
        <div style="background: rgba(139, 92, 246, 0.15); padding: 1.25rem; border-radius: 16px; 
                    text-align: center; border: 1px solid {COLORS['border']};">
            <p style="margin: 0; font-size: 0.85rem; color: {COLORS['text_muted']};">Question Source</p>
            <p style="margin: 0.25rem 0 0 0; font-size: 1.2rem; font-weight: 700; color: {source_color};">
                {question_source}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Out of questions - prompt upgrade
    if not can_gen and questions_remaining <= 0:
        from config.settings import FREE_QUESTION_LIMIT
        st.markdown(f"""
        <div style="background: rgba(239, 68, 68, 0.15); padding: 1.5rem; border-radius: 16px;
                    border: 2px solid {COLORS['error']}; margin-bottom: 1rem; text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 0.75rem;">😔</div>
            <h3 style="color: {COLORS['error']}; margin: 0 0 0.5rem 0;">You have no questions left!</h3>
            <p style="color: {COLORS['text_muted']}; margin: 0 0 1rem 0;">You've used all {FREE_QUESTION_LIMIT} free questions.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("💳 Upgrade Now to Continue", key="upgrade_from_practice", use_container_width=True, type="primary"):
            st.session_state.current_page = "upgrade"
            st.rerun()
        return
    
    # Info for free users
    if is_free_user:
        st.markdown(f"""
        <div style="background: rgba(245, 158, 11, 0.1); padding: 1rem; border-radius: 12px;
                    border: 1px solid rgba(245, 158, 11, 0.3); margin-bottom: 1rem;">
            <p style="margin: 0; color: {COLORS['text']};">
                <strong>📚 FREE Mode:</strong> You have <strong style="color: {COLORS['warning']};">{questions_remaining}</strong> questions remaining.
                Each session uses <strong>{QUESTIONS_PER_BATCH}</strong> from your quota.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # PRO/PREMIUM benefit highlight
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(99, 102, 241, 0.1) 100%);
                    padding: 1rem; border-radius: 12px; margin-bottom: 1rem;
                    border: 1px solid {COLORS['accent']};">
            <p style="margin: 0; color: {COLORS['text']}; font-size: 0.9rem;">
                <strong style="color: {COLORS['accent']};">📚✨ PRO/PREMIUM:</strong> 
                Download admin reviewers & generate AI questions from your materials!
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Exam configuration - all widgets, no DB queries
    st.markdown(f"""
    <div style="background: rgba(30, 41, 59, 0.8); padding: 1.5rem; border-radius: 16px;
                border: 1px solid {COLORS['border']}; margin-bottom: 1rem;">
        <h4 style="color: {COLORS['text']}; margin: 0 0 1rem 0;">⚙️ Exam Configuration</h4>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        education_level = st.selectbox(
            "📚 Education Level",
            options=list(EDUCATION_LEVELS.keys()),
            format_func=lambda x: EDUCATION_LEVELS[x],
            key="education_level_select"
        )
    
    with col2:
        specializations = ELEMENTARY_SPECIALIZATIONS if education_level == "elementary" else SECONDARY_SPECIALIZATIONS
        specialization = st.selectbox(
            "🎯 Specialization",
            options=specializations,
            key="specialization_select"
        )
    
    col1, col2 = st.columns(2)
    
    with col1:
        exam_component = st.selectbox(
            "📋 Exam Component",
            options=list(EXAM_COMPONENTS.keys()),
            format_func=lambda x: f"{EXAM_COMPONENTS[x]['name']} ({EXAM_COMPONENTS[x]['weight']}%)",
            key="exam_component_select"
        )
    
    with col2:
        difficulty = st.select_slider(
            "📊 Difficulty Level",
            options=DIFFICULTY_LEVELS,
            value="Medium",
            key="difficulty_select"
        )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    component_name = EXAM_COMPONENTS[exam_component]['name']
    st.markdown(f"""
    <div style="background: rgba(99, 102, 241, 0.1); padding: 0.75rem 1rem; border-radius: 10px;
                border-left: 4px solid {COLORS['primary']}; margin-bottom: 1rem;">
        <p style="margin: 0; color: {COLORS['text']}; font-size: 0.9rem;">
            📝 Will generate: <strong>{component_name}</strong> questions 
            {f'for <strong>{specialization}</strong> teachers' if exam_component != 'general_education' else '(foundational subjects)'}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Document selection for PRO/PREMIUM - LAZY LOAD
    selected_docs = []
    
    if not is_free_user:
        # Only fetch documents when needed (not on every rerun)
        if "practice_docs_loaded" not in st.session_state:
            st.session_state.practice_docs_loaded = False
        
        with st.expander("📄 Select Reviewer Documents for AI Generation (Optional)", expanded=False):
            if not st.session_state.practice_docs_loaded:
                if st.button("Load My Documents", key="load_docs_btn"):
                    from database.queries import get_user_documents, get_admin_documents
                    st.session_state.user_docs_cache = get_user_documents(email)
                    st.session_state.admin_docs_cache = get_admin_documents() if status.get("can_use_admin_docs") else []
                    st.session_state.practice_docs_loaded = True
                    st.rerun()
            else:
                user_docs = st.session_state.get("user_docs_cache", [])
                admin_docs = st.session_state.get("admin_docs_cache", [])
                
                if user_docs or admin_docs:
                    st.markdown(f"""
                    <p style="color: {COLORS['text_muted']}; margin: 0 0 1rem 0; font-size: 0.9rem;">
                        ✨ Select documents to generate context-aware questions using AI!
                    </p>
                    """, unsafe_allow_html=True)
                    
                    if user_docs:
                        st.markdown(f"**👤 My Documents ({len(user_docs)})**")
                        for doc in user_docs:
                            doc["source"] = "user"
                            if st.checkbox(f"📄 {doc['filename']}", key=f"doc_user_{doc['doc_id']}"):
                                selected_docs.append(doc)
                    
                    if admin_docs:
                        st.markdown(f"**📚 Admin Library ({len(admin_docs)})**")
                        for doc in admin_docs:
                            doc["source"] = "admin"
                            category = doc.get("category", "General")
                            has_text = doc.get("extracted_text") is not None
                            label = f"📚 {doc['filename']} [{category}] {'✅' if has_text else '⚠️'}"
                            if st.checkbox(label, key=f"doc_admin_{doc['doc_id']}"):
                                selected_docs.append(doc)
                    
                    if selected_docs:
                        st.success(f"✅ {len(selected_docs)} document(s) selected")
                else:
                    st.info("No documents available. Upload reviewers or wait for admin to add materials.")
    
    # Generate button section
    is_premium = status["plan"] == PLAN_PREMIUM and status.get("expiry_display") != "Expired"
    can_generate = questions_remaining >= QUESTIONS_PER_BATCH or is_premium
    
    st.markdown(f"""
    <div style="background: rgba(30, 41, 59, 0.8); padding: 1.5rem; border-radius: 16px;
                border: 1px solid {COLORS['border']}; margin-bottom: 1rem;">
        <h4 style="color: {COLORS['text']}; margin: 0 0 0.5rem 0;">🎯 Generate Questions</h4>
        <p style="color: {COLORS['text_muted']}; margin: 0;">
            Generate {QUESTIONS_PER_BATCH} questions. Uses <strong style="color: {COLORS['warning']};">{QUESTIONS_PER_BATCH}</strong> from your quota.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if not can_generate:
        st.error(f"🚫 You have **{questions_remaining}** questions left. Need at least **{QUESTIONS_PER_BATCH}**.")
        if st.button("💳 Upgrade to Continue", key="upgrade_not_enough", use_container_width=True, type="primary"):
            st.session_state.current_page = "upgrade"
            st.rerun()
    else:
        # Use a form to prevent reruns on button click until submitted
        with st.form("generate_form", clear_on_submit=False):
            generate_submit = st.form_submit_button("🚀 Generate Practice Questions", use_container_width=True, type="primary")
            
            if generate_submit:
                handle_question_generation(
                    email, user, status, is_free_user, is_premium,
                    education_level, exam_component, specialization, difficulty, selected_docs
                )
    
    # Display quiz if questions exist
    if "current_questions" in st.session_state and st.session_state.current_questions:
        render_quiz_section(user, email)


def handle_question_generation(email, user, status, is_free_user, is_premium, 
                               education_level, exam_component, specialization, 
                               difficulty, selected_docs):
    """Handle question generation - separated for cleaner code."""
    # Fresh check for question count
    from database.queries import get_fresh_user_by_email
    from services.usage_tracker import refresh_user_session
    
    fresh_user = get_fresh_user_by_email(email)
    fresh_remaining = fresh_user.get("questions_remaining", 0) if fresh_user else 0
    
    if fresh_remaining < QUESTIONS_PER_BATCH and not is_premium:
        st.error(f"🚫 Not enough questions! You have {fresh_remaining} left but need {QUESTIONS_PER_BATCH}.")
        return
    
    with st.spinner("🎓 Generating questions..."):
        if is_free_user:
            from services.preset_questions import get_aligned_preset_questions
            questions = get_aligned_preset_questions(
                education_level=education_level,
                exam_component=exam_component,
                specialization=specialization,
                difficulty=difficulty,
                num_questions=QUESTIONS_PER_BATCH
            )
        else:
            from services.ai_generator import generate_questions
            
            # Collect document content if any documents are selected
            doc_content = ""
            if selected_docs:
                from database.queries import get_admin_document_text
                doc_texts = []
                for doc in selected_docs:
                    if doc.get("source") == "admin":
                        doc_data = get_admin_document_text(doc.get("doc_id"))
                        if doc_data and doc_data.get("text"):
                            doc_texts.append(f"--- {doc_data['filename']} ---\n{doc_data['text'][:8000]}")
                    elif doc.get("extracted_text"):
                        doc_texts.append(f"--- {doc.get('filename')} ---\n{doc.get('extracted_text')[:8000]}")
                if doc_texts:
                    doc_content = "\n\n".join(doc_texts)
            
            # Generate questions using enhanced AI generator
            # The AI will use LEPT competencies if document is not relevant
            questions = generate_questions(
                exam_type=exam_component,
                specialization=specialization,
                difficulty=difficulty,
                document_text=doc_content,
                num_questions=QUESTIONS_PER_BATCH,
                education_level=education_level
            )
    
    if questions:
        ip_address = get_client_ip()
        source_type = "PRESET" if is_free_user else ("MIXED" if selected_docs else "AI_GENERATED")
        use_questions(email, ip_address, QUESTIONS_PER_BATCH, source_type, exam_component, difficulty)
        
        st.session_state.current_questions = questions
        st.session_state.current_answers = {}
        st.session_state.show_results = False
        st.session_state.exam_info = {
            "education_level": EDUCATION_LEVELS[education_level],
            "specialization": specialization,
            "component": EXAM_COMPONENTS[exam_component]['name'],
            "difficulty": difficulty
        }
        
        # Update session state with new user data
        refresh_user_session(force=True)
        
        st.success(f"✅ Generated {len(questions)} questions!")
        st.rerun()
    else:
        st.error("Failed to generate questions. Please try again.")


def render_quiz_section(user, email):
    """Render quiz section - minimal processing."""
    questions = st.session_state.current_questions
    exam_info = st.session_state.get("exam_info", {})
    
    st.markdown(f"""
    <div style="margin-top: 2rem; padding: 1.5rem; background: rgba(30, 41, 59, 0.6);
                border-radius: 16px; border: 1px solid {COLORS['border']};">
        <h3 style="color: {COLORS['text']}; margin: 0 0 0.5rem 0;">📝 Practice Quiz</h3>
        <p style="color: {COLORS['text_muted']}; margin: 0; font-size: 0.9rem;">
            {exam_info.get('education_level', '')} | {exam_info.get('specialization', '')} | 
            {exam_info.get('component', '')} | {exam_info.get('difficulty', '')}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if "current_answers" not in st.session_state:
        st.session_state.current_answers = {}
    
    show_results = st.session_state.get("show_results", False)
    
    for i, q in enumerate(questions):
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.8); padding: 1.5rem; border-radius: 16px; 
                    border: 1px solid {COLORS['border']}; margin-bottom: 1rem;">
            <h4 style="color: {COLORS['primary']}; margin: 0 0 1rem 0;">Question {i + 1}</h4>
            <p style="color: {COLORS['text']}; font-size: 1.05rem; line-height: 1.6; margin: 0;">{q['question']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        options = q.get("options", {})
        correct_answer = q.get("correct_answer", "")
        
        if show_results:
            selected = st.session_state.current_answers.get(f"q_{i}", "")
            for key, value in options.items():
                if key == correct_answer:
                    st.success(f"✓ {key}. {value}")
                elif key == selected and selected != correct_answer:
                    st.error(f"✗ {key}. {value}")
                else:
                    st.markdown(f"<p style='color: {COLORS['text_muted']}; padding: 0.5rem 1rem;'>{key}. {value}</p>", unsafe_allow_html=True)
            
            st.info(f"**Explanation:** {q.get('explanation', 'No explanation.')}")
        else:
            answer = st.radio(
                f"Q{i+1}:",
                options=["A", "B", "C", "D"],
                format_func=lambda x, opts=options: f"{x}. {opts.get(x, '')}",
                key=f"radio_q_{i}",
                horizontal=True,
                label_visibility="collapsed"
            )
            st.session_state.current_answers[f"q_{i}"] = answer
        
        st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if not show_results:
            if st.button("📊 Check Answers", key="check_answers_btn", use_container_width=True, type="primary"):
                st.session_state.show_results = True
                st.rerun()
    
    with col2:
        if st.button("🔄 New Questions", key="new_questions_btn", use_container_width=True):
            st.session_state.current_questions = None
            st.session_state.current_answers = {}
            st.session_state.show_results = False
            st.session_state.exam_info = {}
            st.session_state.practice_docs_loaded = False
            st.rerun()
    
    if show_results:
        correct_count = sum(1 for i, q in enumerate(questions) 
                          if st.session_state.current_answers.get(f"q_{i}") == q.get("correct_answer"))
        score_percent = (correct_count / len(questions)) * 100
        
        score_color = COLORS["success"] if score_percent >= 80 else (COLORS["warning"] if score_percent >= 60 else COLORS["error"])
        score_msg = "Excellent! 🎉" if score_percent >= 80 else ("Good job! 📚" if score_percent >= 60 else "Keep studying! 💪")
        
        st.markdown(f"""
        <div style="background: {score_color}22; padding: 1.5rem; border-radius: 16px; 
                    text-align: center; margin-top: 1rem; border: 2px solid {score_color};">
            <h3 style="color: {score_color}; margin: 0;">Score: {correct_count}/{len(questions)} ({score_percent:.0f}%)</h3>
            <p style="color: {COLORS['text']}; margin: 0.5rem 0 0 0;">{score_msg}</p>
        </div>
        """, unsafe_allow_html=True)
