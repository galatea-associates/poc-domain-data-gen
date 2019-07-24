from domainobjects.generatable import Generatable
from datetime import datetime
import random
import string

class DepotPosition(Generatable):
    
    def generate(self, custom_args, domain_obj_id):        
        instruments = self.cache.retrieve_from_cache('instruments')

        instrument = random.choice(instruments)          
        position_type = self.generate_position_type()
        knowledge_date = self.generate_knowledge_date()
            
        record = {
            'isin': instrument['isin'],                
            'knowledge_date': knowledge_date,
            'effective_date': self.generate_effective_date(3, knowledge_date, position_type),
            'account': self.generate_account(),               
            'qty': self.generate_random_integer(),
            'purpose': self.generate_purpose(),
            'depot_id': self.generate_random_integer(length=5),
            'time_stamp': datetime.now(),
        }
    
        return record
    
    def generate_purpose(self):
        return random.choice(['Holdings', 'Seg'])
