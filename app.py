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

        # Composition Tabs container has multiple Tabs inside it
        self.tabWidget.insertTab(1, QTableWidget(1048576, 2), "Main1 Document")
        self.tabWidget.insertTab(2, QTableWidget(1048576, 3), "Main2 Document")

    def close_tab(self, current_index):
        print("Current Tab Index = ", current_index)
        self.tabWidget.removeTab(current_index)

        # TODO: Add a mechanism to show landing page if all the tabs are closed
        if self.tabWidget.count() == 0:
            print("All Tabs closed, redirect to landing page")

        # TODO: Add a Save check before proceeding to close the tab


class FinPlateTab(QTableWidget):
    pass


class TensionMemberTab(QTableWidget):
    pass


class BCEndPlateTab(QTableWidget):
    pass


class CleatAngleTab(QTableWidget):
    pass


class DataConverter(QMainWindow):

    def __init__(self, windowTitle="Spreadsheet to Data Converter"):
        super(DataConverter, self).__init__()
        uic.loadUi('mainwindow.ui', self)

        # Composition - DataConvertor App has Tabs Container
        self.tabs_container = TabsContainer(self.tabWidget)

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
