from dataclasses import dataclass

@dataclass
class AppState:
    """Shared application state"""
    is_downloading: bool = False
    current_progress: int = 0

# Other shared models and constants