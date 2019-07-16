from domainobjects.generatable import Generatable
from datetime import datetime
import random

class Price(Generatable):
    
    def generate(self, record_count, custom_args):        
        records = []
        instruments = self.cache.retrieve_from_cache('instruments')
                
        for _ in range(0, record_count): 
            instrument = random.choice(instruments)      
            records.append({
                'ric': instrument['ric'],
                'price': self.generate_random_decimal(),
                'curr': self.generate_currency(),
                'time_stamp': datetime.now()
            })
        return records
