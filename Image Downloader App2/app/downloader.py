import os
import time
import requests
from typing import List, Optional
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from PyQt6.QtCore import QObject, pyqtSignal, QRunnable, QThreadPool
from .models import DownloadItem
from .utils import (
    validate_url,
    convert_share_link,
    sanitize_filename,
    get_extension_from_url,
    is_valid_image
)

class DownloadEngine(QObject):
    progress = pyqtSignal(int, int, str)  # current, total, filename
    log = pyqtSignal(str, str)  # message, level
    finished = pyqtSignal(bool)  # success

    def __init__(
        self,
        items: List[DownloadItem],
        output_dir: str,
        batch_size: int = 5,
        max_retries: int = 3,
        max_file_size: int = 100,  # MB
        convert_to: str = "original"
    ):
        super().__init__()
        self.items = items
        self.output_dir = output_dir
        self.batch_size = batch_size
        self.max_retries = max_retries
        self.max_file_size = max_file_size * 1024 * 1024  # Convert to bytes
        self.convert_to = convert_to
        self._cancel = False
        self.failed_items = []
        self.thread_pool = QThreadPool.globalInstance()

    def start(self):
        """Start the download process"""
        try:
            os.makedirs(self.output_dir, exist_ok=True)
            self._download_all()
            self.finished.emit(len(self.failed_items) == 0)
        except Exception as e:
            self.log.emit(f"Download failed: {str(e)}", "error")
            self.finished.emit(False)

    def cancel(self):
        """Cancel the download process"""
        self._cancel = True
        self.log.emit("Cancelling download...", "info")

    def _download_all(self):
        """Download all items in batches"""
        total = len(self.items)
        completed = 0
        self.failed_items = []

        with ThreadPoolExecutor(max_workers=self.batch_size) as executor:
            futures = {
                executor.submit(self._download_item, item): item
                for item in self.items
            }

            for future in as_completed(futures):
                if self._cancel:
                    break

                item = futures[future]
                try:
                    result = future.result()
                    if result:
                        completed += 1
                        self.progress.emit(completed, total, item.filename)
                    else:
                        self.failed_items.append(item)
                except Exception as e:
                    self.log.emit(f"Error processing {item.url}: {str(e)}", "error")
                    item.error = str(e)
                    self.failed_items.append(item)

    def _download_item(self, item: DownloadItem) -> bool:
        """Download a single item with retry logic"""
        for attempt in range(self.max_retries + 1):
            if self._cancel:
                return False

            try:
                # Convert share links to direct download links
                direct_url = convert_share_link(item.url)
                if not direct_url:
                    item.error = "Invalid URL or unsupported cloud service"
                    return False

                # Validate URL
                if not validate_url(direct_url):
                    item.error = "Invalid URL"
                    return False

                # Get filename if not provided
                if not item.filename:
                    item.filename = self._generate_filename(direct_url)

                # Check for file existence and handle collisions
                filepath = self._get_unique_filepath(item.filename)

                # Download with streaming to handle large files
                with requests.get(direct_url, stream=True, timeout=30) as response:
                    response.raise_for_status()

                    # Check file size
                    content_length = int(response.headers.get('content-length', 0))
                    if content_length > self.max_file_size:
                        item.error = f"File too large ({content_length/1024/1024:.1f}MB > {self.max_file_size/1024/1024:.1f}MB)"
                        return False

                    # Check if it's actually an image
                    if not is_valid_image(response.headers.get('content-type', ''), response.content[:1024]):
                        item.error = "URL does not point to a valid image"
                        return False

                    # Stream download
                    with open(filepath, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if self._cancel:
                                return False
                            if chunk:
                                f.write(chunk)

                # If we need to convert the image
                if self.convert_to != "original":
                    self._convert_image(filepath)

                self.log.emit(f"Downloaded {item.filename}", "info")
                return True

            except Exception as e:
                if attempt < self.max_retries:
                    wait_time = 2 ** attempt  # Exponential backoff
                    self.log.emit(
                        f"Attempt {attempt + 1} failed for {item.url}. Retrying in {wait_time}s...",
                        "warning"
                    )
                    time.sleep(wait_time)
                else:
                    item.error = str(e)
                    self.log.emit(
                        f"Failed to download {item.url} after {self.max_retries} attempts: {str(e)}",
                        "error"
                    )
                    return False

        return False

    def _generate_filename(self, url: str) -> str:
        """Generate a filename from URL"""
        # Extract filename from URL
        filename = url.split('/')[-1].split('?')[0]
        
        # If no extension or invalid, try to get from content type
        ext = get_extension_from_url(url)
        if not filename.endswith(ext):
            filename = f"{filename}.{ext}" if ext else f"{filename}.jpg"
        
        return sanitize_filename(filename)

    def _get_unique_filepath(self, filename: str) -> str:
        """Handle filename collisions by adding counters"""
        base, ext = os.path.splitext(filename)
        counter = 1
        filepath = os.path.join(self.output_dir, filename)
        
        while os.path.exists(filepath):
            filepath = os.path.join(self.output_dir, f"{base}_{counter}{ext}")
            counter += 1
            
        return filepath

    def _convert_image(self, filepath: str):
        """Convert image to specified format if needed"""
        # Implementation would use PIL/Pillow to convert formats
        # This is a placeholder for the actual conversion logic
        if self.convert_to == "jpeg":
            pass  # Convert to JPEG
        elif self.convert_to == "png":
            pass  # Convert to PNG
        # etc.