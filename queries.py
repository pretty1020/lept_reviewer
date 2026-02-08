"""
LEPT AI Reviewer - Database Query Functions
OPTIMIZED: Uses cached queries for reads, invalidates cache on writes
"""

from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any

from database.connection import execute_query, execute_write
from database.cached_queries import (
    cached_get_user_by_email, cached_get_admin_documents, cached_get_user_documents,
    cached_is_ip_blocked, invalidate_user_cache, invalidate_admin_docs_cache, 
    invalidate_user_docs_cache
)
from config.settings import (
    PLAN_FREE, PLAN_PRO, PLAN_PREMIUM,
    FREE_QUESTION_LIMIT, PRO_QUESTION_BONUS, PREMIUM_DURATION_DAYS,
    PAYMENT_PENDING, PAYMENT_APPROVED, PAYMENT_REJECTED
)


# ============== USER QUERIES ==============

def get_user_by_email(email: str) -> Optional[Dict]:
    """Get a user by email address - CACHED."""
    return cached_get_user_by_email(email)


def get_fresh_user_by_email(email: str) -> Optional[Dict]:
    """Get fresh (non-cached) user data - use sparingly."""
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


def create_user(email: str, ip_address: str) -> Optional[str]:
    """Create a new user and return the email."""
    query = """
    INSERT INTO USERS (EMAIL, IP_ADDRESS, PLAN_STATUS, QUESTIONS_REMAINING)
    VALUES (%s, %s, %s, %s)
    """
    result = execute_write(query, (email, ip_address, PLAN_FREE, FREE_QUESTION_LIMIT))
    
    if result:
        log_ip_history(email, ip_address)
        log_ip_usage(ip_address)
        invalidate_user_cache(email)
    
    return email if result else None


def update_user_ip(email: str, ip_address: str):
    """Update user's IP address and log to history."""
    query = """
    UPDATE USERS 
    SET IP_ADDRESS = %s, UPDATED_AT = CURRENT_TIMESTAMP()
    WHERE EMAIL = %s
    """
    result = execute_write(query, (ip_address, email))
    if result:
        log_ip_history(email, ip_address)
    return result


def update_user_plan(email: str, plan_type: str, questions_remaining: int = None, premium_expiry: datetime = None):
    """Update a user's plan."""
    if plan_type == PLAN_PREMIUM and premium_expiry is None:
        premium_expiry = datetime.now() + timedelta(days=PREMIUM_DURATION_DAYS)
    
    query = """
    UPDATE USERS 
    SET PLAN_STATUS = %s, QUESTIONS_REMAINING = %s, PREMIUM_EXPIRY = %s, UPDATED_AT = CURRENT_TIMESTAMP()
    WHERE EMAIL = %s
    """
    result = execute_write(query, (plan_type, questions_remaining, premium_expiry, email))
    if result:
        invalidate_user_cache(email)
    return result


def decrement_user_questions(email: str, count: int = 1) -> bool:
    """Decrement a user's remaining questions and increment total used."""
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


def block_user(email: str, blocked: bool = True):
    """Block or unblock a user."""
    query = """
    UPDATE USERS 
    SET IS_BLOCKED = %s, UPDATED_AT = CURRENT_TIMESTAMP()
    WHERE EMAIL = %s
    """
    result = execute_write(query, (blocked, email))
    if result:
        invalidate_user_cache(email)
    return result


def get_all_users(limit: int = 100) -> List[Dict]:
    """Get all users for admin panel - with limit, deduplicated by email."""
    # Use ROW_NUMBER to get only the latest record per email (handles duplicates)
    query = """
    SELECT EMAIL, IP_ADDRESS, PLAN_STATUS, QUESTIONS_USED_TOTAL, QUESTIONS_REMAINING, 
           PREMIUM_EXPIRY, IS_BLOCKED, CREATED_AT, UPDATED_AT
    FROM (
        SELECT EMAIL, IP_ADDRESS, PLAN_STATUS, QUESTIONS_USED_TOTAL, QUESTIONS_REMAINING, 
               PREMIUM_EXPIRY, IS_BLOCKED, CREATED_AT, UPDATED_AT,
               ROW_NUMBER() OVER (PARTITION BY EMAIL ORDER BY UPDATED_AT DESC) as rn
        FROM USERS
    ) 
    WHERE rn = 1
    ORDER BY CREATED_AT DESC
    LIMIT %s
    """
    result = execute_query(query, (limit,))
    users = []
    if result:
        for row in result:
            users.append({
                "email": row[0],
                "ip_address": row[1],
                "plan_type": row[2],
                "questions_used_total": row[3],
                "questions_remaining": row[4],
                "premium_expiry": row[5],
                "is_blocked": row[6],
                "created_at": row[7],
                "updated_at": row[8]
            })
    return users


