from domain_factory.price.price_factory import PriceFactory


class InterestRateFactory(PriceFactory):
    """ Class to generate interest rates. Generate method will
    call the PriceFactory generate method in order to populate fields shared by
    all Prices. The generate method in this class will then populate the
    remaining attributes unique to the Interest Rate domain factory. """

    def generate(self, record_count, start_id):
        """ Generate a set number of Interest Rates

        Parameters
        ----------
        record_count : int
            Number of Interest Rates to generate
        start_id : int
            Starting id to generate from

        Returns
        -------
        List
            Containing 'record_count' Interest Rates
        """

        records = []

        return records
