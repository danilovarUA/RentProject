import sqlite3

DATABASE_NAME = 'rentDatabase.sqlite'


class Database:
    def __init__(self):
        self.connection = sqlite3.connect(DATABASE_NAME)
        self.cursor = self.connection.cursor()

    def add_agreement(self, fields):
        if not(
            validate_string(fields["company"]) or
            validate_string(fields["person"]) or
            validate_number(fields["recovery_price"]) or
            validate_date(fields["last_accept_day"]) or
            validate_number(fields["first_payment"]) or
            validate_number(fields["last_same_payment"]) or
            validate_date(fields["start_day"]) or
            validate_date(fields["end_day"])
        ):
            return False
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
        return True

    def remove_agreements(self, ids):
        for row_id in ids:
            self.cursor.execute("DELETE FROM agreements WHERE id={};".format(row_id))
        print("database removed agreement")
        self.connection.commit()

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

def validate_string(value, max_length=1000):
    return isinstance(value, str) and len(value) <= max_length


def validate_number(value):
    return isinstance(value, str) and value.isnumeric()


def validate_date(value):
    if not isinstance(value, str):
        return False
    day, month, year = value.split("/")
    return (day.isnumeric() and len(day) <= 2
            and month.isnumeric() and len(month) <= 2
            and year.isnumeric() and len(year) == 4)
