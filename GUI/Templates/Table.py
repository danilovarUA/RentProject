from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5 import QtCore
from GUI.Templates.TextWidget import TextWidget


TABLE_MINIMUM_WIDTH = 25
TABLE_ROW_HEIGHT = TABLE_MINIMUM_WIDTH
# Columns is a list of tuples (header, width) if width == 0 MIN_ROW_WIDTH is used instead, if width is None -
#   it will not be specified


class Table(QTableWidget):
    def __init__(self,
                 columns,
                 scrolling=True,
                 sorting=True,
                 table_click_handler=None,
                 item_click_handler=None,
                 table_doubleclick_handler=None):
        super().__init__()
        self.columns = columns
        self.setSortingEnabled(sorting)
        if not scrolling:
            self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.verticalHeader().setMinimumSectionSize(TABLE_MINIMUM_WIDTH)
        self.horizontalHeader().setMinimumSectionSize(TABLE_MINIMUM_WIDTH)
        self.clean()

        headers = [column[0] for column in columns]
        self.setHorizontalHeaderLabels(headers)

        widths = [column[1] for column in columns]
        for index in range(len(widths)):
            width = widths[index]
            if width is None:
                continue
            if width == 0:
                width = TABLE_MINIMUM_WIDTH
            self.setColumnWidth(index, width)

        if table_click_handler is not None:
            self.clicked.connect(table_click_handler)

        if table_doubleclick_handler is not None:
            self.doubleClicked.connect(table_doubleclick_handler)

        if item_click_handler is not None:
            self.itemClicked.connect(item_click_handler)

    def add_row(self, index, data):
        if len(data) + 1 != len(self.columns):
            raise ValueError("{} columns expected, {} received".format(len(self.columns), len(data)))
        row_index = self.rowCount()
        self.setRowCount(row_index + 1)
        self.setRowHeight(row_index, TABLE_ROW_HEIGHT)
        self.setItem(row_index, 0, TableCheckbox(index))
        for counter in range(0, len(data)):
            self.setItem(row_index, counter+1, TextWidget(data[counter]))

    def clean(self):
        self.setRowCount(0)
        self.setColumnCount(len(self.columns))
        #self.move(0, 0)


class TableCheckbox(QTableWidgetItem):
    def __init__(self, row_id):
        super().__init__()
        self.setFlags(QtCore.Qt.ItemIsEditable |
                      QtCore.Qt.ItemIsSelectable |
                      QtCore.Qt.ItemIsEnabled |
                      QtCore.Qt.ItemIsUserCheckable)
        self.setCheckState(QtCore.Qt.Unchecked)
        self.row_id = row_id

    def toggle(self):
        if self.checkState() == QtCore.Qt.Unchecked:
            self.setCheckState(QtCore.Qt.Checked)
        else:
            self.setCheckState(QtCore.Qt.Unchecked)

