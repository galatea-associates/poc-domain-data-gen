import pytest
import datetime
from src.domainobjects import stock_loan_position as generator

class Test_Stock_Loan_Position_Generator(object): 

    def test_generate_haircut_non_cash(self):
        haircut = generator.StockLoanPosition.generate_haircut(self, 'Non Cash')
        assert haircut == '2.00%'

    def test_generate_haircut_cash(self):
        haircut = generator.StockLoanPosition.generate_haircut(self, 'Cash')
        assert haircut is None

    def test_generate_collateral_margin_non_cash(self):
        collateral_margin = generator.StockLoanPosition.generate_collateral_margin(self, 'Non Cash')
        assert collateral_margin is None

    def test_generate_collateral_margin_cash(self):
        collateral_margin = generator.StockLoanPosition.generate_collateral_margin(self, 'Cash')
        assert collateral_margin == '140.00%'

    def test_generate_collateral_type(self):
        collateral_type = generator.StockLoanPosition.generate_collateral_type(self)
        assert collateral_type in ['Cash', 'Non Cash']
    
    def test_generate_termination_date(self):
        # Termination Date's internal generation picks a  random T/F value, and returns a 
        # date if True, returning None if False. Only need to verify the method does return
        # Datetime on 'True'
        knowledge_date = generator.StockLoanPosition.generate_knowledge_date(self)
        assert isinstance(knowledge_date, datetime.datetime)

    def test_generate_rebate_rate_non_cash(self):
        result = generator.StockLoanPosition.generate_rebate_rate(self, 'Non Cash')
        assert result is None

    def test_generate_rebate_rate_cash(self):
        result = generator.StockLoanPosition.generate_rebate_rate(self, 'Cash')
        assert result == '5.75%'

    def test_generate_borrow_fee_non_cash(self):
        result = generator.StockLoanPosition.generate_borrow_fee(self, 'Non Cash')
        assert result == '4.00%'

    def test_generate_borrow_fee_cash(self):
        result = generator.StockLoanPosition.generate_borrow_fee(self, 'Cash')
        assert result is None

    def test_generate_purpose(self):
        purpose = generator.StockLoanPosition.generate_purpose(self)
        assert purpose in ['Borrow','Loan']