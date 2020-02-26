from PyQt5 import uic, QtCore
from PyQt5.QtCore import QObject, pyqtSignal, QThread
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QTableWidgetItem, QDialog, \
    QMessageBox, QVBoxLayout, QCheckBox, QProgressDialog, QInputDialog, QLineEdit
import os
import sys
import csv


class FileLoader:
    def __init__(self, main_window, csv_data_table):
        self.csv_data_table = csv_data_table
        self.main_window = main_window

    # Threaded functions for multi threading the loading for handling large files
    def on_loading_finish(self):
        # Change the cursor back to normal
        QApplication.restoreOverrideCursor()
        self.loading_thread.quit()

    def update_loading_progress(self, value):
        # print("reading row: ", value)
        self.loading_progress.setValue(value)

    def set_maximum_progress_value(self, max_value):
        print("Max Progress Value = ", max_value)
        self.loading_progress.setMaximum(max_value)
        self.loading_progress.setValue(0)

    def load_csv(self):
        """
        Loads the file from file selector to a table
        closes any open file if any before opening new file
        """

        csv_file_path = QFileDialog.getOpenFileName(self.main_window, "Load CSV File", "", 'CSV(*.csv)')

        # Proceed if and only if a valid file is selected and the file dialog is not cancelled
        if csv_file_path[0]:
            # Get only the file name from path. eg. 'data_file.csv'
            filepath = os.path.normpath(csv_file_path[0])
            filename = filepath.split(os.sep)
            self.csv_file_name = filename[-1]

            self.loading_progress = QProgressDialog("Reading Rows. Please wait...", None, 0, 100, self.main_window)
            self.loading_progress.setWindowTitle("Loading CSV File...")
            self.loading_progress.setCancelButton(None)

            # enable custom window hint
            self.loading_progress.setWindowFlags(self.loading_progress.windowFlags() | QtCore.Qt.CustomizeWindowHint)
            # disable (but not hide) close button
            self.loading_progress.setWindowFlags(self.loading_progress.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)

            # Show waiting cursor till the time file is being processed
            QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)

            print("Before worker is initialized")

            self.loading_worker = CsvLoaderWorker(csv_file_path=csv_file_path, csv_data_table=self.csv_data_table)

            print("Worker is initialized")

            self.loading_thread = QThread()
            # Set higher priority to the GUI Thread so UI remains a bit smoother
            QThread.currentThread().setPriority(QThread.HighPriority)

            self.loading_worker.moveToThread(self.loading_thread)
            self.loading_worker.workRequested.connect(self.loading_thread.start)
            self.loading_thread.started.connect(self.loading_worker.process_loading_file)
            self.loading_worker.finished.connect(self.on_loading_finish)

            self.loading_worker.relay.connect(self.update_loading_progress)
            self.loading_worker.progress_max.connect(self.set_maximum_progress_value)
            # self.loading_worker.update_bottom_toolbar.connect(self.set_bottom_toolbar_info)

            self.loading_progress.setValue(0)
            self.loading_worker.request_work()


class CsvLoaderWorker(QObject):
    workRequested = pyqtSignal()
    finished = pyqtSignal()
    relay = pyqtSignal(int)
    progress_max = pyqtSignal(int)

    # update_bottom_toolbar = pyqtSignal()

    def __init__(self, csv_file_path, csv_data_table, parent=None):
        super(CsvLoaderWorker, self).__init__(parent)
        self.csv_file_path = csv_file_path
        self.csv_data_table = csv_data_table

    def request_work(self):
        """
        Signal to begin the loading process
        """
        self.workRequested.emit()

    def process_loading_file(self):
        """
        Starts the thread for populating table from the file without blocking the main UI thread
        """
        print("Inside loading file")

        # Open the file once to get idea of the total rowcount to display progress
        with open(self.csv_file_path[0], newline='', encoding="utf-8") as csv_file:
            # print("LEN = ", len(csv_file.readlines()))
            self.progress_max.emit(len(csv_file.readlines()) - 1)

        print("Progress is obtained")
        # TODO: Increase the reading speed by decreasing load on actual table population
        #
        # self.csv_data_table.hide()

        with open(self.csv_file_path[0], newline='', encoding="utf-8") as csv_file:

            print("Opened file for reading")

            csv_file_read = csv.reader(csv_file, delimiter=',', quotechar='|')

            row_index = 0
            for row_data in csv_file_read:
                print("Row = ", row_index)
                self.relay.emit(row_index)

                for column, stuff in enumerate(row_data):
                    item = QTableWidgetItem(stuff)
                    # print(item.text())
                    self.csv_data_table.setItem(row_index, column, item)
                row_index = row_index + 1

        # Stretch to fill the column width according to content
        self.csv_data_table.resizeColumnsToContents()

        # Update the bottom toolbar to reflect changes
        # self.update_bottom_toolbar.emit()
        print("Emitting finish")
        self.finished.emit()
