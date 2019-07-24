from domainobjects.generatable  import Generatable
from datetime import datetime
import random

class CashBalance(Generatable):
    
    def generate(self, custom_args, domain_obj_id):                  
        record = {
            'amount': self.generate_random_integer(),
            'curr': self.generate_currency(),
            'account_num': self.generate_random_integer(length=8),
            'purpose': self.generate_purpose(),
            'time_stamp': datetime.now(),
        }       
        
        return record
    
    def generate_purpose(self):
        return random.choice(['Cash Balance', 'P&L', 'Fees'])