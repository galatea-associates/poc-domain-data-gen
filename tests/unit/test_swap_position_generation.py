import pytest
from src.domainobjects import swap_position as generator

class Test_Swap_Position_Generator(object):

    def test_generate_account(self):
        account = generator.SwapPosition.generate_account(self)
        assert  account[:3] in ['ICP','ECP']

    def test_generate_long_short(self):
        long_short = generator.SwapPosition.generate_long_short(self)
        assert long_short in ['Long', 'Short']

    def test_generate_purpose(self):
        purpose = generator.SwapPosition.generate_purpose(self)
        assert purpose == 'Outright'