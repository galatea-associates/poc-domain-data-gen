from domainobjects.generatable  import Generatable
import random
import string
from datetime import datetime

class Counterparty(Generatable):
    
    def generate(self, record_count, custom_args):        
        records = []
                
        for i in range(0, record_count):                 
            records.append({
                'counterparty_id':i+1,
                'counterparty_field1': self.generate_random_string(10),
                'counterparty_field2': self.generate_random_string(10),
                'counterparty_field3': self.generate_random_string(10),
                'counterparty_field4': self.generate_random_string(10),
                'counterparty_field5': self.generate_random_string(10),
                'counterparty_field6': self.generate_random_string(10),
                'counterparty_field7': self.generate_random_string(10),
                'counterparty_field8': self.generate_random_string(10),
                'counterparty_field9': self.generate_random_string(10),
                'counterparty_field10': self.generate_random_string(10),
                'time_stamp':datetime.now()})
        
        self.cache.persist_to_cache('counterparties', records)
        return records

   