import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QAction, QMessageBox, QTabWidget, \
    QTableWidget, QTabBar, QMenuBar, QLineEdit, QInputDialog


class TabsContainer(QTabWidget):

    def __init__(self, tabWidget, start_page_tab):
        super(TabsContainer, self).__init__()
        self.tabWidget = tabWidget

        self.start_page_tab = start_page_tab

        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.setTabsClosable(True)
        # self.tabWidget.setStyleSheet("QTabBar::close-button {   image: url(:../icons/close.png);   subcontrol-position: left;   height: 50px;   width: 5px; } QTabBar::close-button:hover { image:url(../icons/close-selected.png);}")
        self.tabWidget.tabCloseRequested.connect(self.close_tab)

        self.tabWidget.tabBarDoubleClicked.connect(self.tab_rename)

    def tab_rename(self, index):
        new_tab_name, is_rename_done_clicked = QInputDialog.getText(
            self, 'Rename Dialog', 'Enter a new tab name:')
        if is_rename_done_clicked:
            self.tabWidget.setTabText(index, new_tab_name)

    def add_tab(self, tab):
        self.tabWidget.insertTab(self.tabWidget.count(), tab.get_tab(), tab.get_tab_title())

    def close_tab(self, current_index):
        print("Current Tab Index = ", current_index)
        self.tabWidget.removeTab(current_index)

        # Show landing page if all tabs are closed
        if self.tabWidget.count() == 0:
            print("All Tabs closed, redirect to landing page")
            self.tabWidget.insertTab(0, self.start_page_tab, "Start Page")

        # TODO: Add a Save check before proceeding to close the tab


class ModuleTab(QTableWidget):
    max_row_count = 1048576  # Defaults to value used by MS Excel

    def __init__(self, tab_title, tab_columns=None):
        super(ModuleTab, self).__init__()
        self.tab = QTableWidget(self.max_row_count, len(tab_columns))
        self.tab_columns = tab_columns

        # Set header labels
        self.tab.setHorizontalHeaderLabels(tab_columns)

        self.tab_title = tab_title

    def get_tab_title(self):
        return self.tab_title

    def get_tab(self):
        return self.tab

    def get_tab_columns(self):
        return self.tab_columns


class FinPlateTab(ModuleTab):
    def __init__(self):
        super(FinPlateTab, self).__init__("FinPlate",
                                          ["ID", "Connection type", "Axial load", "Shear load", "Bolt diameter",
                                           "Bolt grade", "Plate thickness"]
                                          )


class TensionMemberTab(ModuleTab):
    def __init__(self):
        super(TensionMemberTab, self).__init__("TensionMember",
                                               ["ID", "Member length", "Tensile load", "Support condition at End 1",
                                                "Support condition at End 2"]
                                               )


class BCEndPlateTab(ModuleTab):
    def __init__(self):
        super(BCEndPlateTab, self).__init__("BCEndPlate",
                                            ["ID", "End plate type", "Shear load", "Axial Load", "Moment Load",
                                             "Bolt diameter", "Bolt grade", "Plate thickness"]
                                            )


class CleatAngleTab(ModuleTab):
    def __init__(self):
        super(CleatAngleTab, self).__init__("CleatAngle",
                                            ["ID", "Angle leg 1", "Angle leg 2", "Angle thickness", "Shear load",
                                             "Bolt diameter", "Bolt grade"]
                                            )


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
