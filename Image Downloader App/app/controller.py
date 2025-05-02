import os
import json
from typing import List, Dict, Optional
from pathlib import Path
from dataclasses import dataclass
from PyQt6.QtCore import QObject, pyqtSignal, QThread, QSettings
from PyQt6.QtWidgets import QApplication, QMessageBox
from .downloader import DownloadEngine, DownloadItem
from .views.main_window import MainWindow
from .models import AppConfig, DownloadBatch
from .utils import sanitize_filename, validate_url, convert_share_link

class ImageDownloaderApp(QObject):
    download_progress = pyqtSignal(int, int, str)  # current, total, filename
    download_complete = pyqtSignal(bool)  # success
    log_message = pyqtSignal(str, str)  # message, level (info/warning/error)

    def __init__(self):
        super().__init__()
        self.config = self.load_config()
        self.main_window = MainWindow(self)
        self.download_thread = None
        self.download_engine = None
        self.current_batch = None

    def load_config(self) -> AppConfig:
        """Load or create application configuration"""
        config_path = self.get_config_path()
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    return AppConfig(**json.load(f))
            except Exception as e:
                self.log_message.emit(f"Error loading config: {e}", "warning")
        
        # Return default config
        return AppConfig(
            download_folder=str(Path.home() / "Downloads"),
            batch_size=5,
            max_retries=3,
            theme="dark_teal",
            max_file_size=100,  # MB
            default_format="original"
        )

    def save_config(self):
        """Save current configuration to file"""
        config_path = self.get_config_path()
        try:
            with open(config_path, 'w') as f:
                json.dump(self.config.__dict__, f, indent=2)
        except Exception as e:
            self.log_message.emit(f"Error saving config: {e}", "error")

    def get_config_path(self) -> Path:
        """Get platform-specific config file path"""
        if os.name == 'nt':  # Windows
            base = Path(os.getenv('APPDATA'))
        elif os.name == 'posix':  # macOS/Linux
            base = Path.home() / '.config'
        else:
            base = Path.home()
        
        config_dir = base / "ImageDownloader"
        config_dir.mkdir(exist_ok=True)
        return config_dir / "config.json"

    def start_download(self, batch: DownloadBatch):
        """Start a download batch"""
        if self.download_thread and self.download_thread.isRunning():
            self.log_message.emit("A download is already in progress", "warning")
            return

        self.current_batch = batch
        self.download_engine = DownloadEngine(
            items=batch.items,
            output_dir=batch.output_dir,
            batch_size=batch.batch_size,
            max_retries=self.config.max_retries,
            max_file_size=self.config.max_file_size,
            convert_to=self.config.default_format
        )

        self.download_thread = QThread()
        self.download_engine.moveToThread(self.download_thread)

        # Connect signals
        self.download_engine.progress.connect(self.download_progress)
        self.download_engine.log.connect(self.log_message)
        self.download_engine.finished.connect(self.on_download_finished)
        self.download_engine.finished.connect(self.download_thread.quit)

        self.download_thread.started.connect(self.download_engine.start)
        self.download_thread.start()

    def cancel_download(self):
        """Cancel current download"""
        if self.download_engine:
            self.download_engine.cancel()
            self.log_message.emit("Download cancelled by user", "info")

    def on_download_finished(self, success: bool):
        """Handle download completion"""
        if success:
            self.log_message.emit("Download completed successfully", "info")
        else:
            self.log_message.emit("Download completed with errors", "warning")
        
        # Generate error report if needed
        if self.download_engine and self.download_engine.failed_items:
            self.generate_error_report()

    def generate_error_report(self):
        """Generate CSV report of failed downloads"""
        report_path = Path(self.current_batch.output_dir) / "download_errors.csv"
        try:
            with open(report_path, 'w') as f:
                f.write("URL,Filename,Error\n")
                for item in self.download_engine.failed_items:
                    f.write(f"{item.url},{item.filename},{item.error}\n")
            self.log_message.emit(f"Error report saved to {report_path}", "info")
        except Exception as e:
            self.log_message.emit(f"Failed to save error report: {e}", "error")

    def show_preview(self, data: List[Dict[str, str]]):
        """Show preview dialog with first 5 rows"""
        self.main_window.show_preview_dialog(data)

    def exit_app(self):
        """Handle application exit"""
        if self.download_thread and self.download_thread.isRunning():
            reply = QMessageBox.question(
                self.main_window,
                "Downloads in progress",
                "Downloads are still running. Are you sure you want to quit?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return False
        
        self.save_config()
        return True