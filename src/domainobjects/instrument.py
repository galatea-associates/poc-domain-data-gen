from domainobjects.generatable import Generatable
from datetime import datetime

class Instrument(Generatable):
    
    def generate(self, record_count, custom_args):  
        config = self.get_object_config()
        records_per_file = config['max_objects_per_file']
        file_num = 1

        database = self.get_database()
        file_builder = self.get_file_builder()
        
        records = []
        current_tickers = {}

        for i in range(0, record_count):            
            asset_class = self.generate_asset_class()         
            ticker = self.generate_ticker()
            coi = self.generate_coi()
            exchange_code = self.generate_sequential_exchange_code(current_tickers, ticker)
            cusip = str(self.generate_random_integer(length=9))
            isin = self.generate_isin(coi, cusip)
            ric = self.generate_ric(ticker, exchange_code)
            sedol = self.generate_random_integer(length=7)
            j = i+1    

            records.append({
                'instrument_id':j,
                'ric':ric,
                'isin':isin,
                'sedol':sedol,
                'ticker':ticker,
                'cusip':cusip,
                'asset_class':asset_class,
                'coi':coi,
                'time_stamp':datetime.now()})
            
            database.persist("instruments",[ric, cusip, isin])

            if (j % int(records_per_file) == 0):
                file_builder.build(file_num, records)
                file_num += 1
                records = []
        
        if records != []: 
            file_builder.build(file_num, records)
        current_tickers = {}

        database.commit_changes()

    def generate_asset_class(self):
        return 'Stock'

    def generate_sequential_exchange_code(self, current_tickers, ticker):
        if (ticker in current_tickers.keys()):
            cur_val = current_tickers[ticker]
            current_tickers[ticker] = cur_val+1
        else:
            current_tickers[ticker] = 0 
        return current_tickers[ticker]