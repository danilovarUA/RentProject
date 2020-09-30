from PyQt5.QtWidgets import QGridLayout, QWidget
from PyQt5.QtCore import QDate, Qt
from GUI.Templates.Button import Button
from GUI.Templates.Table import Table
from GUI.Templates.Label import Label
from GUI.Templates.TextEntry import TextEntry
from GUI.Templates.DateEntry import DateEntry
from GUI.Templates.Popup import Popup
from GUI.Templates.Checkbox import Checkbox
from GUI.PropertyWindow import PropertyWidget
from GUI.Templates.Line import VLine
from GUI.Templates.NumberEntry import NumberEntry
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

        self.entry_company = TextEntry()
        self.entry_person = TextEntry()
        self.entry_recovery = NumberEntry(min_value=0)
        self.entry_last_accept_day = DateEntry()
        self.entry_monthly_price = TextEntry()
        self.entry_last_month_prepay = Checkbox()
        self.entry_pay_before_day = NumberEntry(min_value=1, step=31, value=10)
        self.entry_first_payment_price = NumberEntry(min_value=0)
        self.entry_second_payment_price = NumberEntry(min_value=0)
        self.entry_first_payment_day = DateEntry()
        self.entry_second_payment_day = DateEntry()
        self.entry_first_stop_day = DateEntry()
        self.entry_second_stop_day = DateEntry()
        self.entry_start_day = DateEntry()
        self.entry_end_day = DateEntry()
        self.entry_edrpou = TextEntry()
        self.entry_address = TextEntry()
        self.entry_ipn = TextEntry()
        self.entry_iban = TextEntry()
        self.entry_swift = TextEntry()
        self.table = Table(Text.properties_table,
                           table_doubleclick_handler=self.handler_doubleclick_table)
        self.setLayout(self.setup_layout())
        if agreement_id != -1:
            self.fill_in_fields()

        self.show()

    def setup_layout(self):
        layout_main = QGridLayout()
        layout_fields = QGridLayout()
        layout_fields_column1 = QGridLayout()
        layout_fields_column2 = QGridLayout()
        layout_table = QGridLayout()
        layout_table_controls = QGridLayout()
        layout_control = QGridLayout()
        layout_fields.addLayout(layout_fields_column1, 0, 0)
        layout_fields.addWidget(VLine(), 0, 1)
        layout_fields.addLayout(layout_fields_column2, 0, 2)
        layout_main.addLayout(layout_fields, 0, 0)
        layout_main.addLayout(layout_table, 1, 0)
        layout_main.addLayout(layout_table_controls, 2, 0)
        layout_main.addLayout(layout_control, 3, 0)

        index = 0
        for row in [(Text.company, self.entry_company),
                    (Text.person, self.entry_person),
                    (Text.recovery, self.entry_recovery),
                    (Text.last_accept_day, self.entry_last_accept_day),
                    (Text.monthly_payment, self.entry_monthly_price),
                    (Text.last_month_prepay, self.entry_last_month_prepay),
                    (Text.agreement_start, self.entry_start_day),
                    (Text.agreement_end, self.entry_end_day),
                    (Text.pay_before_day, self.entry_pay_before_day),
                    (Text.first_payment_price, self.entry_first_payment_price),
                    ]:
            layout_fields_column1.addWidget(Label(row[0]), index, 0)
            layout_fields_column1.addWidget(row[1], index, 1)
            index += 1
        index = 0
        for row in [(Text.second_payment_price, self.entry_second_payment_price),
                (Text.first_payment_day, self.entry_first_payment_day),
                (Text.second_payment_day, self.entry_second_payment_day),
                (Text.first_stop_day, self.entry_first_stop_day),
                (Text.second_stop_day, self.entry_second_stop_day),
                (Text.edrpou, self.entry_edrpou),
                (Text.address, self.entry_address),
                (Text.ipn, self.entry_ipn),
                (Text.iban, self.entry_iban),
                (Text.swift, self.entry_swift),]:
            layout_fields_column2.addWidget(Label(row[0]), index, 3)
            layout_fields_column2.addWidget(row[1], index, 4)
            index += 1

        layout_table.addWidget(self.table, 0, 0)
        self.fill_in_table()

        button_add_property = Button(Text.add_property)
        button_remove_property = Button(Text.remove_properties)
        button_add_property.clicked.connect(self.handler_click_add_property)
        button_remove_property.clicked.connect(self.handler_click_remove_properties)
        layout_table_controls.addWidget(button_add_property, 0, 0)
        layout_table_controls.addWidget(button_remove_property, 0, 1)

        button_done = Button(Text.save)
        button_close = Button(Text.cancel)
        button_done.clicked.connect(self.handler_click_done)
        button_close.clicked.connect(self.close)
        layout_control.addWidget(button_close, 0, 1)
        layout_control.addWidget(button_done, 0, 0)

        return layout_main

    def fill_in_table(self):
        self.table.clean()
        rows = self.database.get_properties(agreement_id=self.agreement_id)
        for row_index in range(len(rows)):
            row = rows[row_index]
            self.table.add_row(row[0], [row[1], row[2], row[3], row[4]])

    def handler_click_add_property(self):
        self.property_window = PropertyWidget(self.app, self.database, self)

    def handler_click_done(self):
        data = {"company": self.entry_company.text(),
                "person": self.entry_person.text(),
                "recovery_price": self.entry_recovery.text(),
                "last_accept_day": self.entry_last_accept_day.text(),
                "first_payment": self.entry_monthly_price.text(),
                "last_same_payment": self.entry_last_month_prepay.text(),
                "start_day": self.entry_start_day.text(),
                "end_day": self.entry_end_day.text()}
        result = self.database.set_agreement(data, self.agreement_id)
        if not result:
            Popup(Text.error_invalid_input, Text.error)
        else:
            if not self.database.assign_properties():
                Popup(Text.error_adding_data, Text.error)
        self.main_window.fill_in_table()
        self.close()

    def fill_in_fields(self):
        rows = self.database.get_agreements(index=self.agreement_id)
        if len(rows) <= 0:
            self.close()
            Popup(Text.error_non_existent_data, Text.error)
            return
        fields = rows[0]
        self.entry_company.setText(str(fields[1]))
        self.entry_person.setText(str(fields[2]))
        self.entry_recovery.setText(str(fields[3]))
        self.entry_last_accept_day.setDate(QDate.fromString(fields[4], 'dd-MM-yyyy'))
        self.entry_monthly_price.setText(str(fields[5]))
        self.entry_last_month_prepay.setText(str(fields[6]))
        self.entry_start_day.setDate(QDate.fromString(fields[7], 'dd-MM-yyyy'))
        self.entry_end_day.setDate(QDate.fromString(fields[8], 'dd-MM-yyyy'))

    def handler_doubleclick_table(self, event):
        index = self.table.item(event.row(), 0).row_id
        print(event.row())
        self.property_window = PropertyWidget(self.app, self.database, self, index)

    def closeEvent(self, close_event=None):
        self.database.remove_agreements([-1])

    def handler_click_remove_properties(self):
        properties_to_delete = []
        for index in range(self.table.rowCount()):
            if self.table.item(index, 0).checkState() == Qt.Checked:
                properties_to_delete.append(self.table.item(index, 0).row_id)
        if len(properties_to_delete) == 0:
            Popup(Text.error_selection_missing, Text.error)
        self.database.remove_properties(ids=properties_to_delete)
        self.fill_in_table()
