import pytest
from src.domainobjects import cash_balance as generator

class Test_Cash_Balance_Generation(object):

    def test_generate_purpose(self):
        purpose = generator.CashBalance.generate_purpose(self)
        assert purpose in ['Cash Balance', 'P&L', 'Fees']