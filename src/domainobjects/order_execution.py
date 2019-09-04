from domainobjects.generatable import Generatable
from datetime import datetime
import random

class OrderExecution(Generatable):
    
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
                'order_id': i,
                'account_num': self.generate_random_integer(length=8),
                'direction': self.generate_credit_debit(),
                'sto_id': self.generate_random_integer(length=7),
                'agent_id': self.generate_random_integer(length=7),
                'price': self.generate_random_decimal(),
                'curr': self.generate_currency(),
                'ric': instrument['ric'],
                'qty': self.generate_random_integer(),
                'time_stamp': datetime.now(),
            })     

            if (i % int(records_per_file) == 0):
                self.write_to_file(file_num, records)
                file_num += 1
                records = []
        
        if records != []:
            self.write_to_file(file_num, records)