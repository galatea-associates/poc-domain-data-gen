from domain_factory.generatable import Generatable
from abc import ABC, abstractmethod

class BrokerageAccount(Generatable):
  """ Abstract Class to generate brokerage accounts. Generate method will generate
    the attributes shared by all brokerage account child classes. """


  @abstractmethod
  def generate(self, record_count, start_id):
    """ Generate a set number of brokerage accounts

        Parameters
        ----------
        record_count : int
            Number of depot positions to generate
        start_id : int
            Starting id to generate from

        Returns
        -------
        List
            Containing 'record_count' depot positions
        """

    records = []

    return records
