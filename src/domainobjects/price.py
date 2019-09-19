from domainobjects.generatable import Generatable
from datetime import datetime
import random

class Price(Generatable):

    def generate(self, record_count, custom_args, start_id):

        records = []

        self.establish_db_connection()
        database = self.get_database()
        instruments = database.retrieve('instruments')
                
        for _ in range(start_id, start_id+record_count):
            instrument = random.choice(instruments)      
            records.append({
                'ric': instrument['ric'],
                'price': self.generate_random_decimal(),
                'curr': self.generate_currency(),
                'time_stamp': datetime.now()
            })

        return records
