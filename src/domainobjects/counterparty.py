from domainobjects.generatable  import Generatable
import random
import string
from datetime import datetime

class Counterparty(Generatable):
    
    def generate(self, record_count, custom_args, domain_config, file_builder):        
        records_per_file = domain_config['max_objects_per_file']
        file_num = 1
        file_extension = "."+str(domain_config['file_builder_name']).lower()
        
        records = []

        for i in range(1, record_count+1):                 
            records.append({
                'counterparty_id':i,
                'book':self.generate_random_string(5, include_numbers=False),
                'counterparty_field1': self.generate_random_string(10),
                'counterparty_field2': self.generate_random_string(10),
                'counterparty_field3': self.generate_random_string(10),
                'counterparty_field4': self.generate_random_string(10),
                'counterparty_field5': self.generate_random_string(10),
                'counterparty_field6': self.generate_random_string(10),
                'counterparty_field7': self.generate_random_string(10),
                'counterparty_field8': self.generate_random_string(10),
                'counterparty_field9': self.generate_random_string(10),
                'counterparty_field10': self.generate_random_string(10),
                'time_stamp':datetime.now()})
            
            if (i % int(records_per_file) == 0):
                file_builder.build(file_extension, file_num, records, domain_config)
                file_num += 1
                records = []

            # TODO: FIX HERE: Add query construction to persisting function
            self.dependency_db.persist_to_database("counterparties","('"+str(i+1)+"')")

        if records != []: 
            file_builder.build(file_extension, file_num, records, domain_config)

   