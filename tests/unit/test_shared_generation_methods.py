import pytest
from src.domainobjects import generatable as generator

class Test_Shared_Generation_Methods(object):

    # Investigate best way you can verify a variable is of Type #
    def test_generate_random_string(self):
        return True

     # Investigate best way you can verify a variable is of Type #
    def test_generate_random_boolean(self):
        return True
    
     # Investigate whether you can verify a Date is of type Datetime #
    def test_generate_random_date(self):
        return True
    
    # Investigate best way you can verify a variable is of Type #
    def test_generate_random_integer(self):
        return True
    
    # Investigate best way you can verify a variable is of Type #
    def test_generate_random_decimal(self):
        return True
    
    def test_generate_currency(self):
        currency = generator.Generatable.generate_currency(self)
        assert currency in ['USD', 'CAD', 'EUR', 'GBP'] 
    
    def test_generate_asset_class(self):
        asset_class = generator.Generatable.generate_asset_class(self)
        assert asset_class in ['Stock', 'Cash']
    
    # Verify it is TICKER.EXCHANGECODE #
    def test_generate_ric(self):
        return True
    
    # Verify is is COI + CUSIP + '4' # 
    def test_generate_isin(self):
        return True
    
    def test_generate_credit_debit(self):
        credit_debit = generator.Generatable.generate_credit_debit(self)
        assert credit_debit in ['Credit', 'Debit']
    
    def test_generate_long_short(self):
        long_short = generator.Generatable.generate_long_short(self)
        assert long_short in ['Long', 'Short']
    
    def test_generate_position_type(self):
        position_type = generator.Generatable.generate_position_type(self)
        assert position_type in ['SD', 'TD']
    
    # Investigate whether you can verify a Date is of type Datetime #
    def test_generate_knowledge_date(self):
        return True
    
    # Investigate whether you can verify a Date is of type Datetime #
    def test_generate_effective_date(self):
        return True
    
    # Investigate ways to verify Account Type [ICP/ECP]RANDDIGIT #
    def test_generate_account(self):
        return True
    
    def test_generate_return_type(self):
        return_type = generator.Generatable.generate_return_type(self)
        assert return_type in ['Outstanding', 'Pending Return', 'Pending Recall',
                              'Partial Return', 'Partial Recall', 'Settled']
    
    # Investigate establishing a local cache in this module #
    def test_generate_ticker(self):
        return True
    
    # Investigate establishing a local cache in this module #
    def test_generate_coi(self):
        return True
    
    # Investigate establishing a local cache in this module #
    def test_generate_exchange_code(self):
        return True
    