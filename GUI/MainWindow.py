from PyQt5.QtWidgets import QGridLayout, QWidget
from PyQt5.QtCore import Qt
from GUI.Templates.Button import Button
from GUI.Templates.Table import Table
from GUI.Templates.Popup import Popup
from GUI import Text
from GUI.AgreementWindow import AgreementWidget


TABLE_ROW_HEIGHT = 25
SIZE_MODIFIER = 0.9


class MainWidget(QWidget):
    def __init__(self, app, database):
        super().__init__()
        self.app = app
        self.database = database
        self.contract_window = None
        self.table = None

        self.setWindowTitle(Text.agreements_window_name)
        self.resize(int(app.primaryScreen().size().width() * SIZE_MODIFIER),
                    int(app.primaryScreen().size().height() * SIZE_MODIFIER))

        self.main_layout = QGridLayout()
        self.buttons_layout = QGridLayout()
        self.table_layout = QGridLayout()

        self.main_layout.addLayout(self.buttons_layout, 0, 0)
        self.main_layout.addLayout(self.table_layout, 1, 0)

        self.setup_buttons_layout()
        self.setup_table_layout()

        self.setLayout(self.main_layout)

        self.show()

        self.fill_in_table()

    def setup_buttons_layout(self):
        add_contract_button = Button(Text.agreements_add_contract_button)
        add_contract_button.clicked.connect(self.add_contract_clicked)
        self.buttons_layout.addWidget(add_contract_button, 0, 0)

        remove_contracts_button = Button(Text.agreements_remove_contracts_button)
        remove_contracts_button.clicked.connect(self.remove_contracts_clicked)
        self.buttons_layout.addWidget(remove_contracts_button, 1, 0)

        self.buttons_layout.addWidget(Button(Text.agreements_produce_contracts_button), 0, 1)

        self.buttons_layout.addWidget(Button(Text.agreements_produce_bills_button), 1, 1)

        self.buttons_layout.addWidget(Button(Text.agreements_problems_button), 0, 2)

        self.buttons_layout.addWidget(Button(Text.agreements_settings_button), 1, 2)

    def setup_table_layout(self):
        self.table = Table(Text.agreements_table_fields, table_doubleclick_handler=self.select_handler)
        self.table_layout.addWidget(self.table)

    def fill_in_table(self):
        self.table.clean()
        rows = self.database.get_agreements()
        for row_index in range(len(rows)):
            row = rows[row_index]
            self.table.add_row(row[0], [row[1], row[2], row[4], row[8], 123, 456, 789])

    def select_handler(self, event):
        index = self.table.item(event.row(), 0).row_id
        print("index ({}), row ({})".format(index, event.row()))
        self.contract_window = AgreementWidget(self.app, self.database, self, agreement_id=index)

    def add_contract_clicked(self):
        self.contract_window = AgreementWidget(self.app, self.database, self)

    def remove_contracts_clicked(self):
        agreements_to_delete = []
        for index in range(self.table.rowCount()):
            if self.table.item(index, 0).checkState() == Qt.Checked:
                agreements_to_delete.append(self.table.item(index, 0).row_id)
        if len(agreements_to_delete) == 0:
            Popup("No selected contracts to delete.", "Error")
        self.database.remove_agreements(agreements_to_delete)
        self.fill_in_table()
