from domainobjects.generatable import Generatable
from datetime import datetime
from utils.cache import Cache
import random

class Instrument(Generatable):

    def generate(self, record_count, custom_args, start_id):

        cache = Cache()

        records = []
        persisting_records = []

        for i in range(start_id, start_id+record_count):
            record = self.generate_record(i, cache)
            records.append(record)
            persisting_records.append(
                [record['ric'], record['cusip'], record['isin']]
            )

        self.persist_records("instruments", persisting_records)
        return records

    def generate_record(self, id, cache):
        asset_class = self.generate_asset_class()
        ticker = self.generate_ticker(cache)
        coi = self.generate_coi(cache)
        exchange_code = id
        cusip = str(self.generate_random_integer(length=9))
        isin = self.generate_isin(coi, cusip)
        ric = self.generate_ric(ticker, exchange_code)
        sedol = self.generate_random_integer(length=7)
        return {
                'instrument_id': id,
                'ric': ric,
                'isin': isin,
                'sedol': sedol,
                'ticker': ticker,
                'cusip': cusip,
                'asset_class': asset_class,
                'coi': coi,
                'time_stamp': datetime.now()
            }

    def generate_asset_class(self):
        return 'Stock'

    def generate_sequential_exchange_code(self, current_tickers, ticker):
        if (ticker in current_tickers.keys()):
            cur_val = current_tickers[ticker]
            current_tickers[ticker] = cur_val+1
        else:
            current_tickers[ticker] = 0
        return current_tickers[ticker]

    def generate_coi(self, cache):
        return random.choice(cache.retrieve_from_cache('cois'))

    def generate_ticker(self, cache):
        return random.choice(cache.retrieve_from_cache('tickers'))

    def generate_exchange_code(self, cache):
        return random.choice(cache.retrieve_from_cache('exchange_codes'))
