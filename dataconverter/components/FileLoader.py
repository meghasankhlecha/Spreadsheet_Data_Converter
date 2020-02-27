from PyQt5 import uic, QtCore
from PyQt5.QtCore import QObject, pyqtSignal, QThread, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QTableWidgetItem, QDialog, \
    QMessageBox, QVBoxLayout, QCheckBox, QProgressDialog, QInputDialog, QLineEdit, QGridLayout, QLabel, QWidget
import os
import sys
import csv
import xlrd
import time


class Worker(QObject):

    def __init__(self, csv_file_path, csv_data_table):
        super(Worker, self).__init__()
        self.csv_file_path = csv_file_path
        self.csv_data_table = csv_data_table

    finished = pyqtSignal()
    intReady = pyqtSignal(int)
    max_progress_value = pyqtSignal(int)
    read_values = pyqtSignal(int, int, str)

    @pyqtSlot()
    def procCounter(self):  # A slot takes no params
        # for i in range(1, 100):
        #     time.sleep(0.2)
        #     self.intReady.emit(i)
        #
        # self.finished.emit()
        # Open the file once to get idea of the total rowcount to display progress
        with open(self.csv_file_path[0], newline='') as csv_file:
            self.max_progress_value.emit(len(csv_file.readlines()) - 1)

        with open(self.csv_file_path[0], newline='') as csv_file:

            print("Opened file for reading")
            csv_file_read = csv.reader(csv_file, delimiter=',', quotechar='|')
            row_index = 0
            for row_data in csv_file_read:
                # print("Row = ", row_index)
                self.intReady.emit(row_index)
                for column, stuff in enumerate(row_data):
                    self.read_values.emit(row_index, column, stuff)
                # item = QTableWidgetItem(stuff)
                # print(item.text())
                # self.csv_data_table.setItem(row_index, column, item)
                row_index = row_index + 1

        print(row_index)

        # Update the bottom toolbar to reflect changes
        # self.update_bottom_toolbar.emit()
        # time.sleep(2)
        print("Emitting finish")
        self.finished.emit()
        # print("Post emitting finish")
        # self.progress_max.emit(9999)


