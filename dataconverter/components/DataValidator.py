import logging

from PyQt5.QtWidgets import QMessageBox


class DataValidator():
    main_window = None

    @staticmethod
    def is_number(x):
        """ Returns True is string is a number. """
        """https://stackoverflow.com/a/23639915/4126370"""
        return x.replace('.', '', 1).isdigit()

    @staticmethod
    def show_not_number_error(tab_name, header_name, row, col, value):
        msg = QMessageBox(DataValidator.main_window)
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Non-numerical input incurred")
        error_msg = "All cells other than headers should only take numerical inputs.\n\nError in {} Tab:\n\nColumn: {}\nRow: {}\nValue: {}".format(
            tab_name,
            header_name, row + 1, value)
        msg.setInformativeText(error_msg)
        msg.setWindowTitle("Validation Error")
        msg.exec_()

    @staticmethod
    def show_file_empty_error(tab_name):
        msg = QMessageBox(DataValidator.main_window)
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Empty File Error")
        error_msg = "The content of the spreadsheet can not be blank, and thus can not be validated.\n\nError in {} Tab".format(
            tab_name)
        msg.setInformativeText(error_msg)
        msg.setWindowTitle("Validation Error")
        msg.exec_()

    @staticmethod
    def show_missing_value_error(tab_name, header_name, row, col):
        msg = QMessageBox(DataValidator.main_window)
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Empty input incurred")
        error_msg = "The content of the cell can not be blank, please fill in a numerical value.\n\nError in {} Tab:\n\nColumn: {}\nRow: {}".format(
            tab_name,
            header_name, row + 1)
        msg.setInformativeText(error_msg)
        msg.setWindowTitle("Validation Error")
        msg.exec_()

    @staticmethod
    def show_duplicate_id_error(tab_name, header_name, row, col, value):
        msg = QMessageBox(DataValidator.main_window)
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Duplicate ID found")
        error_msg = "ID column shall be unique, i.e., ID number should not be repeated\n\nError in {} Tab:\n\nColumn: {}\nRow: {}\nDuplicate Value: {}".format(
            tab_name,
            header_name, row + 1, value)
        msg.setInformativeText(error_msg)
        msg.setWindowTitle("Validation Error")
        msg.exec_()

    @staticmethod
    def show_validation_complete(proceed_to_save=False):
        msg = QMessageBox(DataValidator.main_window)
        msg.setIcon(QMessageBox.Information)
        msg.setText("Validation Complete")
        ok_msg = "Your data is valid"
        if proceed_to_save:
            ok_msg = "Your data is valid, choose a directory to save your files after clicking OK"
        msg.setInformativeText(ok_msg)
        msg.setWindowTitle("Validation Complete")
        msg.exec_()

    @staticmethod
    def is_valid(tab, tab_name, proceed_to_save=False):
        is_error_incurred = False

        id_set = set()

        # Row of table
        for row_index in range(0, tab.rowCount()):
            is_complete_row_empty = True
            is_missing_value = (False, 0)
            # Column of table
            for col_index in range(0, tab.columnCount()):
                item = tab.item(row_index, col_index)

                # Check if the cell is not empty
                if item and item.text():
                    # logging.info(item.text(), end=", ")
                    is_complete_row_empty = False

                    if not DataValidator.is_number(item.text()):
                        is_error_incurred = True
                        tab.setCurrentCell(row_index, col_index)
                        header_name = tab.horizontalHeaderItem(col_index).text()
                        DataValidator.show_not_number_error(tab_name, header_name, row_index, col_index, item.text())
                        break

                    if col_index == 0:  # ID Column
                        # Duplicate value is found for ID column
                        if int(float(item.text())) in id_set:
                            is_error_incurred = True
                            header_name = tab.horizontalHeaderItem(col_index).text()
                            DataValidator.show_duplicate_id_error(tab_name, header_name, row_index, col_index,
                                                                  item.text())
                        else:
                            id_set.add(int(float(item.text())))
                else:
                    is_missing_value = (True, col_index)

            if is_complete_row_empty:
                if row_index == 0:
                    is_error_incurred = True
                    DataValidator.show_file_empty_error(tab_name)
                break

            if is_missing_value[0]:
                is_error_incurred = True
                tab.setCurrentCell(row_index, is_missing_value[1])
                header_name = tab.horizontalHeaderItem(is_missing_value[1]).text()
                DataValidator.show_missing_value_error(tab_name, header_name, row_index, is_missing_value[1])

            if is_error_incurred:
                return False

        if not is_error_incurred:
            logging.info("\nCompleted Validation")
            DataValidator.show_validation_complete(proceed_to_save)
            return True
