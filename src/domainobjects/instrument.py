from domainobjects.generatable import Generatable
from functools import partial

class Instrument(Generatable):

    def get_template(self, data_generator):
        return {
            'ric*': {'func': data_generator.generate_new_ric, 'args': ['asset_class']},
            'isin': {'func': data_generator.generate_isin,
                        'args': ['coi', 'cusip', 'asset_class']},
            'sedol': {'func': data_generator.generate_sedol,
                        'args': ['ticker', 'asset_class']},
            'ticker': {'func': partial(data_generator.generate_ticker, new_ric_generator=True),
                        'args': ['asset_class', 'ric']},
            'cusip': {'func': data_generator.generate_cusip,
                        'args': ['ticker', 'asset_class']},
            'asset_class': {'func': partial(data_generator.generate_asset_class,
                                            generating_inst=True)},
            'coi': {'func': data_generator.generate_coi, 'args': ['asset_class']},
            'time_stamp': {'func': data_generator.generate_time_stamp},
        }