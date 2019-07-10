from domainobjects.generatable  import Generatable
from functools import partial

class Counterparty(Generatable):

    def get_template(self, data_generator):
        return {
            'counterparty_id': {'func': data_generator.generate_rdn, 'field_type': 'id'},
            'counterparty_field1': {'func': data_generator.generate_rdn},
            'counterparty_field2': {'func': data_generator.generate_rdn},
            'counterparty_field3': {'func': data_generator.generate_rdn},
            'counterparty_field4': {'func': data_generator.generate_rdn},
            'counterparty_field5': {'func': data_generator.generate_rdn},
            'counterparty_field6': {'func': data_generator.generate_rdn},
            'counterparty_field7': {'func': data_generator.generate_rdn},
            'counterparty_field8': {'func': data_generator.generate_rdn},
            'counterparty_field9': {'func': data_generator.generate_rdn},
            'counterparty_field10': {'func': data_generator.generate_rdn}
        }