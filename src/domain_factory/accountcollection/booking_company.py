from domain_factory.accountcollection.booking_entity import BookingEntity


class BookingCompany(BookingEntity):
    """ Class to generate Booking Companies.  Generate method will call the
        BookingEntity generate method in order to populate fields
        shared by all Booking Entities.  The generate method in this class
         will then populate the remaining attributes unique to the
         Booking Company domain factory. """

    def generate(self, record_count, start_id):
        """ Generate a set number of Booking Companies

            Parameters
            ----------
            record_count : int
                Number of Booking Companies to generate
            start_id : int
                Starting id to generate from

            Returns
            -------
            List
                Containing 'record_count' Booking Companies
            """

        records = []

        return records
