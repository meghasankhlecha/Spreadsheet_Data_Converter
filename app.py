import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QAction, QMessageBox, QTabWidget, \
    QTableWidget


class TabsContainer(QTabWidget):
    def __init__(self, tabWidget):
        super(TabsContainer, self).__init__()
        self.tabWidget = tabWidget
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.close_tab)

        # Remove Main Tab (index 1) for now
        self.tabWidget.removeTab(1)

        # Composition Tabs container has multiple Tabs inside it
        # self.tabWidget.insertTab(1, QTableWidget(1048576, 2), "Main1 Document")
        # self.tabWidget.insertTab(2, QTableWidget(1048576, 3), "Main2 Document")

    def add_tab(self, tab):
        self.tabWidget.insertTab(self.tabWidget.count(), tab.get_tab(), tab.get_tab_title())

    def close_tab(self, current_index):
        print("Current Tab Index = ", current_index)
        self.tabWidget.removeTab(current_index)

        # TODO: Add a mechanism to show landing page if all the tabs are closed
        if self.tabWidget.count() == 0:
            print("All Tabs closed, redirect to landing page")

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
        uic.loadUi('mainwindow.ui', self)

        # Composition - DataConvertor App has Tabs Container
        self.tabs_container = TabsContainer(self.tabWidget)

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
