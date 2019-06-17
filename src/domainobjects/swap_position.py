from domainobjects.generatable import Generatable
from functools import partial

class SwapPosition(Generatable):

    def get_template(self, data_generator):
        return {
            'ric*': {'func': partial(data_generator.generate_ric, no_cash=True),
                    'args': ['ticker', 'asset_class']},
            'swap_contract_id*': {'func': data_generator.generate_swap_contract_id},
            'position_type*': {'func': data_generator.generate_position_type},
            'knowledge_date*': {'func': data_generator.generate_knowledge_date},
            'effective_date*': {'func': partial(data_generator.generate_effective_date,
                                                n_days_to_add=3),
                                'args': ['knowledge_date', 'position_type']},
            'account*': {'func': data_generator.generate_account},
            'direction': {'func': data_generator.generate_direction},
            'qty': {'func': data_generator.generate_qty},
            'purpose*': {'func': partial(data_generator.generate_purpose, data_type='ST')},
            'time_stamp': {'func': data_generator.generate_time_stamp},
        }