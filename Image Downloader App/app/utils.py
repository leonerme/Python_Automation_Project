import os
import re
import mimetypes
from urllib.parse import urlparse
from pathlib import Path
from typing import Optional, Tuple
import requests

def validate_url(url: str) -> bool:
    """Validate that URL is properly formatted and uses allowed schemes"""
    try:
        result = urlparse(url)
        return all([result.scheme in ('http', 'https'), result.netloc])
    except ValueError:
        return False

def convert_share_link(url: str) -> Optional[str]:
    """Convert cloud service share links to direct download links"""
    # Dropbox
    if 'dropbox.com' in url:
        if 'dl=0' in url:
            return url.replace('dl=0', 'dl=1')
        if '?' in url:
            return f"{url}&dl=1"
        return f"{url}?dl=1"
    
    # Google Drive
    if 'drive.google.com' in url:
        file_id = None
        if '/file/d/' in url:
            file_id = url.split('/file/d/')[1].split('/')[0]
        elif 'id=' in url:
            file_id = url.split('id=')[1].split('&')[0]
        
        if file_id:
            return f"https://drive.google.com/uc?export=download&id={file_id}"
    
    # Return original URL if not a known share link
    return url if validate_url(url) else None

def sanitize_filename(filename: str) -> str:
    """Sanitize filename by removing invalid characters"""
    # Replace invalid characters with underscore
    filename = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', filename)
    # Remove leading/trailing spaces and dots
    filename = filename.strip(' .')
    # Ensure filename is not empty
    if not filename:
        filename = "unnamed"
    return filename

def get_extension_from_url(url: str) -> Optional[str]:
    """Try to get file extension from URL"""
    # Try from URL path
    path = urlparse(url).path
    ext = Path(path).suffix.lower()
    if ext:
        return ext[1:]  # Remove leading dot
    
    # Try from content type if available
    try:
        response = requests.head(url, timeout=5, allow_redirects=True)
        content_type = response.headers.get('content-type', '').split(';')[0]
        return mimetypes.guess_extension(content_type)
    except:
        return None

def is_valid_image(content_type: str, first_bytes: bytes) -> bool:
    """Check if content appears to be a valid image"""
    # Check content type
    image_types = ['image/jpeg', 'image/png', 'image/webp', 'image/gif']
    if content_type.lower() in image_types:
        return True
    
    # Check magic numbers
    magic_numbers = {
        b'\xFF\xD8\xFF': 'jpg',
        b'\x89PNG': 'png',
        b'RIFF....WEBP': 'webp',
        b'GIF8': 'gif'
    }
    
    for magic, _ in magic_numbers.items():
        if first_bytes.startswith(magic):
            return True
    
    return False