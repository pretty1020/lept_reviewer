"""
LEPT AI Reviewer - Cached Database Queries
OPTIMIZED: All SELECT queries are cached to reduce Snowflake calls
"""

import streamlit as st
from typing import Optional, List, Dict
from database.connection import execute_query, execute_write
from config.settings import (
    PLAN_FREE, PLAN_PRO, PLAN_PREMIUM,
    FREE_QUESTION_LIMIT, PRO_QUESTION_BONUS, PREMIUM_DURATION_DAYS,
    PAYMENT_PENDING
)


# ============== CACHED SELECT QUERIES ==============

@st.cache_data(ttl=60, show_spinner=False)
def cached_get_user_by_email(email: str) -> Optional[Dict]:
    """Get user by email - cached for 60 seconds."""
    query = """
    SELECT EMAIL, IP_ADDRESS, PLAN_STATUS, QUESTIONS_USED_TOTAL, QUESTIONS_REMAINING, 
           PREMIUM_EXPIRY, IS_BLOCKED, CREATED_AT, UPDATED_AT
    FROM USERS 
    WHERE EMAIL = %s
    LIMIT 1
    """
    result = execute_query(query, (email,))
    if result and len(result) > 0:
        row = result[0]
        return {
            "email": row[0],
            "ip_address": row[1],
            "plan_type": row[2],
            "questions_used_total": row[3],
            "questions_remaining": row[4],
            "premium_expiry": row[5],
            "is_blocked": row[6],
            "created_at": row[7],
            "updated_at": row[8]
        }
    return None


@st.cache_data(ttl=300, show_spinner=False)
def cached_get_admin_documents() -> List[Dict]:
    """Get admin documents - cached for 5 minutes."""
    query = """
    SELECT ADMIN_DOC_ID, FILE_NAME, FILE_TYPE, STORAGE_PATH, TEXT_STAGE_PATH, 
           IS_DOWNLOADABLE, UPLOADED_AT, UPLOADED_BY, CATEGORY, EXTRACTED_TEXT
    FROM ADMIN_DOCUMENTS 
    WHERE IS_DELETED = FALSE
    ORDER BY UPLOADED_AT DESC
    LIMIT 50
    """
    result = execute_query(query)
    docs = []
    if result:
        for row in result:
            docs.append({
                "doc_id": row[0],
                "filename": row[1],
                "file_type": row[2],
                "storage_path": row[3],
                "text_stage_path": row[4],
                "is_downloadable": row[5],
                "created_at": row[6],
                "uploaded_by": row[7],
                "category": row[8] or "General",
                "extracted_text": row[9]
            })
    return docs


@st.cache_data(ttl=120, show_spinner=False)
def cached_get_user_documents(email: str) -> List[Dict]:
    """Get user documents with extracted text - cached for 2 minutes."""
    # Try with EXTRACTED_TEXT column first
    query_with_text = """
    SELECT DOC_ID, EMAIL, FILE_NAME, FILE_TYPE, STORAGE_PATH, TEXT_STAGE_PATH, UPLOADED_AT, EXTRACTED_TEXT
    FROM USER_DOCUMENTS 
    WHERE EMAIL = %s AND IS_DELETED = FALSE
    ORDER BY UPLOADED_AT DESC
    LIMIT 20
    """
    result = execute_query(query_with_text, (email,))
    
    # Fallback if EXTRACTED_TEXT column doesn't exist
    if result is None:
        query_basic = """
        SELECT DOC_ID, EMAIL, FILE_NAME, FILE_TYPE, STORAGE_PATH, TEXT_STAGE_PATH, UPLOADED_AT
        FROM USER_DOCUMENTS 
        WHERE EMAIL = %s AND IS_DELETED = FALSE
        ORDER BY UPLOADED_AT DESC
        LIMIT 20
        """
        result = execute_query(query_basic, (email,))
        docs = []
        if result:
            for row in result:
                docs.append({
                    "doc_id": row[0],
                    "email": row[1],
                    "filename": row[2],
                    "file_type": row[3],
                    "storage_path": row[4],
                    "text_stage_path": row[5],
                    "created_at": row[6],
                    "extracted_text": None
                })
        return docs
    
    docs = []
    if result:
        for row in result:
            docs.append({
                "doc_id": row[0],
                "email": row[1],
                "filename": row[2],
                "file_type": row[3],
                "storage_path": row[4],
                "text_stage_path": row[5],
                "created_at": row[6],
                "extracted_text": row[7] if len(row) > 7 else None
            })
    return docs


@st.cache_data(ttl=60, show_spinner=False)
def cached_get_pending_payments_count() -> int:
    """Get count of pending payments - cached."""
    query = "SELECT COUNT(*) FROM PAYMENTS WHERE STATUS = %s"
    result = execute_query(query, (PAYMENT_PENDING,))
    if result and result[0]:
        return result[0][0]
    return 0


