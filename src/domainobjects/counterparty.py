from domainobjects.generatable  import Generatable
from functools import partial

class Counterparty(Generatable):

    def get_template(self, data_generator):
        return {
            'counterparty_id': {'func': data_generator.generate_rdn, 'field_type': 'id'},
            'field1': {'func': data_generator.generate_rdn},
            'field2': {'func': data_generator.generate_rdn},
            'field3': {'func': data_generator.generate_rdn},
            'field4': {'func': data_generator.generate_rdn},
            'field5': {'func': data_generator.generate_rdn},
            'field6': {'func': data_generator.generate_rdn},
            'field7': {'func': data_generator.generate_rdn},
            'field8': {'func': data_generator.generate_rdn},
            'field9': {'func': data_generator.generate_rdn},
            'field10': {'func': data_generator.generate_rdn}
        }