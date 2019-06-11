from builtins import StopIteration

import pandas as pd
from Runnable import Runnable

from multiprocessing import Lock
converters = {
    "asset_class": str,
    "coi": str,
    "ric": str,
    "isin": str,
    "sedol": int,
    "cusip": int,
    "ticker": str,
    "qty": int,
    "td_qty": int,
    "sd_qty": int,
    "price": float,
    "curr": str,
    'position_type': str,
    'knowledge_date': str,
    'effective_date': str,
    'termination_date': str,
    'start_date': str,
    'end_date': str,
    'account': str,
    'direction': str,
    'purpose': str,
    'collateral_type': str,
    'depot_id': int,
    'order_id': int,
    'sto_id': int,
    'agent_id': int,
    'stock_loan_contract_id': int,
    'swap_contract_id': int,
    'haircut': str,
    'collateral_margin': str,
    'rebate_rate': str,
    'borrow_fee': str,
    'is_callable': str,
    'return_type': str,
    'reference_rate': str,
    'swap_type': str,
    'status': str,
    'field1': str,
    'field2': str,
    'field3': str,
    'field4': str,
    'field5': str,
    'field6': str,
    'field7': str,
    'field8': str
}

class CSVReader(Runnable):
    def __init__(self):
        self.__file_reader = None
        self.__lock = Lock()

    def __setup_file_reader(self, file, chunksize):
        self.__file_reader = pd.read_csv(
            file,
            chunksize=chunksize,
            low_memory=False,
            converters=converters,
            keep_default_na=True)

    def __get_next_chunk(self):
        with self.__lock:
            try:
                return self.__file_reader.get_chunk().to_dict(orient='records')

            #If EOF a StopIteration exception occurs
            except StopIteration:
                return None

    # In DataConfiguration.py, 'Data Args' field should look like:
    # {'File': './out/prices.csv',
    #  'Format' : 'CSV',
    #  'Chunk Size': 1,
    #  'Loop on end': True}
    def run(self, args):
        with self.__lock:
            if self.__file_reader is None:
                self.__setup_file_reader(file=args["File"], chunksize=args["Chunk Size"])

        data = self.__get_next_chunk()
        
        #Data will be None if EOF occured
        if data is None:
            if args["Loop on end"]:
                
                #If loop on EOF then start reader again at beginning
                self.__setup_file_reader(file=args["File"], chunksize=args["Chunk Size"])
                data = self.__get_next_chunk()
            else:
                return None

        return data

    