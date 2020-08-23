from PyQt5.QtWidgets import QGridLayout, QWidget
from GUI.Template.Button import Button


class MainWidget(QWidget):
    def __init__(self, width, height):
        super().__init__()
        print("super inited")
        self.setWindowTitle("Lol")
        self.resize(width, height)
        print("{}:{} - size".format(width, height))
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.tab_widget = Button("Lol")
        layout.addWidget(self.tab_widget)

        self.setLayout(layout)

        self.show()
        print("showing")