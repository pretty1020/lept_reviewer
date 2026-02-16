-- =============================================
-- LEPT AI Reviewer - Supabase PostgreSQL Schema
-- Run this in Supabase SQL Editor to create all tables
-- =============================================

-- 1. USERS table
CREATE TABLE IF NOT EXISTS users (
    email VARCHAR(255) PRIMARY KEY,
    ip_address VARCHAR(50),
    plan_status VARCHAR(20) DEFAULT 'FREE',
    questions_used_total INTEGER DEFAULT 0,
    questions_remaining INTEGER DEFAULT 15,
    premium_expiry TIMESTAMP,
    is_blocked BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 2. USER_IP_HISTORY table
CREATE TABLE IF NOT EXISTS user_ip_history (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) REFERENCES users(email) ON DELETE CASCADE,
    ip_address VARCHAR(50),
    first_seen TIMESTAMP DEFAULT NOW(),
    last_seen TIMESTAMP DEFAULT NOW()
);

-- 3. IP_USAGE table
CREATE TABLE IF NOT EXISTS ip_usage (
    ip_address VARCHAR(50) PRIMARY KEY,
    questions_used_total INTEGER DEFAULT 0,
    is_blocked BOOLEAN DEFAULT FALSE,
    first_seen TIMESTAMP DEFAULT NOW(),
    last_seen TIMESTAMP DEFAULT NOW()
);

-- 4. USAGE_LOGS table
CREATE TABLE IF NOT EXISTS usage_logs (
    event_id SERIAL PRIMARY KEY,
    email VARCHAR(255),
    ip_address VARCHAR(50),
    event_time TIMESTAMP DEFAULT NOW(),
    questions_generated INTEGER DEFAULT 0,
    source_type VARCHAR(50),
    category VARCHAR(100),
    difficulty VARCHAR(20),
    notes TEXT
);

-- 5. USER_DOCUMENTS table
CREATE TABLE IF NOT EXISTS user_documents (
    doc_id SERIAL PRIMARY KEY,
    email VARCHAR(255),
    file_name VARCHAR(500),
    file_type VARCHAR(20),
    storage_path VARCHAR(1000),
    text_stage_path VARCHAR(1000),
    text_hash VARCHAR(64),
    extracted_text TEXT,
    is_deleted BOOLEAN DEFAULT FALSE,
    uploaded_at TIMESTAMP DEFAULT NOW()
);

-- 6. ADMIN_DOCUMENTS table
CREATE TABLE IF NOT EXISTS admin_documents (
    admin_doc_id SERIAL PRIMARY KEY,
    file_name VARCHAR(500),
    file_type VARCHAR(20),
    storage_path VARCHAR(1000),
    text_stage_path VARCHAR(1000),
    is_downloadable BOOLEAN DEFAULT FALSE,
    uploaded_by VARCHAR(255) DEFAULT 'admin',
    text_hash VARCHAR(64),
    file_content TEXT,
    extracted_text TEXT,
    category VARCHAR(100) DEFAULT 'General',
    is_deleted BOOLEAN DEFAULT FALSE,
    uploaded_at TIMESTAMP DEFAULT NOW()
);

-- 7. PAYMENTS table
CREATE TABLE IF NOT EXISTS payments (
    payment_id SERIAL PRIMARY KEY,
    full_name VARCHAR(255),
    email VARCHAR(255),
    gcash_ref VARCHAR(100),
    plan_requested VARCHAR(20),
    receipt_storage_path VARCHAR(1000),
    submitted_at TIMESTAMP DEFAULT NOW(),
    status VARCHAR(20) DEFAULT 'PENDING',
    admin_notes TEXT,
    approved_at TIMESTAMP,
    approved_by VARCHAR(255)
);

-- 8. ADMIN_ACTIONS table
CREATE TABLE IF NOT EXISTS admin_actions (
    action_id SERIAL PRIMARY KEY,
    admin_user VARCHAR(255),
    action_time TIMESTAMP DEFAULT NOW(),
    action_type VARCHAR(50),
    details TEXT
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_user_docs_email ON user_documents(email);
CREATE INDEX IF NOT EXISTS idx_usage_logs_email ON usage_logs(email);
CREATE INDEX IF NOT EXISTS idx_payments_email ON payments(email);
CREATE INDEX IF NOT EXISTS idx_payments_status ON payments(status);
CREATE INDEX IF NOT EXISTS idx_ip_history_email ON user_ip_history(email);
