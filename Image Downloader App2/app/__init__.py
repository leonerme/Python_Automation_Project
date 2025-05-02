"""
Image Downloader Application Package

This __init__.py file makes the 'app' directory a Python package.
"""

# Package version
__version__ = "1.0.0"

# Import only non-circular components
from .models import (
    DownloadItem,
    DownloadBatch,
    AppConfig
)

# Defer controller import to avoid circularity
def get_controller():
    from .controller import ImageDownloaderApp
    return ImageDownloaderApp

__all__ = [
    'get_controller',
    'DownloadItem',
    'DownloadBatch',
    'AppConfig'
]

# Package initialization
print(f"Initializing {__name__} {__version__}")