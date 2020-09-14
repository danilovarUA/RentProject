from PyQt5.QtWidgets import QGridLayout, QWidget
from PyQt5.QtCore import QDate, Qt
from GUI.Templates.Button import Button
from GUI.Templates.Table import Table
from GUI.Templates.Label import Label
from GUI.Templates.LineEntry import LineEntry
from GUI.Templates.DateEntry import DateEntry
from GUI.Templates.Popup import Popup
from GUI.PropertyWindow import PropertyWidget
from GUI import Text


SIZE_MODIFIER = 0.7


class AgreementWidget(QWidget):
    def __init__(self, app, database, main_window, agreement_id=-1):
        super().__init__()

        self.main_window = main_window
        self.app = app
        self.database = database
        self.property_window = None

        self.agreement_id = agreement_id

        self.setWindowTitle(Text.add_agreement)
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
        self.properties_table = Table(Text.properties_table,
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
        for row in [(Text.company, self.entry_company),
                    (Text.person, self.entry_person),
                    (Text.recovery, self.entry_recovery),
                    (Text.last_accept_day, self.entry_last_accept_day),
                    (Text.first_payment, self.entry_first_month),
                    (Text.last_payment, self.entry_last_month),
                    (Text.agreement_start, self.entry_start_day),
                    (Text.agreement_end, self.entry_end_day), ]:
            self.fields_layout.addWidget(Label(row[0]), index, 0)
            self.fields_layout.addWidget(row[1], index, 1)
            index += 1

    def setup_properties_table_layout(self):
        self.properties_table_layout.addWidget(self.properties_table, 0, 0)
        self.fill_in_properties_table()

    def fill_in_properties_table(self):
        self.properties_table.clean()
        rows = self.database.get_properties(agreement_id=self.agreement_id)
        for row_index in range(len(rows)):
            row = rows[row_index]
            self.properties_table.add_row(row[0], [row[1], row[2], row[3], row[4]])

    def setup_properties_table_controls_and_stats_layout(self):
        add_property_button = Button(Text.add_property)
        add_property_button.clicked.connect(self.add_property_clicked)
        self.properties_table_controls_and_stats_layout.addWidget(
            add_property_button, 0, 0)

        remove_properties_button = Button(Text.remove_properties)
        remove_properties_button.clicked.connect(self.remove_properties_clicked)
        self.properties_table_controls_and_stats_layout.addWidget(remove_properties_button, 0, 1)

    def add_property_clicked(self):
        self.property_window = PropertyWidget(self.app, self.database, self)

    def setup_page_control_layout(self):
        done_button = Button(Text.save)
        done_button.clicked.connect(self.done_clicked)
        self.page_control_layout.addWidget(done_button, 0, 0)
        close_button = Button(Text.cancel)
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

    def remove_properties_clicked(self):
        properties_to_delete = []
        for index in range(self.properties_table.rowCount()):
            if self.properties_table.item(index, 0).checkState() == Qt.Checked:
                properties_to_delete.append(self.properties_table.item(index, 0).row_id)
        if len(properties_to_delete) == 0:
            Popup("No selected properties to delete.", "Error")
        self.database.remove_properties(ids=properties_to_delete)
        self.fill_in_properties_table()
