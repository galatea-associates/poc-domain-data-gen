from abc import ABC, abstractmethod


class Generator(ABC):

    @classmethod
    @abstractmethod
    def instantiate_generator(cls, quantity, database, lock, start_id):
        pass

    @classmethod
    @abstractmethod
    def __get_record(cls, start_id, record_number, database=None):
        pass
