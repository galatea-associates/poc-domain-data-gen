from domainobjects.generatable  import Generatable
from datetime import datetime
import random

class BackOfficePosition(Generatable):
    
    def generate(self, record_count, custom_args):
        config = self.get_object_config()

        records_per_file = config['max_objects_per_file']
        file_num = 1
        records = []

        database = self.get_database()
        file_builder = self.get_file_builder()
        
        instruments = database.retrieve('instruments')
        
        # 1 to record_count+1 preserves requested amount but reduces computation for repeated modulo calculation
        for i in range(1, record_count+1):  
            instrument = random.choice(instruments) 
            position_type = self.generate_position_type()
            knowledge_date = self.generate_knowledge_date()
                
            records.append({
                'cusip': instrument['cusip'],
                'position_type': position_type,
                'knowledge_date': knowledge_date,
                'effective_date': self.generate_effective_date(0, knowledge_date, position_type),
                'account': self.generate_account(account_types=['ICP']),
                'direction': self.generate_credit_debit(),
                'qty': self.generate_random_integer(),
                'purpose': self.generate_purpose(),
                'time_stamp': datetime.now(),
            })      
            
            if (i % int(records_per_file) == 0):
                file_builder.build(file_num, records)
                file_num += 1
                records = []

        if records != []:
            file_builder.build(file_num, records)
    
    def generate_purpose(self):
        return 'Outright'
