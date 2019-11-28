from datetime import datetime, timezone

from domainobjectfactories.creatable import Creatable


class PriceFactory(Creatable):
    """ Class to create prices. Create method will create a set amount
    of prices. """

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

        for _ in range(start_id, start_id+record_count):
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
            'instrument_id': instrument['instrument_id'],
            'price': self.create_random_decimal(min=1, max=10, dp=2),
            'currency': self.create_currency(),
            'created_timestamp': datetime.now(timezone.utc),
            'last_updated_time_stamp': datetime.now(timezone.utc)
            }

        for key, value in self.create_dummy_field_generator():
            record[key] = value

        return record
