import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from components.Tabs import TabsContainer, FinPlateTab, TensionMemberTab, BCEndPlateTab, CleatAngleTab
from components.FileLoaderMultiProcessing import FileLoader


class DataConverter(QMainWindow):

    def __init__(self, windowTitle="Spreadsheet to Data Converter"):
        super(DataConverter, self).__init__()
        uic.loadUi('ui/mainwindow.ui', self)

        # self.menubar.addAction("Validate Data")
        # self.menubar.addAction("Save Data to text file")
        # self.menubar.setStyleSheet("QMenuBar::item {border: 1px solid black; margin: 5px; padding: 5px; border-radius:3px;}")

        # Composition - DataConvertor App has Tabs Container
        self.tabs_container = TabsContainer(self.tabWidget, self.start_tab)

        fin_plate_tab = FinPlateTab()
        tension_member_tab = TensionMemberTab()
        bcend_plate_tab = BCEndPlateTab()
        cleat_angle_tab = CleatAngleTab()

        self.tabs_container.add_tab(fin_plate_tab)
        self.tabs_container.add_tab(tension_member_tab)
        self.tabs_container.add_tab(bcend_plate_tab)
        self.tabs_container.add_tab(cleat_angle_tab)

        file_load = FileLoader(self, fin_plate_tab.get_tab())
        file_load.load_csv()

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


def run():
    app = QApplication(sys.argv)
    GUI = DataConverter("Spreadsheet to Data Converter")
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
