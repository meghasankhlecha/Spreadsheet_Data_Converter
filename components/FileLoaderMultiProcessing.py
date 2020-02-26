from PyQt5 import uic, QtCore
from PyQt5.QtCore import QObject, pyqtSignal, QThread, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QTableWidgetItem, QProgressDialog, QLabel, QWidget
import os
import sys
import csv
import xlrd


class Worker(QObject):

    def __init__(self, file_path, file_extension):
        super(Worker, self).__init__()
        self.file_path = file_path
        self.file_extension = file_extension

    # Signals for broadcasting the current status of loading
    finished = pyqtSignal()
    current_progress = pyqtSignal(int)
    max_progress_value = pyqtSignal(int)
    read_values = pyqtSignal(int, int, str)

    @pyqtSlot()
    def load_file(self):

        if FileLoader.is_csv_file(self.file_extension):

            # Open the file once to get idea of the total rowcount to display progress
            with open(self.file_path[0], newline='') as csv_file:
                self.max_progress_value.emit(len(csv_file.readlines()) - 1)

            with open(self.file_path[0], newline='') as csv_file:
                print("Opened file for reading")
                csv_file_read = csv.reader(csv_file, delimiter=',', quotechar='|')
                row_index = 0
                for row_data in csv_file_read:
                    self.current_progress.emit(row_index)
                    for column, stuff in enumerate(row_data):
                        self.read_values.emit(row_index, column, stuff)

                    row_index = row_index + 1

            print("Total Rows processed: ", row_index)
        elif FileLoader.is_excel_file(self.file_extension):
            workbook = xlrd.open_workbook(self.file_path[0])
            # Support only first sheet of excel file at this time
            sheet = workbook.sheet_by_index(0)

            print("Max sheet rows:", sheet.nrows)
            self.max_progress_value.emit(sheet.nrows - 1)

            for rowx in range(sheet.nrows):
                self.current_progress.emit(rowx)
                cols = sheet.row_values(rowx)
                col_index = 0
                for col in cols:
                    # Do a string conversion as widget accepts only strings
                    self.read_values.emit(rowx, col_index, str(col))
                    # item = QTableWidgetItem(str(col))
                    # self.xlsx_data_table.setItem(rowx, col_index, item)
                    col_index += 1

        # Update the bottom toolbar to reflect changes
        # self.update_bottom_toolbar.emit()
        print("Emitting finish")
        self.finished.emit()


class FileLoader:
    def __init__(self, main_window, tab_data_table):
        super(FileLoader, self).__init__()
        self.tab_data_table = tab_data_table
        self.main_window = main_window

    def __del__(self):
        print('Destructor call check to ensure it fires after complete execution')

    @staticmethod
    def is_csv_file(file_extension):
        return file_extension.lower() == ".csv"

    @staticmethod
    def is_excel_file(file_extension):
        return file_extension.lower() == ".xlsx"

    def load_csv(self):
        """
                Loads the file from file selector to a table
        """

        loaded_file_path = QFileDialog.getOpenFileName(self.main_window, "Load File", "",
                                                       'csv or xlxs(*.csv *.xlsx);;CSV(*.csv);; XLSX(*.xlsx)')

        filename, self.file_extension = os.path.splitext(loaded_file_path[0])
        print("Extensions: ", self.file_extension)

        # Proceed if and only if a valid file is selected and the file dialog is not cancelled
        if loaded_file_path[0]:
            # Get only the file name from path. eg. 'data_file.csv'
            filepath = os.path.normpath(loaded_file_path[0])
            filename = filepath.split(os.sep)
            self.csv_file_name = filename[-1]

            self.initUI()

            self.worker = Worker(file_path=loaded_file_path, file_extension=self.file_extension)

            self.thread = QThread()
            self.worker.current_progress.connect(self.set_progress_value)
            self.worker.read_values.connect(self.update_table_values)

            self.worker.moveToThread(self.thread)

            self.worker.max_progress_value.connect(self.set_max_progress_value)
            self.worker.finished.connect(self.task_finished)

            self.thread.started.connect(self.worker.load_file)

            self.thread.start()

            QApplication.restoreOverrideCursor()

    def update_table_values(self, row, col, value):
        item = QTableWidgetItem(value)
        self.tab_data_table.setItem(row, col, item)

    def initUI(self):
        # # Show waiting cursor till the time file is being processed
        QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)

        self.loading_progress = QProgressDialog("Reading Rows. Please wait...", None, 0, 99999, self.main_window)

        if self.is_csv_file(self.file_extension):
            self.loading_progress.setWindowTitle("Loading CSV File...")
        elif self.is_excel_file(self.file_extension):
            self.loading_progress.setWindowTitle("Loading XLSX File...")

        self.loading_progress.setCancelButton(None)

        # enable custom window hint
        self.loading_progress.setWindowFlags(self.loading_progress.windowFlags() | QtCore.Qt.CustomizeWindowHint)
        # disable (but not hide) close button
        self.loading_progress.setWindowFlags(self.loading_progress.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)

    def set_progress_value(self, val):
        print("update:", val)
        self.loading_progress.setValue(val)

    def set_max_progress_value(self, val):
        # Set the maximum progress for progressbar (fetch values from signal)
        self.loading_progress.setMaximum(val)
        self.loading_progress.setValue(0)

    def task_finished(self):
        print("on_task_finish_called")
        # Stretch to fill the column width according to content
        self.tab_data_table.resizeColumnsToContents()

        # Change the cursor back to normal
        QApplication.restoreOverrideCursor()

        self.thread.quit()

        # Remove pointer to the current FileLoader so it can be GCed
        self.tab_data_table.setProperty("file_pointer", None)


class XlsxLoaderWorker():

    def __init__(self, xlsx_file_path, xlsx_data_table, parent=None):
        self.xlsx_file_path = xlsx_file_path
        self.xlsx_data_table = xlsx_data_table
        self.process_loading_file()

    def process_loading_file(self):
        """
        Starts the thread for populating table from the file without blocking the main UI thread
        """
        print("Inside loading file")

        workbook = xlrd.open_workbook(self.xlsx_file_path[0])
        sheet = workbook.sheet_by_index(0)

        for rowx in range(sheet.nrows):
            cols = sheet.row_values(rowx)
            # print("Cols:", cols)
            col_index = 0
            for col in cols:
                # Do a string conversion as widget accepts only strings
                item = QTableWidgetItem(str(col))
                # print(item.text())
                self.xlsx_data_table.setItem(rowx, col_index, item)
                col_index += 1

        print("Column Resize")
        # Stretch to fill the column width according to content
        self.xlsx_data_table.resizeColumnsToContents()
