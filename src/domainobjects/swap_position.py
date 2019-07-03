from domainobjects.generatable import Generatable
from functools import partial
import random

class SwapPosition(Generatable):

    def generate(self, data_generator, record_count, custom_args):
        # Get the existing swap contracts and the range of ins per swap counts
        swap_contracts = data_generator.retrieve_from_global_state('swap_contract_id')
        ins_per_swap_range = list(filter(lambda custom_arg: custom_arg['name'] == 'ins_per_swap', custom_args))[0]
        records = []

        # For each existing swap contract, put the SC ID in the cache and then generate a random number of positions for that SC ID
        for swap_contract in swap_contracts:
            data_generator.persist_to_current_record_state('swap_contract_id', swap_contract)
            ins_count = random.randint(int(ins_per_swap_range['min']), int(ins_per_swap_range['max']))
            for i in range(0, ins_count):
                records.append(self.generate_record(data_generator, i + 1))
            
            data_generator.clear_current_record_state()
        
        return records

    def get_template(self, data_generator):
        return {
            'ric': {'func': partial(data_generator.generate_ric, no_cash=True),
                    'args': ['asset_class']},
            'swap_contract_id': {'func': partial(data_generator.retrieve_from_current_record_state, 'swap_contract_id')},
            'instrument_id': {'func': data_generator.generate_swap_contract_id,
                                    'field_type': 'key'},
            'position_type': {'func': data_generator.generate_position_type},
            'knowledge_date': {'func': data_generator.generate_knowledge_date},
            'effective_date': {'func': partial(data_generator.generate_effective_date,
                                                n_days_to_add=3),
                                'args': ['knowledge_date', 'position_type']},
            'account': {'func': data_generator.generate_account},
            'direction': {'func': data_generator.generate_direction},
            'qty': {'func': data_generator.generate_qty},
            'purpose': {'func': partial(data_generator.generate_purpose, data_type='ST')},
            'time_stamp': {'func': data_generator.generate_time_stamp},
        }