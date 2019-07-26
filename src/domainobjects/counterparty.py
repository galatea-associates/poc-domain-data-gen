from domainobjects.generatable  import Generatable
import random
import string
from datetime import datetime

class Counterparty(Generatable):
    
    def generate(self, custom_args, domain_obj_id):        
        record = {
            'counterparty_id':domain_obj_id,
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
            'time_stamp':datetime.now()}
        
        self.cache.append_to_cache('counterparties', record)
        return record

   