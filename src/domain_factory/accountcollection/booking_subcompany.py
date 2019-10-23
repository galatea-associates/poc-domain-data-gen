from abc import abstractmethod

from domain_factory.accountcollection.booking_entity import BookingEntity


class BookingSubcompany(BookingEntity):
    """ Abstract class to generate Booking Subcompanies.  Generate method will call the
    BookingEntity generate method in order to populate fields
    shared by all Booking Entities.  The generate method in this class
    will then populate the remaining attributes unique to the
    Booking Subcompany domain factory. """

    @abstractmethod
    def generate(self, record_count, start_id):
        """ Generate a set number of Booking Subcompanies

            Parameters
            ----------
            record_count : int
                Number of Booking Subcompanies to generate
            start_id : int
                Starting id to generate from

            Returns
            -------
            List
                Containing 'record_count' Booking Subcompanies
        """

        pass
