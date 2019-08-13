from domainobjects.generatable import Generatable
from datetime import datetime
import random

class FrontOfficePosition(Generatable):
    
    def generate(self, record_count, custom_args, domain_config):
        records_per_file = domain_config['max_objects_per_file']
        file_num = 1
        file_extension = "."+str(domain_config['file_builder_name']).lower()
        records = []    
        
        file_builder = self.get_file_builder()
        database = self.get_database()
        instruments = database.retrieve('instruments')    
        
        for j in range(1, record_count+1):  
            instrument = random.choice(instruments)                    
            position_type = self.generate_position_type()
            knowledge_date = self.generate_knowledge_date()
                
            records.append({
                'ric': instrument['ric'],
                'position_type': position_type,
                'knowledge_date': knowledge_date,
                'effective_date': self.generate_effective_date(0, knowledge_date, position_type),
                'account': self.generate_account(),
                'direction': self.generate_credit_debit(),
                'qty': self.generate_random_integer(),
                'purpose': self.generate_purpose(),
                'time_stamp': datetime.now(),
            })        

            if (j % int(records_per_file) == 0):
                file_builder.build(None, file_extension, file_num, records, domain_config)
                file_num += 1
                records = []

        if records != []: 
            file_builder.build(None, file_extension, file_num, records, domain_config)

    def generate_purpose(self):
        return 'Outright'