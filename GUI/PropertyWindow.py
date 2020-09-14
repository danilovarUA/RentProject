from PyQt5.QtWidgets import QGridLayout, QWidget
from PyQt5.QtCore import QDate
from GUI.Templates.Button import Button
from GUI.Templates.Label import Label
from GUI.Templates.LineEntry import LineEntry
from GUI.Templates.DateEntry import DateEntry
from GUI.Templates.Popup import Popup
from GUI import Text


SIZE_MODIFIER = 0.4


class PropertyWidget(QWidget):
    def __init__(self, app, database, agreements_window, property_index=-1):
        super().__init__()

        self.app = app
        self.database = database
        self.agreements_window = agreements_window

        self.property_index = property_index
        self.agreement_id = agreements_window.agreement_id

        self.setWindowTitle(Text.add_agreement)
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

        if self.property_index != -1:
            self.fill_in_fields()

        self.show()

    def setup_fields_layout(self):
        index = 0
        for row in [(Text.name, self.entry_name),
                    (Text.address, self.entry_address),
                    (Text.area, self.entry_area),
                    (Text.given_day, self.entry_given_day), ]:
            self.fields_layout.addWidget(Label(row[0]), index, 0)
            self.fields_layout.addWidget(row[1], index, 1)
            index += 1

    def setup_page_control_layout(self):
        done_button = Button(Text.save)
        done_button.clicked.connect(self.done_clicked)
        self.page_control_layout.addWidget(done_button, 0, 0)
        self.page_control_layout.addWidget(Button(Text.cancel), 0, 1)

    def done_clicked(self):
        data = {"name": self.entry_name.text(),
                "address": self.entry_address.text(),
                "area": self.entry_area.text(),
                "given_day": self.entry_given_day.text(),
                "agreement_id": self.agreement_id
             }
        result = self.database.set_property(data, self.property_index)
        if not result:
            Popup("Some fields were not validated", "Error")
        self.agreements_window.fill_in_properties_table()
        self.close()

    def fill_in_fields(self):
        print(self.property_index)
        rows = self.database.get_properties(index=self.property_index)
        if len(rows) <= 0:
            # TODO popup and close window
            raise ValueError("Something went wrong - there is no property like that")
        fields = rows[0]
        self.entry_name.setText(str(fields[1]))
        self.entry_address.setText(str(fields[2]))
        self.entry_area.setText(str(fields[3]))
        self.entry_given_day.setDate(QDate.fromString(fields[4], 'dd-MM-yyyy'))
