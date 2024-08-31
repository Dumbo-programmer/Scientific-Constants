import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, 
    QHBoxLayout, QMessageBox, QTableWidget, QTableWidgetItem, QComboBox, 
    QStackedWidget, QTextEdit, QGroupBox, QGridLayout, QCheckBox, QColorDialog, QFileDialog
)
from PyQt5.QtGui import QIcon, QColor, QPalette
from PyQt5.QtCore import Qt

# Dictionary of scientific constants
CONSTANTS = {
    'Physics': {
        'Speed of Light (c)': {
            'value': '299,792,458 m/s',
            'description': 'The speed at which light propagates through a vacuum.'
        },
        'Gravitational Constant (G)': {
            'value': '6.67430 × 10^-11 m^3 kg^-1 s^-2',
            'description': 'The fundamental constant that determines the strength of gravitational force.'
        },
        'Planck Constant (h)': {
            'value': '6.62607015 × 10^-34 J s',
            'description': 'A fundamental constant that relates the energy of a photon to its frequency.'
        }
    },
    'Chemistry': {
        'Avogadro Constant (NA)': {
            'value': '6.02214076 × 10^23 mol^-1',
            'description': 'The number of constituent particles (usually atoms or molecules) in one mole of a substance.'
        },
        'Boltzmann Constant (kB)': {
            'value': '1.380649 × 10^-23 J K^-1',
            'description': 'Relates the average kinetic energy of particles in a gas with the temperature of the gas.'
        },
        'Gas Constant (R)': {
            'value': '8.314462618 J mol^-1 K^-1',
            'description': 'The constant used in the ideal gas law, relating pressure, volume, and temperature.'
        }
    }
}

class ConstantsViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Advanced Scientific Constants Viewer')
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon('icon.png'))  # Use a valid icon path if available
        
        # Main layout
        main_layout = QVBoxLayout()

        # Dropdown to select category
        self.category_box = QComboBox(self)
        self.category_box.addItems(CONSTANTS.keys())
        self.category_box.currentIndexChanged.connect(self.update_table)
        
        # Search bar
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search for a constant...")
        self.search_bar.textChanged.connect(self.update_table)

        # Table for displaying constants
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(['Constant', 'Value'])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.itemSelectionChanged.connect(self.show_constant_details)

        # Text edit for displaying constant details
        self.details_box = QTextEdit(self)
        self.details_box.setReadOnly(True)
        self.details_box.setPlaceholderText("Select a constant to view details...")

        # Copy button
        self.copy_button = QPushButton('Copy Selected Constant', self)
        self.copy_button.clicked.connect(self.copy_constant)

        # History button
        self.history_button = QPushButton('View Copy History', self)
        self.history_button.clicked.connect(self.view_history)

        # Export button
        self.export_button = QPushButton('Export Constants', self)
        self.export_button.clicked.connect(self.export_constants)

        # Theme button
        self.theme_button = QPushButton('Change Theme', self)
        self.theme_button.clicked.connect(self.change_theme)

        # Layout arrangement
        control_layout = QHBoxLayout()
        control_layout.addWidget(self.category_box)
        control_layout.addWidget(self.search_bar)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.copy_button)
        button_layout.addWidget(self.history_button)
        button_layout.addWidget(self.export_button)
        button_layout.addWidget(self.theme_button)

        main_layout.addLayout(control_layout)
        main_layout.addWidget(self.table)
        main_layout.addWidget(self.details_box)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        # Variables to store history
        self.copy_history = []

        # Populate the table initially
        self.update_table()

    def update_table(self):
        # Clear the table
        self.table.setRowCount(0)
        
        # Get the selected category and search query
        selected_category = self.category_box.currentText()
        search_query = self.search_bar.text().lower()

        # Populate the table with constants that match the search query
        constants_in_category = CONSTANTS[selected_category]
        for constant, data in constants_in_category.items():
            if search_query in constant.lower():
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                self.table.setItem(row_position, 0, QTableWidgetItem(constant))
                self.table.setItem(row_position, 1, QTableWidgetItem(data['value']))

    def show_constant_details(self):
        # Display details of the selected constant
        selected_items = self.table.selectedItems()
        if selected_items:
            constant_name = selected_items[0].text()
            category = self.category_box.currentText()
            description = CONSTANTS[category][constant_name]['description']
            value = CONSTANTS[category][constant_name]['value']
            details = f"**{constant_name}**\n\n**Value**: {value}\n\n**Description**: {description}"
            self.details_box.setText(details)
        else:
            self.details_box.clear()

    def copy_constant(self):
        # Get selected constant value
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "No constant selected. Please select a constant to copy.")
            return
        
        # Get value and copy to clipboard
        value_item = selected_items[1]
        constant_value = value_item.text()
        clipboard = QApplication.clipboard()
        clipboard.setText(constant_value)
        QMessageBox.information(self, "Copied", f"Copied to clipboard: {constant_value}")
        
        # Add to history
        self.copy_history.append(constant_value)

    def view_history(self):
        # Show copy history
        if not self.copy_history:
            QMessageBox.information(self, "Copy History", "No constants have been copied yet.")
            return
        
        history_text = "\n".join(self.copy_history)
        QMessageBox.information(self, "Copy History", f"Copy History:\n\n{history_text}")

    def export_constants(self):
        # Export the constants to a text file
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getSaveFileName(self, "Export Constants", "", "Text Files (*.txt);;All Files (*)")
        
        if file_path:
            with open(file_path, 'w') as file:
                for category, constants in CONSTANTS.items():
                    file.write(f"{category}:\n")
                    for constant, data in constants.items():
                        file.write(f"  {constant}: {data['value']}\n")
                    file.write("\n")
            QMessageBox.information(self, "Export Successful", f"Constants exported to {file_path}")

    def change_theme(self):
        # Open color dialog to change theme
        color = QColorDialog.getColor()
        if color.isValid():
            palette = self.palette()
            palette.setColor(QPalette.Window, color)
            self.setPalette(palette)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = ConstantsViewer()
    viewer.show()
    sys.exit(app.exec_())
