from abc import ABC, abstractmethod
import random

class Generatable(ABC):

    @abstractmethod
    def get_template(self, data_generator, custom_args):
        pass
    
    def generate(self, data_generator, record_count, custom_args):
        records = []
        for i in range(0, record_count):
            records.append(self.generate_record(data_generator, i + 1))
            data_generator.clear_current_record_state()
        
        return records

    def generate_record(self, data_generator, current_record):
        data = {}
        template = self.get_template(data_generator)
        for field, field_data in template.items():
            field_generator = field_data.get('func')
            field_args = field_data.get('args')
            field_type = field_data.get('field_type')

            if field_type == "id":
                data[field] = current_record                
                data_generator.persist_to_global_state(field, current_record)   
                continue
            elif field_type == "key":
                values = data_generator.retrieve_from_global_state(field)
                data[field] = random.choice(values)   
                continue

            if not self.__field_already_generated(field, data):
                if self.__is_key(field, data):
                    suffix = '*'
                    field = self.__remove_asterisk_from_field_name(field)
                else:
                    suffix = ''

                if data_generator.state_contains_field(field):
                    data[field + suffix] = data_generator.get_state_value(field)
                elif 'args' in field_data:
                    args_needed = field_args
                    args_generated = self.__generate_args_for_generator_function(data_generator, args_needed, data)
                    data[field + suffix] = field_generator(**args_generated)
                else:
                    data[field + suffix] = field_generator()
        
        return data

    def __remove_asterisk_from_field_name(self, field):
        return field.replace('*', '')

    def __is_key(self, field, data):
        return field + '*' in data

    def __field_already_generated(self, field, data):
        return field in data

    def __generate_args_for_generator_function(self, data_generator, args_needed, data):
        args_generated = {}
        for field in args_needed:
            if self.__field_already_generated(field, data):
                args_generated[field] = data[field]
            elif self.__is_key(field, data):
                args_generated[field] = data[field + '*']
            elif data_generator.state_contains_field(field):
                args_generated[field] = data_generator.get_state_value(field)
        return args_generated

   
