from domainobjects.generatable import Generatable
from datetime import datetime, timedelta
import random
import string
import pandas as pd

class SwapPosition(Generatable):
    
    def generate(self, custom_args, swap_position_id):        
        swap_contracts = self.cache.retrieve_from_cache('swap_contracts')
        ins_per_swap_range = custom_args['ins_per_swap']
        records = []
        i = 1
        all_instruments = self.cache.retrieve_from_cache('instruments')
        start_date = datetime.strptime(custom_args['start_date'], '%Y%m%d')
        date_range = pd.date_range(start_date, datetime.today(), freq='D')        
        
        for swap_contract in swap_contracts:                                    
            ins_count = random.randint(int(ins_per_swap_range['min']), int(ins_per_swap_range['max']))
            instruments = random.sample(all_instruments, ins_count)              

            for instrument in instruments:                                 
                long_short =  self.generate_long_short()  
                purpose = self.generate_purpose()  
                for position_type in ['S', 'I', 'E']:
                    quantity = self.generate_random_integer()
                    for date in date_range:                        
                        records.append({
                            'swap_position_id': swap_position_id,
                            'ric': instrument['ric'],
                            'swap_contract_id': swap_contract['swap_contract_id'],           
                            'position_type': position_type,
                            'knowledge_date': date.date(),
                            'effective_date': date.date(),
                            'account': self.generate_account(),
                            'long_short': long_short,
                            'qty': quantity,
                            'purpose': purpose,
                            'time_stamp': datetime.now(),
                        })
                        i += 1
        
        self.cache.persist_to_cache('swap_positions', records)
        return records
    
    def generate_account(self):
        account_type = random.choice(['ICP', 'ECP'])
        return account_type + ''.join([random.choice(string.digits) for _ in range(4)])   
    
    def generate_long_short(self):       
        return random.choice(['Long', 'Short'])  
    
    def generate_purpose(self):
        return 'Outright'