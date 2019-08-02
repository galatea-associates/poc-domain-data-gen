from domainobjects.generatable import Generatable
from datetime import datetime, timedelta
import random
import string
import pandas as pd

class SwapPosition(Generatable):
    
    def generate(self, record_count, custom_args, domain_config, file_builder):        
        swap_contracts = self.dependency_db.retrieve_from_database('swap_contracts')
        ins_per_swap_range = custom_args['ins_per_swap']
        
        records_per_file = domain_config['max_objects_per_file']
        file_num = 1
        file_extension = "."+str(domain_config['file_builder_name']).lower()
        records = []

        i = 1
        all_instruments = self.dependency_db.retrieve_from_database('instruments')
        start_date = datetime.strptime(custom_args['start_date'], '%Y%m%d')
        date_range = pd.date_range(start_date, datetime.today(), freq='D')        
        
        for swap_contract in swap_contracts:                                    
            ins_count = random.randint(int(ins_per_swap_range['min']), int(ins_per_swap_range['max']))
            instruments = random.sample(all_instruments, ins_count) 

            for instrument in instruments:                                 
                long_short =  self.generate_long_short()  
                purpose = self.generate_purpose()  
                for position_type in ['S', 'I', 'E']:
                    quantity = self.generate_random_integer(negative=long_short.upper() == "SHORT")
                    for date in date_range:                        
                        records.append({
                            'swap_position_id': i,
                            'ric': instrument['ric'],
                            'swap_contract_id': swap_contract['id'],           
                            'position_type': position_type,
                            'knowledge_date': date.date(),
                            'effective_date': date.date(),
                            'account': self.generate_account(),
                            'long_short': long_short,
                            'td_quantity': quantity,
                            'purpose': purpose,
                            'time_stamp': datetime.now(),
                        })
                        
                        # TODO: FIX HERE
                        row_to_add = "('"+str(swap_contract['id'])+"','"+instrument['ric']+"','"+position_type+"','"+datetime.strftime(date.date(), '%Y%m%d')+"','"+str(long_short)+"')"
                        self.dependency_db.persist_to_database('swap_positions', row_to_add)
                        
                        if (i % int(records_per_file) == 0):
                            file_builder.build(file_extension, file_num, records, domain_config)
                            file_num += 1
                            records = []
                        
                        i += 1

        if records != []: 
            file_builder.build(file_extension, file_num, records, domain_config)
    
    def generate_account(self):
        account_type = random.choice(['ICP', 'ECP'])
        return account_type + ''.join([random.choice(string.digits) for _ in range(4)])   
    
    def generate_long_short(self):       
        return random.choice(['Long', 'Short'])  
    
    def generate_purpose(self):
        return 'Outright'