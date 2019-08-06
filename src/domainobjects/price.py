from domainobjects.generatable import Generatable
from datetime import datetime
import random

class Price(Generatable):
    
    def generate(self, record_count, custom_args, domain_config, file_builder):        
        records_per_file = domain_config['max_objects_per_file']
        file_num = 1
        file_extension = "."+str(domain_config['file_builder_name']).lower()
        records = []

        instruments = self.dependency_db.retrieve_from_database('instruments')
                
        for i in range(1, record_count+1): 
            instrument = random.choice(instruments)      
            records.append({
                'ric': instrument['ric'],
                'price': self.generate_random_decimal(),
                'curr': self.generate_currency(),
                'time_stamp': datetime.now()
            })

            if (i % int(records_per_file) == 0):
                file_builder.build(None, file_extension, file_num, records, domain_config)
                file_num += 1
                records = []

        if records != []: 
            file_builder.build(None, file_extension, file_num, records, domain_config)
