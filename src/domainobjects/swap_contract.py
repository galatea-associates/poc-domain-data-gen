from domainobjects.generatable import Generatable
from functools import partial
import random

class SwapContract(Generatable):

    def generate(self, data_generator, record_count, custom_args):
        # Get the existing swap contracts and the range of ins per swap counts
        counterparties = data_generator.retrieve_from_global_state('counterparty_id')
        swap_per_counterparty_range = custom_args['swap_per_counterparty']
        records = []
        i = 1

        # For each existing swap contract, put the SC ID in the cache and then generate a random number of positions for that SC ID
        for counterparty in counterparties:
            data_generator.persist_to_current_record_state('counterparty_id', counterparty)
            swap_count = random.randint(int(swap_per_counterparty_range['min']), int(swap_per_counterparty_range['max']))
            for j in range(0, swap_count):
                records.append(self.generate_record(data_generator, i))
                i += 1
            
            data_generator.clear_current_record_state()
        
        return records

    def get_template(self, data_generator):
        return {
            'swap_contract_id': {'func': data_generator.generate_new_swap_contract_id,
                                'field_type': 'id'},
            'counterparty_id':  {'func': partial(data_generator.retrieve_from_current_record_state, 'counterparty_id')},
            'swap_mnemonic': {'func': data_generator.generate_rdn},
            'is_short_mtm_financed': {'func': data_generator.generate_rdn},
            'accounting_area': {'func': data_generator.generate_rdn,},
            'status': {'func': data_generator.generate_status},
            'start_date': {'func': data_generator.generate_swap_start_date},
            'end_date': {'func': data_generator.generate_swap_end_date,
                        'args': ['status', 'start_date']},
            'swap_type': {'func': data_generator.generate_swap_type},
            'reference_rate': {'func': data_generator.generate_reference_rate},
            'swap_contract_field1': {'func': data_generator.generate_rdn},
            'swap_contract_field2': {'func': data_generator.generate_rdn},
            'swap_contract_field3': {'func': data_generator.generate_rdn},
            'swap_contract_field4': {'func': data_generator.generate_rdn},
            'swap_contract_field5': {'func': data_generator.generate_rdn},
            'swap_contract_field6': {'func': data_generator.generate_rdn},
            'swap_contract_field7': {'func': data_generator.generate_rdn},
            'swap_contract_field8': {'func': data_generator.generate_rdn},
            'time_stamp': {'func': data_generator.generate_time_stamp},
        }