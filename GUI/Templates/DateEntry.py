from PyQt5.QtWidgets import QDateEdit
from PyQt5.QtCore import QDate


class DateEntry(QDateEdit):
    def __init__(self):
        super().__init__(calendarPopup=True)
        # date = QDate.fromString('2020-08-27', 'yyyy-MM-dd')
        # self.date = "01/01/2020"
