"""
Views package initialization

Note: Don't import from controller here to avoid circular imports
"""

# Package version
__version__ = "1.0.0"

# Only import view-related components
from .main_window import MainWindow
from .preview_dialog import PreviewDialog
from .widgets import ThumbnailGrid

__all__ = [
    'MainWindow',
    'PreviewDialog',
    'ThumbnailGrid'
]