def adjust_user_quota(email: str, new_quota: int):
    """Manually adjust a user's question quota."""
    query = """
    UPDATE USERS 
    SET QUESTIONS_REMAINING = %s, UPDATED_AT = CURRENT_TIMESTAMP()
    WHERE EMAIL = %s
    """
    result = execute_write(query, (new_quota, email))
    if result:
        invalidate_user_cache(email)
    return result


def delete_user(email: str) -> bool:
    """Delete a user and all related records."""
    execute_write("DELETE FROM USER_IP_HISTORY WHERE EMAIL = %s", (email,))
    execute_write("DELETE FROM USAGE_LOGS WHERE EMAIL = %s", (email,))
    execute_write("DELETE FROM USER_DOCUMENTS WHERE EMAIL = %s", (email,))
    execute_write("DELETE FROM PAYMENTS WHERE EMAIL = %s", (email,))
    
    query = "DELETE FROM USERS WHERE EMAIL = %s"
    result = execute_write(query, (email,))
    if result:
        invalidate_user_cache(email)
    return result


def change_user_plan(email: str, new_plan: str, questions_remaining: int = None) -> bool:
    """Change a user's plan with appropriate quota."""
    premium_expiry = None
    
    if new_plan == PLAN_FREE:
        if questions_remaining is None:
            questions_remaining = FREE_QUESTION_LIMIT
        premium_expiry = None
    elif new_plan == PLAN_PRO:
        if questions_remaining is None:
            questions_remaining = PRO_QUESTION_BONUS
        premium_expiry = None
    elif new_plan == PLAN_PREMIUM:
        if questions_remaining is None:
            questions_remaining = 9999
        premium_expiry = datetime.now() + timedelta(days=PREMIUM_DURATION_DAYS)
    
    query = """
    UPDATE USERS 
    SET PLAN_STATUS = %s, QUESTIONS_REMAINING = %s, PREMIUM_EXPIRY = %s, UPDATED_AT = CURRENT_TIMESTAMP()
    WHERE EMAIL = %s
    """
    result = execute_write(query, (new_plan, questions_remaining, premium_expiry, email))
    if result:
        invalidate_user_cache(email)
    return result


def check_premium_expiry(email: str) -> bool:
    """Check if premium has expired and revert to free if needed."""
    user = get_fresh_user_by_email(email)  # Need fresh data for expiry check
    if user and user["plan_type"] == PLAN_PREMIUM:
        if user["premium_expiry"] and user["premium_expiry"] < datetime.now():
            update_user_plan(email, PLAN_FREE, 0, None)
            return True
    return False


# ============== IP TRACKING QUERIES ==============

def log_ip_history(email: str, ip_address: str):
    """Log IP address in user history."""
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


def log_ip_usage(ip_address: str):
    """Log or update IP usage."""
    check_query = "SELECT IP_ADDRESS FROM IP_USAGE WHERE IP_ADDRESS = %s LIMIT 1"
    existing = execute_query(check_query, (ip_address,))
    
    if existing and len(existing) > 0:
        update_query = "UPDATE IP_USAGE SET LAST_SEEN = CURRENT_TIMESTAMP() WHERE IP_ADDRESS = %s"
        execute_write(update_query, (ip_address,))
    else:
        insert_query = "INSERT INTO IP_USAGE (IP_ADDRESS) VALUES (%s)"
        execute_write(insert_query, (ip_address,))


def increment_ip_usage(ip_address: str, count: int = 1):
    """Increment questions used by IP."""
    query = """
    UPDATE IP_USAGE 
    SET QUESTIONS_USED_TOTAL = QUESTIONS_USED_TOTAL + %s, LAST_SEEN = CURRENT_TIMESTAMP()
    WHERE IP_ADDRESS = %s
    """
    execute_write(query, (count, ip_address))


def is_ip_blocked(ip_address: str) -> bool:
    """Check if an IP is blocked - CACHED."""
    return cached_is_ip_blocked(ip_address)


# ============== USAGE LOG QUERIES ==============

