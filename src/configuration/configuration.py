class Configuration():

    def __init__(self, configurations):
        """ Assign internal variables to the 4 elements of provided
        configuration dictionary.

        Parameters
        ----------
        configurations : dict
            4 element dictionary containing:
                1. object factory generation arguments
                2. object factory location in codebase
                3. file builder location in codebase
                4. multiprocessing generation arguments
        """

        self.__user_generation_args = configurations['generation_arguments']
        self.__user_shared_generation_args = configurations['shared_arguments']
        self.__dev_file_builder_args = configurations['file_builders']
        self.__dev_factory_args = configurations['domain_objects']

    def get_user_generation_args(self):
        return self.__user_generation_args

    def get_user_shared_generation_args(self):
        return self.__user_shared_generation_args

    def get_dev_file_builder_args(self):
        return self.__dev_file_builder_args

    def get_dev_factory_args(self):
        return self.__dev_factory_args
