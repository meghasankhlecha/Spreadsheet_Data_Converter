from PyQt5.QtWidgets import QTabWidget, QTableWidget, QInputDialog, QMessageBox
from dataconverter.components.FileLoaderMultiProcessing import FileLoader


class Singleton(type(QTabWidget)):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


# Allow only one instance of TabsContainer - Singleton Pattern
class TabsContainer(QTabWidget, metaclass=Singleton):

    def __init__(self, main_window, tabWidget, start_page_tab, menu_action_validate_data, menu_action_save_data):
        super(TabsContainer, self).__init__()
        self.main_window = main_window

        self.tabWidget = tabWidget

        self.start_page_tab = start_page_tab

        self.menu_action_validate_data = menu_action_validate_data
        self.menu_action_save_data = menu_action_save_data

        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.close_tab)

        self.tabWidget.tabBarDoubleClicked.connect(self.tab_rename)

    def tab_rename(self, index):
        # Only allow renaming if it is not Start Page tab
        clicked_tab_name = self.tabWidget.tabText(index)
        if clicked_tab_name != "Start Page":
            new_tab_name, is_rename_done_clicked = QInputDialog.getText(
                self.main_window, 'Rename Tab', 'Enter a new tab name:')
            if is_rename_done_clicked:
                self.tabWidget.setTabText(index, new_tab_name)

    def is_start_tab(self):
        return self.tabWidget.tabText(self.tabWidget.currentIndex()) == "Start Page"

    def add_tab(self, tab):
        # Check if only one start page is opened if so close it
        first_tab_name = self.tabWidget.tabText(0)
        if first_tab_name == "Start Page":
            self.tabWidget.removeTab(0)

        self.tabWidget.insertTab(self.tabWidget.count(), tab.get_tab(), tab.get_tab_title())
        # Set the new opened tab as current
        self.tabWidget.setCurrentIndex(self.tabWidget.count() - 1)

        # Add property for accessing the module of the tab
        self.get_current_tab().setProperty("module_name", tab.get_tab_module())

        # Enable validate and save menu options
        self.menu_action_validate_data.setEnabled(True)
        self.menu_action_save_data.setEnabled(True)

    def close_tab(self, current_index):
        print("Current Tab Index = ", current_index)
        if not self.is_start_tab():
            choice = QMessageBox.question(self.main_window, 'Close Tab',
                                          "Are you sure you want to close the current tab?",
                                          QMessageBox.Yes | QMessageBox.No)
            if choice == QMessageBox.Yes:
                self.tabWidget.removeTab(current_index)

        # Show landing page if all tabs are closed
        if self.tabWidget.count() == 0:
            print("All Tabs closed, redirect to landing page")
            self.tabWidget.insertTab(0, self.start_page_tab, "Start Page")
            # Disable Validate and Save options
            self.menu_action_validate_data.setEnabled(False)
            self.menu_action_save_data.setEnabled(False)

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

    def get_tab_module(self):
        return self.tab_module_name

    def get_tab_title(self):
        return self.tab_title

    def get_tab(self):
        return self.tab

    def get_tab_columns(self):
        return self.tab_columns

    def load_file(self):
        print("Load File called for tab: ", self.tab_module_name)
        # This will ensure that the file pointer is not destroyed before completion of loading
        # This will keep the FileLoader in memory till the finished signal is emitted avoid garbage collection
        self.get_tab().setProperty("file_pointer", FileLoader(self, self.get_tab()))
        self.get_tab().property("file_pointer").load_csv()


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
