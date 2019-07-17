import pytest
import datetime
from src.domainobjects import generatable as generator

# Tests generation methods as provided by generatable #
class Test_Shared_Generation_Methods(object):

    def test_generate_random_string(self):
        random_string = generator.Generatable.generate_random_string(self, 10)
        assert isinstance(random_string, str)

    def test_generate_random_boolean(self):
        random_bool = generator.Generatable.generate_random_boolean(self)
        assert isinstance(random_bool, bool)
    
    def test_generate_random_date(self):
        random_date = generator.Generatable.generate_random_date(self)
        assert isinstance(random_date, datetime.datetime)
    
    def test_generate_random_integer(self):
        random_integer = generator.Generatable.generate_random_integer(self)
        assert isinstance(random_integer, int)
    
    def test_generate_random_decimal(self):
        random_decimal = generator.Generatable.generate_random_decimal(self)
        assert isinstance(random_decimal, float)
    
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
    # Provide mock COI, cusip, assert that a 4 is appended #
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
    
    def test_generate_knowledge_date(self):
        knowledge_date = generator.Generatable.generate_knowledge_date(self)
        assert isinstance(knowledge_date, datetime.datetime)
    
    def test_generate_effective_date(self):
        effective_date = generator.Generatable.generate_effective_date(self)
        assert isinstance(effective_date, datetime.datetime)
    
    def test_generate_account(self):
        account = generator.Generatable.generate_account(self)
        assert account[:3] in ['ICP','ECP']
    
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
    