class Configuration():

    def __init__(self, configurations):
    """ Assign internal variables to the 4 elements of provided configuration
    dictionary.

    Parameters
    ----------
    configurations : dict
        4 element dictionary containing:
            1. object factory generation arguments
            2. object factory location in codebase
            3. file builder location in codebase
            4. multiprocessing generation arguments

    
