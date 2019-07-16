import abc


class FileBuilder(abc.ABC):

    @abc.abstractmethod
    def build(self, output_dir, file_name, file_extension, data, objects_per_file, root_element_name):
        pass