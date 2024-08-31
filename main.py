import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QMessageBox, QTableWidget, QTableWidgetItem, QComboBox,
    QStackedWidget, QTextEdit, QGroupBox, QGridLayout, QCheckBox, QColorDialog, 
    QFileDialog, QDialog, QFormLayout, QSpinBox, QSlider, QMenuBar, QAction
)
from PyQt5.QtGui import QIcon, QColor, QPalette
from PyQt5.QtCore import Qt

# Dictionary of scientific constants
CONSTANTS = {
    'Physics': {
        'Speed of Light (c)': {
            'value': '299,792,458 m/s',
            'description': 'The speed at which light propagates through a vacuum.',
            'history': [299792458, 299792450, 299792460],  # Example historical data
        },
        'Gravitational Constant (G)': {
            'value': '6.67430 × 10^-11 m^3 kg^-1 s^-2',
            'description': 'The fundamental constant that determines the strength of gravitational force.',
            'history': [6.67430e-11, 6.67428e-11, 6.67435e-11],
        },
        'Planck Constant (h)': {
            'value': '6.62607015 × 10^-34 J s',
            'description': 'A fundamental constant that relates the energy of a photon to its frequency.',
            'history': [6.62607015e-34, 6.626068e-34, 6.626070e-34],
        }
    },
    'Chemistry': {
        'Avogadro Constant (NA)': {
            'value': '6.02214076 × 10^23 mol^-1',
            'description': 'The number of constituent particles (usually atoms or molecules) in one mole of a substance.',
            'history': [6.02214076e23, 6.0221367e23, 6.022136e23],
        },
        'Boltzmann Constant (kB)': {
            'value': '1.380649 × 10^-23 J K^-1',
            'description': 'Relates the average kinetic energy of particles in a gas with the temperature of the gas.',
            'history': [1.380649e-23, 1.38064852e-23, 1.38064878e-23],
        },
        'Gas Constant (R)': {
            'value': '8.314462618 J mol^-1 K^-1',
            'description': 'The constant used in the ideal gas law, relating pressure, volume, and temperature.',
            'history': [8.314462618, 8.3144621, 8.31447],
        }
    }
}

class ConstantsViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Advanced Scientific Constants Viewer')
        self.setGeometry(100, 100, 1000, 800)
        self.setWindowIcon(QIcon('icon.png'))  # Use a valid icon path if available

        # Menu bar
        self.menu_bar = QMenuBar(self)
        self.file_menu = self.menu_bar.addMenu('File')
        self.import_action = QAction('Import Custom Constants', self)
        self.export_action = QAction('Export Custom Constants', self)
        self.file_menu.addAction(self.import_action)
        self.file_menu.addAction(self.export_action)

        self.import_action.triggered.connect(self.import_constants)
        self.export_action.triggered.connect(self.export_constants)

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

        # Buttons for features
        self.copy_button = QPushButton('Copy Selected Constant', self)
        self.copy_button.clicked.connect(self.copy_constant)

        self.history_button = QPushButton('View Copy History', self)
        self.history_button.clicked.connect(self.view_history)

        self.export_button = QPushButton('Export Constants', self)
        self.export_button.clicked.connect(self.export_constants)

        self.theme_button = QPushButton('Change Theme', self)
        self.theme_button.clicked.connect(self.change_theme)

        self.add_custom_button = QPushButton('Add Custom Constant', self)
        self.add_custom_button.clicked.connect(self.add_custom_constant)

        self.unit_convert_button = QPushButton('Unit Conversion', self)
        self.unit_convert_button.clicked.connect(self.unit_conversion)

        self.language_button = QPushButton('Change Language', self)
        self.language_button.clicked.connect(self.change_language)

        self.graph_button = QPushButton('Show History Graph', self)
        self.graph_button.clicked.connect(self.show_history_graph)

        # Layout arrangement
        control_layout = QHBoxLayout()
        control_layout.addWidget(self.category_box)
        control_layout.addWidget(self.search_bar)

        button_layout = QGridLayout()
        button_layout.addWidget(self.copy_button, 0, 0)
        button_layout.addWidget(self.history_button, 0, 1)
        button_layout.addWidget(self.export_button, 0, 2)
        button_layout.addWidget(self.theme_button, 0, 3)
        button_layout.addWidget(self.add_custom_button, 1, 0)
        button_layout.addWidget(self.unit_convert_button, 1, 1)
        button_layout.addWidget(self.language_button, 1, 2)
        button_layout.addWidget(self.graph_button, 1, 3)

        main_layout.addWidget(self.menu_bar)
        main_layout.addLayout(control_layout)
        main_layout.addWidget(self.table)
        main_layout.addWidget(self.details_box)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        # Variables to store history and custom constants
        self.copy_history = []
        self.custom_constants = {}

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
            QMessageBox.warning(self, "No Selection", "Please select a constant to copy.")
            return

        constant_name = selected_items[0].text()
        category = self.category_box.currentText()
        value = CONSTANTS[category][constant_name]['value']

        # Copy to clipboard
        clipboard = QApplication.clipboard()
        clipboard.setText(value)

        # Add to copy history
        self.copy_history.append((constant_name, value))
        QMessageBox.information(self, "Copied", f"Copied {constant_name} to clipboard.")

    def view_history(self):
        # Display copy history
        if not self.copy_history:
            QMessageBox.information(self, "No History", "No constants have been copied yet.")
            return

        history_text = "\n".join([f"{name}: {value}" for name, value in self.copy_history])
        QMessageBox.information(self, "Copy History", history_text)

    def export_constants(self):
        # Export custom constants to a JSON file
        try:
            file_name, _ = QFileDialog.getSaveFileName(self, "Export Constants", "", "JSON Files (*.json)")
            if not file_name:
                return
            with open(file_name, 'w') as file:
                json.dump(self.custom_constants, file)
            QMessageBox.information(self, "Exported", "Custom constants exported successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def import_constants(self):
        # Import custom constants from a JSON file
        try:
            file_name, _ = QFileDialog.getOpenFileName(self, "Import Constants", "", "JSON Files (*.json)")
            if not file_name:
                return
            with open(file_name, 'r') as file:
                self.custom_constants = json.load(file)
            QMessageBox.information(self, "Imported", "Custom constants imported successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def change_theme(self):
        # Theme customization dialog
        color = QColorDialog.getColor()
        if color.isValid():
            palette = self.palette()
            palette.setColor(QPalette.Window, color)
            self.setPalette(palette)

    def add_custom_constant(self):
        # Dialog to add a new custom constant
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Custom Constant")
        layout = QFormLayout(dialog)

        constant_name_input = QLineEdit(dialog)
        constant_value_input = QLineEdit(dialog)
        constant_desc_input = QLineEdit(dialog)

        layout.addRow("Constant Name:", constant_name_input)
        layout.addRow("Constant Value:", constant_value_input)
        layout.addRow("Constant Description:", constant_desc_input)

        button_box = QHBoxLayout()
        add_button = QPushButton("Add", dialog)
        add_button.clicked.connect(lambda: self.save_custom_constant(dialog, constant_name_input, constant_value_input, constant_desc_input))
        button_box.addWidget(add_button)
        layout.addRow(button_box)

        dialog.setLayout(layout)
        dialog.exec_()

    def save_custom_constant(self, dialog, name_input, value_input, desc_input):
        # Save the new custom constant
        name = name_input.text()
        value = value_input.text()
        description = desc_input.text()

        if not name or not value or not description:
            QMessageBox.warning(self, "Incomplete Data", "Please provide all fields.")
            return

        self.custom_constants[name] = {'value': value, 'description': description}
        dialog.accept()
        QMessageBox.information(self, "Added", f"Custom constant '{name}' added successfully!")

    def unit_conversion(self):
        # Simple unit conversion dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Unit Conversion")
        layout = QFormLayout(dialog)

        # From and To unit inputs
        from_unit_input = QLineEdit(dialog)
        to_unit_input = QLineEdit(dialog)
        amount_input = QLineEdit(dialog)

        layout.addRow("From Unit:", from_unit_input)
        layout.addRow("To Unit:", to_unit_input)
        layout.addRow("Amount:", amount_input)

        convert_button = QPushButton("Convert", dialog)
        convert_button.clicked.connect(lambda: self.perform_conversion(dialog, from_unit_input, to_unit_input, amount_input))
        layout.addRow(convert_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def perform_conversion(self, dialog, from_unit_input, to_unit_input, amount_input):
        # Dummy conversion logic (for demonstration purposes)
        try:
            from_unit = from_unit_input.text()
            to_unit = to_unit_input.text()
            amount = float(amount_input.text())

            # Dummy conversion rate
            conversion_rate = 1.0  # Placeholder
            result = amount * conversion_rate

            QMessageBox.information(self, "Conversion Result", f"{amount} {from_unit} = {result} {to_unit}")
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter valid numbers for amount.")

    def change_language(self):
        # Change language dialog
        languages = ["English", "French", "Spanish", "Chinese"]
        dialog = QDialog(self)
        dialog.setWindowTitle("Change Language")
        layout = QVBoxLayout(dialog)

        for language in languages:
            button = QPushButton(language, dialog)
            button.clicked.connect(lambda: self.set_language(dialog, language))
            layout.addWidget(button)

        dialog.setLayout(layout)
        dialog.exec_()

    def set_language(self, dialog, language):
        # Set application language (placeholder)
        QMessageBox.information(self, "Language Changed", f"Language changed to {language}.")
        dialog.accept()

    def show_history_graph(self):
        # Display a graph showing the historical values of a selected constant (dummy implementation)
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select a constant to view its history graph.")
            return

        constant_name = selected_items[0].text()
        category = self.category_box.currentText()
        history_data = CONSTANTS[category][constant_name]['history']

        # Dummy graph display (for demonstration purposes)
        QMessageBox.information(self, "History Graph", f"Showing history graph for {constant_name}: {history_data}")


def main():
    app = QApplication(sys.argv)
    viewer = ConstantsViewer()
    viewer.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
