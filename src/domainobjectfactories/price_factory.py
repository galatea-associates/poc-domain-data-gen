from datetime import datetime

from domainobjectfactories.creatable import Creatable


class PriceFactory(Creatable):
    """ Class to create prices. Create method will create a set amount
    of prices. """

    country_of_issuance_to_currency = {'US': 'USD', 'GB': 'GBP', 'CA': 'CAD',
                                       'FR': 'EUR', 'DE': 'EUR', 'CH': 'CHF',
                                       'SG': 'SGD', 'JP': 'JPY'}

    def create(self, record_count, start_id):
        """ Create a set number of prices

        Parameters
        ----------
        record_count : int
            Number of prices to create
        start_id : int
            Starting id to create from

        Returns
        -------
        List
            Containing 'record_count' prices
        """

        records = []
        self.instruments = self.retrieve_records('instruments')

        for _ in range(start_id, start_id + record_count):
            record = self.create_record()
            records.append(record)

        return records

    def create_record(self):
        """ Create a single price

        Returns
        -------
        dict
            A single price object
        """

        instrument = self.get_random_instrument()
        record = {
            'ric': instrument['ric'],
            'price': self.create_random_decimal(),
            'currency': self.country_of_issuance_to_currency[
                instrument['country_of_issuance']],
            'time_stamp': datetime.now()
        }

        for key, value in self.create_dummy_field_generator():
            record[key] = value

        return record
