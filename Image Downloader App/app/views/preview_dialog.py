from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QDialogButtonBox, QLabel
)
from PyQt6.QtCore import Qt

class PreviewDialog(QDialog):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Preview Data")
        self.setModal(True)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Add info label
        info_label = QLabel("Showing first 5 rows of data:")
        layout.addWidget(info_label)
        
        # Create table
        self.table = QTableWidget()
        self.table.setRowCount(min(5, len(data)))
        
        if data:
            headers = list(data[0].keys())
            self.table.setColumnCount(len(headers))
            
            # Set headers
            self.table.setHorizontalHeaderLabels(headers)
            
            # Populate data
            for row_idx, row_data in enumerate(data[:5]):
                for col_idx, (key, value) in enumerate(row_data.items()):
                    item = QTableWidgetItem(str(value))
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    self.table.setItem(row_idx, col_idx, item)
        
        layout.addWidget(self.table)
        
        # Add buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)