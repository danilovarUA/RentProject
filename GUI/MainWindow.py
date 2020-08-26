from PyQt5.QtWidgets import QGridLayout, QWidget
from GUI.Templates.Button import Button
from GUI.Templates.Table import Table, TableCheckbox
from GUI.Templates.TextWidget import TextWidget
from GUI import Text
from GUI.AddAgreementWindow import AddAgreementsWidget


TABLE_ROW_HEIGHT = 25
SIZE_MODIFIER = 0.9


class MainWidget(QWidget):
    def __init__(self, app, database):
        super().__init__()
        self.app = app
        self.database = database

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

        self.buttons_layout.addWidget(Button(Text.agreements_remove_contracts_button), 1, 0)

        self.buttons_layout.addWidget(Button(Text.agreements_produce_contracts_button), 0, 1)

        self.buttons_layout.addWidget(Button(Text.agreements_produce_bills_button), 1, 1)

        self.buttons_layout.addWidget(Button(Text.agreements_problems_button), 0, 2)

        self.buttons_layout.addWidget(Button(Text.agreements_settings_button), 1, 2)

    def setup_table_layout(self):
        self.table = Table(Text.agreements_table_fields, item_click_handler=self.item_click_handler)
        self.table_layout.addWidget(self.table)

    def fill_in_table(self):
        rows = self.database.get_agreements()
        self.table.setRowCount(len(rows))
        for row_index in range(len(rows)):
            row = rows[row_index]
            self.table.setRowHeight(row_index, TABLE_ROW_HEIGHT)
            checkbox = TableCheckbox()
            self.table.setItem(row_index, 0, checkbox)
            self.table.setItem(row_index, 1, TextWidget(row[1]))
            self.table.setItem(row_index, 2, TextWidget(row[2]))
            self.table.setItem(row_index, 3, TextWidget(row[4]))
            self.table.setItem(row_index, 4, TextWidget(row[8]))
            self.table.setItem(row_index, 5, TextWidget(123))
            self.table.setItem(row_index, 6, TextWidget(234))
            self.table.setItem(row_index, 7, TextWidget(456))

    def item_click_handler(self, item):
        print(item)

    def add_contract_clicked(self):
        print("Clicked add contract button")
        self.add_contract_window = AddAgreementsWidget(self.app, self.database)
