"""
LEPT AI Reviewer - Payment Handling Service
Updated for email-based user identification
"""

import base64
from datetime import datetime, timedelta
from typing import Tuple, Optional

import streamlit as st

from config.settings import (
    PLAN_PRO, PLAN_PREMIUM,
    PRO_PRICE, PREMIUM_PRICE,
    PRO_QUESTION_BONUS, PREMIUM_DURATION_DAYS,
    PAYMENT_PENDING, PAYMENT_APPROVED, PAYMENT_REJECTED,
    ACTION_PAYMENT_APPROVED, ACTION_PAYMENT_REJECTED
)
from database.queries import (
    create_payment, get_user_payments, approve_payment, reject_payment,
    get_pending_payments, get_all_payments, update_user_plan,
    log_admin_action, get_user_by_email
)
from utils.file_utils import encode_file_to_base64
from utils.validators import validate_full_name, validate_email, validate_gcash_reference


def submit_payment_request(
    email: str,
    full_name: str,
    plan_requested: str,
    gcash_ref: str = None,
    receipt_file = None
) -> Tuple[bool, str]:
    """
    Submit a new payment request.
    
    Args:
        email: User's email
        full_name: Customer's full name
        plan_requested: PRO or PREMIUM
        gcash_ref: GCash reference number (optional)
        receipt_file: Uploaded receipt file
    
    Returns:
        Tuple of (success, message)
    """
    # Validate inputs
    valid, msg = validate_full_name(full_name)
    if not valid:
        return False, msg
    
    valid, msg = validate_email(email)
    if not valid:
        return False, msg
    
    if gcash_ref:
        valid, msg = validate_gcash_reference(gcash_ref)
        if not valid:
            return False, msg
    
    if plan_requested not in [PLAN_PRO, PLAN_PREMIUM]:
        return False, "Invalid plan selected"
    
    # Process receipt file - store path for now (actual file storage would use Snowflake stages)
    receipt_path = ""
    if receipt_file:
        receipt_path = f"@STAGE_RECEIPTS/{email}/{receipt_file.name}"
    
    # Create payment record
    payment_id = create_payment(
        email=email,
        full_name=full_name,
        plan_requested=plan_requested,
        gcash_ref=gcash_ref,
        receipt_storage_path=receipt_path
    )
    
    if payment_id:
        return True, "Payment request submitted successfully! Please allow 12-24 hours for processing."
    
    return False, "Failed to submit payment request. Please try again."


def process_payment_approval(payment_id: int, payment_data: dict, admin_notes: str = None) -> Tuple[bool, str]:
    """
    Process payment approval by admin.
    
    Args:
        payment_id: Payment ID to approve
        payment_data: Payment details dictionary
        admin_notes: Optional admin notes
    
    Returns:
        Tuple of (success, message)
    """
    email = payment_data.get("email")
    plan_requested = payment_data.get("plan_requested")
    
    if not email or not plan_requested:
        return False, "Invalid payment data"
    
    # Get current user data
    user = get_user_by_email(email)
    if not user:
        return False, "User not found"
    
    # Calculate new quota/expiry
    current_questions = user.get("questions_remaining", 0)
    
    if plan_requested == PLAN_PRO:
        new_questions = current_questions + PRO_QUESTION_BONUS
        new_expiry = None
        update_user_plan(email, PLAN_PRO, new_questions, new_expiry)
    
    elif plan_requested == PLAN_PREMIUM:
        new_expiry = datetime.now() + timedelta(days=PREMIUM_DURATION_DAYS)
        # Premium users get unlimited (high number for display)
        update_user_plan(email, PLAN_PREMIUM, 999999, new_expiry)
    
    # Update payment status
    approve_payment(payment_id, admin_notes, "admin")
    
    # Log action
    log_admin_action("admin", ACTION_PAYMENT_APPROVED, f"Approved {plan_requested} for {email}")
    
    return True, f"Payment approved! User upgraded to {plan_requested}."


def process_payment_rejection(payment_id: int, payment_data: dict, admin_notes: str = None) -> Tuple[bool, str]:
    """
    Process payment rejection by admin.
    
    Args:
        payment_id: Payment ID to reject
        payment_data: Payment details dictionary
        admin_notes: Optional rejection reason
    
    Returns:
        Tuple of (success, message)
    """
    email = payment_data.get("email")
    
    # Update payment status
    reject_payment(payment_id, admin_notes, "admin")
    
    # Log action
    log_admin_action("admin", ACTION_PAYMENT_REJECTED, f"Rejected payment for {email}: {admin_notes}")
    
    return True, "Payment rejected."


def get_user_payment_status(email: str) -> dict:
    """
    Get payment status summary for a user.
    
    Args:
        email: User's email
    
    Returns:
        Dictionary with payment status info
    """
    payments = get_user_payments(email)
    
    pending = [p for p in payments if p.get("status") == PAYMENT_PENDING]
    approved = [p for p in payments if p.get("status") == PAYMENT_APPROVED]
    rejected = [p for p in payments if p.get("status") == PAYMENT_REJECTED]
    
    return {
        "total_payments": len(payments),
        "pending_count": len(pending),
        "approved_count": len(approved),
        "rejected_count": len(rejected),
        "has_pending": len(pending) > 0,
        "latest_pending": pending[0] if pending else None,
        "payments": payments
    }


def get_plan_details(plan_type: str) -> dict:
    """
    Get plan details for display.
    
    Args:
        plan_type: FREE, PRO, or PREMIUM
    
    Returns:
        Dictionary with plan details
    """
    plans = {
        "FREE": {
            "name": "FREE",
            "price": "Free",
            "price_value": 0,
            "questions": "15 questions",
            "features": [
                "15 preset LEPT questions",
                "Elementary & Secondary",
                "GenEd, ProfEd, Specialization"
            ],
            "limitations": [
                "Preset questions only",
                "No AI-generated questions",
                "No upload/download feature",
                "No admin reviewer access"
            ]
        },
        "PRO": {
            "name": "PRO",
            "price": f"₱{PRO_PRICE}",
            "price_value": PRO_PRICE,
            "questions": f"+{PRO_QUESTION_BONUS} AI questions",
            "features": [
                f"🤖 AI-generated questions",
                f"Additional {PRO_QUESTION_BONUS} questions",
                "📤 Upload your reviewers",
                "📥 Download admin reviewers"
            ],
            "limitations": [
                "Questions are consumable"
            ]
        },
        "PREMIUM": {
            "name": "PREMIUM",
            "price": f"₱{PREMIUM_PRICE}",
            "price_value": PREMIUM_PRICE,
            "questions": "Unlimited for 30 days",
            "features": [
                "🤖 Unlimited AI questions",
                f"Valid for {PREMIUM_DURATION_DAYS} days",
                "📤 Upload unlimited reviewers",
                "📥 Full admin library access",
                "⭐ Priority support"
            ],
            "limitations": []
        }
    }
    
    return plans.get(plan_type, plans["FREE"])
