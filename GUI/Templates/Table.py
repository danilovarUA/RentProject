from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5 import QtCore


TABLE_MINIMUM_WIDTH = 25


class Table(QTableWidget):

    def __init__(self,
                 columns,
                 scrolling_off=False,
                 sorting_off=False,
                 table_click_handler=None,
                 item_click_handler=None):
        # Columns is a list of tuples (header, width) if width == 0 MIN_ROW_WIDTH is used instead, if width is None -
        # it will not be specified
        super().__init__()

        if not sorting_off:
            self.setSortingEnabled(True)

        self.verticalHeader().setMinimumSectionSize(TABLE_MINIMUM_WIDTH)
        self.horizontalHeader().setMinimumSectionSize(TABLE_MINIMUM_WIDTH)

        self.setRowCount(0)
        self.setColumnCount(len(columns))

        self.move(0, 0)

        if scrolling_off:
            self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

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

        if item_click_handler is not None:
            self.itemClicked.connect(item_click_handler)


class TableCheckbox(QTableWidgetItem):
    def __init__(self):
        super().__init__()
        self.setFlags(QtCore.Qt.ItemIsEditable |
                      QtCore.Qt.ItemIsSelectable |
                      QtCore.Qt.ItemIsEnabled |
                      QtCore.Qt.ItemIsUserCheckable)
        self.setCheckState(QtCore.Qt.Unchecked)

    def toggle(self):
        if self.checkState() == QtCore.Qt.Unchecked:
            self.setCheckState(QtCore.Qt.Checked)
        else:
            self.setCheckState(QtCore.Qt.Unchecked)
