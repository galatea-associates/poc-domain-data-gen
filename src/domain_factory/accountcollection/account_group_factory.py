from domain_factory.accountcollection.account_collection_factory import \
    AccountCollectionFactory


class AccountGroupFactory(AccountCollectionFactory):
    """ Class to generate Account Groups.  Generate method will call the
        AccountCollectionFactory generate method in order to populate fields
        shared by all Account Collections.  The generate method in this class
         will then populate the remaining attributes unique to the
         Account Group domain factory. """

    def generate(self, record_count, start_id):
        """ Generate a set number of Account Groups

            Parameters
            ----------
            record_count : int
                Number of Account Groups to generate
            start_id : int
                Starting id to generate from

            Returns
            -------
            List
                Containing 'record_count' Account Groups
            """

        records = []

        return records
