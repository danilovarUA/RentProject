from PyQt5.QtWidgets import QGridLayout, QWidget
from GUI.Templates.Button import Button
from GUI.Templates.Table import Table
from GUI.Templates.Label import Label
from GUI.Templates.LineEntry import LineEntry
from GUI import Text


SIZE_MODIFIER = 0.8


class AddAgreementsWidget(QWidget):
    def __init__(self, app, database):
        super().__init__()

        self.app = app
        self.database = database

        self.setWindowTitle(Text.agreements_window_name)
        self.resize(int(app.primaryScreen().size().width() * SIZE_MODIFIER),
                    int(app.primaryScreen().size().height() * SIZE_MODIFIER))

        self.main_layout = QGridLayout()
        self.company_layout = QGridLayout()
        self.person_layout = QGridLayout()
        self.recovery_and_info_layout = QGridLayout()
        self.properties_layout = QGridLayout()
        self.table_controls_and_stats_layout = QGridLayout()
        self.payments_layout = QGridLayout()
        self.start_and_end_dates_layout = QGridLayout()
        self.form_control_layout = QGridLayout()
        self.recovery_layout = QGridLayout()
        self.info_layout = QGridLayout()
        self.table_controls_layout = QGridLayout()
        self.table_stats_layout = QGridLayout()

        self.recovery_and_info_layout.addLayout(self.recovery_layout, 0, 0)
        self.recovery_and_info_layout.addLayout(self.info_layout, 0, 1)

        self.table_controls_and_stats_layout.addLayout(self.table_controls_layout, 0, 0)
        self.table_controls_and_stats_layout.addLayout(self.table_stats_layout, 0, 1)

        self.main_layout.addLayout(self.company_layout, 0, 0)
        self.main_layout.addLayout(self.person_layout, 1, 0)
        self.main_layout.addLayout(self.recovery_and_info_layout, 2, 0)
        self.main_layout.addLayout(self.properties_layout, 3, 0)
        self.main_layout.addLayout(self.table_controls_and_stats_layout, 4, 0)
        self.main_layout.addLayout(self.payments_layout, 5, 0)
        self.main_layout.addLayout(self.start_and_end_dates_layout, 6, 0)
        self.main_layout.addLayout(self.form_control_layout, 7, 0)

        self.setup_company_layout()
        self.setup_person_layout()
        self.setup_recovery_layout()
        self.setup_info_layout()
        self.setup_properties_layout()
        self.setup_table_controls_layout()
        self.setup_table_stats_layout()
        self.setup_payments_layout()
        self.setup_start_and_end_dates_layout()
        self.setup_form_control_layout()

        self.setLayout(self.main_layout)

        self.show()

    def setup_company_layout(self):
        self.company_layout.addWidget(Label("Company"), 0, 0)
        self.company_layout.addWidget(LineEntry(), 0, 1)

    def setup_person_layout(self):
        self.person_layout.addWidget(Label("Person"), 0, 0)
        self.person_layout.addWidget(LineEntry(), 0, 1)

    def setup_recovery_layout(self):
        self.recovery_layout.addWidget(Label("Recovery Price"), 0, 0)
        self.recovery_layout.addWidget(LineEntry(), 0, 1)

    def setup_info_layout(self):
        self.info_layout.addWidget(Label("Some useful information here olololololololol"), 0, 0)

    def setup_properties_layout(self):
        self.properties_layout.addWidget(Table(Text.properties_table_fields), 0, 0)

    def setup_table_controls_layout(self):
        self.table_controls_layout.addWidget(Button("Add Property"), 0, 0)
        self.table_controls_layout.addWidget(Button("Remove Properties"), 0, 1)

    def setup_table_stats_layout(self):
        self.table_stats_layout.addWidget(Label("Total area: XX"), 0, 0)
        self.table_stats_layout.addWidget(Label("Total Price: XX"), 0, 1)

    def setup_payments_layout(self):
        self.payments_layout.addWidget(Label("First payment amount"), 0, 0)
        self.payments_layout.addWidget(LineEntry(), 0, 1)
        self.payments_layout.addWidget(Label("Last month as well"), 0, 2)
        self.payments_layout.addWidget(LineEntry(), 0, 3)

    def setup_start_and_end_dates_layout(self):
        self.start_and_end_dates_layout.addWidget(Label("Contract starts"), 0, 0)
        self.start_and_end_dates_layout.addWidget(LineEntry(), 0, 1)
        self.start_and_end_dates_layout.addWidget(Label("Contract starts"), 1, 0)
        self.start_and_end_dates_layout.addWidget(LineEntry(), 1, 1)

    def setup_form_control_layout(self):
        self.form_control_layout.addWidget(Button("Add"))
        self.form_control_layout.addWidget(Button("Cancel"))
