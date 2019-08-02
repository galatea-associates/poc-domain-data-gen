from domainobjects.generatable import Generatable
from functools import partial
from datetime import datetime
import random

class StockLoanPosition(Generatable):

    def generate(self, record_count, custom_args, domain_config, file_builder):
        records_per_file = domain_config['max_objects_per_file']
        file_num = 1
        file_extension = "."+str(domain_config['file_builder_name']).lower()
        records = []
        instruments = self.dependency_db.retrieve_from_database('instruments')
        
        for i in range(1, record_count+1):   
            instrument = random.choice(instruments)      
            position_type = self.generate_position_type()
            knowledge_date = self.generate_knowledge_date() 
            collateral_type = self.generate_collateral_type()    
                
            records.append({
                'stock_loan_contract_id': i,
                'ric': instrument['ric'],
                'knowledge_date': knowledge_date,
                'effective_date': self.generate_effective_date(0, knowledge_date, position_type),
                'purpose': self.generate_purpose(),
                'td_qty': self.generate_random_integer(),
                'sd_qty': self.generate_random_integer(),
                'collateral_type': collateral_type,
                'haircut': self.generate_haircut(collateral_type),
                'collateral_margin': self.generate_collateral_margin(collateral_type),
                'rebate_rate': self.generate_rebate_rate(collateral_type),
                'borrow_fee': self.generate_borrow_fee(collateral_type),
                'termination_date': self.generate_termination_date(),
                'account': self.generate_account(),
                'is_callable': self.generate_random_boolean(),
                'return_type': self.generate_return_type(),
                'time_stamp': datetime.now()
            })

            if (i % int(records_per_file) == 0):
                file_builder.build(file_extension, file_num, records, domain_config)
                file_num += 1
                records = []        

        if records != []: 
            file_builder.build(file_extension, file_num, records, domain_config)
    
    def generate_haircut(self, collateral_type):      
        return '2.00%' if collateral_type == 'Non Cash' else None
    
    def generate_collateral_margin(self, collateral_type): 
        return '140.00%' if collateral_type == 'Cash' else None
    
    def generate_collateral_type(self):      
        return random.choice(['Cash', 'Non Cash'])
    
    def generate_termination_date(self):
        does_exist = random.choice([True, False])        
        return None if not does_exist else self.generate_knowledge_date()
        
    def generate_rebate_rate(self, collateral_type):       
        return '5.75%' if collateral_type == 'Cash' else None
    
    def generate_borrow_fee(self, collateral_type):      
        return '4.00%'if collateral_type == 'Non Cash' else None
    
    def generate_purpose(self):      
        return random.choice(['Borrow', 'Loan'])