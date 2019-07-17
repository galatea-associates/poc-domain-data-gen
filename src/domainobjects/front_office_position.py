from domainobjects.generatable import Generatable
from datetime import datetime
import random

class FrontOfficePosition(Generatable):
    
    def generate(self, record_count, custom_args):
        records = []    
        instruments = self.cache.retrieve_from_cache('instruments')    
        
        for _ in range(0, record_count):  
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
        
        return records

    def generate_purpose(self):
        return 'Outright'