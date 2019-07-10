from domainobjects.generatable import Generatable
from functools import partial
from datetime import datetime, timedelta
import random

class SwapPosition(Generatable):

    def generate(self, data_generator, record_count, custom_args):
        # Get the existing swap contracts and the range of ins per swap counts
        swap_contracts = data_generator.retrieve_from_global_state('swap_contract_id')
        ins_per_swap_range = custom_args['ins_per_swap']
        records = []
        i = 1

        # For each existing swap contract, put the SC ID in the cache and then generate a random number of positions for that SC ID
        for swap_contract in swap_contracts:
            data_generator.persist_to_current_record_state('swap_contract_id', swap_contract)            
            start_date = datetime.strptime(custom_args['start_date'], '%Y%m%d')
            day_count = (datetime.today() - start_date).days + 1

            ins_count = random.randint(int(ins_per_swap_range['min']), int(ins_per_swap_range['max']))
            instruments = random.sample(data_generator.retrieve_from_global_state('instrument_id'), ins_count)       

            for instrument in instruments:
                data_generator.persist_to_current_record_state('instrument_id', instrument)    
                data_generator.persist_to_global_state("swap_contract_instrument", (swap_contract, instrument))        
                
                for position_type in ['S', 'I', 'E']:
                    data_generator.persist_to_current_record_state('position_type', position_type)

                    for date in (start_date + timedelta(n) for n in range(day_count)):
                        data_generator.persist_to_current_record_state('effective_date', date.date())                                    
                        records.append(self.generate_record(data_generator, i))
                        i += 1
                
            data_generator.clear_current_record_state()
        
        return records

    def get_template(self, data_generator):
        return {
            'swap_position_id': {'func': data_generator.generate_new_swap_contract_id,
                                'field_type': 'id'},
            'ric': {'func': partial(data_generator.generate_ric, no_cash=True),
                    'args': ['asset_class']},
            'swap_contract_id': {'func': partial(data_generator.retrieve_from_current_record_state, 'swap_contract_id')},           
            'position_type': {'func': partial(data_generator.retrieve_from_current_record_state, 'position_type')},
            'knowledge_date': {'func': data_generator.generate_knowledge_date},
            'effective_date': {'func': partial(data_generator.retrieve_from_current_record_state, 'effective_date')},
            'account': {'func': data_generator.generate_account},
            'direction': {'func': data_generator.generate_direction},
            'qty': {'func': data_generator.generate_qty},
            'purpose': {'func': partial(data_generator.generate_purpose, data_type='ST')},
            'time_stamp': {'func': data_generator.generate_time_stamp},
        }