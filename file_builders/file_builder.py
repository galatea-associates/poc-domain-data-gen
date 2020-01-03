from abc import ABC, abstractmethod
from main import get_class
from database.database import Database


class FileBuilder(ABC):

    @classmethod
    @abstractmethod
    def build(
            cls,
            output_directory,
            file_name,
            generator_config,
            quantity,
            lock,
            start_id
    ):
        pass

    @staticmethod
    def get_generator(generator_config, quantity, lock, start_id):
        lock.acquire()
        database = Database()
        lock.release()
        module_name = generator_config["module_name"]
        class_name = generator_config["class_name"]
        generator_class = get_class(
            "generators", module_name, class_name
        )
        generator = generator_class.instantiate_generator(
            quantity, database, lock, start_id
        )
        return generator

