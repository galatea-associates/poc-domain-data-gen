from domainobjects.generatable import Generatable
from datetime import datetime

class Instrument(Generatable):
    
    def generate(self, custom_args, instrument_id):            
        asset_class = self.generate_asset_class()         
        ticker = self.generate_currency() if asset_class == 'Cash' else self.generate_ticker()
        coi = '' if asset_class == 'Cash' else self.generate_coi()
        exchange_code = '' if asset_class == 'Cash' else self.generate_exchange_code()
        cusip = '' if asset_class == 'Cash' else str(self.generate_random_integer(length=9))
        isin = '' if asset_class == 'Cash' else self.generate_isin(coi, cusip)
        ric = '' if asset_class == 'Cash' else self.generate_ric(ticker, exchange_code)
        sedol = '' if asset_class == 'Cash' else self.generate_random_integer(length=7)
            
        record = {
            'instrument_id':instrument_id,
            'ric':ric,
            'isin':isin,
            'sedol':sedol,
            'ticker':ticker,
            'cusip':cusip,
            'asset_class':asset_class,
            'coi':coi,
            'time_stamp':datetime.now()}
    
        self.cache.append_to_cache('instruments', record)
        return record