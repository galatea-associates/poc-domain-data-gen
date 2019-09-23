from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from utils.sqlite_database import Sqlite_Database
import random
import string


class Generatable(ABC):

    LONG_SHORT = ['Long', 'Short']
    ACCOUNT_TYPES = ['ICP', 'ECP']
    TRUE_FALSE = [True, False]
    CURRENCIES = ['USD', 'CAD', 'EUR', 'GBP']
    ASSET_CLASSES = ['Stock', 'Cash']
    CREDIT_DEBIT = ['Credit', 'Debit']
    POSITION_TYPES = ['SD', 'TD']
    RETURN_TYPES = ['Outstanding', 'Pending Return', 'Pending Recall',
                    'Partial Return', 'Partial Recall', 'Settled']

    def __init__(self, file_builder, domain_object_config):
        self.__file_builder = file_builder
        self.__config = domain_object_config
        self.__database = None

    @abstractmethod
    def generate(self, record_count, start_id):
       pass

    def establish_db_connection(self):
        self.__database = Sqlite_Database()
        return self.__database

    def generate_random_string(self, length,
                               include_letters=True, include_numbers=True):
        choices = ''
        if include_letters:
            choices += string.ascii_uppercase

        if include_numbers:
            choices += string.digits

        return ''.join(random.choices(choices, k=length))

    def generate_random_boolean(self):
        return random.choice(self.TRUE_FALSE)

    def generate_random_date(self, from_year=2016, to_year=2017,
                                 from_month=1, to_month=12,
                                 from_day=1, to_day=28):
        year = random.randint(from_year, to_year)
        month = random.randint(from_month, to_month)
        day = random.randint(from_day, to_day)
        return datetime(year, month, day).date()

    def generate_random_integer(self, min=1, max=10000,
                                length=None, negative=False):
        if length is not None:
            min = 10**(length-1)
            max = (10**length)-1

        value = random.randint(min, max)
        return value if not negative else -value

    def generate_random_decimal(self, min=10, max=10000, dp=2):
        return round(random.uniform(min, max), dp)

    def generate_currency(self):
        return random.choice(self.CURRENCIES)

    def generate_asset_class(self):
        return random.choice(self.ASSET_CLASSES)

    def generate_ric(self, ticker, exchange_code):
        return '{0}.{1}'.format(ticker, exchange_code)

    def generate_isin(self, coi, cusip):
        return ''.join([coi, cusip, '4'])

    def generate_credit_debit(self):
        return random.choice(self.CREDIT_DEBIT)

    def generate_long_short(self):
        return random.choice(self.LONG_SHORT)

    def generate_position_type(self, no_sd=False, no_td=False):
        choices = self.POSITION_TYPES
        if no_sd:
            choices.remove('SD')
        if no_td:
            choices.remove('TD')
        return random.choice(choices)

    def generate_knowledge_date(self):
        return datetime.today()

    def generate_effective_date(self, n_days_to_add=3,
                                knowledge_date=None, position_type=None):
        return knowledge_date if position_type == 'SD' \
            else knowledge_date + timedelta(days=n_days_to_add)

    def generate_account(self, account_types=ACCOUNT_TYPES):
        account_type = random.choice(account_types)
        random_string = ''.join(random.choices(string.digits, k=4))
        return ''.join([account_type, random_string])

    def generate_return_type(self):
        return random.choice(self.RETURN_TYPES)

    def get_random_instrument(self):
        return random.choice(self.instruments)

    def persist_records(self, table_name, records):
        if(self.__database is None): self.establish_db_connection()
        self.__database.persist_batch(table_name, records)
        self.__database.commit_changes()

    def retrieve_records(self, table_name):
        if(self.__database is None): self.establish_db_connection()
        return self.__database.retrieve(table_name)

    def retrieve_batch_records(self, table_name, amount, start_pos):
        if(self.__database is None): self.establish_db_connection()
        return self.__database.retrieve_batch(table_name, amount, start_pos)

    def get_database(self):
        return self.__database

    def get_file_builder(self):
        return self.__file_builder

    def get_object_config(self):
        return self.__config
    
    def get_custom_args(self):
        return self.__config['custom_args']