def log_usage(email: str, ip_address: str, questions_generated: int, 
              source_type: str = None, category: str = None, difficulty: str = None, notes: str = None):
    """Log a usage event."""
    query = """
    INSERT INTO USAGE_LOGS (EMAIL, IP_ADDRESS, QUESTIONS_GENERATED, SOURCE_TYPE, CATEGORY, DIFFICULTY, NOTES)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    return execute_write(query, (email, ip_address, questions_generated, source_type, category, difficulty, notes))


def get_user_logs(email: str, limit: int = 20) -> List[Dict]:
    """Get usage logs for a specific user - limited."""
    query = """
    SELECT EVENT_ID, EMAIL, IP_ADDRESS, EVENT_TIME, QUESTIONS_GENERATED, SOURCE_TYPE, CATEGORY, DIFFICULTY, NOTES
    FROM USAGE_LOGS 
    WHERE EMAIL = %s
    ORDER BY EVENT_TIME DESC
    LIMIT %s
    """
    result = execute_query(query, (email, limit))
    logs = []
    if result:
        for row in result:
            logs.append({
                "event_id": row[0],
                "email": row[1],
                "ip_address": row[2],
                "event_time": row[3],
                "questions_generated": row[4],
                "source_type": row[5],
                "category": row[6],
                "difficulty": row[7],
                "notes": row[8]
            })
    return logs


def get_all_logs(limit: int = 50) -> List[Dict]:
    """Get all usage logs for admin panel - limited."""
    query = """
    SELECT EVENT_ID, EMAIL, IP_ADDRESS, EVENT_TIME, QUESTIONS_GENERATED, SOURCE_TYPE, CATEGORY, DIFFICULTY, NOTES
    FROM USAGE_LOGS
    ORDER BY EVENT_TIME DESC
    LIMIT %s
    """
    result = execute_query(query, (limit,))
    logs = []
    if result:
        for row in result:
            logs.append({
                "event_id": row[0],
                "email": row[1],
                "ip_address": row[2],
                "event_time": row[3],
                "questions_generated": row[4],
                "source_type": row[5],
                "category": row[6],
                "difficulty": row[7],
                "notes": row[8]
            })
    return logs


# ============== USER DOCUMENT QUERIES ==============

def save_user_document(email: str, filename: str, file_type: str, storage_path: str, 
                       text_hash: str = None, extracted_text: str = None) -> Optional[int]:
    """Save a user-uploaded document with extracted text for AI use."""
    result = False
    
    # Try with EXTRACTED_TEXT column first (if column exists in table)
    if extracted_text:
        query_with_text = """
        INSERT INTO USER_DOCUMENTS (EMAIL, FILE_NAME, FILE_TYPE, STORAGE_PATH, TEXT_HASH, EXTRACTED_TEXT)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        result = execute_write(query_with_text, (email, filename, file_type, storage_path, text_hash, extracted_text))
    
    # Fallback: try without EXTRACTED_TEXT column
    if not result:
        query_basic = """
        INSERT INTO USER_DOCUMENTS (EMAIL, FILE_NAME, FILE_TYPE, STORAGE_PATH, TEXT_HASH)
        VALUES (%s, %s, %s, %s, %s)
        """
        result = execute_write(query_basic, (email, filename, file_type, storage_path, text_hash))
    
    if result:
        invalidate_user_docs_cache(email)
        id_query = "SELECT MAX(DOC_ID) FROM USER_DOCUMENTS WHERE EMAIL = %s AND FILE_NAME = %s LIMIT 1"
        id_result = execute_query(id_query, (email, filename))
        if id_result and id_result[0]:
            return id_result[0][0]
    return None


def get_user_documents(email: str) -> List[Dict]:
    """Get all documents uploaded by a user - CACHED."""
    return cached_get_user_documents(email)


def delete_user_document(doc_id: int, email: str) -> bool:
    """Soft delete a user's document."""
    query = """
    UPDATE USER_DOCUMENTS SET IS_DELETED = TRUE
    WHERE DOC_ID = %s AND EMAIL = %s
    """
    result = execute_write(query, (doc_id, email))
    if result:
        invalidate_user_docs_cache(email)
    return result


# ============== ADMIN DOCUMENT QUERIES ==============

