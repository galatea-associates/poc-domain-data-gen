from domainobjects.generatable import Generatable
from datetime import datetime

class Instrument(Generatable):
    
    def generate(self, record_count, custom_args):        
        records = []
        persisting = [] # Store only the critical attributes required to generate other domain objects

        for i in range(0, record_count):            
            asset_class = self.generate_asset_class()         
            ticker = self.generate_ticker()
            coi = self.generate_coi()
            exchange_code = self.generate_exchange_code()
            cusip = str(self.generate_random_integer(length=9))
            isin = self.generate_isin(coi, cusip)
            ric = self.generate_ric(ticker, exchange_code)
            sedol = self.generate_random_integer(length=7)
                
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

            persisting.append({
                'ric':ric,
                'cusip':cusip,
                'isin':isin
            })
        
        self.cache.persist_to_cache('instruments', persisting)
        return records
   
    def generate_asset_class(self):
        return 'Stock'
  