@st.cache_data(ttl=30, show_spinner=False)
def cached_is_ip_blocked(ip_address: str) -> bool:
    """Check if IP is blocked - cached for 30 seconds."""
    query = "SELECT IS_BLOCKED FROM IP_USAGE WHERE IP_ADDRESS = %s LIMIT 1"
    result = execute_query(query, (ip_address,))
    if result and len(result) > 0:
        return bool(result[0][0])
    return False


# ============== CACHE INVALIDATION FUNCTIONS ==============

def invalidate_user_cache(email: str):
    """Invalidate user cache after updates."""
    cached_get_user_by_email.clear()


def invalidate_admin_docs_cache():
    """Invalidate admin documents cache after updates."""
    cached_get_admin_documents.clear()


def invalidate_user_docs_cache(email: str):
    """Invalidate user documents cache after updates."""
    cached_get_user_documents.clear()


def invalidate_all_caches():
    """Invalidate all cached queries."""
    cached_get_user_by_email.clear()
    cached_get_admin_documents.clear()
    cached_get_user_documents.clear()
    cached_get_pending_payments_count.clear()
    cached_is_ip_blocked.clear()


# ============== WRITE OPERATIONS (NO CACHING) ==============

def write_create_user(email: str, ip_address: str) -> Optional[str]:
    """Create a new user."""
    query = """
    INSERT INTO USERS (EMAIL, IP_ADDRESS, PLAN_STATUS, QUESTIONS_REMAINING)
    VALUES (%s, %s, %s, %s)
    """
    result = execute_write(query, (email, ip_address, PLAN_FREE, FREE_QUESTION_LIMIT))
    
    if result:
        # Invalidate cache
        invalidate_user_cache(email)
        # Log IP
        write_log_ip_history(email, ip_address)
        write_log_ip_usage(ip_address)
    
    return email if result else None


def write_update_user_ip(email: str, ip_address: str):
    """Update user's IP address."""
    query = """
    UPDATE USERS 
    SET IP_ADDRESS = %s, UPDATED_AT = CURRENT_TIMESTAMP()
    WHERE EMAIL = %s
    """
    result = execute_write(query, (ip_address, email))
    if result:
        write_log_ip_history(email, ip_address)
    return result


def write_decrement_questions(email: str, count: int = 1) -> bool:
    """Decrement user's remaining questions."""
    query = """
    UPDATE USERS 
    SET QUESTIONS_REMAINING = QUESTIONS_REMAINING - %s,
        QUESTIONS_USED_TOTAL = QUESTIONS_USED_TOTAL + %s,
        UPDATED_AT = CURRENT_TIMESTAMP()
    WHERE EMAIL = %s AND QUESTIONS_REMAINING >= %s
    """
    result = execute_write(query, (count, count, email, count))
    if result:
        invalidate_user_cache(email)
    return result


def write_log_ip_history(email: str, ip_address: str):
    """Log IP in user history."""
    # Check if exists
    check_query = "SELECT ID FROM USER_IP_HISTORY WHERE EMAIL = %s AND IP_ADDRESS = %s LIMIT 1"
    existing = execute_query(check_query, (email, ip_address))
    
    if existing and len(existing) > 0:
        update_query = """
        UPDATE USER_IP_HISTORY SET LAST_SEEN = CURRENT_TIMESTAMP() 
        WHERE EMAIL = %s AND IP_ADDRESS = %s
        """
        execute_write(update_query, (email, ip_address))
    else:
        insert_query = "INSERT INTO USER_IP_HISTORY (EMAIL, IP_ADDRESS) VALUES (%s, %s)"
        execute_write(insert_query, (email, ip_address))


def write_log_ip_usage(ip_address: str):
    """Log or update IP usage."""
    check_query = "SELECT IP_ADDRESS FROM IP_USAGE WHERE IP_ADDRESS = %s LIMIT 1"
    existing = execute_query(check_query, (ip_address,))
    
    if existing and len(existing) > 0:
        update_query = "UPDATE IP_USAGE SET LAST_SEEN = CURRENT_TIMESTAMP() WHERE IP_ADDRESS = %s"
        execute_write(update_query, (ip_address,))
    else:
        insert_query = "INSERT INTO IP_USAGE (IP_ADDRESS) VALUES (%s)"
        execute_write(insert_query, (ip_address,))


def write_log_usage(email: str, ip_address: str, questions_generated: int, 
                    source_type: str = None, category: str = None, difficulty: str = None):
    """Log a usage event."""
    query = """
    INSERT INTO USAGE_LOGS (EMAIL, IP_ADDRESS, QUESTIONS_GENERATED, SOURCE_TYPE, CATEGORY, DIFFICULTY)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    execute_write(query, (email, ip_address, questions_generated, source_type, category, difficulty))


def write_increment_ip_usage(ip_address: str, count: int = 1):
    """Increment questions used by IP."""
    query = """
    UPDATE IP_USAGE 
    SET QUESTIONS_USED_TOTAL = QUESTIONS_USED_TOTAL + %s, LAST_SEEN = CURRENT_TIMESTAMP()
    WHERE IP_ADDRESS = %s
    """
    execute_write(query, (count, ip_address))
