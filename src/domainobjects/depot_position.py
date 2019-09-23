from domainobjects.generatable import Generatable
from datetime import datetime
import random
import string

class DepotPosition(Generatable):

    def generate(self, record_count, custom_args, start_id):

        self.instruments = self.retrieve_records('instruments')

        records = []

        for _ in range(start_id, start_id+record_count):
            instrument = self.get_random_instrument()
            records.append(self.get_record(instrument))

        return records

    def get_record(self, instrument):
        position_type = self.generate_position_type()
        knowledge_date = self.generate_knowledge_date()
        return {
            'isin': instrument['isin'],
            'knowledge_date': knowledge_date,
            'effective_date': self.generate_effective_date(
                                3, knowledge_date, position_type),
            'account': self.generate_account(),
            'qty': self.generate_random_integer(),
            'purpose': self.generate_purpose(),
            'depot_id': self.generate_random_integer(length=5),
            'time_stamp': datetime.now()            
        }

    def generate_purpose(self):
        return random.choice(['Holdings', 'Seg'])
