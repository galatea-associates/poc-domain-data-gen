import pandas as pd

class Cache:

    def __init__(self):
        self.__cache = {}
        self.persist_to_cache('currencies', ['USD', 'CAD', 'EUR', 'GBP'])
        self.persist_to_cache('tickers', pd.read_csv('tickers.csv')['Symbol'].drop_duplicates().values.tolist())
        self.persist_to_cache('exchange_codes', ['L', 'N', 'OQ', 'SI', 'AL', 'VI', 'BB', 'BM', 'BR', 'BG', 'TC', 'TO', 'HK', 'SS',
                                    'FR', 'BE', 'DE', 'JA', 'DE', 'IL', 'VX', 'MFM', 'PA', 'ME', 'NZ'])
        self.persist_to_cache('cois', ['US', 'GB', 'CA', 'FR', 'DE', 'CH', 'SG', 'JP'])         

    def persist_to_cache(self, field_name, field_value):            
        self.__cache[field_name] = field_value       

    def retrieve_from_cache(self, field_name):    
        return self.__cache[field_name]

   