import pandas as pd

class Cache:

    def __init__(self):
        self.__cache = {}         

    def persist_to_cache(self, field_name, field_value):            
        self.__cache[field_name] = field_value       

    def retrieve_from_cache(self, field_name):    
        return self.__cache[field_name]

   