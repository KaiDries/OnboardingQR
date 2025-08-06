"""
Utility functions for AnyKrowd Onboarding QR Generator
"""

import re
import os
from typing import Tuple, Optional
from datetime import datetime


def clean_email_text(text: str) -> str:
    """
    Clean text for email generation by removing special characters
    
    Args:
        text: Input text to clean
        
    Returns:
        Cleaned text with only alphanumeric characters in lowercase
    """
    return re.sub(r'[^a-zA-Z0-9]', '', text).lower()


def parse_onboarding_name(onboarding_name: str) -> Tuple[str, str]:
    """
    Parse onboarding name to extract firstname and lastname
    
    Args:
        onboarding_name: Full onboarding name string
        
    Returns:
        Tuple of (firstname, lastname)
    """
    parts = onboarding_name.split(' | ')
    if len(parts) >= 2:
        return parts[0].strip(), parts[1].strip()
    else:
        return onboarding_name.strip(), ''


def generate_expected_email(firstname: str, lastname: str, domain: str) -> str:
    """
    Generate expected email address from name components
    
    Args:
        firstname: First name
        lastname: Last name  
        domain: Email domain
        
    Returns:
        Generated email address
    """
    firstname_clean = clean_email_text(firstname)
    lastname_clean = clean_email_text(lastname)
    return f"{firstname_clean}{lastname_clean}@{domain}"


def ensure_directory_exists(directory_path: str) -> None:
    """
    Ensure a directory exists, create if it doesn't
    
    Args:
        directory_path: Path to directory
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def format_timestamp() -> str:
    """
    Get current timestamp in Dutch format
    
    Returns:
        Formatted timestamp string
    """
    return datetime.now().strftime("%d/%m/%Y %H:%M")


def validate_whatsapp_url(url: str) -> bool:
    """
    Validate WhatsApp URL format
    
    Args:
        url: WhatsApp URL to validate
        
    Returns:
        True if valid WhatsApp URL
    """
    if not url:
        return False
        
    whatsapp_patterns = [
        r'^https://chat\.whatsapp\.com/',
        r'^https://wa\.me/',
        r'^whatsapp://send'
    ]
    
    return any(re.match(pattern, url) for pattern in whatsapp_patterns)


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human readable format
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename safe for filesystem
    """
    # Remove invalid characters for Windows/Linux filesystems
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Remove extra spaces and dots
    filename = re.sub(r'\s+', '_', filename)
    filename = re.sub(r'\.+', '.', filename)
    
    return filename.strip('._')


def get_tenant_variable_name(tenant_id: int) -> str:
    """
    Generate tenant variable name format
    
    Args:
        tenant_id: Tenant ID number
        
    Returns:
        Formatted tenant variable name
    """
    return f"tenant-{tenant_id}"


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate text to maximum length with suffix
    
    Args:
        text: Text to truncate
        max_length: Maximum allowed length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix
