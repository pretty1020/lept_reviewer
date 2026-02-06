"""
LEPT AI Reviewer - IP Address Utilities
"""

import streamlit as st
import requests


def get_client_ip() -> str:
    """
    Get the client's IP address.
    
    In Streamlit Cloud or behind a proxy, we try multiple methods:
    1. X-Forwarded-For header (when behind proxy/load balancer)
    2. External IP service (fallback)
    3. Default placeholder if all else fails
    
    Returns:
        Client IP address as string
    """
    # Try to get from Streamlit's experimental features if available
    try:
        # Check for headers in session state (if set by middleware)
        if "client_ip" in st.session_state:
            return st.session_state.client_ip
    except:
        pass
    
    # Try external IP service as fallback
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=5)
        if response.status_code == 200:
            ip = response.json().get("ip", "unknown")
            return ip
    except:
        pass
    
    # Try alternative service
    try:
        response = requests.get("https://ifconfig.me/ip", timeout=5)
        if response.status_code == 200:
            return response.text.strip()
    except:
        pass
    
    # Return placeholder if all methods fail
    return "unknown"


def mask_ip(ip: str) -> str:
    """
    Mask an IP address for display (privacy).
    Example: 192.168.1.100 -> 192.168.xxx.xxx
    """
    if not ip or ip == "unknown":
        return "unknown"
    
    parts = ip.split(".")
    if len(parts) == 4:
        return f"{parts[0]}.{parts[1]}.xxx.xxx"
    
    # For IPv6 or other formats
    return ip[:len(ip)//2] + "..."


def is_valid_ip(ip: str) -> bool:
    """
    Check if a string is a valid IP address.
    """
    if not ip or ip == "unknown":
        return False
    
    # Check IPv4
    parts = ip.split(".")
    if len(parts) == 4:
        try:
            for part in parts:
                num = int(part)
                if num < 0 or num > 255:
                    return False
            return True
        except ValueError:
            return False
    
    # Basic IPv6 check
    if ":" in ip:
        return True
    
    return False
