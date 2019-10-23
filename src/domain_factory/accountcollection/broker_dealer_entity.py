from domain_factory.accountcollection.booking_subcompany import BookingSubcompany


class BrokerDealerEntity(BookingSubcompany):
    """ Class to generate Broker Dealer Entities.  Generate method will call the
        BookingSubcompany generate method in order to populate fields
        shared by all Booking Subcompanies.  The generate method in this class
         will then populate the remaining attributes unique to the
         Broker Dealer Entity domain factory. """

    def generate(self, record_count, start_id):
        """ Generate a set number of Broker Dealer Entities

            Parameters
            ----------
            record_count : int
                Number of Broker Dealer Entities to generate
            start_id : int
                Starting id to generate from

            Returns
            -------
            List
                Containing 'record_count' Broker Dealer Entities
            """

        records = []

        return records