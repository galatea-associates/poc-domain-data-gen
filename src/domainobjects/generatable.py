from abc import ABC, abstractmethod

class Generatable(ABC):
    
    def generate(self, data_generator, record_count):
        records = []
        for i in range(0, record_count):
            records.append(self.__generate_record(data_generator))
        
        return records

    def __generate_record(self, data_generator):
        data = {}
        template = self.get_template(data_generator)
        for field, generator_function in template.items():
            if not self.__field_already_generated(field, data):
                if self.__is_key(field, data):
                    suffix = '*'
                    field = self.__remove_asterisk_from_field_name(field)
                else:
                    suffix = ''

                if data_generator.state_contains_field(field):
                    data[field + suffix] = data_generator.get_state_value(field)
                elif 'args' in generator_function:
                    args_needed = generator_function['args']
                    args_generated = self.__generate_args_for_generator_function(data_generator, args_needed, data)
                    data[field + suffix] = generator_function['func'](**args_generated)
                else:
                    data[field + suffix] = generator_function['func']()
        data_generator.clear_state()
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

    @abstractmethod
    def get_template(self, data_generator):
        pass
