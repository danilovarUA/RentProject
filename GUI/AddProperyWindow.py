from PyQt5.QtWidgets import QGridLayout, QWidget
from GUI.Templates.Button import Button
from GUI.Templates.Table import Table
from GUI.Templates.Label import Label
from GUI.Templates.LineEntry import LineEntry
from GUI.Templates.DateEntry import DateEntry
from GUI import Text


SIZE_MODIFIER = 0.75


class AddPropertyWidget(QWidget):
    def __init__(self, app, database):
        super().__init__()

        self.app = app
        self.database = database

        self.setWindowTitle(Text.add_agreement_window_name)
        self.resize(int(app.primaryScreen().size().width() * SIZE_MODIFIER),
                    int(app.primaryScreen().size().height() * SIZE_MODIFIER))

        self.main_layout = QGridLayout()
        # self.fields_layout = QGridLayout()
        # self.properties_table_layout = QGridLayout()
        # self.properties_table_controls_and_stats_layout = QGridLayout()
        # self.page_control_layout = QGridLayout()

        # self.main_layout.addLayout(self.fields_layout, 0, 0)
        # self.main_layout.addLayout(self.properties_table_layout, 1, 0)
        # self.main_layout.addLayout(self.properties_table_controls_and_stats_layout, 2, 0)
        # self.main_layout.addLayout(self.page_control_layout, 3, 0)

        # self.setup_fields_layout()
        # self.setup_properties_table_layout()
        # self.setup_properties_table_controls_and_stats_layout()
        # self.setup_page_control_layout()

        self.setLayout(self.main_layout)

        self.show()
