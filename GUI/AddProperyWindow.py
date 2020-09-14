from PyQt5.QtWidgets import QGridLayout, QWidget
from GUI.Templates.Button import Button
from GUI.Templates.Label import Label
from GUI.Templates.LineEntry import LineEntry
from GUI.Templates.DateEntry import DateEntry
from GUI.Templates.Popup import Popup
from GUI import Text


SIZE_MODIFIER = 0.75


class AddPropertyWidget(QWidget):
    def __init__(self, app, database, agreements_window):
        super().__init__()

        self.app = app
        self.database = database
        self.agreements_window = agreements_window

        self.setWindowTitle(Text.add_agreement_window_name)
        self.resize(int(app.primaryScreen().size().width() * SIZE_MODIFIER),
                    int(app.primaryScreen().size().height() * SIZE_MODIFIER))

        self.main_layout = QGridLayout()
        self.fields_layout = QGridLayout()
        self.page_control_layout = QGridLayout()

        self.entry_name = LineEntry()
        self.entry_address = LineEntry()
        self.entry_area = LineEntry()
        self.entry_given_day = DateEntry()

        self.main_layout.addLayout(self.fields_layout, 0, 0)
        self.main_layout.addLayout(self.page_control_layout, 1, 0)

        self.setup_fields_layout()
        self.setup_page_control_layout()

        self.setLayout(self.main_layout)

        self.show()

    def setup_fields_layout(self):
        index = 0
        for row in [(Text.add_property_name_label, self.entry_name),
                    (Text.add_property_address_label, self.entry_address),
                    (Text.add_property_area_label, self.entry_area),
                    (Text.add_property_given_date_label, self.entry_given_day),]:
            self.fields_layout.addWidget(Label(row[0]), index, 0)
            self.fields_layout.addWidget(row[1], index, 1)
            index += 1

    def setup_page_control_layout(self):
        done_button = Button(Text.add_agreement_add_button)
        done_button.clicked.connect(self.done_clicked)
        self.page_control_layout.addWidget(done_button, 0, 0)
        self.page_control_layout.addWidget(Button(Text.add_agreement_cancel_button), 0, 1)

    def done_clicked(self):
        data = {"name": self.entry_name.text(),
                "address": self.entry_address.text(),
                "area": self.entry_area.text(),
                "given_day": self.entry_given_day.text(),
                "agreement_id": -1,  # -1 is an id for yet non-existent agreement. Once contract is created - all -1 ids
                # are changed to its id
             }
        result = self.database.add_property(data)
        if not result:
            Popup("Some fields were not validated", "Error")
        self.agreements_window.fill_in_properties_table()
        self.close()
