import sqlite3

DATABASE_NAME = 'rentDatabase.sqlite'


class Database:
    def __init__(self):
        self.connection = sqlite3.connect(DATABASE_NAME)
        self.cursor = self.connection.cursor()

    def add_agreement(self, fields):
        query = ("INSERT INTO agreements(" +
                 "company, " +
                 "person, " +
                 "recovery_price," +
                 "last_accept_day," +
                 "first_payment," +
                 "last_same_payment," +
                 "start_day," +
                 "end_day" +
                 ") VALUES (" +
                 "'{}', ".format(fields["company"]) +
                 "'{}', ".format(fields["person"]) +
                 "{}, ".format(fields["recovery_price"]) +
                 "'{}', ".format(fields["last_accept_day"]) +
                 "'{}', ".format(fields["first_payment"]) +
                 "{}, ".format(fields["last_same_payment"]) +
                 "'{}', ".format(fields["start_day"]) +
                 "'{}' ".format(fields["end_day"]) +
                 ")")
        self.cursor.execute(query)
        self.connection.commit()

    def remove_agreements(self, ids):
        self.connection.commit()
        raise ValueError("Function not finished")

    def change_agreement(self, agreement_id, fields):
        self.connection.commit()
        raise ValueError("Function not finished")

    def get_agreements(self):
        self.cursor.execute("SELECT * FROM agreements")
        return self.cursor.fetchall()

    def add_property(self, fields):
        self.connection.commit()
        raise ValueError("Function not finished")

    def remove_properties(self, ids, agreement_ids):
        self.connection.commit()
        raise ValueError("Function not finished")

    def change_property(self, property_id, fields):
        self.connection.commit()
        raise ValueError("Function not finished")

    def get_properties(self, agreement_id):
        raise ValueError("Function not finished")

    def __del__(self):
        self.connection.commit()
        self.connection.close()


# db = Database()
# for row in db.get_agreements():
#     print(row)
# db.add_agreement({"company": "какаятокомпания",
#                   "person": "рожа",
#                   "recovery_price": "1001234",
#                   "last_accept_day": "прием 12ю12ю1212",
#                   "first_payment": 1234,
#                   "last_same_payment": "1",
#                   "start_day": "начало 12ю12ю1212",
#                   "end_day": "конец 12ю12ю1212"
# })
