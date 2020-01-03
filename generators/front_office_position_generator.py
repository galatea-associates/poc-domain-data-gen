from generators.generator import Generator
from datetime import datetime, timezone, timedelta
from random import choice, randint


class FrontOfficePositionGenerator(Generator):

    @classmethod
    def instantiate_generator(cls, quantity, database, lock, start_id):
        for record_number in range(quantity):
            record = cls.__get_record(start_id, record_number, database)
            yield record

    @classmethod
    def __get_record(cls, start_id, record_number, database=None):
        as_of_date = datetime.now(timezone.utc).date()
        value_date = choice(
            (
                datetime.now(timezone.utc).date(),
                datetime.now(timezone.utc).date() + timedelta(days=2)
            )
        )
        account_id = database.get_random_value("accounts", "account_id")
        cusip = database.get_random_value("instruments", "cusip")
        quantity = randint(1, 10000) * choice((1, -1))
        purpose = "Outright"
        record = {
            'as_of_date': as_of_date,
            'value_date': value_date,
            'account_id': account_id,
            'cusip': cusip,
            'quantity': quantity,
            'purpose': purpose
        }
        return record




