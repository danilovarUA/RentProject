from PyQt5.QtWidgets import QDateEdit
from PyQt5.QtCore import QDate
from datetime import datetime


class DateEntry(QDateEdit):
    def __init__(self):
        super().__init__(calendarPopup=True)
        self.setDate(QDate(datetime.now()))
