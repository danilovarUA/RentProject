from PyQt5.QtWidgets import QGridLayout, QWidget
from PyQt5.QtCore import Qt
from GUI.Templates.Button import Button
from GUI.Templates.Table import Table
from GUI.Templates.Popup import Popup
from GUI import Text
from GUI.AgreementWindow import AgreementWidget


SIZE_MODIFIER = 0.8


class MainWidget(QWidget):
    def __init__(self, app, database):
        super().__init__()
        self.app = app
        self.database = database
        self.contract_window = None
        self.table = None
        self.setWindowTitle(Text.agreements)
        self.resize(int(app.primaryScreen().size().width() * SIZE_MODIFIER),
                    int(app.primaryScreen().size().height() * SIZE_MODIFIER))
        self.setLayout(self.setup_layout())
        self.fill_in_table()
        self.show()

    def setup_layout(self):
        layout_main = QGridLayout()
        layout_buttons = QGridLayout()
        layout_table = QGridLayout()
        layout_table_controls = QGridLayout()

        layout_main.addLayout(layout_buttons, 0, 0)
        layout_main.addLayout(layout_table, 1, 0)
        layout_main.addLayout(layout_table_controls, 2, 0)

        button_add_contract = Button(Text.add_agreement)
        button_add_contract.clicked.connect(self.handler_click_add_contract)
        layout_buttons.addWidget(button_add_contract, 0, 0)

        button_remove_contracts = Button(Text.remove_agreements)
        button_remove_contracts.clicked.connect(self.handler_click_remove_contracts)
        layout_buttons.addWidget(button_remove_contracts, 1, 0)

        button_produce_contracts = Button(Text.produce_contracts)
        button_produce_contracts.clicked.connect(self.handler_click_produce_contracts)
        layout_buttons.addWidget(button_produce_contracts, 0, 1)

        button_produce_bills = Button(Text.produce_bills)
        button_produce_bills.clicked.connect(self.handler_click_produce_bills)
        layout_buttons.addWidget(button_produce_bills, 1, 1)

        button_problems = Button(Text.find_problems)
        button_problems.clicked.connect(self.handler_click_problems)
        layout_buttons.addWidget(button_problems, 0, 2)

        button_settings = Button(Text.settings)
        button_settings.clicked.connect(self.handler_click_settings)
        layout_buttons.addWidget(button_settings, 1, 2)

        self.table = Table(Text.agreements_table, table_doubleclick_handler=self.handler_doubleclick_table)
        layout_table.addWidget(self.table)

        button_select = Button(Text.select_all)
        button_select.clicked.connect(self.handler_click_select)
        layout_table_controls.addWidget(button_select, 0, 0)

        button_deselect = Button(Text.deselect_all)
        button_deselect.clicked.connect(self.handler_click_deselect)
        layout_table_controls.addWidget(button_deselect, 0, 1)

        return layout_main

    def fill_in_table(self):
        rows_properties = self.database.get_properties()
        max_properties_by_agreement = {}
        given_properties_by_agreement = {}
        max_areas_by_agreement = {}
        given_areas_by_agreement = {}

        for row_property in rows_properties:
            agreement_id = row_property[5]
            area = int(row_property[3])
            given = True  # TODO how am I suppose to get that?

            if agreement_id in max_properties_by_agreement:
                max_properties_by_agreement[agreement_id] += 1
                max_areas_by_agreement[agreement_id] += area
                if given:
                    given_properties_by_agreement[agreement_id] += 1
                    given_areas_by_agreement[agreement_id] += area

            else:
                max_properties_by_agreement[agreement_id] = 1
                max_areas_by_agreement[agreement_id] = area
                if given:
                    given_properties_by_agreement[agreement_id] = 1
                    given_areas_by_agreement[agreement_id] = area
                else:
                    given_properties_by_agreement[agreement_id] = 0
                    given_areas_by_agreement[agreement_id] = 0

        self.table.clean()
        rows_agreements = self.database.get_agreements()
        for row_index in range(len(rows_agreements)):
            row = rows_agreements[row_index]
            current_income = int(row[5]) * given_areas_by_agreement[row[0]] / max_areas_by_agreement[row[0]]
            max_income = int(row[5])

            try:
                max_amount = max_properties_by_agreement[row[0]]
                given_amount = given_properties_by_agreement[row[0]]
                max_area = max_areas_by_agreement[row[0]]
                given_area = given_areas_by_agreement[row[0]]

            except KeyError:
                max_amount = 0
                given_amount = 0
                max_area = 0
                given_area = 0
            self.table.add_row(row[0], [row[1], row[2], row[4], row[8], max_amount, given_amount, max_area, given_area,
                                        max_income, current_income])

    def handler_click_select(self):
        self.table.set_all_checkboxes()

    def handler_click_deselect(self):
        self.table.set_all_checkboxes(negative=True)

    def handler_click_produce_contracts(self):
        Popup("Данная фунция еще не закончена")
        # TODO finish

    def handler_click_produce_bills(self):
        Popup("Данная фунция еще не закончена")
        # TODO finish

    def handler_click_problems(self):
        Popup("Данная фунция еще не закончена")
        # TODO finish

    def handler_click_settings(self):
        Popup("Данная фунция еще не закончена")
        # TODO finish

    def handler_doubleclick_table(self, event):
        index = self.table.item(event.row(), 0).row_id
        self.contract_window = AgreementWidget(self.app, self.database, self, agreement_id=index)

    def handler_click_add_contract(self):
        self.contract_window = AgreementWidget(self.app, self.database, self)

    def handler_click_remove_contracts(self):
        agreements_to_delete = []
        for index in range(self.table.rowCount()):
            if self.table.item(index, 0).checkState() == Qt.Checked:
                agreements_to_delete.append(self.table.item(index, 0).row_id)
        if len(agreements_to_delete) == 0:
            Popup(Text.error_selection_missing, Text.error)
        self.database.remove_agreements(agreements_to_delete)
        self.fill_in_table()
