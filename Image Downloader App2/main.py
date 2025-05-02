import sys
from PyQt6.QtWidgets import QApplication
from app import get_controller

def main():
    app = QApplication(sys.argv)
    
    # Get controller through the factory function
    downloader = get_controller()()
    downloader.main_window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()