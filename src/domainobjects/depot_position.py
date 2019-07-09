from domainobjects.generatable import Generatable
from functools import partial

class DepotPosition(Generatable):

    def get_template(self, data_generator):
        return {
            'isin': {'func': partial(data_generator.generate_isin, no_cash=True),
                    'args': ['coi', 'cusip', 'asset_class']},
            'knowledge_date': {'func': data_generator.generate_knowledge_date},
            'effective_date': {'func': data_generator.generate_effective_date,
                                'args': ['knowledge_date', 'position_type']},
            'account': {'func': partial(data_generator.generate_account, no_ecp=True)},
            'qty': {'func': data_generator.generate_qty},
            'purpose': {'func': partial(data_generator.generate_purpose, data_type='DP')},
            'depot_id': {'func': data_generator.generate_depot_id},
            'time_stamp': {'func': data_generator.generate_time_stamp},
        }