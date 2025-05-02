from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit, 
    QProgressBar, QMenuBar, QMenu, QFileDialog, QStatusBar, QLabel,
    QHBoxLayout, QScrollArea, QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction, QTextCursor, QPixmap
from qt_material import apply_stylesheet
from .models import DownloadBatch
from .preview_dialog import PreviewDialog
from .widgets import ThumbnailGrid

class MainWindow(QMainWindow):
    start_download = pyqtSignal(DownloadBatch)
    cancel_download = pyqtSignal()
    load_file = pyqtSignal(str)

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Image Downloader")
        self.setGeometry(100, 100, 800, 600)
        
        # Apply material theme
        apply_stylesheet(self, theme='dark_teal.xml')
        
        self._setup_ui()
        self._connect_signals()
        
        # Initialize state
        self.download_in_progress = False
        self.current_file = None

    def _setup_ui(self):
        """Setup the main window UI"""
        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Menu bar
        self._setup_menu_bar()
        
        # File selection area
        self.file_label = QLabel("No file selected")
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.file_label)
        
        # Thumbnail preview area
        self.thumbnail_grid = ThumbnailGrid()
        thumbnail_scroll = QScrollArea()
        thumbnail_scroll.setWidgetResizable(True)
        thumbnail_scroll.setWidget(self.thumbnail_grid)
        layout.addWidget(thumbnail_scroll)
        
        # Log area
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setFontFamily("Courier New")
        layout.addWidget(self.log_area)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setTextVisible(True)
        layout.addWidget(self.progress_bar)
        
        # Button area
        button_layout = QHBoxLayout()
        
        self.start_button = QPushButton("Start Download")
        self.start_button.setEnabled(False)
        button_layout.addWidget(self.start_button)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setEnabled(False)
        button_layout.addWidget(self.cancel_button)
        
        self.clear_button = QPushButton("Clear Log")
        button_layout.addWidget(self.clear_button)
        
        layout.addLayout(button_layout)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

    def _setup_menu_bar(self):
        """Setup the menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        open_action = QAction("Open...", self)
        open_action.triggered.connect(self._on_open_file)
        file_menu.addAction(open_action)
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Settings menu
        settings_menu = menubar.addMenu("Settings")
        
        theme_menu = settings_menu.addMenu("Theme")
        dark_action = QAction("Dark", self)
        light_action = QAction("Light", self)
        theme_menu.addAction(dark_action)
        theme_menu.addAction(light_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        about_action = QAction("About", self)
        help_menu.addAction(about_action)

    def _connect_signals(self):
        """Connect UI signals to slots"""
        self.start_button.clicked.connect(self._on_start_download)
        self.cancel_button.clicked.connect(self.cancel_download.emit)
        self.clear_button.clicked.connect(self.log_area.clear)
        
        # Connect controller signals
        self.controller.download_progress.connect(self._update_progress)
        self.controller.download_complete.connect(self._on_download_complete)
        self.controller.log_message.connect(self._log_message)

    def _on_open_file(self):
        """Handle file open action"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Data File",
            "",
            "Data Files (*.csv *.xlsx *.xls);;All Files (*)"
        )
        
        if file_path:
            self.load_file.emit(file_path)
            self.current_file = file_path
            self.file_label.setText(f"Selected: {file_path}")
            self.status_bar.showMessage(f"Loaded {file_path}")

    def _on_start_download(self):
        """Handle start download button click"""
        if not hasattr(self, 'current_batch'):
            return
            
        # Get download folder
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Download Folder",
            self.controller.config.download_folder
        )
        
        if folder:
            self.current_batch.output_dir = folder
            self.start_download.emit(self.current_batch)
            self._set_download_ui_state(True)
            self.status_bar.showMessage("Downloading...")

    def _on_download_complete(self, success: bool):
        """Handle download completion"""
        self._set_download_ui_state(False)
        if success:
            self.status_bar.showMessage("Download completed successfully")
        else:
            self.status_bar.showMessage("Download completed with errors")

    def _set_download_ui_state(self, downloading: bool):
        """Update UI state based on download status"""
        self.download_in_progress = downloading
        self.start_button.setEnabled(not downloading)
        self.cancel_button.setEnabled(downloading)
        
        if not downloading:
            self.progress_bar.reset()

    def _update_progress(self, current: int, total: int, filename: str):
        """Update progress bar and status"""
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(current)
        self.status_bar.showMessage(f"Downloading {filename} ({current}/{total})")

    def _log_message(self, message: str, level: str = "info"):
        """Add a message to the log area with appropriate formatting"""
        if level == "error":
            formatted = f"[ERROR] {message}"
            self.log_area.setTextColor(Qt.GlobalColor.red)
        elif level == "warning":
            formatted = f"[WARNING] {message}"
            self.log_area.setTextColor(Qt.GlobalColor.yellow)
        else:
            formatted = f"[INFO] {message}"
            self.log_area.setTextColor(Qt.GlobalColor.white)
        
        self.log_area.append(formatted)
        self.log_area.moveCursor(QTextCursor.MoveOperation.End)
        
    def show_preview_dialog(self, data: list):
        """Show the preview dialog with data"""
        dialog = PreviewDialog(data, self)
        if dialog.exec() == PreviewDialog.DialogCode.Accepted:
            # Create download batch from preview data
            items = [
                DownloadItem(url=row['url'], filename=row.get('filename'))
                for row in data
            ]
            self.current_batch = DownloadBatch(
                items=items,
                output_dir=self.controller.config.download_folder,
                batch_size=self.controller.config.batch_size
            )
            self.start_button.setEnabled(True)
            self.status_bar.showMessage("Ready to download")

    def closeEvent(self, event):
        """Handle window close event"""
        if self.download_in_progress:
            reply = QMessageBox.question(
                self,
                "Download in progress",
                "A download is currently running. Are you sure you want to quit?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                event.ignore()
                return
        
        self.controller.exit_app()
        event.accept()