from domainobjects.generatable import Generatable
from datetime import datetime
import random

class Price(Generatable):
    
    def generate(self, record_count, custom_args):        
        records = []
                
        for _ in range(0, record_count): 
            asset_class = self.generate_asset_class()
            ticker = self.generate_currency() if asset_class == 'Cash' else self.generate_ticker()       
            exchange_code = '' if asset_class == 'Cash' else self.generate_exchange_code() 
            ric = '' if asset_class == 'Cash' else self.generate_ric(ticker, exchange_code)                
            records.append({
                'ric': ric,
                'price': self.generate_random_decimal(),
                'curr': self.generate_currency(),
                'time_stamp': datetime.now()
            })
        return records
