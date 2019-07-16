from domainobjects.generatable  import Generatable
from datetime import datetime
import random

class BackOfficePosition(Generatable):
    
    def generate(self, record_count, custom_args):
        records = []
        
        for _ in range(0, record_count):            
            asset_class = self.generate_asset_class()             
            cusip = '' if asset_class == 'Cash' else str(self.generate_random_integer(length=9))
            position_type = self.generate_position_type()
            knowledge_date = self.generate_knowledge_date()
                
            records.append({
                'cusip': cusip,
                'position_type': position_type,
                'knowledge_date': knowledge_date,
                'effective_date': self.generate_effective_date(0, knowledge_date, position_type),
                'account': self.generate_account(account_types=['ICP']),
                'direction': self.generate_credit_debit(),
                'qty': self.generate_random_integer(),
                'purpose': self.generate_purpose(),
                'time_stamp': datetime.now(),
            })        
        
        return records
    
    def generate_purpose(self):
        return 'Outright'
