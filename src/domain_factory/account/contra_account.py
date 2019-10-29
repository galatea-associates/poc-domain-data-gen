from domain_factory.account.external_counterparty_account import ECPAccount


class ContraAccount(ECPAccount):
    """ Class to generate contra ecp accounts. Generate method will call the
    ECPAccount generate method in order to populate fields shared by all ECP
    accounts. The generate method in this class will then populate the
    remaining attributes unique to the Contra Account domain factory. """

    def generate(self, record_count, start_id):
        """ Generate a set number of Contra accounts

            Parameters
            ----------
            record_count : int
                Number of Contra accounts to generate
            start_id : int
                Starting id to generate from

            Returns
            -------
            List
                Containing 'record_count' Contra accounts
            """

        records = []

        return records
