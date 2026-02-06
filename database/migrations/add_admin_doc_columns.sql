-- Migration: Add FILE_CONTENT, EXTRACTED_TEXT, and CATEGORY columns to ADMIN_DOCUMENTS
-- Run this in Snowflake to enable document storage and AI question generation

-- Add FILE_CONTENT column to store base64 encoded file content
ALTER TABLE APP.ADMIN_DOCUMENTS 
ADD COLUMN IF NOT EXISTS FILE_CONTENT VARCHAR(16777216);

-- Add EXTRACTED_TEXT column to store extracted text from documents
ALTER TABLE APP.ADMIN_DOCUMENTS 
ADD COLUMN IF NOT EXISTS EXTRACTED_TEXT VARCHAR(16777216);

-- Add CATEGORY column for document categorization
ALTER TABLE APP.ADMIN_DOCUMENTS 
ADD COLUMN IF NOT EXISTS CATEGORY VARCHAR(100) DEFAULT 'General';

-- Verify the changes
DESCRIBE TABLE APP.ADMIN_DOCUMENTS;
