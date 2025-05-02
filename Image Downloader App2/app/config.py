import json
import os
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass, asdict

@dataclass
class AppConfig:
    """
    Application configuration settings with default values.
    """
    download_folder: str = str(Path.home() / "Downloads")
    batch_size: int = 5
    max_retries: int = 3
    theme: str = "dark_teal"
    max_file_size: int = 100  # MB
    default_format: str = "original"  # 'original', 'jpeg', 'png', 'webp'
    last_used_file: Optional[str] = None
    window_geometry: Optional[Dict[str, int]] = None
    auth_tokens: Dict[str, str] = None  # For cloud service authentication

    def __post_init__(self):
        if self.auth_tokens is None:
            self.auth_tokens = {}

class ConfigManager:
    """
    Manages loading and saving application configuration to JSON file.
    """
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file or self.get_default_config_path()
        self.config = self.load_or_create()

    @staticmethod
    def get_default_config_path() -> Path:
        """Get platform-specific config file path"""
        if os.name == 'nt':  # Windows
            base = Path(os.getenv('APPDATA'))
        elif os.name == 'posix':  # macOS/Linux
            base = Path.home() / '.config'
        else:
            base = Path.home()
        
        config_dir = base / "ImageDownloader"
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir / "config.json"

    def load_or_create(self) -> AppConfig:
        """Load config from file or create with defaults if doesn't exist"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    return AppConfig(**data)
        except Exception as e:
            print(f"Error loading config: {e}. Using defaults.")
        
        # Return default config if file doesn't exist or is invalid
        return AppConfig()

    def save(self):
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(asdict(self.config), f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")

    def update(self, **kwargs):
        """Update configuration values"""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
        self.save()

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value"""
        return getattr(self.config, key, default)

# Example usage:
if __name__ == "__main__":
    # Initialize config manager
    config_manager = ConfigManager()
    
    # Access configuration
    print(f"Current download folder: {config_manager.config.download_folder}")
    
    # Update configuration
    config_manager.update(download_folder="/new/download/path", batch_size=10)
    
    # Save configuration
    config_manager.save()