from domainobjects.generatable import Generatable
from datetime import datetime
import random

class OrderExecution(Generatable):
    
    def generate(self, custom_args, order_id):
        instruments = self.cache.retrieve_from_cache('instruments')
        instrument = random.choice(instruments)
            
        record = {
            'order_id': order_id,
            'account_num': self.generate_random_integer(length=8),
            'direction': self.generate_credit_debit(),
            'sto_id': self.generate_random_integer(length=7),
            'agent_id': self.generate_random_integer(length=7),
            'price': self.generate_random_decimal(),
            'curr': self.generate_currency(),
            'ric': instrument['ric'],
            'qty': self.generate_random_integer(),
            'time_stamp': datetime.now(),
        }
        
        return record