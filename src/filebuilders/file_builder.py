import abc


class FileBuilder(abc.ABC):

    @abc.abstractmethod
    def build(self, file_extension, data, domain_object):      
        pass