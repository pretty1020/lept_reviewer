"""
LEPT AI Reviewer - File Handling Utilities
"""

import os
import base64
from pathlib import Path
from typing import Optional, Tuple

from config.settings import ALLOWED_EXTENSIONS, MAX_FILE_SIZE_MB


def validate_file(uploaded_file) -> Tuple[bool, str]:
    """
    Validate an uploaded file.
    
    Args:
        uploaded_file: Streamlit UploadedFile object
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if uploaded_file is None:
        return False, "No file uploaded"
    
    # Check file extension
    filename = uploaded_file.name
    ext = Path(filename).suffix.lower()
    
    if ext not in ALLOWED_EXTENSIONS:
        return False, f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
    
    # Check file size
    file_size_mb = uploaded_file.size / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        return False, f"File too large. Maximum size: {MAX_FILE_SIZE_MB}MB"
    
    return True, ""


def get_file_extension(filename: str) -> str:
    """Get the file extension in lowercase."""
    return Path(filename).suffix.lower()


def encode_file_to_base64(file_bytes: bytes) -> str:
    """Encode file bytes to base64 string for storage."""
    return base64.b64encode(file_bytes).decode('utf-8')


def decode_base64_to_bytes(base64_string: str) -> bytes:
    """Decode base64 string back to bytes."""
    return base64.b64decode(base64_string)


def ensure_upload_directory(base_path: str = "uploads") -> str:
    """
    Ensure the upload directory exists.
    
    Args:
        base_path: Base directory path
    
    Returns:
        Full path to upload directory
    """
    upload_dir = Path(base_path)
    upload_dir.mkdir(parents=True, exist_ok=True)
    return str(upload_dir)


def save_uploaded_file(uploaded_file, user_id: str, base_path: str = "uploads") -> Optional[str]:
    """
    Save an uploaded file to disk.
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        user_id: User's ID for directory organization
        base_path: Base directory path
    
    Returns:
        Full path to saved file, or None if failed
    """
    try:
        # Create user-specific directory
        user_dir = Path(base_path) / user_id
        user_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate unique filename
        import uuid
        ext = get_file_extension(uploaded_file.name)
        unique_filename = f"{uuid.uuid4()}{ext}"
        file_path = user_dir / unique_filename
        
        # Save file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        return str(file_path)
    except Exception as e:
        print(f"Error saving file: {e}")
        return None


def delete_file(file_path: str) -> bool:
    """
    Delete a file from disk.
    
    Args:
        file_path: Path to the file
    
    Returns:
        True if deleted successfully, False otherwise
    """
    try:
        path = Path(file_path)
        if path.exists():
            path.unlink()
            return True
        return False
    except Exception as e:
        print(f"Error deleting file: {e}")
        return False


def get_file_icon(filename: str) -> str:
    """
    Get an appropriate icon for a file type.
    """
    ext = get_file_extension(filename)
    
    icons = {
        ".pdf": "📄",
        ".docx": "📝",
        ".doc": "📝",
        ".txt": "📃",
        ".png": "🖼️",
        ".jpg": "🖼️",
        ".jpeg": "🖼️"
    }
    
    return icons.get(ext, "📁")
