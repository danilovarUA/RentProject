from PyQt5.QtWidgets import QGridLayout, QWidget
from GUI.Templates.Button import Button
from GUI.Templates.Table import Table
from GUI.Templates.Label import Label
from GUI.Templates.LineEntry import LineEntry
from GUI.Templates.DateEntry import DateEntry
from GUI import Text


SIZE_MODIFIER = 0.85


class AddAgreementsWidget(QWidget):
    def __init__(self, app, database):
        super().__init__()

        self.app = app
        self.database = database

        self.setWindowTitle(Text.add_agreement_window_name)
        self.resize(int(app.primaryScreen().size().width() * SIZE_MODIFIER),
                    int(app.primaryScreen().size().height() * SIZE_MODIFIER))

        self.main_layout = QGridLayout()
        self.fields_layout = QGridLayout()
        self.properties_table_layout = QGridLayout()
        self.properties_table_controls_and_stats_layout = QGridLayout()
        self.page_control_layout = QGridLayout()

        self.main_layout.addLayout(self.fields_layout, 0, 0)
        self.main_layout.addLayout(self.properties_table_layout, 1, 0)
        self.main_layout.addLayout(self.properties_table_controls_and_stats_layout, 2, 0)
        self.main_layout.addLayout(self.page_control_layout, 3, 0)

        self.setup_fields_layout()
        self.setup_properties_table_layout()
        self.setup_properties_table_controls_and_stats_layout()
        self.setup_page_control_layout()

        self.setLayout(self.main_layout)

        self.show()

    def setup_fields_layout(self):
        self.fields_layout.addWidget(Label(Text.add_agreement_company_label), 0, 0)
        self.fields_layout.addWidget(LineEntry(), 0, 1)

        self.fields_layout.addWidget(Label(Text.add_agreement_person_label), 1, 0)
        self.fields_layout.addWidget(LineEntry(), 1, 1)

        self.fields_layout.addWidget(Label(Text.add_agreement_recovery_label), 2, 0)
        self.fields_layout.addWidget(LineEntry(), 2, 1)

        self.fields_layout.addWidget(Label(Text.add_agreement_last_accept_day), 3, 0)
        self.fields_layout.addWidget(DateEntry(), 3, 1)

        self.fields_layout.addWidget(Label(Text.add_agreement_first_payment), 4, 0)
        self.fields_layout.addWidget(LineEntry(), 4, 1)

        self.fields_layout.addWidget(Label(Text.add_agreement_last_month_payment), 5, 0)
        self.fields_layout.addWidget(LineEntry(), 5, 1)

        self.fields_layout.addWidget(Label(Text.add_agreement_start_day_label), 6, 0)
        self.fields_layout.addWidget(DateEntry(), 6, 1)

        self.fields_layout.addWidget(Label(Text.add_agreement_end_day_label), 7, 0)
        self.fields_layout.addWidget(DateEntry(), 7, 1)

    def setup_properties_table_layout(self):
        self.properties_table_layout.addWidget(Table(Text.properties_table_fields), 0, 0)

    def setup_properties_table_controls_and_stats_layout(self):
        self.properties_table_controls_and_stats_layout.addWidget(
            Button(Text.add_agreement_add_property_button), 0, 0)
        self.properties_table_controls_and_stats_layout.addWidget(
            Button(Text.add_agreement_remove_properties_button), 0, 1)

    def setup_page_control_layout(self):
        self.page_control_layout.addWidget(Button(Text.add_agreement_add_button), 0, 0)
        self.page_control_layout.addWidget(Button(Text.add_agreement_cancel_button), 0, 1)
