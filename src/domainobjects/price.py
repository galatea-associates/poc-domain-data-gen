from domainobjects.generatable import Generatable
from datetime import datetime
import random

class Price(Generatable):

    def generate(self, record_count, start_id):

        records = []
        self.instruments = self.retrieve_records('instruments')

        for _ in range(start_id, start_id+record_count):
            record = self.generate_record()
            records.append(record)

        return records

    def generate_record(self):
        instrument = self.get_random_instrument()
        return {
                'ric': instrument['ric'],
                'price': self.generate_random_decimal(),
                'curr': self.generate_currency(),
                'time_stamp': datetime.now()
            }