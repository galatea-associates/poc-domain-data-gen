from domainobjects.generatable import Generatable
from datetime import datetime

class Instrument(Generatable):
    
    def generate(self, record_count, custom_args):        
        records = []
        
        for i in range(0, record_count):            
            asset_class = self.generate_asset_class()         
            ticker = self.generate_currency() if asset_class == 'Cash' else self.generate_ticker()            
            exchange_country = '' if asset_class == 'Cash' else self.generate_exchange_country()
            exchange_code = '' if asset_class == 'Cash' else exchange_country[0]
            coi = '' if asset_class == 'Cash' else exchange_country[1]            
            cusip = '' if asset_class == 'Cash' else str(self.generate_random_integer(length=9))
            isin = '' if asset_class == 'Cash' else self.generate_isin(coi, cusip)
            ric = '' if asset_class == 'Cash' else self.generate_ric(ticker, exchange_code)
            sedol = '' if asset_class == 'Cash' else self.generate_random_integer(length=7)
                
            records.append({
                'instrument_id':i+1,
                'ric':ric,
                'isin':isin,
                'sedol':sedol,
                'ticker':ticker,
                'cusip':cusip,
                'asset_class':asset_class,
                'coi':coi,
                'time_stamp':datetime.now()})
        
        self.cache.persist_to_cache('instruments', records)
        return records
   
  