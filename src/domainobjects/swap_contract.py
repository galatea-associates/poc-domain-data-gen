from domainobjects.generatable import Generatable
import random
from datetime import datetime, timedelta

class SwapContract(Generatable):
    
    def generate(self, record_count, custom_args, domain_config, file_builder):
        
        # Get the existing swap contracts and the range of ins per swap counts
        # counterparties = self.cache.retrieve_from_cache('counterparties')
        counterparties = self.dependency_db.retrieve_from_database('counterparties')
        swap_per_counterparty_min = int(custom_args['swap_per_counterparty']['min'])
        swap_per_counterparty_max = int(custom_args['swap_per_counterparty']['max'])
        
        records_per_file = domain_config['max_objects_per_file']
        file_num = 1
        file_extension = "."+str(domain_config['file_builder_name']).lower()
        records = []
        i = 1

        # For each existing swap contract, put the SC ID in the cache and then generate a random number of positions for that SC ID
        for counterparty in counterparties:            
            swap_count = random.randint(swap_per_counterparty_min, swap_per_counterparty_max)
            for _ in range(0, swap_count):
                start_date = self.generate_random_date()
                status = self.generate_status()
                records.append({
                    'swap_contract_id': i,
                    'counterparty_id': counterparty['id'],
                    'swap_mnemonic': self.generate_random_string(10),
                    'is_short_mtm_financed': self.generate_random_boolean(),
                    'accounting_area': self.generate_random_string(10),
                    'status': status,
                    'start_date': start_date,
                    'end_date': self.generate_swap_end_date(start_date=start_date, status=status),
                    'swap_type': self.generate_swap_type(),
                    'reference_rate': self.generate_reference_rate(),
                    'swap_contract_field1': self.generate_random_string(10),
                    'swap_contract_field2': self.generate_random_string(10),
                    'swap_contract_field3': self.generate_random_string(10),
                    'swap_contract_field4': self.generate_random_string(10),
                    'swap_contract_field5': self.generate_random_string(10),
                    'swap_contract_field6': self.generate_random_string(10),
                    'swap_contract_field7': self.generate_random_string(10),
                    'swap_contract_field8': self.generate_random_string(10),
                    'time_stamp': datetime.now(),
                })

                # TODO: FIX HERE: Add query construction to persisting function
                self.dependency_db.persist_to_database("swap_contracts","('"+str(i)+"')")

                if (i % int(records_per_file) == 0):
                    file_builder.build(None, file_extension, file_num, records, domain_config)
                    file_num += 1
                    records = []
                
                i += 1
        
        if records != []: 
            file_builder.build(None, file_extension, file_num, records, domain_config)  
        
        self.dependency_db.commit_changes()
    
    def generate_swap_end_date(self, years_to_add=5, start_date=None, status=None):
        return None if status == 'Live' else start_date + timedelta(days=365 * years_to_add)
    
    def generate_swap_type(self):      
        return random.choice(['Equity', 'Portfolio'])
    
    def generate_reference_rate(self):
        return random.choice(['LIBOR'])
    
    def generate_status(self):      
        return random.choice(['Live', 'Dead'])