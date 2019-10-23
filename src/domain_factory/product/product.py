from abc import abstractmethod

from domain_factory.generatable import Generatable


class Product(Generatable):
    """ Abstract Class to generate products. Generate method will
    generate the attributes shared by all product child classes.

       Product [dir]
        ->Product[abstract]
          -> Internal Product [conc]
          -> External Product [abstract]
          -> Service [conc]

       """

    @abstractmethod
    def generate(self, record_count, start_id):
        """ Generate a set number of products

        Parameters
        ----------
        record_count : int
            Number of Products to generate
        start_id : int
            Starting id to generate from

        Returns
        -------
        List
            Containing 'record_count' Products
        """

        pass
