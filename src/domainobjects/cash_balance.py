from domainobjects.generatable  import Generatable
from functools import partial

class CashBalance(Generatable):

    def get_template(self, data_generator):
        return {
            'amount': {'func': data_generator.generate_qty},
            'curr': {'func': data_generator.generate_currency},
            'account_num': {'func': data_generator.generate_account_number},
            'purpose': {'func': partial(data_generator.generate_purpose, data_type='C')},
            'time_stamp': {'func': data_generator.generate_time_stamp},
        }