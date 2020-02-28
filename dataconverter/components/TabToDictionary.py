import json
import logging

from PyQt5.QtWidgets import QFileDialog, QMessageBox


class TabToDictionary:
    main_window = None

    @staticmethod
    def tab_data_to_dict(tab, tab_name):
        tab_module_name = tab.property("module_name")
        logging.info("Tab Module: {}".format(tab_module_name))
        logging.info("Tab Name: {}".format(tab_name))

        save_directory = str(QFileDialog.getExistingDirectory(TabToDictionary.main_window, "Select Directory"))

        if save_directory:
            header_names = []
            for col_index in range(0, tab.columnCount()):
                header_names.append(tab.horizontalHeaderItem(col_index).text())

            # Row of table
            for row_index in range(0, tab.rowCount()):
                is_complete_row_empty = True
                dict_to_save = {}
                row_id = None

                # Column of table
                for col_index in range(0, tab.columnCount()):
                    item = tab.item(row_index, col_index)

                    # Check if the cell is not empty
                    if item and item.text():
                        is_complete_row_empty = False
                        dict_to_save[header_names[col_index]] = item.text()

                        if col_index == 0:
                            row_id = item.text()

                if is_complete_row_empty:
                    break

                output_row = json.dumps(dict_to_save).replace("{", "").replace("}", "")
                with open(save_directory + "/{}_{}.txt".format(tab_module_name, row_id), "w") as output_file:
                    output_file.write(output_row)

                    logging.info(output_row)

            logging.info("The files have been saved to directory {}".format(save_directory))
            TabToDictionary.show_file_saved_success(save_directory)

    @staticmethod
    def show_file_saved_success(save_directory):
        msg = QMessageBox(TabToDictionary.main_window)
        msg.setIcon(QMessageBox.Information)
        msg.setText("Data saved successfully!")
        ok_msg = "Your data has been saved successfully inside {}/".format(save_directory)
        msg.setInformativeText(ok_msg)
        msg.setWindowTitle("Data save successful!")
        msg.exec_()
