from domainobjects.generatable import Generatable
from functools import partial

class Price(Generatable):

    def get_template(self, data_generator):
        return {
            'ric': {'func': partial(data_generator.generate_ric, no_cash=True),
                    'args': ['ticker', 'ric']},
            'price': {'func': data_generator.generate_price, 'args': ['ticker']},
            'curr': {'func': partial(data_generator.generate_currency, for_ticker=True)},
            'update_time_stamp*': {'func': data_generator.generate_update_time_stamp}
        }