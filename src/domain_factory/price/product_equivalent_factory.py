from domain_factory.price.price_factory import PriceFactory


class ProductEquivalentFactory(PriceFactory):
    """ Class to generate product equivalent prices. Generate method will
    call the PriceFactory generate method in order to populate fields shared by
    all Prices. The generate method in this class will then populate the
    remaining attributes unique to the Product Equivalent domain factory. """

    def generate(self, record_count, start_id):
        """ Generate a set number of Contra accounts

        Parameters
        ----------
        record_count : int
            Number of Contra accounts to generate
        start_id : int
            Starting id to generate from

        Returns
        -------
        List
            Containing 'record_count' Contra accounts
        """

        records = []

        return records
