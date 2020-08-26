from PyQt5.QtWidgets import QMessageBox


class Popup(QMessageBox):
    def __init__(self, text, title=None):
        super().__init__()
        if title is None:
            title = text
        self.setWindowTitle(title)
        self.setText(text)
        self.exec_()
