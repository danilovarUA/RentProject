from PyQt5.QtWidgets import QApplication
from GUI.MainWindow import MainWidget
import sys
from Storage import Database


def startup_tasks():
    # TODO if there is a property with -1 - remove it

    pass


def main():
    database = Database()
    startup_tasks()
    app = QApplication([])
    main_window = MainWidget(app, database)
    exec_code = app.exec_()
    sys.exit(exec_code)


main()
