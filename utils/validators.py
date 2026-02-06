"""
LEPT AI Reviewer - Input Validation Utilities
"""

import re
from typing import Tuple


def validate_email(email: str) -> Tuple[bool, str]:
    """
    Validate an email address.
    
    Args:
        email: Email address to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not email:
        return False, "Email address is required"
    
    email = email.strip().lower()
    
    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        return False, "Please enter a valid email address"
    
    # Check for common typos
    if email.endswith('.con'):
        return False, "Did you mean .com?"
    
    if '..' in email:
        return False, "Invalid email format"
    
    return True, ""


def validate_full_name(name: str) -> Tuple[bool, str]:
    """
    Validate a full name.
    
    Args:
        name: Name to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name:
        return False, "Full name is required"
    
    name = name.strip()
    
    if len(name) < 2:
        return False, "Name is too short"
    
    if len(name) > 100:
        return False, "Name is too long"
    
    # Check for only letters, spaces, and common name characters
    pattern = r'^[a-zA-Z\s\.\-\']+$'
    if not re.match(pattern, name):
        return False, "Name contains invalid characters"
    
    return True, ""


def validate_gcash_reference(ref: str) -> Tuple[bool, str]:
    """
    Validate a GCash reference number.
    
    Args:
        ref: Reference number to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not ref:
        return True, ""  # Optional field
    
    ref = ref.strip()
    
    # GCash references are typically alphanumeric
    pattern = r'^[a-zA-Z0-9\-]+$'
    if not re.match(pattern, ref):
        return False, "Reference number contains invalid characters"
    
    if len(ref) < 4:
        return False, "Reference number is too short"
    
    if len(ref) > 50:
        return False, "Reference number is too long"
    
    return True, ""


def sanitize_input(text: str) -> str:
    """
    Sanitize user input to prevent injection attacks.
    
    Args:
        text: Input text to sanitize
    
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    # Remove potential SQL injection characters
    sanitized = text.replace("'", "''")
    sanitized = sanitized.replace(";", "")
    sanitized = sanitized.replace("--", "")
    
    # Remove HTML tags
    sanitized = re.sub(r'<[^>]+>', '', sanitized)
    
    return sanitized.strip()


def validate_password(password: str) -> Tuple[bool, str]:
    """
    Validate admin password format.
    
    Args:
        password: Password to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not password:
        return False, "Password is required"
    
    if len(password) < 1:
        return False, "Password cannot be empty"
    
    return True, ""
