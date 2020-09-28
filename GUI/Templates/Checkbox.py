from PyQt5.QtWidgets import QCheckBox


class Checkbox(QCheckBox):
    def __init__(self, text):
        super().__init__(text)
