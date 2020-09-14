from PyQt5.QtWidgets import QGridLayout, QWidget
from GUI.Templates.Button import Button
from GUI.Templates.Table import Table, TableCheckbox
from GUI.Templates.Label import Label
from GUI.Templates.LineEntry import LineEntry
from GUI.Templates.DateEntry import DateEntry
from GUI.Templates.Popup import Popup
from GUI.AddProperyWindow import AddPropertyWidget
from GUI.Templates.TextWidget import TextWidget
from GUI import Text


TABLE_ROW_HEIGHT = 25
SIZE_MODIFIER = 0.85


class AgreementWidget(QWidget):
    def __init__(self, app, database, main_window, agreement_id=None):
        super().__init__()

        self.main_window = main_window
        self.app = app
        self.database = database
        self.add_property_window = None

        self.setWindowTitle(Text.add_agreement_window_name)
        self.resize(int(app.primaryScreen().size().width() * SIZE_MODIFIER),
                    int(app.primaryScreen().size().height() * SIZE_MODIFIER))

        self.main_layout = QGridLayout()
        self.fields_layout = QGridLayout()
        self.properties_table_layout = QGridLayout()
        self.properties_table_controls_and_stats_layout = QGridLayout()
        self.page_control_layout = QGridLayout()

        self.entry_company = LineEntry()
        self.entry_person = LineEntry()
        self.entry_recovery = LineEntry()
        self.entry_last_accept_day = DateEntry()
        self.entry_fist_month = LineEntry()
        self.entry_last_month = LineEntry()
        self.entry_start_day = DateEntry()
        self.entry_end_day = DateEntry()
        self.properties_table = Table(Text.properties_table_fields)

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
        index = 0
        for row in [(Text.add_agreement_company_label, self.entry_company),
                    (Text.add_agreement_person_label, self.entry_person),
                    (Text.add_agreement_recovery_label, self.entry_recovery),
                    (Text.add_agreement_last_accept_day, self.entry_last_accept_day),
                    (Text.add_agreement_first_payment, self.entry_fist_month),
                    (Text.add_agreement_last_month_payment, self.entry_last_month),
                    (Text.add_agreement_start_day_label, self.entry_start_day),
                    (Text.add_agreement_end_day_label, self.entry_end_day),]:
            self.fields_layout.addWidget(Label(row[0]), index, 0)
            self.fields_layout.addWidget(row[1], index, 1)
            index += 1

    def setup_properties_table_layout(self):
        self.properties_table_layout.addWidget(self.properties_table, 0, 0)

    def fill_in_properties_table(self):
        rows = self.database.get_properties_by_agreement(-1)
        self.properties_table.setRowCount(len(rows))
        for row_index in range(len(rows)):
            row = rows[row_index]
            self.properties_table.setRowHeight(row_index, TABLE_ROW_HEIGHT)
            checkbox = TableCheckbox(row[0])
            self.properties_table.setItem(row_index, 0, checkbox)
            self.properties_table.setItem(row_index, 1, TextWidget(row[1]))
            self.properties_table.setItem(row_index, 2, TextWidget(row[2]))
            self.properties_table.setItem(row_index, 3, TextWidget(row[3]))
            self.properties_table.setItem(row_index, 4, TextWidget(row[4]))

    def setup_properties_table_controls_and_stats_layout(self):
        add_property_button = Button(Text.add_agreement_add_property_button)
        add_property_button.clicked.connect(self.add_property_clicked)
        self.properties_table_controls_and_stats_layout.addWidget(
            add_property_button, 0, 0)
        self.properties_table_controls_and_stats_layout.addWidget(
            Button(Text.add_agreement_remove_properties_button), 0, 1)

    def add_property_clicked(self):
        self.add_property_window = AddPropertyWidget(self.app, self.database, self)

    def setup_page_control_layout(self):
        done_button = Button(Text.add_agreement_add_button)
        done_button.clicked.connect(self.done_clicked)
        print("set up clicked connection")
        self.page_control_layout.addWidget(done_button, 0, 0)
        self.page_control_layout.addWidget(Button(Text.add_agreement_cancel_button), 0, 1)

    def done_clicked(self):
        data = {"company": self.entry_company.text(),
                "person": self.entry_person.text(),
                "recovery_price": self.entry_recovery.text(),
                "last_accept_day": self.entry_last_accept_day.text(),
                "first_payment": self.entry_fist_month.text(),
                "last_same_payment": self.entry_last_month.text(),
                "start_day": self.entry_start_day.text(),
                "end_day": self.entry_end_day.text()}
        result = self.database.add_agreement(data)
        if not result:
            Popup("Some fields were not validated", "Error")
        else:
            if not self.database.assign_properties():
                Popup("Something went wrong when adding properties", "Error")
        self.main_window.fill_in_table()
        self.close()
