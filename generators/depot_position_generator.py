from generators.generator import Generator
from datetime import datetime, timezone, timedelta
from random import choice, randint


class DepotPositionGenerator(Generator):

    @classmethod
    def instantiate_generator(cls, quantity, database, lock, start_id):
        for record_number in range(quantity):
            record = cls.__get_record(start_id, record_number, database)
            yield record

    @classmethod
    def __get_record(cls, start_id, record_number, database=None):
        instrument_row = database.get_random_value("instruments")
        as_of_date = datetime.now(timezone.utc).date()
        value_date = choice(
            (
                datetime.now(timezone.utc).date(),
                datetime.now(timezone.utc).date() + timedelta(days=2)
            )
        )
        isin = instrument_row[2]
        cusip = instrument_row[1]
        market = instrument_row[3]
        depot_id = cls.__get_depot_id(database)
        quantity = randint(1, 10000)
        purpose = choice(("Holdings", "Seg", "Pending Holdings"))
        record = {
            'as_of_date': as_of_date,
            'value_date': value_date,
            'isin': isin,
            "cusip": cusip,
            "market": market,
            "depot_id": depot_id,
            'quantity': quantity,
            'purpose': purpose
        }
        return record

    @classmethod
    def __get_depot_id(cls, database):
        query = "SELECT account_id FROM accounts WHERE " + \
                "account_type = 'Depot' ORDER BY RANDOM() LIMIT 1"
        depot_id = database.execute_query(query)
        return depot_id



