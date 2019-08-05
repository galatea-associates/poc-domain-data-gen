from domainobjects.generatable import Generatable
from datetime import datetime

class Instrument(Generatable):
    
    def generate(self, record_count, custom_args, domain_config, file_builder):        
        records_per_file = domain_config['max_objects_per_file']
        file_num = 1
        file_extension = "."+str(domain_config['file_builder_name']).lower()
        records = []

        for i in range(0, record_count):            
            asset_class = self.generate_asset_class()         
            ticker = self.generate_ticker()
            coi = self.generate_coi()
            exchange_code = self.generate_exchange_code()
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
            
            # TODO: FIX HERE: Add query construction to persisting function
            self.dependency_db.persist_to_database("instruments","('"+ric+"','"+cusip+"','"+isin+"')")

            if (j % int(records_per_file) == 0):
                file_builder.build(file_extension, file_num, records, domain_config)
                file_num += 1
                records = []
        
        if records != []: 
            file_builder.build(file_extension, file_num, records, domain_config)
   
    def generate_asset_class(self):
        return 'Stock'
  