def save_admin_document(filename: str, file_type: str, storage_path: str, 
                        is_downloadable: bool = False, uploaded_by: str = "admin", 
                        text_hash: str = None, file_content: bytes = None, 
                        extracted_text: str = None, category: str = "General") -> Optional[int]:
    """Save an admin-uploaded reviewer document with file content."""
    import base64
    
    file_content_b64 = base64.b64encode(file_content).decode('utf-8') if file_content else None
    
    query = """
    INSERT INTO ADMIN_DOCUMENTS (FILE_NAME, FILE_TYPE, STORAGE_PATH, IS_DOWNLOADABLE, 
                                 UPLOADED_BY, TEXT_HASH, FILE_CONTENT, EXTRACTED_TEXT, CATEGORY)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    result = execute_write(query, (filename, file_type, storage_path, is_downloadable, 
                                   uploaded_by, text_hash, file_content_b64, extracted_text, category))
    if result:
        invalidate_admin_docs_cache()
        id_query = "SELECT MAX(ADMIN_DOC_ID) FROM ADMIN_DOCUMENTS WHERE FILE_NAME = %s LIMIT 1"
        id_result = execute_query(id_query, (filename,))
        if id_result and id_result[0]:
            return id_result[0][0]
    return None


def get_admin_documents() -> List[Dict]:
    """Get all admin reviewer documents - CACHED."""
    return cached_get_admin_documents()


def get_admin_document_content(doc_id: int) -> Optional[bytes]:
    """Get the file content of an admin document for download."""
    import base64
    
    query = """
    SELECT FILE_CONTENT, FILE_NAME, FILE_TYPE
    FROM ADMIN_DOCUMENTS 
    WHERE ADMIN_DOC_ID = %s AND IS_DELETED = FALSE
    LIMIT 1
    """
    result = execute_query(query, (doc_id,))
    if result and result[0] and result[0][0]:
        file_content_b64 = result[0][0]
        filename = result[0][1]
        file_type = result[0][2]
        try:
            file_bytes = base64.b64decode(file_content_b64)
            return {"content": file_bytes, "filename": filename, "file_type": file_type}
        except Exception:
            return None
    return None


def get_admin_document_text(doc_id: int) -> Optional[str]:
    """Get the extracted text from an admin document."""
    query = """
    SELECT EXTRACTED_TEXT, FILE_NAME
    FROM ADMIN_DOCUMENTS 
    WHERE ADMIN_DOC_ID = %s AND IS_DELETED = FALSE
    LIMIT 1
    """
    result = execute_query(query, (doc_id,))
    if result and result[0]:
        return {"text": result[0][0], "filename": result[0][1]}
    return None


def update_admin_document_downloadable(doc_id: int, is_downloadable: bool):
    """Update the downloadable status of an admin document."""
    query = """
    UPDATE ADMIN_DOCUMENTS 
    SET IS_DOWNLOADABLE = %s
    WHERE ADMIN_DOC_ID = %s
    """
    result = execute_write(query, (is_downloadable, doc_id))
    if result:
        invalidate_admin_docs_cache()
    return result


def delete_admin_document(doc_id: int) -> bool:
    """Soft delete an admin document."""
    query = """
    UPDATE ADMIN_DOCUMENTS SET IS_DELETED = TRUE
    WHERE ADMIN_DOC_ID = %s
    """
    result = execute_write(query, (doc_id,))
    if result:
        invalidate_admin_docs_cache()
    return result


# ============== PAYMENT QUERIES ==============

def create_payment(email: str, full_name: str, plan_requested: str, 
                   gcash_ref: str = None, receipt_storage_path: str = None) -> Optional[int]:
    """Create a new payment request."""
    query = """
    INSERT INTO PAYMENTS (FULL_NAME, EMAIL, GCASH_REF, PLAN_REQUESTED, RECEIPT_STORAGE_PATH, STATUS)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    result = execute_write(query, (full_name, email, gcash_ref, plan_requested, 
                                   receipt_storage_path or '', PAYMENT_PENDING))
    if result:
        id_query = "SELECT MAX(PAYMENT_ID) FROM PAYMENTS WHERE EMAIL = %s LIMIT 1"
        id_result = execute_query(id_query, (email,))
        if id_result and id_result[0]:
            return id_result[0][0]
    return None


