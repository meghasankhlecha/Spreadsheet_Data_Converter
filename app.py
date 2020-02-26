import os
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from components.Tabs import TabsContainer, FinPlateTab, TensionMemberTab, BCEndPlateTab, CleatAngleTab
from components.DataValidator import DataValidator


class DataConverter(QMainWindow):

    def __init__(self, windowTitle="Spreadsheet to Data Converter"):
        super(DataConverter, self).__init__()
        # define UI file paths
        RESOURCE_PATH = os.path.dirname(__file__)  # <-- absolute dir the script is in
        mainwindowui_file = os.path.join(RESOURCE_PATH, "ui/mainwindow.ui")
        uic.loadUi(mainwindowui_file, self)

        # Composition - DataConvertor App has Tabs Container
        self.tabs_container = TabsContainer(self.tabWidget, self.start_tab)

        self.menu_action_validate_data = self.menubar.addAction("Validate Data")
        self.menu_action_save_data = self.menubar.addAction("Save Data to text file")

        self.set_connections()

        # CALL THE DESIRED VIEW
        self.show()

    # CHANGE THE DEFAULT BEHAVIOUR OF THE CLOSE WINDOW
    def closeEvent(self, QCloseEvent):
        QCloseEvent.ignore()
        self.close_application()

    def close_application(self):
        # ADD CONFIRM POPUP
        choice = QMessageBox.question(self, 'Quit', "Are you sure you want to quit?",
                                      QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            print("Quiting")
            sys.exit()

    def set_connections(self):
        # File Menu
        self.action_load_fin_plate.triggered.connect(self.load_fin_plate)
        self.action_blank_fin_plate.triggered.connect(self.load_blank_fin_plate)
        self.action_load_tension_member.triggered.connect(self.load_tension_member)
        self.action_blank_tension_member.triggered.connect(self.load_blank_tension_member)
        self.action_load_bc_end_plate.triggered.connect(self.load_bc_end_plate)
        self.action_blank_bc_end_plate.triggered.connect(self.load_blank_bc_end_plate)
        self.action_load_cleat_angle.triggered.connect(self.load_cleat_angle)
        self.action_blank_cleat_angle.triggered.connect(self.load_blank_cleat_angle)

        # Start Page Push Buttons for modules
        self.push_btn_fin_plate.clicked.connect(self.load_fin_plate)
        self.push_btn_tension_member.clicked.connect(self.load_tension_member)
        self.push_btn_bc_end_plate.clicked.connect(self.load_bc_end_plate)
        self.push_btn_cleat_angle.clicked.connect(self.load_cleat_angle)

        # Menubar actions
        self.menu_action_validate_data.triggered.connect(self.validate_current_tab_data)

    def load_fin_plate(self):
        # Open file action for Fin Plate Tab
        fin_plate_tab = FinPlateTab()
        self.tabs_container.add_tab(fin_plate_tab)
        fin_plate_tab.load_file()

    def load_blank_fin_plate(self):
        self.tabs_container.add_tab(FinPlateTab())

    def load_tension_member(self):
        tension_member = TensionMemberTab()
        self.tabs_container.add_tab(tension_member)
        tension_member.load_file()

    def load_blank_tension_member(self):
        self.tabs_container.add_tab(TensionMemberTab())

    def load_bc_end_plate(self):
        bc_end_plate = BCEndPlateTab()
        self.tabs_container.add_tab(bc_end_plate)
        bc_end_plate.load_file()

    def load_blank_bc_end_plate(self):
        self.tabs_container.add_tab(BCEndPlateTab())

    def load_cleat_angle(self):
        cleat_angle = CleatAngleTab()
        self.tabs_container.add_tab(cleat_angle)
        cleat_angle.load_file()

    def load_blank_cleat_angle(self):
        self.tabs_container.add_tab(CleatAngleTab())

    def validate_current_tab_data(self):
        print("Validating current tab")
        if self.tabs_container.get_current_tab_name() != "Start Page":
            DataValidator.is_valid(self.tabs_container.get_current_tab())


def run():
    app = QApplication(sys.argv)
    GUI = DataConverter("Spreadsheet to Data Converter")
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
