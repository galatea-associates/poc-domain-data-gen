class ConfigError(Exception):
    """ Raised when there is an issue with the user-defined configuration.
    Due to prior checks compiling a list of these, all are returned and
    displayed to the user.
    """

    def __init__(self):
        pass