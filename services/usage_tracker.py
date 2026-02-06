"""
LEPT AI Reviewer - Usage Tracking Service
Updated for email-based user identification
"""

from datetime import datetime
from typing import Tuple, Optional

import streamlit as st

from config.settings import (
    PLAN_FREE, PLAN_PRO, PLAN_PREMIUM,
    FREE_QUESTION_LIMIT, PRO_QUESTION_BONUS, PREMIUM_DURATION_DAYS
)
from database.queries import (
    get_user_by_email, create_user, update_user_ip,
    decrement_user_questions, log_usage, check_premium_expiry,
    update_user_plan, increment_ip_usage, is_ip_blocked
)
from utils.ip_utils import get_client_ip


def get_or_create_user(email: str) -> Tuple[Optional[dict], str]:
    """
    Get existing user or create new one based on email and IP.
    
    Args:
        email: User's email address
    
    Returns:
        Tuple of (user_dict, message)
    """
    ip_address = get_client_ip()
    
    # Check if IP is blocked
    if is_ip_blocked(ip_address):
        return None, "This IP address has been blocked. Please contact support."
    
    # Check for existing user with this email
    existing_user = get_user_by_email(email)
    
    if existing_user:
        # Check if blocked
        if existing_user.get("is_blocked"):
            return None, "This account has been blocked. Please contact support."
        
        # Update IP address
        update_user_ip(email, ip_address)
        
        # Check premium expiry
        if existing_user.get("plan_type") == PLAN_PREMIUM:
            check_premium_expiry(email)
            # Refresh user data
            existing_user = get_user_by_email(email)
        
        return existing_user, "Welcome back!"
    
    # Create new user
    created_email = create_user(email, ip_address)
    
    if created_email:
        new_user = get_user_by_email(email)
        return new_user, "Account created successfully!"
    
    return None, "Failed to create account. Please try again."


def can_generate_questions(user: dict) -> Tuple[bool, str]:
    """
    Check if user can generate questions.
    
    Args:
        user: User dictionary
    
    Returns:
        Tuple of (can_generate, reason)
    """
    if not user:
        return False, "User not found"
    
    if user.get("is_blocked"):
        return False, "Your account has been blocked."
    
    plan_type = user.get("plan_type", PLAN_FREE)
    
    # Premium users - check expiry
    if plan_type == PLAN_PREMIUM:
        expiry = user.get("premium_expiry")
        if expiry:
            if isinstance(expiry, str):
                expiry = datetime.fromisoformat(expiry)
            if expiry > datetime.now():
                return True, "Premium access active"
            else:
                # Premium expired
                return False, "Your Premium subscription has expired. Please renew to continue."
    
    # Free and Pro users - check quota
    questions_remaining = user.get("questions_remaining", 0)
    
    if questions_remaining <= 0:
        if plan_type == PLAN_FREE:
            return False, "You've used all your free questions. Upgrade to PRO or PREMIUM for more!"
        else:
            return False, "You've used all your questions. Upgrade to PREMIUM for unlimited access!"
    
    return True, f"{questions_remaining} questions remaining"


def use_questions(email: str, ip_address: str, count: int = 1, 
                  source_type: str = None, category: str = None, difficulty: str = None) -> bool:
    """
    Decrement question count for a user and log usage.
    
    Args:
        email: User's email
        ip_address: User's IP address
        count: Number of questions used
        source_type: Source of documents (USER_DOCS, ADMIN_DOCS, MIXED)
        category: Exam category
        difficulty: Difficulty level
    
    Returns:
        True if successful
    """
    # Get fresh user data
    user = get_user_by_email(email)
    
    if not user:
        return False
    
    # Log the usage
    log_usage(email, ip_address, count, source_type, category, difficulty)
    
    # Increment IP usage
    increment_ip_usage(ip_address, count)
    
    # Premium users don't decrement quota
    if user.get("plan_type") == PLAN_PREMIUM:
        expiry = user.get("premium_expiry")
        if expiry and expiry > datetime.now():
            return True
    
    # Decrement for Free and Pro users
    result = decrement_user_questions(email, count)
    
    return result


def get_user_status(user: dict) -> dict:
    """
    Get formatted user status for display.
    
    Args:
        user: User dictionary
    
    Returns:
        Status dictionary with display-ready values
    """
    if not user:
        return {
            "plan": "Unknown",
            "plan_badge": "secondary",
            "questions_display": "N/A",
            "questions_used": 0,
            "expiry_display": None,
            "can_use_admin_docs": False
        }
    
    plan_type = user.get("plan_type", PLAN_FREE)
    questions = user.get("questions_remaining", 0)
    questions_used = user.get("questions_used_total", 0)
    expiry = user.get("premium_expiry")
    
    # Questions display
    if plan_type == PLAN_PREMIUM and expiry:
        if isinstance(expiry, str):
            expiry = datetime.fromisoformat(expiry)
        if expiry > datetime.now():
            questions_display = "Unlimited"
        else:
            questions_display = str(questions)
    else:
        questions_display = str(questions)
    
    # Expiry display
    expiry_display = None
    if plan_type == PLAN_PREMIUM and expiry:
        if isinstance(expiry, str):
            expiry = datetime.fromisoformat(expiry)
        if expiry > datetime.now():
            days_left = (expiry - datetime.now()).days
            expiry_display = f"{days_left} days left"
        else:
            expiry_display = "Expired"
    
    return {
        "plan": plan_type,
        "questions_display": questions_display,
        "questions_used": questions_used,
        "expiry_display": expiry_display,
        "can_use_admin_docs": plan_type in [PLAN_PRO, PLAN_PREMIUM]
    }


def refresh_user_session():
    """Refresh user data in session state."""
    if "user" in st.session_state and st.session_state.user:
        email = st.session_state.user.get("email")
        if email:
            fresh_user = get_user_by_email(email)
            if fresh_user:
                st.session_state.user = fresh_user
