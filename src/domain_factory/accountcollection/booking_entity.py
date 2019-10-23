from abc import abstractmethod

from domain_factory.accountcollection.account_collection import \
    AccountCollection


class BookingEntity(AccountCollection):
    """ Abstract class to generate Booking Entities.  Generate method will call the
    AccountCollection generate method in order to populate fields
    shared by all Account Collections.  The generate method in this class
    will then populate the remaining attributes unique to the
    Booking Entity domain factory. """

    @abstractmethod
    def generate(self, record_count, start_id):
        """ Generate a set number of Booking Entities

            Parameters
            ----------
            record_count : int
                Number of Booking Entities to generate
            start_id : int
                Starting id to generate from

            Returns
            -------
            List
                Containing 'record_count' Booking Entities
        """

        pass
