from domainobjects.generatable  import Generatable
from functools import partial

class Cashflow(Generatable):

    def get_template(self, data_generator):
        return {
            'cashflow_id': {'func': data_generator.generate_rdn, 'field_type': 'id'},
            'swap_contract_id': {'func': data_generator.generate_rdn},
            'instrument_id': {'func': data_generator.generate_rdn},
            'type': {'func': data_generator.generate_rdn},
            'pay_date': {'func': data_generator.generate_rdn},
            'effective_date': {'func': data_generator.generate_rdn},
            'currency': {'func': data_generator.generate_rdn},
            'amount': {'func': data_generator.generate_rdn},
            'long_short': {'func': data_generator.generate_rdn},
            'field1': {'func': data_generator.generate_rdn},
            'field2': {'func': data_generator.generate_rdn},
            'field3': {'func': data_generator.generate_rdn},
            'field4': {'func': data_generator.generate_rdn},
            'field5': {'func': data_generator.generate_rdn}            
        }