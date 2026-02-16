"""
LEPT AI Reviewer - Database Query Functions
OPTIMIZED: Uses cached queries for reads, invalidates cache on writes
Adapted for Supabase PostgreSQL
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
    SELECT email, ip_address, plan_status, questions_used_total, questions_remaining, 
           premium_expiry, is_blocked, created_at, updated_at
    FROM users 
    WHERE email = %s
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
    INSERT INTO users (email, ip_address, plan_status, questions_remaining)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (email) DO NOTHING
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
    UPDATE users 
    SET ip_address = %s, updated_at = NOW()
    WHERE email = %s
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
    UPDATE users 
    SET plan_status = %s, questions_remaining = %s, premium_expiry = %s, updated_at = NOW()
    WHERE email = %s
    """
    result = execute_write(query, (plan_type, questions_remaining, premium_expiry, email))
    if result:
        invalidate_user_cache(email)
    return result


def decrement_user_questions(email: str, count: int = 1) -> bool:
    """Decrement a user's remaining questions and increment total used."""
    query = """
    UPDATE users 
    SET questions_remaining = questions_remaining - %s,
        questions_used_total = questions_used_total + %s,
        updated_at = NOW()
    WHERE email = %s AND questions_remaining >= %s
    """
    result = execute_write(query, (count, count, email, count))
    if result:
        invalidate_user_cache(email)
    return result


def block_user(email: str, blocked: bool = True):
    """Block or unblock a user."""
    query = """
    UPDATE users 
    SET is_blocked = %s, updated_at = NOW()
    WHERE email = %s
    """
    result = execute_write(query, (blocked, email))
    if result:
        invalidate_user_cache(email)
    return result


def get_all_users(limit: int = 100) -> List[Dict]:
    """Get all users for admin panel - with limit, deduplicated by email."""
    query = """
    SELECT DISTINCT ON (email) email, ip_address, plan_status, questions_used_total, questions_remaining, 
           premium_expiry, is_blocked, created_at, updated_at
    FROM users
    ORDER BY email, updated_at DESC
    """
    result = execute_query(query)
    users = []
    if result:
        # Sort by created_at DESC after dedup and apply limit
        sorted_result = sorted(result, key=lambda r: r[7] or datetime.min, reverse=True)[:limit]
        for row in sorted_result:
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
    UPDATE users 
    SET questions_remaining = %s, updated_at = NOW()
    WHERE email = %s
    """
    result = execute_write(query, (new_quota, email))
    if result:
        invalidate_user_cache(email)
    return result


def delete_user(email: str) -> bool:
    """Delete a user and all related records."""
    execute_write("DELETE FROM user_ip_history WHERE email = %s", (email,))
    execute_write("DELETE FROM usage_logs WHERE email = %s", (email,))
    execute_write("DELETE FROM user_documents WHERE email = %s", (email,))
    execute_write("DELETE FROM payments WHERE email = %s", (email,))
    
    query = "DELETE FROM users WHERE email = %s"
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
    UPDATE users 
    SET plan_status = %s, questions_remaining = %s, premium_expiry = %s, updated_at = NOW()
    WHERE email = %s
    """
    result = execute_write(query, (new_plan, questions_remaining, premium_expiry, email))
    if result:
        invalidate_user_cache(email)
    return result


def check_premium_expiry(email: str) -> bool:
    """Check if premium has expired and revert to free if needed."""
    user = get_fresh_user_by_email(email)
    if user and user["plan_type"] == PLAN_PREMIUM:
        if user["premium_expiry"] and user["premium_expiry"] < datetime.now():
            update_user_plan(email, PLAN_FREE, 0, None)
            return True
    return False


# ============== IP TRACKING QUERIES ==============

def log_ip_history(email: str, ip_address: str):
    """Log IP address in user history."""
    check_query = "SELECT id FROM user_ip_history WHERE email = %s AND ip_address = %s LIMIT 1"
    existing = execute_query(check_query, (email, ip_address))
    
    if existing and len(existing) > 0:
        update_query = """
        UPDATE user_ip_history SET last_seen = NOW() 
        WHERE email = %s AND ip_address = %s
        """
        execute_write(update_query, (email, ip_address))
    else:
        insert_query = "INSERT INTO user_ip_history (email, ip_address) VALUES (%s, %s)"
        execute_write(insert_query, (email, ip_address))


def log_ip_usage(ip_address: str):
    """Log or update IP usage."""
    check_query = "SELECT ip_address FROM ip_usage WHERE ip_address = %s LIMIT 1"
    existing = execute_query(check_query, (ip_address,))
    
    if existing and len(existing) > 0:
        update_query = "UPDATE ip_usage SET last_seen = NOW() WHERE ip_address = %s"
        execute_write(update_query, (ip_address,))
    else:
        insert_query = "INSERT INTO ip_usage (ip_address) VALUES (%s)"
        execute_write(insert_query, (ip_address,))


