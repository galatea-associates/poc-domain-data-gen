from domainobjects.generatable import Generatable
from datetime import datetime
import random
import string

class DepotPosition(Generatable):

    def generate(self, record_count, custom_args, start_id):

        records = []
        self.establish_db_connection()
        database = self.get_database()
        instruments = database.retrieve('instruments')

        for _ in range(start_id, start_id+record_count):
            instrument = random.choice(instruments)
            position_type = self.generate_position_type()
            knowledge_date = self.generate_knowledge_date()

            records.append({
                'isin': instrument['isin'],
                'knowledge_date': knowledge_date,
                'effective_date': self.generate_effective_date(
                                    3, knowledge_date, position_type),
                'account': self.generate_account(),
                'qty': self.generate_random_integer(),
                'purpose': self.generate_purpose(),
                'depot_id': self.generate_random_integer(length=5),
                'time_stamp': datetime.now(),
            })

        return records

    def generate_purpose(self):
        return random.choice(['Holdings', 'Seg'])
