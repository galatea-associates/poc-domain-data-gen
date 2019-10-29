from domain_factory.account.brokerage_account import BrokerageAccount


class DepotAccount(BrokerageAccount):
  """ Class to generate depot accounts. Generate method will call the
  BrokerageAccount generate method in order to populate fields shared by all
  Brokerage accounts. The generate method in this class will then populate the
  remaining attributes unique to the Depot Account domain factory. """

  def generate(self, record_count, start_id):
    """ Generate a set number of Depot accounts

        Parameters
        ----------
        record_count : int
            Number of Depot accounts to generate
        start_id : int
            Starting id to generate from

        Returns
        -------
        List
            Containing 'record_count' Depot accounts
        """

    records = []

    return records
