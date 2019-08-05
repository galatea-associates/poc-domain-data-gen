from domainobjects.generatable import Generatable
from datetime import datetime, timedelta
import random
import timeit
import string
import pandas as pd

class SwapPosition(Generatable):
    
    def generate(self, record_count, custom_args, domain_config, file_builder):        
        ins_per_swap_range = custom_args['ins_per_swap']
        
        records_per_file = domain_config['max_objects_per_file']
        file_extension = "."+str(domain_config['file_builder_name']).lower()
        file_num = 1
        records = []
        i = 1
        
        all_instruments = self.dependency_db.retrieve_from_database('instruments')
        start_date = datetime.strptime(custom_args['start_date'], '%Y%m%d')
        date_range = pd.date_range(start_date, datetime.today(), freq='D')        
        
        batch_size = int(records_per_file)
        offset = 0

        while True:
            batch_start_time = timeit.default_timer()
            swap_contract_batch = self.dependency_db.retrieve_batch_from_database('swap_contracts', batch_size, offset)
            offset += batch_size

            for swap_contract in swap_contract_batch:                                    
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
                            
                            # TODO: FIX HERE: Add query construction to persisting function
                            row_to_add = "('"+str(swap_contract['id'])+"','"+instrument['ric']+"','"+position_type+"','"+datetime.strftime(date.date(), '%Y%m%d')+"','"+str(long_short)+"')"
                            # TODO: Alter query to only persist those with position type "E", remove for loop from cashflow generation referencing the same
                            self.dependency_db.persist_to_database('swap_positions', row_to_add)
                            
                            if (i % int(records_per_file) == 0):
                                file_builder.build(file_extension, file_num, records, domain_config)
                                file_num += 1
                                records = []
                            
                            i += 1
            batch_end_time = timeit.default_timer()
            print ("Swap Position Batch: "+str(file_num)+" took "+str(batch_end_time-batch_start_time))
            if not swap_contract_batch:
                break

        if records != []: 
            file_builder.build(file_extension, file_num, records, domain_config)
    
    def generate_account(self):
        account_type = random.choice(['ICP', 'ECP'])
        return account_type + ''.join([random.choice(string.digits) for _ in range(4)])   
    
    def generate_long_short(self):       
        return random.choice(['Long', 'Short'])  
    
    def generate_purpose(self):
        return 'Outright'