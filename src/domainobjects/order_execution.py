from domainobjects.generatable import Generatable
from functools import partial

class OrderExecution(Generatable):

    def get_template(self, data_generator):
        return {
            'order_id*': {'func': data_generator.generate_order_id, 'args': ['asset_class']},
            'account_num': {'func': data_generator.generate_account_number},
            'direction': {'func': data_generator.generate_direction},
            'sto_id': {'func': data_generator.generate_sto_id, 'args': ['asset_class']},
            'agent_id': {'func': data_generator.generate_agent_id, 'args': ['asset_class']},
            'price': {'func': data_generator.generate_price, 'args': ['inst_id']},
            'curr': {'func': data_generator.generate_currency},
            'ric': {'func': partial(data_generator.generate_ric, no_cash=True),
                    'args': ['ticker', 'asset_class']},
            'qty': {'func': data_generator.generate_qty},
            'time_stamp': {'func': data_generator.generate_time_stamp},
        }