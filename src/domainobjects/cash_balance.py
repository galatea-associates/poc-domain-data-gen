from domainobjects.generatable  import Generatable
from datetime import datetime
import random

class CashBalance(Generatable):
    
    def generate(self, record_count, custom_args, domain_config):
        records_per_file = domain_config['max_objects_per_file']
        file_num = 1
        file_extension = "."+str(domain_config['file_builder_name']).lower()

        file_builder = self.get_file_builder()
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
                file_builder.build(None, file_extension, file_num, records, domain_config)
                file_num += 1
                records = []
        
        if records != []: 
            file_builder.build(None, file_extension, file_num, records, domain_config)
    
    def generate_purpose(self):
        return random.choice(['Cash Balance', 'P&L', 'Fees'])