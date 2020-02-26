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

    def load_csv(self):
        print("loading csv")
        # Close the start page tab and load the file tab
        # self.tabWidget.removeTab(0)
        # self.tabWidget.insertTab(1, self.csv_table_tab, "Main Document")
        # Disable cell change check to avoid crashes

        csv_file_path = QFileDialog.getOpenFileName(self.main_window, "Load CSV File", "", 'CSV(*.csv)')

        # Proceed if and only if a valid file is selected and the file dialog is not cancelled
        if csv_file_path[0]:
            with open(csv_file_path[0], newline='', encoding="utf-8") as csv_file:

                # self.csv_data_table.setRowCount(0)
                # self.csv_data_table.setColumnCount(0)

                csv_file_read = csv.reader(csv_file, delimiter=',', quotechar='|')

                # Fetch the column headers and move the iterator to actual data
                # column_headers = next(csv_file_read)
                row_index = 0
                for row_data in csv_file_read:
                    print("Row = ", row_index)
                    # row = self.csv_data_table.rowCount()
                    # self.csv_data_table.insertRow(row)
                    # self.csv_data_table.setColumnCount(len(row_data))
                    for column, stuff in enumerate(row_data):
                        item = QTableWidgetItem(stuff)
                        print(item.text())
                        self.csv_data_table.setItem(row_index, column, item)
                    row_index = row_index + 1

            # Set WordWrap to True to make the cells change height according to content
            # Currently set it to false as it looks very decent and makes cell size uniform throughout
            # self.csv_data_table.setWordWrap(False)
            # Uncomment below line to stretch to fill the column width according to content
            self.csv_data_table.resizeColumnsToContents()

            self.check_cell_change = True

            print("End of function")

            # Close the start page tab and load the file tab
            # self.tabWidget.removeTab(0)
            # self.tabWidget.insertTab(1, self.csv_table_tab, "Main Document")
