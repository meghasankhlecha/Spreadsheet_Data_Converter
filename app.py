import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QAction, QMessageBox


class DataConverter(QMainWindow):

    def __init__(self, windowTitle="Spreadsheet to Data Converter"):
        super(DataConverter, self).__init__()
        uic.loadUi('mainwindow.ui', self)

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
