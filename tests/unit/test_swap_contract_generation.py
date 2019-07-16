import pytest
from src.domainobjects import swap_contract as generator

class Test_Swap_Contract_Generation(object):

    # Investigate whether you can verify a Date is of type Datetime #
    def test_generate_swap_end_date(self):
        return True

    def test_generate_swap_type(self):
        swap_type = generator.SwapContract.generate_swap_type(self)
        assert swap_type in ['Equity', 'Portfolio']

    def test_generate_reference_rate(self):
        reference_rate = generator.SwapContract.generate_reference_rate(self)
        assert reference_rate == 'LIBOR'

    def test_generate_status(self):
        status = generator.SwapContract.generate_status(self)
        assert status in ['Live', 'Dead']