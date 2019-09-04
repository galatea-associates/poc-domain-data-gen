from domainobjects.generatable import Generatable
from datetime import datetime
import random

class Price(Generatable):

    def generate(self, record_count, custom_args):
        config = self.get_object_config()
        records_per_file = config['max_objects_per_file']
        file_num = 1
        records = []

        database = self.get_database()
        instruments = database.retrieve('instruments')
                
        for i in range(1, record_count+1):
            instrument = random.choice(instruments)      
            records.append({
                'ric': instrument['ric'],
                'price': self.generate_random_decimal(),
                'curr': self.generate_currency(),
                'time_stamp': datetime.now()
            })

            if (i % int(records_per_file) == 0):
                self.write_to_file(file_num, records)
                file_num += 1
                records = []

        if records != []:
            self.write_to_file(file_num, records)
