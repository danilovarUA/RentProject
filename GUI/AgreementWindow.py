from PyQt5.QtWidgets import QGridLayout, QWidget
from PyQt5.QtCore import QDate
from GUI.Templates.Button import Button
from GUI.Templates.Table import Table, TableCheckbox
from GUI.Templates.Label import Label
from GUI.Templates.LineEntry import LineEntry
from GUI.Templates.DateEntry import DateEntry
from GUI.Templates.Popup import Popup
from GUI.PropertyWindow import PropertyWidget
from GUI.Templates.TextWidget import TextWidget
from GUI import Text


TABLE_ROW_HEIGHT = 25
SIZE_MODIFIER = 0.85


class AgreementWidget(QWidget):
    def __init__(self, app, database, main_window, agreement_id=-1):
        super().__init__()

        self.main_window = main_window
        self.app = app
        self.database = database
        self.property_window = None

        self.agreement_id = agreement_id

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
        self.entry_first_month = LineEntry()
        self.entry_last_month = LineEntry()
        self.entry_start_day = DateEntry()
        self.entry_end_day = DateEntry()
        self.properties_table = Table(Text.properties_table_fields,
                                      table_doubleclick_handler=self.property_select_handler)

        self.main_layout.addLayout(self.fields_layout, 0, 0)
        self.main_layout.addLayout(self.properties_table_layout, 1, 0)
        self.main_layout.addLayout(self.properties_table_controls_and_stats_layout, 2, 0)
        self.main_layout.addLayout(self.page_control_layout, 3, 0)

        self.setup_fields_layout()
        self.setup_properties_table_layout()
        self.setup_properties_table_controls_and_stats_layout()
        self.setup_page_control_layout()

        self.setLayout(self.main_layout)

        if agreement_id != -1:
            self.fill_in_fields()

        self.show()

    def setup_fields_layout(self):
        index = 0
        for row in [(Text.add_agreement_company_label, self.entry_company),
                    (Text.add_agreement_person_label, self.entry_person),
                    (Text.add_agreement_recovery_label, self.entry_recovery),
                    (Text.add_agreement_last_accept_day, self.entry_last_accept_day),
                    (Text.add_agreement_first_payment, self.entry_first_month),
                    (Text.add_agreement_last_month_payment, self.entry_last_month),
                    (Text.add_agreement_start_day_label, self.entry_start_day),
                    (Text.add_agreement_end_day_label, self.entry_end_day),]:
            self.fields_layout.addWidget(Label(row[0]), index, 0)
            self.fields_layout.addWidget(row[1], index, 1)
            index += 1

    def setup_properties_table_layout(self):
        self.properties_table_layout.addWidget(self.properties_table, 0, 0)
        self.fill_in_properties_table()

    def fill_in_properties_table(self):
        rows = self.database.get_properties(agreement_id=self.agreement_id)
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
        self.property_window = PropertyWidget(self.app, self.database, self.agreement_id, self)

    def setup_page_control_layout(self):
        done_button = Button(Text.add_agreement_add_button)
        done_button.clicked.connect(self.done_clicked)
        self.page_control_layout.addWidget(done_button, 0, 0)
        close_button = Button(Text.add_agreement_cancel_button)
        close_button.clicked.connect(self.close)
        self.page_control_layout.addWidget(close_button, 0, 1)

    def done_clicked(self):
        data = {"company": self.entry_company.text(),
                "person": self.entry_person.text(),
                "recovery_price": self.entry_recovery.text(),
                "last_accept_day": self.entry_last_accept_day.text(),
                "first_payment": self.entry_first_month.text(),
                "last_same_payment": self.entry_last_month.text(),
                "start_day": self.entry_start_day.text(),
                "end_day": self.entry_end_day.text()}
        result = self.database.set_agreement(data, self.agreement_id)
        if not result:
            Popup("Some fields were not validated", "Error")
        else:
            if not self.database.assign_properties():
                Popup("Something went wrong when adding properties", "Error")
        self.main_window.fill_in_table()
        self.close()

    def fill_in_fields(self):
        rows = self.database.get_agreements(index=self.agreement_id)
        if len(rows) <= 0:
            # TODO popup and close window
            raise ValueError("Something went wrong - there is no agreement like that")
        agreement_fields = rows[0]
        self.entry_company.setText(str(agreement_fields[1]))
        self.entry_person.setText(str(agreement_fields[2]))
        self.entry_recovery.setText(str(agreement_fields[3]))
        self.entry_last_accept_day.setDate(QDate.fromString(agreement_fields[4], 'dd-MM-yyyy'))
        self.entry_first_month.setText(str(agreement_fields[5]))
        self.entry_last_month.setText(str(agreement_fields[6]))
        self.entry_start_day.setDate(QDate.fromString(agreement_fields[7], 'dd-MM-yyyy'))
        self.entry_end_day.setDate(QDate.fromString(agreement_fields[8], 'dd-MM-yyyy'))

    def property_select_handler(self, event):
        index = self.properties_table.item(event.row(), 0).row_id
        print(event.row())
        self.property_window = PropertyWidget(self.app, self.database, self, index)

    def closeEvent(self, close_event=None):
        self.database.remove_agreements([-1])

