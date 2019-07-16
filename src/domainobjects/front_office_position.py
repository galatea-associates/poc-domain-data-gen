from domainobjects.generatable import Generatable
from datetime import datetime
import random

class FrontOfficePosition(Generatable):
    
    def generate(self, record_count, custom_args):
        records = []        
        
        for _ in range(0, record_count):            
            asset_class = self.generate_asset_class()  
            ticker = self.generate_currency() if asset_class == 'Cash' else self.generate_ticker()       
            exchange_code = '' if asset_class == 'Cash' else self.generate_exchange_code() 
            ric = '' if asset_class == 'Cash' else self.generate_ric(ticker, exchange_code)
            position_type = self.generate_position_type()
            knowledge_date = self.generate_knowledge_date()
                
            records.append({
                'ric': ric,
                'position_type': position_type,
                'knowledge_date': knowledge_date,
                'effective_date': self.generate_effective_date(0, knowledge_date, position_type),
                'account': self.generate_account(),
                'direction': self.generate_credit_debit(),
                'qty': self.generate_random_integer(),
                'purpose': self.generate_purpose(),
                'time_stamp': datetime.now(),
            })        
        
        return records

    def generate_purpose(self):
        return 'Outright'