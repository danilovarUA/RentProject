from PyQt5.QtWidgets import QCheckBox


class Checkbox(QCheckBox):
    def __init__(self, text="", click_handler=None):
        super().__init__(text)
        if click_handler is not None:
            self.clicked.connect(click_handler)
