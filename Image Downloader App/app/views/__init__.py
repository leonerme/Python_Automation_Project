"""
Image Downloader Application Package

This __init__.py file makes the 'app' directory a Python package.
It can also be used to control package-level imports.
"""

# Package version
__version__ = "1.0.0"

# Package metadata
__author__ = "TTC"
__email__ = "leoner4848@gmail.com"
__license__ = "TTC License"
__status__ = "Development"

# Import key components to make them available at package level
from .models import (
    DownloadItem,
    DownloadBatch,
    AppConfig,
    DownloadStats,
    ImageConversionSettings,
    CloudServiceAuth
)

from ..controller import ImageDownloaderApp
from .main_window import MainWindow
from ..downloader import DownloadEngine

# Define what gets imported with 'from app import *'
__all__ = [
    'ImageDownloaderApp',
    'MainWindow',
    'DownloadEngine',
    'DownloadItem',
    'DownloadBatch',
    'AppConfig',
    'DownloadStats',
    'ImageConversionSettings',
    'CloudServiceAuth'
]

# Package initialization code (runs when package is imported)
print(f"Initializing Image Downloader {__version__}")

# You can add package-level configuration here if needed
CONFIG = {
    'default_theme': 'dark_teal',
    'max_workers': 5
}