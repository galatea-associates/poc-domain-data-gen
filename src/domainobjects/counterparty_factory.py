from datetime import datetime

from domainobjects.creatable import Creatable


class CounterpartyFactory(Creatable):
    """ A class to create counterparties. Create method will create a
    set amount of positions. """

    def create(self, record_count, start_id):
        """ Create a set number of counterparties.

        Parameters
        ----------
        record_count : int
            Number of counterparties to create
        start_id : int
            Starting id to create from

        Returns
        -------
        List
            Containing 'record_count' counterparties
        """

        records = []

        for i in range(start_id, record_count+start_id):
            records.append(self.get_record(i))
            self.persist_record([str(i)])

        self.persist_records("counterparties")
        return records

    def get_record(self, current_id):
        """ Create a single counterparty record

        Parameters
        ----------
        current_id : int
            Current id of the counterparty being created

        Returns
        -------
        dict
            A single counterparty objects
        """

        record = {
            'counterparty_id': current_id,
            'book': self.create_random_string(5, include_numbers=False),
            'time_stamp': datetime.now()
        }

        for key, value in self.get_dummy_field_generator():
            record[key] = value

        return record
