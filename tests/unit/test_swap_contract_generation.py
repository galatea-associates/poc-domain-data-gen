import pytest
import datetime
from src.domainobjects import swap_contract as generator

class Test_Swap_Contract_Generation(object):

    # To enable multiple assertions, a list of errors is build, then an
    # assertion made that the list is empty. In the case of an error, 
    # the list can be inspected to determine which part(s) errored.
    def test_generate_swap_end_date(self):
        errors = []
        live_status_date = generator.SwapContract.generate_swap_end_date(self, 5, None, 'Live')
        dead_status_date = generator.SwapContract.generate_swap_end_date(self, 5, None, 'Dead')
        if not isinstance(dead_status_date, datetime.datetime):
            errors.append("The Dead record is not generating an End Date successfully")
        if live_status_date is not None:
            errors.append("The Live record does not return 'None' as its End Date")
        assert errors is False

    def test_generate_swap_type(self):
        swap_type = generator.SwapContract.generate_swap_type(self)
        assert swap_type in ['Equity', 'Portfolio']

    def test_generate_reference_rate(self):
        reference_rate = generator.SwapContract.generate_reference_rate(self)
        assert reference_rate == 'LIBOR'

    def test_generate_status(self):
        status = generator.SwapContract.generate_status(self)
        assert status in ['Live', 'Dead']