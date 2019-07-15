from domainobjects.generatable import Generatable
from functools import partial

class FrontOfficePosition(Generatable):

    def get_template(self, data_generator):
        return {
            'ric': {'func': partial(data_generator.generate_ric, no_cash=True),
                    'args': ['ticker', 'asset_class']},
            'position_type': {'func': data_generator.generate_position_type},
            'knowledge_date': {'func': data_generator.generate_knowledge_date},
            'effective_date': {
                'func': partial(data_generator.generate_effective_date, n_days_to_add=0),
                'args': ['knowledge_date', 'position_type']},
            'account': {'func': partial(data_generator.generate_account, no_ecp=True)},
            'direction': {'func': data_generator.generate_direction},
            'qty': {'func': data_generator.generate_qty},
            'purpose': {'func': partial(data_generator.generate_purpose, data_type='FOP')},
            'time_stamp': {'func': data_generator.generate_time_stamp},
        }