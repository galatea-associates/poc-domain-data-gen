from abc import abstractmethod

from domain_factory.factory import Factory


class PriceFactory(Factory):
    """ Abstract Class to generate prices. Generate method will
    generate the attributes shared by all price factory child
    classes.

       Price [dir]
        ->Price [abstract]
          ->Product Equivalent [conc]
          ->Interest Rate [conc]
          ->Discount Rate [conc]

       """

    @abstractmethod
    def generate(self, record_count, start_id):
        """ Generate a set number of prices

        Parameters
        ----------
        record_count : int
            Number of Prices to generate
        start_id : int
            Starting id to generate from

        Returns
        -------
        List
            Containing 'record_count' Prices
        """

        pass

    def generate_record(self, id):
        """ Generate a single brokerage account

        Returns
        -------
        dict
            A single brokerage account object
        """

        return {
            'product_id': self.get_instrument_product_id(id),
            'creation_time_stamp': self.generate_timestamp(),
            'updated_time_stamp': self.generate_timestamp()
        }

    def get_instrument_product_id(self, id):
        """ Get an instrument product id

        Returns
        -------
        string
            A single product Id
        """

        """ get instrument and return the id """
        productId = id

        return productId
