class Configuration:

    def __init__(self, configurations):
        """ Assign internal variables to the 4 elements of provided
        configuration dictionary.

        Parameters
        ----------
        configurations : dict
            4 element dictionary containing:
                1. object factory generation arguments (factory definitions)
                2. object factory location in codebase (dev_factory_args)
                3. file builder location in codebase (file_builder_args)
                4. multiprocessing generation arguments (shared_args)
        """

        self.__factory_definitions = configurations['factory_definitions']
        self.__shared_args = configurations['shared_args']
        self.__dev_file_builder_args = configurations['dev_file_builder_args']
        self.__dev_factory_args = configurations['dev_factory_args']

    def get_factory_definitions(self):
        """ Return the user-specific object generation arguments.

        Returns
        -------
        dict
            User-specific object generation arguments
        """

        return self.__factory_definitions

    def get_shared_args(self):
        """ Return the user-specific multiprocessing-centric generation
        arguments.

        Returns
        -------
        dict
            User-specific multiprocessing-centric generation arguments
        """

        return self.__shared_args

    def get_dev_file_builder_args(self):
        """ Return the developer-specific file builder arguments. These are
        used when locating file builders in the codebase by module/class
        names.

        Returns
        -------
        dict
            Developer-specific file builder arguments
        """

        return self.__dev_file_builder_args

    def get_dev_factory_args(self):
        """ Return the developer-specific object factory arguments. These are
        used when locating object factories in the codebase by module/class
        names.

        Returns
        -------
        dict
            Developer-specific object factory arguments.
        """

        return self.__dev_factory_args
