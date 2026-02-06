"""
LEPT AI Reviewer - Card Components
"""

import streamlit as st
from config.settings import COLORS


def render_nav_card(icon: str, title: str, description: str, page_key: str, color: str = None):
    """
    Render a navigation card button.
    
    Args:
        icon: Emoji icon
        title: Card title
        description: Card description
        page_key: Page key to navigate to
        color: Optional accent color
    """
    if color is None:
        color = COLORS["primary"]
    
    card_html = f"""
    <div class="nav-card" onclick="document.getElementById('nav_card_{page_key}').click();" 
         style="cursor: pointer; background: white; padding: 1.5rem; border-radius: 12px; 
                box-shadow: 0 2px 8px rgba(0,0,0,0.08); border-left: 4px solid {color};
                transition: all 0.3s ease; margin-bottom: 1rem;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
        <h3 style="color: {COLORS['primary']}; margin: 0 0 0.5rem 0;">{title}</h3>
        <p style="color: #666; margin: 0; font-size: 0.9rem;">{description}</p>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)
    
    # Hidden button for click handling
    if st.button(f"Go to {title}", key=f"nav_card_{page_key}", use_container_width=True):
        st.session_state.current_page = page_key
        st.rerun()


def render_stat_card(title: str, value: str, icon: str = None, color: str = None):
    """
    Render a statistics card.
    
    Args:
        title: Card title
        value: Main value to display
        icon: Optional emoji icon
        color: Optional accent color
    """
    if color is None:
        color = COLORS["secondary"]
    
    icon_html = f'<span style="font-size: 1.5rem;">{icon}</span>' if icon else ""
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {color}22 0%, {color}11 100%); 
                padding: 1rem; border-radius: 10px; text-align: center;">
        {icon_html}
        <h4 style="color: {COLORS['text']}; margin: 0.5rem 0 0 0; font-size: 0.9rem;">{title}</h4>
        <p style="color: {color}; margin: 0; font-size: 1.5rem; font-weight: bold;">{value}</p>
    </div>
    """, unsafe_allow_html=True)


def render_plan_card(plan_name: str, price: str, features: list, is_current: bool = False, 
                    is_recommended: bool = False, color: str = None):
    """
    Render a pricing plan card.
    
    Args:
        plan_name: Name of the plan
        price: Price display string
        features: List of feature strings
        is_current: Whether this is the user's current plan
        is_recommended: Whether to show recommended badge
        color: Optional accent color
    """
    if color is None:
        color = COLORS["primary"]
    
    border_style = f"3px solid {color}" if is_recommended else "1px solid #eee"
    badge_html = '<span style="background: #E9C46A; color: #333; padding: 2px 10px; border-radius: 20px; font-size: 0.75rem; position: absolute; top: -10px; right: 10px;">RECOMMENDED</span>' if is_recommended else ""
    current_badge = '<span style="background: #4CAF50; color: white; padding: 2px 10px; border-radius: 20px; font-size: 0.75rem; margin-left: 10px;">CURRENT</span>' if is_current else ""
    
    features_html = "".join([f'<li style="padding: 0.3rem 0; color: #555;">✓ {f}</li>' for f in features])
    
    st.markdown(f"""
    <div style="background: white; padding: 1.5rem; border-radius: 12px; 
                border: {border_style}; position: relative; height: 100%;">
        {badge_html}
        <h3 style="color: {color}; margin: 0;">{plan_name}{current_badge}</h3>
        <p style="font-size: 2rem; font-weight: bold; color: {COLORS['text']}; margin: 0.5rem 0;">{price}</p>
        <ul style="list-style: none; padding: 0; margin: 1rem 0;">
            {features_html}
        </ul>
    </div>
    """, unsafe_allow_html=True)


def render_info_card(title: str, content: str, icon: str = "ℹ️", card_type: str = "info"):
    """
    Render an information card.
    
    Args:
        title: Card title
        content: Card content (can include HTML)
        icon: Emoji icon
        card_type: Type of card (info, warning, success, error)
    """
    colors = {
        "info": COLORS["secondary"],
        "warning": COLORS["warning"],
        "success": COLORS["success"],
        "error": COLORS["error"]
    }
    
    bg_colors = {
        "info": "#E8F5E9",
        "warning": "#FFF3E0",
        "success": "#E8F5E9",
        "error": "#FFEBEE"
    }
    
    color = colors.get(card_type, COLORS["secondary"])
    bg_color = bg_colors.get(card_type, "#E8F5E9")
    
    st.markdown(f"""
    <div style="background: {bg_color}; padding: 1rem; border-radius: 10px; 
                border-left: 4px solid {color}; margin: 1rem 0;">
        <h4 style="color: {COLORS['text']}; margin: 0 0 0.5rem 0;">{icon} {title}</h4>
        <div style="color: #555;">{content}</div>
    </div>
    """, unsafe_allow_html=True)


def render_document_card(filename: str, doc_id: str, is_locked: bool = False, 
                        is_selected: bool = False, show_delete: bool = False):
    """
    Render a document card for reviewer files.
    
    Args:
        filename: Name of the file
        doc_id: Document ID
        is_locked: Whether the document is locked (for free users)
        is_selected: Whether the document is currently selected
        show_delete: Whether to show delete button
    
    Returns:
        Tuple of (selected, deleted) booleans
    """
    from utils.file_utils import get_file_icon
    
    icon = get_file_icon(filename)
    
    if is_locked:
        lock_icon = "🔒"
        opacity = "0.6"
        tooltip = "Upgrade to PRO or PREMIUM to use this reviewer"
    else:
        lock_icon = ""
        opacity = "1"
        tooltip = ""
    
    border_color = COLORS["secondary"] if is_selected else "#ddd"
    bg_color = f"{COLORS['secondary']}11" if is_selected else "white"
    
    st.markdown(f"""
    <div style="background: {bg_color}; padding: 0.75rem 1rem; border-radius: 8px; 
                border: 2px solid {border_color}; margin-bottom: 0.5rem; opacity: {opacity};"
         title="{tooltip}">
        <span style="font-size: 1.2rem;">{icon}</span>
        <span style="margin-left: 0.5rem; color: {COLORS['text']};">{filename}</span>
        <span style="float: right;">{lock_icon}</span>
    </div>
    """, unsafe_allow_html=True)


def render_question_card(question_num: int, question_text: str, options: dict,
                        selected_answer: str = None, correct_answer: str = None,
                        show_result: bool = False, explanation: str = None):
    """
    Render a question card for practice exams.
    
    Args:
        question_num: Question number
        question_text: The question text
        options: Dictionary of options (A, B, C, D)
        selected_answer: User's selected answer
        correct_answer: The correct answer
        show_result: Whether to show correct/incorrect result
        explanation: Explanation text
    """
    st.markdown(f"""
    <div style="background: white; padding: 1.5rem; border-radius: 12px; 
                box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 1rem;">
        <h4 style="color: {COLORS['primary']}; margin: 0 0 1rem 0;">Question {question_num}</h4>
        <p style="color: {COLORS['text']}; font-size: 1.05rem; line-height: 1.6;">{question_text}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Options as radio buttons
    option_labels = [f"{key}. {value}" for key, value in options.items()]
    
    if show_result and selected_answer:
        for key, value in options.items():
            if key == correct_answer:
                st.success(f"✓ {key}. {value}")
            elif key == selected_answer and selected_answer != correct_answer:
                st.error(f"✗ {key}. {value}")
            else:
                st.write(f"   {key}. {value}")
        
        if explanation:
            st.info(f"**Explanation:** {explanation}")
    
    return None
