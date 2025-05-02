import sys
from PyQt6.QtWidgets import QApplication
from app.controller import ImageDownloaderApp

def main():
    app = QApplication(sys.argv)
    
    # Create and show the main application
    downloader = ImageDownloaderApp()
    downloader.main_window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()