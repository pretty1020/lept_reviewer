"""
LEPT AI Reviewer - Configuration Settings
Updated with 2026 PRC LEPT Guidelines
"""

# Application Settings
APP_NAME = "LEPT AI Reviewer"
APP_TAGLINE = "PH Edition"
APP_DESCRIPTION = "AI-Powered Reviewer for the Philippine Licensure Examination for Professional Teachers"

# Plan Types
PLAN_FREE = "FREE"
PLAN_PRO = "PRO"
PLAN_PREMIUM = "PREMIUM"

# Usage Limits
FREE_QUESTION_LIMIT = 15
PRO_QUESTION_BONUS = 75
PREMIUM_DURATION_DAYS = 30

# Pricing (PHP)
PRO_PRICE = 99
PREMIUM_PRICE = 499

# GCash Payment Details
GCASH_NUMBER = "0927 159 5709"
GCASH_ACCOUNT_NAME = "M**K L***D S."

# ============== 2026 PRC LEPT STRUCTURE ==============

# Education Levels
EDUCATION_LEVELS = {
    "elementary": "Elementary Education (BEEd)",
    "secondary": "Secondary Education (BSEd)"
}

# Exam Components with Weights
EXAM_COMPONENTS = {
    "general_education": {
        "name": "General Education (GenEd)",
        "weight": 20,
        "description": "Covers English, Filipino, Mathematics, Science, and Social Studies fundamentals"
    },
    "professional_education": {
        "name": "Professional Education (ProfEd)",
        "weight": 40,
        "description": "Covers teaching principles, child development, curriculum, and assessment"
    },
    "specialization": {
        "name": "Area of Specialization",
        "weight": 40,
        "description": "Covers your specific major/field of study"
    }
}

# Elementary Education Specializations (BEEd) - Effective 2026
ELEMENTARY_SPECIALIZATIONS = [
    "Early Childhood Education (ECE)",
    "Special Needs Education (SNE)",
    "General Education"
]

# Secondary Education Specializations (BSEd)
SECONDARY_SPECIALIZATIONS = [
    "English",
    "Filipino",
    "Mathematics",
    "Science",
    "Social Studies",
    "Values Education",
    "Technology and Livelihood Education (TLE)",
    "Technical-Vocational Teacher Education (TVTE)",
    "Physical Education (PE)",
    "Culture and Arts Education"
]

# TLE Sub-specializations (for Secondary TLE majors)
TLE_SUBSPECIALIZATIONS = [
    "Agriculture and Fishery Arts",
    "Home Economics",
    "Information and Communication Technology (ICT)",
    "Industrial Arts"
]

# Legacy - keeping for backward compatibility
EXAM_CATEGORIES = {
    "general_education": "General Education (GenEd)",
    "professional_education": "Professional Education (ProfEd)",
    "specialization": "Area of Specialization"
}

SPECIALIZATIONS = SECONDARY_SPECIALIZATIONS  # Default to secondary

# Difficulty Levels
DIFFICULTY_LEVELS = ["Easy", "Medium", "Hard"]

# Questions per generation
QUESTIONS_PER_BATCH = 5

# Modern Techy UI Theme Colors
COLORS = {
    "primary": "#6366F1",        # Indigo
    "primary_dark": "#4F46E5",   # Darker Indigo
    "secondary": "#06B6D4",      # Cyan
    "accent": "#8B5CF6",         # Purple
    "success": "#10B981",        # Emerald
    "warning": "#F59E0B",        # Amber
    "error": "#EF4444",          # Red
    "background": "#0F172A",     # Slate 900
    "background_light": "#1E293B", # Slate 800
    "surface": "#334155",        # Slate 700
    "text": "#F8FAFC",           # Slate 50
    "text_muted": "#94A3B8",     # Slate 400
    "border": "#475569",         # Slate 600
    "gradient_start": "#6366F1",
    "gradient_end": "#06B6D4",
    "glow": "rgba(99, 102, 241, 0.4)"
}

# Payment Status
PAYMENT_PENDING = "PENDING"
PAYMENT_APPROVED = "APPROVED"
PAYMENT_REJECTED = "REJECTED"

# Action Types for Logging
ACTION_LOGIN = "LOGIN"
ACTION_QUESTION_GENERATED = "QUESTION_GENERATED"
ACTION_DOCUMENT_UPLOADED = "DOCUMENT_UPLOADED"
ACTION_PAYMENT_SUBMITTED = "PAYMENT_SUBMITTED"
ACTION_PAYMENT_APPROVED = "APPROVE_PAYMENT"
ACTION_PAYMENT_REJECTED = "REJECT_PAYMENT"
ACTION_USER_BLOCKED = "BLOCK_USER"
ACTION_USER_UNBLOCKED = "UNBLOCK_USER"
ACTION_QUOTA_ADJUSTED = "ADJUST_QUOTA"
ACTION_UPLOAD_ADMIN_DOC = "UPLOAD_ADMIN_DOC"
ACTION_USER_DELETED = "DELETE_USER"
ACTION_PLAN_CHANGED = "CHANGE_PLAN"
ACTION_DELETE_ADMIN_DOC = "DELETE_ADMIN_DOC"

# File Upload Settings
ALLOWED_EXTENSIONS = [".pdf", ".docx"]
MAX_FILE_SIZE_MB = 200  # Allow large files up to 200MB

# Warning Messages
EMAIL_SHARING_WARNING = "⚠️ **DO NOT share your email address. Sharing may result in access issues or blocking.**"

# Snowflake Configuration
SNOWFLAKE_SCHEMA = "APP"
SNOWFLAKE_WAREHOUSE = "COMPUTE_WH"
