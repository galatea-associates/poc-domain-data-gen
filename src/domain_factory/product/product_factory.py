import random
from abc import abstractmethod

from domain_factory.factory import Factory


class ProductFactory(Factory):
    """ Abstract Class to generate products. Generate method will
    generate the attributes shared by all ProductFactory child classes.

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

    def generate_record(self, start_id):
        """ Generate a single product

        Returns
        -------
        dict
            A single product object
        """

        return {
            'product_id': self.generate_product_id(start_id),
            'creation_time_stamp': self.generate_timestamp(),
            'updated_time_stamp': self.generate_timestamp(),
            'product_id_xref': self.generate_product_xref(),
            'product_short_name': self.generate_short_name(),
            'description': self.generate_description()
        }

    def generate_product_id(self, id):
        """ Generate a single productId

        Returns
        -------
        string
            A single product Id
        """

        return 1000 + id

    def generate_product_xref(self, id):
        """ Generate a product xref dict

        Returns
        -------
        Dict
            A product xref
        """

        """ Get ticker from the ticker file / database table. Create other 
        ids as function of ticker """

        ticker = "TEST"
        market = "NY"
        ric = ticker + "." + market
        isin = market + random.randint(1000000000, 9999999999)
        cusip = random.randint(10000000, 999999999)
        sedol = market + random.randint(1000000, 9999999)
        bloomberg = ticker + " " + market

        return {
            'ric': ric,
            'isin': isin,
            'cusip': cusip,
            'sedol': sedol,
            'bloomberg': bloomberg,
            'ticker': ticker
        }

    def generate_short_name(self):
        """ Generate a short name

        Returns
        -------
        string
            A short name
        """

        return "instrument short name"

    def generate_description(self):
        """ Generate a description

        Returns
        -------
        string
            A Description
        """

        return "instrument description"
