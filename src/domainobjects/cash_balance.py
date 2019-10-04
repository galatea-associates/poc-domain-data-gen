from domainobjects.generatable  import Generatable
from datetime import datetime
import random

class CashBalance(Generatable):
    
    def generate(self, record_count, custom_args):
        config = self.get_object_config()
        records_per_file = config['max_objects_per_file']
        file_num = 1

        records = []        

        for i in range(1, record_count+1):
            records.append({
                'amount': self.generate_random_integer(),
                'curr': self.generate_currency(),
                'account_num': self.generate_random_integer(length=8),
                'purpose': self.generate_purpose(),
                'time_stamp': datetime.now(),
            })

            if (i % int(records_per_file) == 0):
                self.write_to_file(file_num, records)
                file_num += 1
                records = []

        if records != []:
            self.write_to_file(file_num, records)
    
    def generate_purpose(self):
        return random.choice(['Cash Balance', 'P&L', 'Fees'])