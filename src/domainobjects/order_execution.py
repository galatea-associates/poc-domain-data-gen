from domainobjects.generatable import Generatable
from datetime import datetime
import random

class OrderExecution(Generatable):
    
    def generate(self, record_count, custom_args):
        records = []
        
        for i in range(0, record_count):    
            asset_class = self.generate_asset_class()
            ticker = self.generate_currency() if asset_class == 'Cash' else self.generate_ticker()       
            exchange_code = '' if asset_class == 'Cash' else self.generate_exchange_code()     
            ric = '' if asset_class == 'Cash' else self.generate_ric(ticker, exchange_code)  
                
            records.append({
                'order_id': i,
                'account_num': self.generate_random_integer(length=8),
                'direction': self.generate_credit_debit(),
                'sto_id': self.generate_random_integer(length=7),
                'agent_id': self.generate_random_integer(length=7),
                'price': self.generate_random_decimal(),
                'curr': self.generate_currency(),
                'ric': ric,
                'qty': self.generate_random_integer(),
                'time_stamp': datetime.now(),
            })     
        
        return records