class FileLoader(QWidget):
    def __init__(self, main_window, tab_data_table):
        super(FileLoader, self).__init__()
        self.tab_data_table = tab_data_table
        self.main_window = main_window

        self.label = QLabel("0")

    def is_csv_file(self):
        return self.file_extension.lower() == ".csv"

    def is_excel_file(self):
        return self.file_extension.lower() == ".xlsx"

    def load_csv(self):
        """
                Loads the file from file selector to a table
                closes any open file if any before opening new file
                """

        loaded_file_path = QFileDialog.getOpenFileName(self.main_window, "Load File", "",
                                                       'CSV/XLSX(*.csv *.xlsx);;CSV(*.csv);; XLSX(*.xlsx)')

        print("File path: ", loaded_file_path)
        filename, self.file_extension = os.path.splitext(loaded_file_path[0])
        print("Extensions: ", self.file_extension)

        # Proceed if and only if a valid file is selected and the file dialog is not cancelled
        if loaded_file_path[0]:
            # Get only the file name from path. eg. 'data_file.csv'
            filepath = os.path.normpath(loaded_file_path[0])
            filename = filepath.split(os.sep)
            self.csv_file_name = filename[-1]

            # self.loading_progress = QProgressDialog("Reading Rows. Please wait...", None, 0, 99999, self.main_window)
            #
            # if self.is_csv_file(self.file_extension):
            #     self.loading_progress.setWindowTitle("Loading CSV File...")
            # elif self.is_excel_file(self.file_extension):
            #     self.loading_progress.setWindowTitle("Loading XLSX File...")
            #
            # self.loading_progress.setCancelButton(None)
            #
            # # enable custom window hint
            # self.loading_progress.setWindowFlags(self.loading_progress.windowFlags() | QtCore.Qt.CustomizeWindowHint)
            # # disable (but not hide) close button
            # self.loading_progress.setWindowFlags(self.loading_progress.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)
            # #
            # # # Show waiting cursor till the time file is being processed
            # QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)

            # if self.is_csv_file(self.file_extension):
            #     self.loading_worker = CsvLoaderWorker(csv_file_path=loaded_file_path,
            #                                           csv_data_table=self.tab_data_table)
            # elif self.is_excel_file(self.file_extension):
            #     self.loading_worker = XlsxLoaderWorker(xlsx_file_path=loaded_file_path,
            #                                            xlsx_data_table=self.tab_data_table)

            self.worker = Worker(csv_file_path=loaded_file_path,
                                 csv_data_table=self.tab_data_table)
            # self.thread = FileLoadingWorker(csv_file_path=loaded_file_path,
            #                                 csv_data_table=self.tab_data_table)
            self.thread = QThread()
            self.worker.intReady.connect(self.set_progress_value)
            self.worker.read_values.connect(self.update_table_values)

            self.worker.moveToThread(self.thread)

            self.worker.max_progress_value.connect(self.set_max_progress_value)
            self.worker.finished.connect(self.task_finished)

            self.thread.started.connect(self.worker.procCounter)

            self.thread.start()

            self.initUI()

            QApplication.restoreOverrideCursor()

    def update_table_values(self, row, col, value):
        print("val = ", value)
        item = QTableWidgetItem(value)
        self.tab_data_table.setItem(row, col, item)

    def initUI(self):
        # grid = QGridLayout()
        # self.setLayout(grid)
        # grid.addWidget(self.label, 0, 0)
        # 
        # self.move(300, 150)
        # self.setWindowTitle('thread test')
        # self.show()
        self.loading_progress = QProgressDialog("Reading Rows. Please wait...", None, 0, 99999, self.main_window)

        if self.is_csv_file():
            self.loading_progress.setWindowTitle("Loading CSV File...")
        elif self.is_excel_file():
            self.loading_progress.setWindowTitle("Loading XLSX File...")

        self.loading_progress.setCancelButton(None)

        # enable custom window hint
        self.loading_progress.setWindowFlags(self.loading_progress.windowFlags() | QtCore.Qt.CustomizeWindowHint)
        # disable (but not hide) close button
        self.loading_progress.setWindowFlags(self.loading_progress.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)
        #
        # # Show waiting cursor till the time file is being processed
        QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)

    def set_progress_value(self, val):
        print("update:", val)
        self.loading_progress.setValue(val)
        # self.label.setText("{}".format(val))

    def set_max_progress_value(self, val):
        self.loading_progress.setMaximum(val)
        self.loading_progress.setValue(0)

    def task_finished(self):
        print("on_loading_finish_called")
        print("Column Resize")
        # Stretch to fill the column width according to content
        # self.tab_data_table.resizeColumnsToContents()
        # Change the cursor back to normal
        QApplication.restoreOverrideCursor()
        # self.close()


class CsvLoaderWorker():

    def __init__(self, csv_file_path, csv_data_table, parent=None):
        self.csv_file_path = csv_file_path
        self.csv_data_table = csv_data_table
        self.process_loading_file()

    def process_loading_file(self):
        # TODO: Increase the reading speed by decreasing load on actual table population
        #
        # self.csv_data_table.hide()

        with open(self.csv_file_path[0], newline='') as csv_file:

            print("Opened file for reading")

            csv_file_read = csv.reader(csv_file, delimiter=',', quotechar='|')

            row_index = 0
            for row_data in csv_file_read:
                # print("Row = ", row_index)
                for column, stuff in enumerate(row_data):
                    item = QTableWidgetItem(stuff)
                    # print(item.text())
                    self.csv_data_table.setItem(row_index, column, item)
                row_index = row_index + 1

        print("Column Resize")
        # Stretch to fill the column width according to content
        self.csv_data_table.resizeColumnsToContents()


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
