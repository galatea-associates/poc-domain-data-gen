from domainobjects.generatable  import Generatable
from datetime import datetime
import random

class BackOfficePosition(Generatable):
    
    def generate(self, custom_args, domain_obj_id):
        instruments = self.cache.retrieve_from_cache('instruments')
        
        instrument = random.choice(instruments) 
        position_type = self.generate_position_type()
        knowledge_date = self.generate_knowledge_date()
            
        record = {
            'cusip': instrument['cusip'],
            'position_type': position_type,
            'knowledge_date': knowledge_date,
            'effective_date': self.generate_effective_date(0, knowledge_date, position_type),
            'account': self.generate_account(account_types=['ICP']),
            'direction': self.generate_credit_debit(),
            'qty': self.generate_random_integer(),
            'purpose': self.generate_purpose(),
            'time_stamp': datetime.now(),
        }        
        
        return record
    
    def generate_purpose(self):
        return 'Outright'
