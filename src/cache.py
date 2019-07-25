import pandas as pd

class Cache:

    def __init__(self):
        self.__cache = {}         

    def persist_to_cache(self, field_name, field_value):            
        self.__cache[field_name] = field_value       

    def append_to_cache(self, field_name, field_value):
        if field_name in self.__cache:
            self.__cache[field_name].append(field_value)
        else:
            field_name_list = []
            field_name_list.append(field_value)
            self.__cache[field_name] = field_name_list
            

    def retrieve_from_cache(self, field_name):    
        return self.__cache[field_name]