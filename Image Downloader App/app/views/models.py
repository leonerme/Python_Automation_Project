from dataclasses import dataclass
from typing import List, Dict, Optional
from pathlib import Path
import json

@dataclass
class DownloadItem:
    """Represents a single download item with URL and optional filename"""
    url: str
    filename: Optional[str] = None
    error: Optional[str] = None

@dataclass
class DownloadBatch:
    """Represents a batch of downloads with common settings"""
    items: List[DownloadItem]
    output_dir: str
    batch_size: int = 5

@dataclass
class AppConfig:
    """Application configuration settings"""
    download_folder: str
    batch_size: int
    max_retries: int
    theme: str
    max_file_size: int  # In MB
    default_format: str  # 'original', 'jpeg', 'png', etc.
    
    @classmethod
    def from_json(cls, json_str: str) -> 'AppConfig':
        """Create config from JSON string"""
        data = json.loads(json_str)
        return cls(**data)
    
    def to_json(self) -> str:
        """Serialize config to JSON string"""
        return json.dumps(self.__dict__, indent=2)

@dataclass
class DownloadStats:
    """Tracks download statistics"""
    total: int = 0
    success: int = 0
    failed: int = 0
    skipped: int = 0
    
    def increment_success(self):
        self.success += 1
        self.total += 1
    
    def increment_failed(self):
        self.failed += 1
        self.total += 1
    
    def increment_skipped(self):
        self.skipped += 1
        self.total += 1

@dataclass 
class ImageConversionSettings:
    """Settings for image conversion"""
    output_format: str = 'jpeg'
    max_width: int = 1024
    max_height: int = 1024
    quality: int = 85
    preserve_metadata: bool = False

@dataclass
class CloudServiceAuth:
    """Authentication credentials for cloud services"""
    dropbox_token: Optional[str] = None
    google_drive_credentials: Optional[Dict] = None
    aws_keys: Optional[Dict] = None