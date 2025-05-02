from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QSize

class ThumbnailGrid(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.thumbnails = []
        self.max_columns = 5
        
    def add_thumbnail(self, image_path: str):
        """Add a thumbnail to the grid"""
        thumbnail = QLabel()
        thumbnail.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            # Scale the pixmap while keeping aspect ratio
            scaled = pixmap.scaled(
                QSize(100, 100),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            thumbnail.setPixmap(scaled)
            thumbnail.setToolTip(image_path)
            
            # Add to layout
            position = len(self.thumbnails)
            row = position // self.max_columns
            col = position % self.max_columns
            self.layout.addWidget(thumbnail, row, col)
            self.thumbnails.append(thumbnail)