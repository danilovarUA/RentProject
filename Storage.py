import sqlite3

DATABASE_NAME = 'rentDatabase.sqlite'
AGREEMENTS_TABLE_NAME = "agreements"
PROPERTIES_TABLE_NAME = "properties"  # TODO use these only


class Database:
    def __init__(self):
        self.connection = sqlite3.connect(DATABASE_NAME)
        self.cursor = self.connection.cursor()

    def set_agreement(self, fields, index):
        if not(validate_string(fields["company"]) or validate_string(fields["person"]) or
               validate_number(fields["recovery_price"]) or validate_date(fields["last_accept_day"]) or
               validate_number(fields["first_payment"]) or validate_number(fields["last_same_payment"]) or
               validate_date(fields["start_day"]) or validate_date(fields["end_day"])):
            return False

        if index == -1:
            query = ("INSERT INTO {}(company, person, recovery_price, last_accept_day, ".format(AGREEMENTS_TABLE_NAME) +
                     "first_payment, last_same_payment, start_day, end_day) " +
                     "VALUES ({}, {}, {}, {}, {}, {}, {}, {})".format(
                         fields["company"], fields["person"], fields["recovery_price"], fields["last_accept_day"],
                         fields["first_payment"], fields["last_same_payment"], fields["start_day"], fields["end_day"]))
        else:
            query = ("UPDATE {} SET ".format(AGREEMENTS_TABLE_NAME) +
                     "company = '{}', person = '{}', recovery_price = '{}', ".format(
                         fields["company"], fields["person"], fields["recovery_price"]) +
                     "last_accept_day = '{}', first_payment = '{}', last_same_payment = '{}', ".format(
                       fields["last_accept_day"], fields["first_payment"], fields["last_same_payment"]) +
                     "start_day = '{}', end_day = '{}' ".format(
                       fields["start_day"], fields["end_day"]) +
                     "WHERE id={}".format(index))
        return self._execute_(query)

    def assign_properties(self):
        last_id = self.cursor.lastrowid
        query = "UPDATE {} SET agreement_id = {} WHERE agreement_id = -1;".format(PROPERTIES_TABLE_NAME, last_id)
        return self._execute_(query)

    def _execute_(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except sqlite3.OperationalError as e:
            print("DBError[{}]: ({})".format(e, query))
            return False
        print("Done: {}".format(query))
        return True

    def remove_agreements(self, ids):
        for row_id in ids:
            if not self._execute_("DELETE FROM {} WHERE id={};".format(AGREEMENTS_TABLE_NAME, row_id)):
                return False
        self.remove_properties(agreement_ids=ids)
        return True

    def get_agreements(self, index=None):
        if index is None:
            self._execute_("SELECT * FROM agreements")
        else:
            self._execute_("SELECT * FROM {} WHERE id={}".format(AGREEMENTS_TABLE_NAME, index))
        return self.cursor.fetchall()

    def set_property(self, fields, index):
        if not (validate_string(fields["name"]) or validate_string(fields["address"]) or
                validate_number(fields["area"]) or validate_date(fields["given_day"]) or
                validate_number(fields["agreement_id"])):
            return False

        if index == -1:
            query = ("INSERT INTO {}(name, address, area, given_day, agreement_id)".format(PROPERTIES_TABLE_NAME) +
                     "VALUES ('{}', '{}', '{}', '{}', '{}')".format(
                         fields["name"], fields["address"], fields["area"], fields["given_day"],
                         fields["agreement_id"]))
        else:
            query = ("UPDATE {} SET ".format(PROPERTIES_TABLE_NAME) +
                     "name = '{}', address = '{}', area = '{}', ".format(
                       fields["name"], fields["address"], fields["area"]) +
                     "given_day = '{}' ".format(fields["given_day"]) +
                     "WHERE id={}".format(index))

        return self._execute_(query)

    def remove_properties(self, ids=None, agreement_ids=None):
        if ids is not None:
            for row_id in ids:
                if not self._execute_("DELETE FROM {} WHERE id={};".format(PROPERTIES_TABLE_NAME, row_id)):
                    return False
        if agreement_ids is not None:
            for agreement_id in agreement_ids:
                if not self._execute_("DELETE FROM {} WHERE agreement_id={};".format(PROPERTIES_TABLE_NAME,
                                                                                     agreement_id)):
                    return False
        return True

    def get_properties(self, agreement_id=None, index=None):
        if index is not None and agreement_id is None:
            self._execute_("SELECT * FROM {} WHERE id = {}".format(PROPERTIES_TABLE_NAME, index))
        elif agreement_id is not None and index is None:
            self._execute_("SELECT * FROM {} WHERE agreement_id = {}".format(PROPERTIES_TABLE_NAME, agreement_id))
        elif agreement_id is None and index is None:
            self._execute_("SELECT * FROM properties")
        else:
            raise ValueError("Both index and agreement_id were passed")
        return self.cursor.fetchall()

    def __del__(self):
        self.connection.close()


def validate_string(value, max_length=1000):
    return isinstance(value, str) and len(value) <= max_length


def validate_number(value):
    return isinstance(value, str) and value.isnumeric()


def validate_date(value):
    if not isinstance(value, str):
        return False
    day, month, year = value.split("/")
    return (day.isnumeric() and len(day) <= 2 and day in range(0, 32)
            and month.isnumeric() and len(month) <= 2 and month in range(0, 13)
            and year.isnumeric() and len(year) == 4)
