from domainobjects.generatable import Generatable
from functools import partial

class SwapContract(Generatable):

    def get_template(self, data_generator):
        return {
            'swap_contract_id*': {'func': data_generator.generate_new_swap_contract_id},
            'status': {'func': data_generator.generate_status},
            'start_date': {'func': data_generator.generate_swap_start_date},
            'end_date': {'func': data_generator.generate_swap_end_date,
                        'args': ['status', 'start_date']},
            'swap_type': {'func': data_generator.generate_swap_type},
            'reference_rate': {'func': data_generator.generate_reference_rate},
            'field1': {'func': data_generator.generate_rdn},
            'field2': {'func': data_generator.generate_rdn},
            'field3': {'func': data_generator.generate_rdn},
            'field4': {'func': data_generator.generate_rdn},
            'field5': {'func': data_generator.generate_rdn},
            'field6': {'func': data_generator.generate_rdn},
            'field7': {'func': data_generator.generate_rdn},
            'field8': {'func': data_generator.generate_rdn},
            'time_stamp': {'func': data_generator.generate_time_stamp},
        }