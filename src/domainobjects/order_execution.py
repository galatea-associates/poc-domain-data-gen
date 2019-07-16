from src.domainobjects.generatable import Generatable
from datetime import datetime
import random

class OrderExecution(Generatable):
    
    def generate(self, record_count, custom_args):
        records = []
        instruments = self.cache.retrieve_from_cache('instruments')
        
        for i in range(0, record_count):    
            instrument = random.choice(instruments)
                
            records.append({
                'order_id': i,
                'account_num': self.generate_random_integer(length=8),
                'direction': self.generate_credit_debit(),
                'sto_id': self.generate_random_integer(length=7),
                'agent_id': self.generate_random_integer(length=7),
                'price': self.generate_random_decimal(),
                'curr': self.generate_currency(),
                'ric': instrument['ric'],
                'qty': self.generate_random_integer(),
                'time_stamp': datetime.now(),
            })     
        
        return records