def get_pending_payments() -> List[Dict]:
    """Get all pending payment requests - limited."""
    query = """
    SELECT PAYMENT_ID, FULL_NAME, EMAIL, GCASH_REF, PLAN_REQUESTED, 
           RECEIPT_STORAGE_PATH, SUBMITTED_AT, STATUS, ADMIN_NOTES
    FROM PAYMENTS
    WHERE STATUS = %s
    ORDER BY SUBMITTED_AT ASC
    LIMIT 50
    """
    result = execute_query(query, (PAYMENT_PENDING,))
    payments = []
    if result:
        for row in result:
            payments.append({
                "payment_id": row[0],
                "full_name": row[1],
                "email": row[2],
                "gcash_ref": row[3],
                "plan_requested": row[4],
                "receipt_storage_path": row[5],
                "created_at": row[6],
                "status": row[7],
                "admin_notes": row[8]
            })
    return payments


def get_all_payments(limit: int = 50) -> List[Dict]:
    """Get all payment requests for admin - limited."""
    query = """
    SELECT PAYMENT_ID, FULL_NAME, EMAIL, GCASH_REF, PLAN_REQUESTED, 
           RECEIPT_STORAGE_PATH, SUBMITTED_AT, STATUS, ADMIN_NOTES, APPROVED_AT, APPROVED_BY
    FROM PAYMENTS
    ORDER BY SUBMITTED_AT DESC
    LIMIT %s
    """
    result = execute_query(query, (limit,))
    payments = []
    if result:
        for row in result:
            payments.append({
                "payment_id": row[0],
                "full_name": row[1],
                "email": row[2],
                "gcash_ref": row[3],
                "plan_requested": row[4],
                "receipt_storage_path": row[5],
                "created_at": row[6],
                "status": row[7],
                "admin_notes": row[8],
                "approved_at": row[9],
                "approved_by": row[10]
            })
    return payments


def get_user_payments(email: str, limit: int = 10) -> List[Dict]:
    """Get all payments for a specific user - limited."""
    query = """
    SELECT PAYMENT_ID, FULL_NAME, EMAIL, GCASH_REF, PLAN_REQUESTED, 
           RECEIPT_STORAGE_PATH, SUBMITTED_AT, STATUS, ADMIN_NOTES
    FROM PAYMENTS 
    WHERE EMAIL = %s
    ORDER BY SUBMITTED_AT DESC
    LIMIT %s
    """
    result = execute_query(query, (email, limit))
    payments = []
    if result:
        for row in result:
            payments.append({
                "payment_id": row[0],
                "full_name": row[1],
                "email": row[2],
                "gcash_ref": row[3],
                "plan_requested": row[4],
                "receipt_storage_path": row[5],
                "created_at": row[6],
                "status": row[7],
                "admin_notes": row[8]
            })
    return payments


def approve_payment(payment_id: int, admin_notes: str = None, approved_by: str = "admin"):
    """Approve a payment request."""
    query = """
    UPDATE PAYMENTS 
    SET STATUS = %s, ADMIN_NOTES = %s, APPROVED_AT = CURRENT_TIMESTAMP(), APPROVED_BY = %s
    WHERE PAYMENT_ID = %s
    """
    return execute_write(query, (PAYMENT_APPROVED, admin_notes, approved_by, payment_id))


def reject_payment(payment_id: int, admin_notes: str = None, approved_by: str = "admin"):
    """Reject a payment request."""
    query = """
    UPDATE PAYMENTS 
    SET STATUS = %s, ADMIN_NOTES = %s, APPROVED_AT = CURRENT_TIMESTAMP(), APPROVED_BY = %s
    WHERE PAYMENT_ID = %s
    """
    return execute_write(query, (PAYMENT_REJECTED, admin_notes, approved_by, payment_id))


# ============== ADMIN ACTION QUERIES ==============

def log_admin_action(admin_user: str, action_type: str, details: str = None):
    """Log an admin action."""
    query = """
    INSERT INTO ADMIN_ACTIONS (ADMIN_USER, ACTION_TYPE, DETAILS)
    VALUES (%s, %s, %s)
    """
    return execute_write(query, (admin_user, action_type, details))


def get_admin_actions(limit: int = 50) -> List[Dict]:
    """Get admin actions for audit log - limited."""
    query = """
    SELECT ACTION_ID, ADMIN_USER, ACTION_TIME, ACTION_TYPE, DETAILS
    FROM ADMIN_ACTIONS
    ORDER BY ACTION_TIME DESC
    LIMIT %s
    """
    result = execute_query(query, (limit,))
    actions = []
    if result:
        for row in result:
            actions.append({
                "action_id": row[0],
                "admin_user": row[1],
                "action_time": row[2],
                "action_type": row[3],
                "details": row[4]
            })
    return actions
