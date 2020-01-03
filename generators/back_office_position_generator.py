from generators.generator import Generator
from datetime import datetime, timezone, timedelta
from random import choice, randint


class BackOfficePositionGenerator(Generator):

    @classmethod
    def instantiate_generator(cls, quantity, database, lock, start_id):
        for record_number in range(quantity):
            record = cls.__get_record(start_id, record_number, database)
            yield record

    @classmethod
    def __get_record(cls, start_id, record_number, database=None):
        instrument_row = database.get_random_value("instruments")
        account_row = database.get_random_value("accounts")
        as_of_date = datetime.now(timezone.utc).date()
        value_date = choice(
            (
                datetime.now(timezone.utc).date(),
                datetime.now(timezone.utc).date() + timedelta(days=2)
            )
        )
        ledger = choice(("TD", "SD"))
        instrument_id = instrument_row[0]
        isin = instrument_row[2]
        account_id = account_row[0]
        account_type = account_row[1]
        quantity = randint(1, 10000) * choice((1, -1))
        purpose = choice(("Outright", "Obligation"))
        record = {
            'as_of_date': as_of_date,
            'value_date': value_date,
            'ledger': ledger,
            'instrument_id': instrument_id,
            'isin': isin,
            'account_id': account_id,
            'account_type': account_type,
            'quantity': quantity,
            'purpose': purpose
        }
        return record




