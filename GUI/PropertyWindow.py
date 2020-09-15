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
        self.entry_name = LineEntry()
        self.entry_address = LineEntry()
        self.entry_area = LineEntry()
        self.entry_given_day = DateEntry()
        self.setLayout(self.setup_layout())

        if self.property_index != -1:
            self.fill_in_fields()

        self.show()

    def setup_layout(self):
        layout_main = QGridLayout()
        layout_fields = QGridLayout()
        layout_control = QGridLayout()
        layout_main.addLayout(layout_fields, 0, 0)
        layout_main.addLayout(layout_control, 1, 0)

        index = 0
        for row in [(Text.name, self.entry_name),
                    (Text.address, self.entry_address),
                    (Text.area, self.entry_area),
                    (Text.given_day, self.entry_given_day), ]:
            layout_fields.addWidget(Label(row[0]), index, 0)
            layout_fields.addWidget(row[1], index, 1)
            index += 1

        button_done = Button(Text.save)
        button_done.clicked.connect(self.handler_click_done)
        layout_control.addWidget(button_done, 0, 0)
        layout_control.addWidget(Button(Text.cancel), 0, 1)

        return layout_main

    def handler_click_done(self):
        data = {"name": self.entry_name.text(),
                "address": self.entry_address.text(),
                "area": self.entry_area.text(),
                "given_day": self.entry_given_day.text(),
                "agreement_id": self.agreement_id
             }
        result = self.database.set_property(data, self.property_index)
        if not result:
            Popup("Some fields were not validated", "Error")
        self.agreements_window.fill_in_table()
        self.close()

    def fill_in_fields(self):
        rows = self.database.get_properties(index=self.property_index)
        if len(rows) <= 0:
            self.close()
            Popup("Something went wrong - there is no property like that", "Error")
        fields = rows[0]
        self.entry_name.setText(str(fields[1]))
        self.entry_address.setText(str(fields[2]))
        self.entry_area.setText(str(fields[3]))
        self.entry_given_day.setDate(QDate.fromString(fields[4], 'dd-MM-yyyy'))
