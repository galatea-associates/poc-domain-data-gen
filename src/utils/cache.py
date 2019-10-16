"""Utility class containing instrument-specific information. This information
is used to generate domain-valid currencies, ticker symbols, exchange codes,
countries of origin, and any combination thereof such as RICs 
"""

import pandas as pd

class Cache:
    """
    A Class acting as a remote store for instrument-specific information.
    Created to keep track of which combinations of the hard-coded values have
    already been generated with the sole purpose of avoiding duplication.

    Attributes
    ----------
    cache : dict
        Stores specified key, value(s) pairs. Primarily used to keep track of
        what prior generations have yielded to avoid duplications.
        Further use to store domain-specific data such as that listed.

    Methods
    -------
    persist_to_cache(field_name, field_value)
        Stores the given value in the pseudo-cache(dict) under the given key

    retrieve_from_cache(field_name)
        Returns the value stored under given key 

    """

    def __init__(self):
        self.__cache = {}
        self.persist_to_cache('currencies', ['USD', 'CAD', 'EUR', 'GBP'])
        self.persist_to_cache('tickers', pd.read_csv('tickers.csv')['Symbol']
                              .drop_duplicates().values.tolist())
        self.persist_to_cache('exchange_codes', ['L', 'N', 'OQ', 'SI', 'AL',
                                                 'VI', 'BB', 'BM', 'BR', 'BG',
                                                 'TC', 'TO', 'HK', 'SS', 'FR',
                                                 'BE', 'DE', 'JA', 'DE', 'IL',
                                                 'VX', 'MFM', 'PA', 'ME',
                                                 'NZ'])
        self.persist_to_cache('countries_of_issuance', 
                              ['US', 'GB', 'CA', 'FR',
                               'DE', 'CH', 'SG', 'JP'])

    def persist_to_cache(self, field_name, field_value):
        """Stores a given value into the cache under a given key.

        Parameters
        ----------
        field_name : String
            Key value to store under
        field_value : String
            Value to store
        """
        self.__cache[field_name] = field_value

    def retrieve_from_cache(self, field_name):
        """ Retrieves a value from the cache stored under a given key.

        Parameters
        ----------
        field_name : String
            Key value to retrieve the corresponding value of

        Returns
        -------
        Value
            The value stored under the provided key value
        """
        return self.__cache[field_name]
