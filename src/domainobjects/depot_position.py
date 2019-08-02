from domainobjects.generatable import Generatable
from datetime import datetime
import random
import string

class DepotPosition(Generatable):
    
    def generate(self, record_count, custom_args, domain_config, file_builder):
        records_per_file = domain_config['max_objects_per_file']
        file_num = 1
        file_extension = "."+str(domain_config['file_builder_name']).lower()
        
        records = []        
        instruments = self.dependency_db.retrieve_from_database('instruments')

        for i in range(1, record_count+1): 
            instrument = random.choice(instruments)          
            position_type = self.generate_position_type()
            knowledge_date = self.generate_knowledge_date()
                
            records.append({
                'isin': instrument['isin'],                
                'knowledge_date': knowledge_date,
                'effective_date': self.generate_effective_date(3, knowledge_date, position_type),
                'account': self.generate_account(),               
                'qty': self.generate_random_integer(),
                'purpose': self.generate_purpose(),
                'depot_id': self.generate_random_integer(length=5),
                'time_stamp': datetime.now(),
            })        

            if (i % int(records_per_file) == 0):
                file_builder.build(file_extension, file_num, records, domain_config)
                file_num += 1
                records = []
        
        if records != []: 
            file_builder.build(file_extension, file_num, records, domain_config)
    
    def generate_purpose(self):
        return random.choice(['Holdings', 'Seg'])
