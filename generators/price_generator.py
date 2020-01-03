from generators.generator import Generator
from datetime import datetime, timezone
from random import uniform, choice


class PriceGenerator(Generator):

    @classmethod
    def instantiate_generator(cls, quantity, database, lock, start_id):
        for record_number in range(quantity):
            record = cls.__get_record(start_id, record_number, database)
            yield record

    @classmethod
    def __get_record(cls, start_id, record_number, database=None):
        instrument_id = database.get_random_value(
            "instruments", "instrument_id"
        )
        price = round(uniform(1, 10), 2)
        currency = choice(('USD', 'CAD', 'EUR', 'GBP', 'CHF', 'JPY', 'SGD'))
        created_timestamp = datetime.now(timezone.utc)
        last_updated_timestamp = datetime.now(timezone.utc)
        record = {
            'instrument_id': instrument_id,
            'price': price,
            'currency': currency,
            'created_timestamp': created_timestamp,
            'last_updated_time_stamp': last_updated_timestamp
        }
        return record