def increment_ip_usage(ip_address: str, count: int = 1):
    """Increment questions used by IP."""
    query = """
    UPDATE ip_usage 
    SET questions_used_total = questions_used_total + %s, last_seen = NOW()
    WHERE ip_address = %s
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
    INSERT INTO usage_logs (email, ip_address, questions_generated, source_type, category, difficulty, notes)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    return execute_write(query, (email, ip_address, questions_generated, source_type, category, difficulty, notes))


def get_user_logs(email: str, limit: int = 20) -> List[Dict]:
    """Get usage logs for a specific user - limited."""
    query = """
    SELECT event_id, email, ip_address, event_time, questions_generated, source_type, category, difficulty, notes
    FROM usage_logs 
    WHERE email = %s
    ORDER BY event_time DESC
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
    SELECT event_id, email, ip_address, event_time, questions_generated, source_type, category, difficulty, notes
    FROM usage_logs
    ORDER BY event_time DESC
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
    query = """
    INSERT INTO user_documents (email, file_name, file_type, storage_path, text_hash, extracted_text)
    VALUES (%s, %s, %s, %s, %s, %s)
    RETURNING doc_id
    """
    result = execute_query(query, (email, filename, file_type, storage_path, text_hash, extracted_text), fetch=False)
    
    if result:
        invalidate_user_docs_cache(email)
        # Get the new doc_id
        id_query = "SELECT MAX(doc_id) FROM user_documents WHERE email = %s AND file_name = %s"
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
    UPDATE user_documents SET is_deleted = TRUE
    WHERE doc_id = %s AND email = %s
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
    INSERT INTO admin_documents (file_name, file_type, storage_path, is_downloadable, 
                                 uploaded_by, text_hash, file_content, extracted_text, category)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    result = execute_write(query, (filename, file_type, storage_path, is_downloadable, 
                                   uploaded_by, text_hash, file_content_b64, extracted_text, category))
    if result:
        invalidate_admin_docs_cache()
        id_query = "SELECT MAX(admin_doc_id) FROM admin_documents WHERE file_name = %s"
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
    SELECT file_content, file_name, file_type
    FROM admin_documents 
    WHERE admin_doc_id = %s AND is_deleted = FALSE
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
    SELECT extracted_text, file_name
    FROM admin_documents 
    WHERE admin_doc_id = %s AND is_deleted = FALSE
    LIMIT 1
    """
    result = execute_query(query, (doc_id,))
    if result and result[0]:
        return {"text": result[0][0], "filename": result[0][1]}
    return None


def update_admin_document_downloadable(doc_id: int, is_downloadable: bool):
    """Update the downloadable status of an admin document."""
    query = """
    UPDATE admin_documents 
    SET is_downloadable = %s
    WHERE admin_doc_id = %s
    """
    result = execute_write(query, (is_downloadable, doc_id))
    if result:
        invalidate_admin_docs_cache()
    return result


def delete_admin_document(doc_id: int) -> bool:
    """Soft delete an admin document."""
    query = """
    UPDATE admin_documents SET is_deleted = TRUE
    WHERE admin_doc_id = %s
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
    INSERT INTO payments (full_name, email, gcash_ref, plan_requested, receipt_storage_path, status)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    result = execute_write(query, (full_name, email, gcash_ref, plan_requested, 
                                   receipt_storage_path or '', PAYMENT_PENDING))
    if result:
        id_query = "SELECT MAX(payment_id) FROM payments WHERE email = %s"
        id_result = execute_query(id_query, (email,))
        if id_result and id_result[0]:
            return id_result[0][0]
    return None


def get_pending_payments() -> List[Dict]:
    """Get all pending payment requests - limited."""
    query = """
    SELECT payment_id, full_name, email, gcash_ref, plan_requested, 
           receipt_storage_path, submitted_at, status, admin_notes
    FROM payments
    WHERE status = %s
    ORDER BY submitted_at ASC
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
    SELECT payment_id, full_name, email, gcash_ref, plan_requested, 
           receipt_storage_path, submitted_at, status, admin_notes, approved_at, approved_by
    FROM payments
    ORDER BY submitted_at DESC
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
    SELECT payment_id, full_name, email, gcash_ref, plan_requested, 
           receipt_storage_path, submitted_at, status, admin_notes
    FROM payments 
    WHERE email = %s
    ORDER BY submitted_at DESC
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
    UPDATE payments 
    SET status = %s, admin_notes = %s, approved_at = NOW(), approved_by = %s
    WHERE payment_id = %s
    """
    return execute_write(query, (PAYMENT_APPROVED, admin_notes, approved_by, payment_id))


def reject_payment(payment_id: int, admin_notes: str = None, approved_by: str = "admin"):
    """Reject a payment request."""
    query = """
    UPDATE payments 
    SET status = %s, admin_notes = %s, approved_at = NOW(), approved_by = %s
    WHERE payment_id = %s
    """
    return execute_write(query, (PAYMENT_REJECTED, admin_notes, approved_by, payment_id))


# ============== ADMIN ACTION QUERIES ==============

def log_admin_action(admin_user: str, action_type: str, details: str = None):
    """Log an admin action."""
    query = """
    INSERT INTO admin_actions (admin_user, action_type, details)
    VALUES (%s, %s, %s)
    """
    return execute_write(query, (admin_user, action_type, details))


def get_admin_actions(limit: int = 50) -> List[Dict]:
    """Get admin actions for audit log - limited."""
    query = """
    SELECT action_id, admin_user, action_time, action_type, details
    FROM admin_actions
    ORDER BY action_time DESC
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
