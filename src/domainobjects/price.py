from domainobjects.generatable import Generatable
from datetime import datetime
import random

class Price(Generatable):
    
    def generate(self, custom_args, domain_obj_id):        
        instruments = self.cache.retrieve_from_cache('instruments')

        instrument = random.choice(instruments)      
        record = {
            'ric': instrument['ric'],
            'price': self.generate_random_decimal(),
            'curr': self.generate_currency(),
            'time_stamp': datetime.now()
        }
        return record
