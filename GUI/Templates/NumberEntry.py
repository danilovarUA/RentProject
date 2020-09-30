from PyQt5.QtWidgets import QSpinBox


class NumberEntry(QSpinBox):
    def __init__(self, value=0, min_value=0, max_value=None, step=1):
        super().__init__()
        self.setValue(value)
        self.setMinimum(min_value)
        if max_value is not None:
            self.setMaximum(max_value)
        # self.setSingleStep(step)
