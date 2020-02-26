import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QTabWidget, QTableWidget, QInputDialog
from components.FileLoaderMultiProcessing import FileLoader
import random


class TabsContainer(QTabWidget):

    def __init__(self, tabWidget, start_page_tab):
        super(TabsContainer, self).__init__()
        self.tabWidget = tabWidget

        self.start_page_tab = start_page_tab

        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.close_tab)

        self.tabWidget.tabBarDoubleClicked.connect(self.tab_rename)

    def tab_rename(self, index):
        # Only allow renaming if it is not Start Page tab
        clicked_tab_name = self.tabWidget.tabText(index)
        print(clicked_tab_name)
        if clicked_tab_name != "Start Page":
            new_tab_name, is_rename_done_clicked = QInputDialog.getText(
                self, 'Rename Dialog', 'Enter a new tab name:')
            if is_rename_done_clicked:
                self.tabWidget.setTabText(index, new_tab_name)

    def add_tab(self, tab):
        # Check if only one start page is opened if so close it
        first_tab_name = self.tabWidget.tabText(0)
        if first_tab_name == "Start Page":
            self.tabWidget.removeTab(0)

        self.tabWidget.insertTab(self.tabWidget.count(), tab.get_tab(), tab.get_tab_title())
        # Set the new opened tab as current
        self.tabWidget.setCurrentIndex(self.tabWidget.count() - 1)

    def close_tab(self, current_index):
        print("Current Tab Index = ", current_index)
        self.tabWidget.removeTab(current_index)

        # Show landing page if all tabs are closed
        if self.tabWidget.count() == 0:
            print("All Tabs closed, redirect to landing page")
            self.tabWidget.insertTab(0, self.start_page_tab, "Start Page")

        # TODO: Add a Save check before proceeding to close the tab

    def get_current_tab_index(self):
        return self.tabWidget.currentIndex()

    def get_current_tab_name(self):
        return self.tabWidget.tabText(self.get_current_tab_index())

    def get_current_tab(self):
        return self.tabWidget.currentWidget()


class ModuleTab(QTableWidget):
    max_row_count = 1048576  # Defaults to value used by MS Excel = 1048576
    tab_module_name = None

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

    def load_file(self):
        print("Load File called for tab: ", self.tab_module_name)
        # self.file_loader = FileLoader(self, self.get_tab())
        # self.file_loader.load_csv()
        # This will ensure that the file pointer is not destroyed before completion of loading
        # This will keep the FileLoader in memory till the finished signal is emitted avoid garbage collection
        self.get_tab().setProperty("file_pointer", FileLoader(self, self.get_tab()))
        self.get_tab().property("file_pointer").load_csv()
        print("Finished Loading File")


class FinPlateTab(ModuleTab):
    def __init__(self):
        super(FinPlateTab, self).__init__("FinPlate",
                                          ["ID", "Connection type", "Axial load", "Shear load", "Bolt diameter",
                                           "Bolt grade", "Plate thickness"]
                                          )
        self.tab_module_name = "FinPlate"


class TensionMemberTab(ModuleTab):
    def __init__(self):
        super(TensionMemberTab, self).__init__("TensionMember",
                                               ["ID", "Member length", "Tensile load", "Support condition at End 1",
                                                "Support condition at End 2"]
                                               )
        self.tab_module_name = "TensionMember"


class BCEndPlateTab(ModuleTab):
    def __init__(self):
        super(BCEndPlateTab, self).__init__("BCEndPlate",
                                            ["ID", "End plate type", "Shear load", "Axial Load", "Moment Load",
                                             "Bolt diameter", "Bolt grade", "Plate thickness"]
                                            )
        self.tab_module_name = "BCEndPlate"


class CleatAngleTab(ModuleTab):
    def __init__(self):
        super(CleatAngleTab, self).__init__("CleatAngle",
                                            ["ID", "Angle leg 1", "Angle leg 2", "Angle thickness", "Shear load",
                                             "Bolt diameter", "Bolt grade"]
                                            )
        self.tab_module_name = "CleatAngle"
