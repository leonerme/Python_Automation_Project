from enum import Enum, auto
from pathlib import Path
import platform
import os

class FileType(Enum):
    """Supported file types for input data"""
    CSV = auto()
    EXCEL = auto()
    JSON = auto()

class ImageFormat(Enum):
    """Supported output image formats"""
    ORIGINAL = auto()
    JPEG = auto()
    PNG = auto()
    WEBP = auto()

# Application constants
APP_NAME = "Image Downloader"
APP_VERSION = "1.0.0"
ORGANIZATION_NAME = "ImageTools"
DEFAULT_CONFIG_FILENAME = "config.json"
SUPPORTED_INPUT_FORMATS = [".csv", ".xlsx", ".xls"]
SUPPORTED_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".webp", ".gif"]

# Network constants
MAX_RETRIES = 3
RETRY_DELAYS = [1, 2, 4]  # Seconds between retries (exponential backoff)
TIMEOUT = 30  # Seconds
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB in bytes
CHUNK_SIZE = 8192  # For streaming downloads

# UI constants
DEFAULT_THEME = "dark_teal"
THEMES = [
    "dark_teal",
    "dark_amber",
    "dark_cyan",
    "light_teal",
    "light_amber",
    "light_cyan"
]
MAX_THUMBNAIL_SIZE = 100  # pixels
MAX_PREVIEW_ROWS = 5
LOG_LINE_LIMIT = 1000  # Max lines in log window

# Platform-specific paths
if platform.system() == "Windows":
    CONFIG_DIR = Path(os.getenv('APPDATA')) / ORGANIZATION_NAME
else:
    CONFIG_DIR = Path.home() / ".config" / ORGANIZATION_NAME

DOWNLOADS_DIR = Path.home() / "Downloads"

# Cloud service constants
DROPBOX_DL_PARAM = "dl=1"
GOOGLE_DRIVE_BASE = "https://drive.google.com/uc?export=download"
AWS_S3_EXPIRY = 3600  # 1 hour for temporary URLs

# Error messages
ERROR_INVALID_URL = "Invalid URL format"
ERROR_FILE_TOO_LARGE = "File exceeds maximum size limit"
ERROR_UNSUPPORTED_TYPE = "Unsupported file type"
ERROR_NETWORK = "Network error occurred"
ERROR_AUTH_REQUIRED = "Authentication required"

# Status messages
STATUS_READY = "Ready"
STATUS_LOADING = "Loading file..."
STATUS_DOWNLOADING = "Downloading images..."
STATUS_COMPLETED = "Download completed"
STATUS_CANCELLED = "Download cancelled"

class LogLevel(Enum):
    """Logging level constants"""
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    DEBUG = "DEBUG"

# MIME type mappings
MIME_TO_EXTENSION = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
    "image/gif": ".gif"
}

# Magic numbers for image validation
IMAGE_MAGIC_NUMBERS = {
    b'\xFF\xD8\xFF': "JPEG",
    b'\x89PNG': "PNG",
    b'RIFF....WEBP': "WEBP",
    b'GIF8': "GIF"
}