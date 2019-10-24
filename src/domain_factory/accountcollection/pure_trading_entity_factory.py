from domain_factory.accountcollection.booking_subcompany_factory import \
    BookingSubcompanyFactory


class PureTradingEntityFactory(BookingSubcompanyFactory):
    """ Class to generate Pure Trading Entities.  Generate method will call the
        BookingSubcompanyFactory generate method in order to populate fields
        shared by all Booking Subcompanies.  The generate method in this class
         will then populate the remaining attributes unique to the
         Pure Trading Entity domain factory. """

    def generate(self, record_count, start_id):
        """ Generate a set number of Pure Trading Entities

            Parameters
            ----------
            record_count : int
                Number of Pure Trading Entities to generate
            start_id : int
                Starting id to generate from

            Returns
            -------
            List
                Containing 'record_count' Pure Trading Entities
            """

        records = []

        return records
