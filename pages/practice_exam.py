"""
LEPT AI Reviewer - Practice Exam Page
Updated with 2026 PRC LEPT Guidelines
Modern Techy Theme - Optimized
"""

import streamlit as st

from components.auth import get_current_user
from services.usage_tracker import get_user_status, can_generate_questions, use_questions, refresh_user_session
from services.ai_generator import generate_questions
from services.preset_questions import get_aligned_preset_questions
from database.queries import get_user_documents, get_admin_documents, get_user_by_email, get_admin_document_text
from utils.ip_utils import get_client_ip
from config.settings import (
    COLORS, EXAM_COMPONENTS, DIFFICULTY_LEVELS, QUESTIONS_PER_BATCH,
    PLAN_FREE, PLAN_PRO, PLAN_PREMIUM,
    EDUCATION_LEVELS, ELEMENTARY_SPECIALIZATIONS, SECONDARY_SPECIALIZATIONS
)


def render_practice_page():
    """Render the practice exam page with 2026 LEPT structure."""
    user = get_current_user()
    
    if not user:
        st.error("Please log in to continue.")
        return
    
    email = user.get("email")
    
    # Get fresh user data from database
    fresh_user = get_user_by_email(email)
    if fresh_user:
        user = fresh_user
        st.session_state.user = fresh_user
    
    status = get_user_status(user)
    is_free_user = status["plan"] == PLAN_FREE
    questions_remaining = user.get("questions_remaining", 0)
    
    # Header
    st.markdown(f"""
    <div style="padding: 2rem; 
                background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(6, 182, 212, 0.1) 100%);
                border-radius: 20px; margin-bottom: 1.5rem;
                border: 1px solid {COLORS['border']};">
        <h2 style="color: {COLORS['text']}; margin: 0; display: flex; align-items: center; gap: 0.5rem;">
            <span style="filter: drop-shadow(0 0 10px {COLORS['primary']});">🧠</span>
            Practice Exam
        </h2>
        <p style="color: {COLORS['text_muted']}; margin: 0.5rem 0 0 0;">
            Based on <strong style="color: {COLORS['secondary']};">2026 PRC LEPT Guidelines</strong> | 
            GenEd (20%) + ProfEd (40%) + Specialization (40%)
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if user can generate questions
    can_gen, reason = can_generate_questions(user)
    
    # Display remaining questions and plan info
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
    
    # Check if out of questions - prompt upgrade (only when truly 0)
    if not can_gen and questions_remaining <= 0:
        st.markdown(f"""
        <div style="background: rgba(239, 68, 68, 0.15); padding: 1.5rem; border-radius: 16px;
                    border: 2px solid {COLORS['error']}; margin-bottom: 1rem; text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 0.75rem;">😔</div>
            <h3 style="color: {COLORS['error']}; margin: 0 0 0.5rem 0;">You have no questions left!</h3>
            <p style="color: {COLORS['text_muted']}; margin: 0 0 1rem 0;">You've used all 10 free questions.</p>
            <p style="color: {COLORS['text']}; margin: 0;">
                Upgrade to <strong style="color: {COLORS['primary']};">PRO</strong> for +75 AI-generated questions or 
                <strong style="color: {COLORS['accent']};">PREMIUM</strong> for unlimited questions!
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("💳 Upgrade Now to Continue", key="upgrade_from_practice", use_container_width=True, type="primary"):
            st.session_state.current_page = "upgrade"
            st.rerun()
        return
    
    # Show info for free users with remaining count
    if is_free_user:
        st.markdown(f"""
        <div style="background: rgba(245, 158, 11, 0.1); padding: 1rem; border-radius: 12px;
                    border: 1px solid rgba(245, 158, 11, 0.3); margin-bottom: 1rem;">
            <p style="margin: 0; color: {COLORS['text']};">
                <strong>📚 FREE Mode:</strong> You have <strong style="color: {COLORS['warning']};">{questions_remaining}</strong> questions remaining out of 10.
                Each practice session generates {QUESTIONS_PER_BATCH} questions and uses <strong style="color: {COLORS['error']};">{QUESTIONS_PER_BATCH}</strong> from your quota.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Highlight download benefit for FREE users
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(99, 102, 241, 0.1) 100%);
                    padding: 1rem; border-radius: 12px; margin-bottom: 1rem;
                    border: 1px solid {COLORS['accent']};">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <span style="font-size: 1.5rem;">📚✨</span>
                <div>
                    <p style="margin: 0; color: {COLORS['text']}; font-size: 0.9rem;">
                        <strong style="color: {COLORS['accent']};">PRO/PREMIUM Benefit:</strong> 
                        Download admin reviewers & generate AI questions from your own materials!
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Exam configuration
    st.markdown(f"""
    <div style="background: rgba(30, 41, 59, 0.8); padding: 1.5rem; border-radius: 16px;
                border: 1px solid {COLORS['border']}; margin-bottom: 1rem;">
        <h4 style="color: {COLORS['text']}; margin: 0 0 1rem 0;">⚙️ Exam Configuration</h4>
    """, unsafe_allow_html=True)
    
    # Education Level Selection
    col1, col2 = st.columns(2)
    
    with col1:
        education_level = st.selectbox(
            "📚 Education Level",
            options=list(EDUCATION_LEVELS.keys()),
            format_func=lambda x: EDUCATION_LEVELS[x],
            key="education_level_select",
            help="Select Elementary (BEEd) or Secondary (BSEd)"
        )
    
    with col2:
        # Dynamic specializations based on education level
        if education_level == "elementary":
            specializations = ELEMENTARY_SPECIALIZATIONS
        else:
            specializations = SECONDARY_SPECIALIZATIONS
        
        specialization = st.selectbox(
            "🎯 Specialization",
            options=specializations,
            key="specialization_select",
            help="Select your area of specialization"
        )
    
    # Exam Component and Difficulty
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
    
    # Show what questions will be generated
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
    
    # For PRO/PREMIUM users - Document selection
    selected_docs = []
    
    if not is_free_user:
        user_docs = get_user_documents(email)
        admin_docs = get_admin_documents() if status.get("can_use_admin_docs") else []
        
        if user_docs or admin_docs:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(30, 41, 59, 0.8) 100%); 
                        padding: 1.5rem; border-radius: 16px;
                        border: 1px solid {COLORS['accent']}; margin-bottom: 1rem;">
                <h4 style="color: {COLORS['text']}; margin: 0 0 0.5rem 0;">
                    📄 Select Reviewer Documents for AI Generation
                </h4>
                <p style="color: {COLORS['text_muted']}; margin: 0 0 1rem 0; font-size: 0.9rem;">
                    ✨ <strong style="color: {COLORS['accent']};">PRO/PREMIUM Feature:</strong> 
                    Select your uploaded documents or admin reviewers to generate context-aware questions using AI!
                </p>
            """, unsafe_allow_html=True)
            
            # My Documents Section
            if user_docs:
                st.markdown(f"""
                <p style='color: {COLORS['secondary']}; font-weight: 600; margin-bottom: 0.5rem; font-size: 0.95rem;'>
                    👤 My Uploaded Documents ({len(user_docs)})
                </p>
                """, unsafe_allow_html=True)
                
                for doc in user_docs:
                    doc["source"] = "user"
                    doc_key = f"doc_select_user_{doc['doc_id']}"
                    col1, col2 = st.columns([0.1, 0.9])
                    with col1:
                        selected = st.checkbox("", key=doc_key, label_visibility="collapsed")
                    with col2:
                        st.markdown(f"""
                        <span style="color: {COLORS['text']};">📄 {doc['filename']}</span>
                        """, unsafe_allow_html=True)
                    if selected:
                        selected_docs.append(doc)
            
            # Admin Reviewers Section
            if admin_docs:
                st.markdown(f"""
                <p style='color: {COLORS['accent']}; font-weight: 600; margin: 1rem 0 0.5rem 0; font-size: 0.95rem;'>
                    📚 Admin Reviewer Library ({len(admin_docs)})
                </p>
                """, unsafe_allow_html=True)
                
                for doc in admin_docs:
                    doc["source"] = "admin"
                    doc_key = f"doc_select_admin_{doc['doc_id']}"
                    category = doc.get("category", "General")
                    has_text = doc.get("extracted_text") is not None
                    
                    col1, col2 = st.columns([0.1, 0.9])
                    with col1:
                        selected = st.checkbox("", key=doc_key, label_visibility="collapsed")
                    with col2:
                        text_status = "✅" if has_text else "⚠️"
                        st.markdown(f"""
                        <span style="color: {COLORS['text']};">📚 {doc['filename']}</span>
                        <span style="background: {COLORS['primary']}33; color: {COLORS['primary']}; 
                                     padding: 2px 8px; border-radius: 10px; font-size: 0.7rem; margin-left: 0.5rem;">
                            {category}
                        </span>
                        <span style="font-size: 0.75rem; margin-left: 0.25rem;" title="{'Text extracted' if has_text else 'No text available'}">{text_status}</span>
                        """, unsafe_allow_html=True)
                    if selected:
                        selected_docs.append(doc)
            
            # Show selected count
            if selected_docs:
                st.markdown(f"""
                <div style="background: rgba(16, 185, 129, 0.1); padding: 0.5rem 1rem; border-radius: 8px; margin-top: 0.75rem;">
                    <p style="margin: 0; color: {COLORS['success']}; font-size: 0.9rem;">
                        ✅ <strong>{len(selected_docs)}</strong> document(s) selected for AI question generation
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background: rgba(245, 158, 11, 0.1); padding: 1rem; border-radius: 12px;
                        border: 1px solid rgba(245, 158, 11, 0.3); margin-bottom: 1rem;">
                <p style="margin: 0; color: {COLORS['text']}; font-size: 0.9rem;">
                    📄 <strong>No documents available.</strong> Upload your own reviewers or wait for admin reviewers to be added!
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    # Check if enough questions remaining (PREMIUM users have unlimited)
    is_premium = status["plan"] == PLAN_PREMIUM and status.get("expiry_display") != "Expired"
    can_generate = questions_remaining >= QUESTIONS_PER_BATCH or is_premium
    
    # Generate questions button
    st.markdown(f"""
    <div style="background: rgba(30, 41, 59, 0.8); padding: 1.5rem; border-radius: 16px;
                border: 1px solid {COLORS['border']}; margin-bottom: 1rem;">
        <h4 style="color: {COLORS['text']}; margin: 0 0 0.5rem 0;">🎯 Generate Questions</h4>
        <p style="color: {COLORS['text_muted']}; margin: 0;">
            Generate {QUESTIONS_PER_BATCH} practice questions. 
            <strong style="color: {COLORS['warning']};">This will use {QUESTIONS_PER_BATCH} questions from your quota.</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show warning and block generation if not enough questions
    if not can_generate:
        st.error(f"🚫 You only have **{questions_remaining}** questions left. You need at least **{QUESTIONS_PER_BATCH}** to generate a new batch.")
        if st.button("💳 Upgrade to Continue", key="upgrade_not_enough", use_container_width=True, type="primary"):
            st.session_state.current_page = "upgrade"
            st.rerun()
        # DO NOT show generate button when not enough questions
    else:
        # Only show generate button if user CAN generate
        generate_clicked = st.button("🚀 Generate Practice Questions", key="generate_btn", use_container_width=True, type="primary")
        
        if generate_clicked:
            # Double-check before generation (prevent race conditions)
            fresh_check = get_user_by_email(email)
            fresh_remaining = fresh_check.get("questions_remaining", 0) if fresh_check else 0
            
            if fresh_remaining < QUESTIONS_PER_BATCH and not is_premium:
                st.error(f"🚫 Not enough questions! You have {fresh_remaining} left but need {QUESTIONS_PER_BATCH}. Please upgrade.")
            else:
                # Proceed with generation
                with st.spinner("🎓 Generating questions..."):
                    if is_free_user:
                        # Use preset questions for FREE users - aligned to configuration
                        questions = get_aligned_preset_questions(
                            education_level=education_level,
                            exam_component=exam_component,
                            specialization=specialization,
                            difficulty=difficulty,
                            num_questions=QUESTIONS_PER_BATCH
                        )
                    else:
                        # Use AI for PRO/PREMIUM users
                        # Gather document content from selected docs
                        doc_content = ""
                        if selected_docs:
                            doc_texts = []
                            for doc in selected_docs:
                                if doc.get("source") == "admin":
                                    # Get extracted text from admin doc
                                    doc_data = get_admin_document_text(doc.get("doc_id"))
                                    if doc_data and doc_data.get("text"):
                                        doc_texts.append(f"--- Content from '{doc_data['filename']}' ---\n{doc_data['text'][:5000]}")
                                elif doc.get("extracted_text"):
                                    doc_texts.append(f"--- Content from '{doc.get('filename')}' ---\n{doc.get('extracted_text')[:5000]}")
                            
                            if doc_texts:
                                doc_content = "\n\n".join(doc_texts)
                        
                        combined_text = f"""
                        Generate LEPT exam questions for:
                        - Education Level: {EDUCATION_LEVELS[education_level]}
                        - Exam Component: {EXAM_COMPONENTS[exam_component]['name']}
                        - Specialization: {specialization}
                        - Difficulty: {difficulty}
                        
                        IMPORTANT: Generate ONLY {EXAM_COMPONENTS[exam_component]['name']} questions.
                        {"These should be General Education questions covering foundational subjects." if exam_component == 'general_education' else ""}
                        {"These should be Professional Education questions about teaching methods, theories, and pedagogy relevant to " + specialization + " teachers." if exam_component == 'professional_education' else ""}
                        {"These should be content questions specific to " + specialization + " subject matter." if exam_component == 'specialization' else ""}
                        
                        Follow the 2026 PRC LEPT competencies and guidelines.
                        
                        {f"Use the following reviewer content to create context-specific questions:\n\n{doc_content}" if doc_content else ""}
                        """
                        
                        questions = generate_questions(
                            exam_type=exam_component,
                            specialization=specialization,
                            difficulty=difficulty,
                            document_text=combined_text,
                            num_questions=QUESTIONS_PER_BATCH
                        )
                
                if questions:
                    # Deduct the full batch count from quota
                    ip_address = get_client_ip()
                    source_type = "PRESET" if is_free_user else ("MIXED" if selected_docs else "AI_GENERATED")
                    use_questions(email, ip_address, QUESTIONS_PER_BATCH, source_type, exam_component, difficulty)
                    
                    # Store questions in session state
                    st.session_state.current_questions = questions
                    st.session_state.current_answers = {}
                    st.session_state.show_results = False
                    st.session_state.exam_info = {
                        "education_level": EDUCATION_LEVELS[education_level],
                        "specialization": specialization,
                        "component": EXAM_COMPONENTS[exam_component]['name'],
                        "difficulty": difficulty
                    }
                    
                    # Refresh user data and check remaining
                    refresh_user_session()
                    updated_user = get_user_by_email(email)
                    new_remaining = updated_user.get("questions_remaining", 0) if updated_user else 0
                    
                    if is_free_user and new_remaining <= 0:
                        st.warning(f"⚠️ You have no questions left! You've used all 10 free questions. Upgrade to continue practicing.")
                    else:
                        st.success(f"✅ Generated {len(questions)} questions! ({QUESTIONS_PER_BATCH} deducted from quota)")
                    
                    st.rerun()
                else:
                    st.error("Failed to generate questions. Please try again.")
    
    # Display current questions if any
    if "current_questions" in st.session_state and st.session_state.current_questions:
        render_quiz_section(user, email)


def render_quiz_section(user, email):
    """Render the quiz section with generated questions."""
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
    
    # Initialize answers dict if not exists
    if "current_answers" not in st.session_state:
        st.session_state.current_answers = {}
    
    show_results = st.session_state.get("show_results", False)
    
    for i, q in enumerate(questions):
        question_num = i + 1
        
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.8); padding: 1.5rem; border-radius: 16px; 
                    border: 1px solid {COLORS['border']}; margin-bottom: 1rem;">
            <h4 style="color: {COLORS['primary']}; margin: 0 0 1rem 0;">Question {question_num}</h4>
            <p style="color: {COLORS['text']}; font-size: 1.05rem; line-height: 1.6; margin: 0;">{q['question']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Options
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
            
            # Show explanation
            explanation = q.get("explanation", "No explanation provided.")
            st.info(f"**Explanation:** {explanation}")
        else:
            # Radio buttons for selection
            answer = st.radio(
                f"Select your answer for Question {question_num}:",
                options=["A", "B", "C", "D"],
                format_func=lambda x: f"{x}. {options.get(x, '')}",
                key=f"radio_q_{i}",
                horizontal=True
            )
            st.session_state.current_answers[f"q_{i}"] = answer
        
        st.markdown("<br>", unsafe_allow_html=True)
    
    # Submit/Results buttons
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
            st.rerun()
    
    # Show score if results are displayed
    if show_results:
        correct_count = 0
        for i, q in enumerate(questions):
            selected = st.session_state.current_answers.get(f"q_{i}", "")
            if selected == q.get("correct_answer"):
                correct_count += 1
        
        score_percent = (correct_count / len(questions)) * 100
        
        if score_percent >= 80:
            score_color = COLORS["success"]
            score_msg = "Excellent! You're ready for the LEPT! 🎉"
        elif score_percent >= 60:
            score_color = COLORS["warning"]
            score_msg = "Good job! Keep reviewing to improve. 📚"
        else:
            score_color = COLORS["error"]
            score_msg = "Keep studying! Practice makes perfect! 💪"
        
        st.markdown(f"""
        <div style="background: {score_color}22; padding: 1.5rem; border-radius: 16px; 
                    text-align: center; margin-top: 1rem; border: 2px solid {score_color};">
            <h3 style="color: {score_color}; margin: 0;">Your Score: {correct_count}/{len(questions)} ({score_percent:.0f}%)</h3>
            <p style="color: {COLORS['text']}; margin: 0.5rem 0 0 0;">{score_msg}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Check fresh user data for remaining questions
        fresh_user = get_user_by_email(email)
        if fresh_user:
            status = get_user_status(fresh_user)
            if status["plan"] == PLAN_FREE:
                remaining = fresh_user.get('questions_remaining', 0)
                if remaining <= 0:
                    st.markdown(f"""
                    <div style="background: rgba(239, 68, 68, 0.15); padding: 1rem; border-radius: 12px;
                                border: 1px solid {COLORS['error']}; margin-top: 1rem; text-align: center;">
                        <p style="margin: 0; color: {COLORS['text']};">
                            🚨 <strong style="color: {COLORS['error']};">You have no questions left!</strong>
                            <br>You've used all 10 free questions. Upgrade to continue practicing!
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("💳 Upgrade to Continue", key="upgrade_after_quiz", use_container_width=True, type="primary"):
                        st.session_state.current_page = "upgrade"
                        st.rerun()
