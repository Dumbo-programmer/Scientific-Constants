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
from constants import CONSTANTS

# Dictionary of scientific constants
CONSTANTS = {
    'Physics': {
        'Speed of Light': {
            'value': '299,792,458 m/s',
            'description': 'The speed of light in vacuum.'
        },
        'Gravitational Constant': {
            'value': '6.67430 × 10^-11 m^3 kg^-1 s^-2',
            'description': 'The constant of proportionality in Newton\'s law of gravitation.'
        },
        'Planck\'s Constant': {
            'value': '6.62607015 × 10^-34 J s',
            'description': 'The fundamental constant relating energy and frequency of photons.'
        },
        'Boltzmann Constant': {
            'value': '1.380649 × 10^-23 J/K',
            'description': 'The physical constant relating the average kinetic energy of particles in a gas with the temperature of the gas.'
        },
        'Elementary Charge': {
            'value': '1.602176634 × 10^-19 C',
            'description': 'The magnitude of electric charge carried by a single proton.'
        },
        'Magnetic Constant': {
            'value': '4π × 10^-7 N/A^2',
            'description': 'The proportionality constant in the magnetic component of Maxwell\'s equations.'
        },
        'Fine-Structure Constant': {
            'value': '0.0072973525693',
            'description': 'A dimensionless constant characterizing the strength of the electromagnetic interaction.'
        },
        'Cosmological Constant': {
            'value': '8πGρ/3 - Λ',
            'description': 'The constant in Einstein\'s field equations of General Relativity, associated with dark energy.'
        },
        'Stefan-Boltzmann Constant': {
            'value': '5.670374419 × 10^-8 W m^-2 K^-4',
            'description': 'The constant in Stefan-Boltzmann law relating temperature to thermal radiation emitted by a black body.'
        },
        'Gas Constant': {
            'value': '8.314462618 J mol^-1 K^-1',
            'description': 'The constant in the ideal gas law.'
        },
        'Avogadro\'s Number': {
            'value': '6.02214076 × 10^23 mol^-1',
            'description': 'The number of atoms or molecules in one mole of a substance.'
        },
        'Faraday Constant': {
            'value': '96485.33212 C/mol',
            'description': 'The magnitude of electric charge per mole of electrons.'
        },
        'Standard Atmosphere': {
            'value': '101,325 Pa',
            'description': 'The standard pressure at sea level.'
        },
        'Molar Mass of Carbon-12': {
            'value': '12.00000 g/mol',
            'description': 'The molar mass of the carbon-12 isotope, used as the standard for atomic mass units.'
        },
    },
    'Chemistry': {
        'Gas Constant': {
            'value': '8.314462618 J mol^-1 K^-1',
            'description': 'The constant in the ideal gas law.'
        },
        'Avogadro\'s Number': {
            'value': '6.02214076 × 10^23 mol^-1',
            'description': 'The number of atoms or molecules in one mole of a substance.'
        },
        'Faraday Constant': {
            'value': '96485.33212 C/mol',
            'description': 'The magnitude of electric charge per mole of electrons.'
        },
        'Standard Atmosphere': {
            'value': '101,325 Pa',
            'description': 'The standard pressure at sea level.'
        },
        'Molar Mass of Carbon-12': {
            'value': '12.00000 g/mol',
            'description': 'The molar mass of the carbon-12 isotope, used as the standard for atomic mass units.'
        },
        'Ionization Energy of Hydrogen': {
            'value': '13.598 eV',
            'description': 'The energy required to ionize a hydrogen atom.'
        },
        'Bond Dissociation Energy of H2': {
            'value': '435.88 kJ/mol',
            'description': 'The energy required to dissociate a hydrogen molecule into two hydrogen atoms.'
        },
        'Standard Molar Entropy of Water': {
            'value': '69.91 J mol^-1 K^-1',
            'description': 'The entropy of water in its standard state at 298 K.'
        },
        'Standard Enthalpy of Formation of Water': {
            'value': '-285.83 kJ/mol',
            'description': 'The enthalpy change when one mole of water is formed from its elements in their standard states.'
        },
        'Thermal Conductivity of Copper': {
            'value': '401 W m^-1 K^-1',
            'description': 'The ability of copper to conduct heat.'
        },
    },
    'Mathematics': {
        'Euler\'s Number (e)': {
            'value': '2.718281828',
            'description': 'The base of the natural logarithm, used extensively in mathematics.'
        },
        'Pi (π)': {
            'value': '3.14159265359',
            'description': 'The ratio of the circumference of a circle to its diameter.'
        },
        'Golden Ratio (φ)': {
            'value': '1.61803398875',
            'description': 'The number that appears in various contexts in mathematics, art, and nature.'
        },
        'Square Root of 2 (√2)': {
            'value': '1.41421356237',
            'description': 'The length of the diagonal of a square with side length 1.'
        },
        'Square Root of 3 (√3)': {
            'value': '1.73205080757',
            'description': 'The length of the diagonal of a cube with side length 1.'
        },
        'Natural Logarithm of 2 (ln 2)': {
            'value': '0.69314718056',
            'description': 'The natural logarithm of 2.'
        },
        'Logarithm Base 10 of 2 (log10 2)': {
            'value': '0.30102999566',
            'description': 'The logarithm of 2 with base 10.'
        },
        'Catalan\'s Constant': {
            'value': '0.91596559416',
            'description': 'A constant that appears in combinatorial mathematics.'
        },
        'Ramanujan\'s Constant': {
            'value': '1.2824271291',
            'description': 'A constant related to the distribution of prime numbers.'
        },
        'Feigenbaum Constants': {
            'value': 'δ ≈ 4.66920160910, α ≈ 2.50290787595',
            'description': 'Constants that arise in the study of bifurcations in chaotic systems.'
        },
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
     selected_items = self.constants_list_widget.selectedItems()
     if not selected_items:
        return

     # Retrieve the selected constant name
     constant_name = selected_items[0].text()
     category = self.category_combobox.currentText()

     # Ensure the constant name exists in the constants dictionary
     if category in CONSTANTS and constant_name in CONSTANTS[category]:
         constant_value = CONSTANTS[category][constant_name]['value']
         description = CONSTANTS[category][constant_name].get('description', "No description available.")

        # Show the constant details in a dialog
         QMessageBox.information(self, "Constant Details",
                                f"Name: {constant_name}\nValue: {constant_value}\nDescription: {description}")
     else:
         # Handle the case where the constant name doesn't exist in the dictionary
          QMessageBox.warning(self, "Error", f"Details for constant '{constant_name}' not found in category '{category}'.")


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
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

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
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def change_theme(self):
        # Allow users to choose a theme color
        color = QColorDialog.getColor()
        if color.isValid():
            palette = self.palette()
            palette.setColor(QPalette.Window, color)
            self.setPalette(palette)

    def add_custom_constant(self):
        # Dialog to add a custom constant
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Custom Constant")
        form_layout = QFormLayout(dialog)

        name_input = QLineEdit(dialog)
        value_input = QLineEdit(dialog)
        description_input = QLineEdit(dialog)

        form_layout.addRow("Constant Name:", name_input)
        form_layout.addRow("Value:", value_input)
        form_layout.addRow("Description:", description_input)

        add_button = QPushButton("Add", dialog)
        add_button.clicked.connect(lambda: self.save_custom_constant(dialog, name_input.text(), value_input.text(), description_input.text()))
        form_layout.addWidget(add_button)

        dialog.setLayout(form_layout)
        dialog.exec_()

    def save_custom_constant(self, dialog, name, value, description):
        if name and value:
            self.custom_constants[name] = {'value': value, 'description': description}
            QMessageBox.information(self, "Success", f"Custom constant '{name}' added.")
            dialog.accept()
        else:
            QMessageBox.warning(self, "Incomplete Data", "Please provide both a name and value for the constant.")

    def unit_conversion(self):
        # Dummy unit conversion feature
        QMessageBox.information(self, "Unit Conversion", "This feature is under development.")

    def change_language(self):
        # Dummy change language feature
        QMessageBox.information(self, "Change Language", "This feature is under development.")

    def show_history_graph(self):
        # Dummy history graph feature
        QMessageBox.information(self, "History Graph", "This feature is under development.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = ConstantsViewer()
    viewer.show()
    sys.exit(app.exec_())
