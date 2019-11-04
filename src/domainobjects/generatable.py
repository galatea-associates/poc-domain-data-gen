from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from utils.sqlite_database import Sqlite_Database
import random
import string


class Generatable(ABC):
    """ Parents class of all domain objects. Contains shared generation
    methods, and defines an abstract method for generation. Pre-defines
    lists of potential values for some variations to minimise number of
    list constructions.

    Attributes
    ----------
    LONG_SHORT : List
        Possible values for objects long or short attribute

    ACCOUNT_TYPES : List
        Possible values for objects account_type attribute

    TRUE_FALSE : List
        Possible values for boolean object attribute

    CURRENCIES : List
        Possible values for objects currency attribute

    ASSET_CLASSES : List
        Possible values for objects asset class attribute

    CREDIT_DEBIT : List
        Possible values for objects credit or debit attribute

    POSITION_TYPES : List
        Possible values for objects position type attribute

    RETURN TYPES : List
        Possible values for objects return type attribute

    config : Dict
        User-specified configuration for domain objects. For shared config and
        domain-specific values, such as swaps per counterparty

    database : SQLite3 Connection
        Connection to the dependency database

    persisting_records : List
        Records, or partial records, to persist to the database. Used to store
        attributes or objects other generations depend on

    Methods
    -------
    generate(record_count, start_id) : Abstract
        Generate a given number of records, if id'd starting from given number

    generate_random_string(length, include_letters, include_numbers)
        Generate a random string of letters and/or numbers of given length

    generate_random_boolean()
        Select a random boolean value

    generate_random_date(from_year, to_year, from_month,
                         to_month, from_day, to_day)
        Select a random date between a given range

    generate_random_integer(min, max, length, negative)
        Generate a random digit between given values of set length. Boolean
        flag as to positive or negative

    generate_random_decimal(min, max, dp)
        Generate a random number between two values to a given number of
        decimal places

    generate_currency()
        Select a random currency from a pre-defined set

    generate_asset_class()
        Select a random asset class from a pre-defined set

    generate_ric(ticker, exchange_code)
        Create a RIC value from given ticker and exchange values

    generate_isin(country_of_issuance, cusip)
        Create an ISIN value from given county of issuance and CUSIP values

    generate_credit_debit()
        Select a random value between credit or debit

    generate_long_short()
        Select a random value between long and short

    generate_position_type(no_sd, no_td)
        Select a random position type, considering whether there should be
        inclusion of settlement or trade date positions

    generate_knowledge_date()
        Return todays date

    generate_effective_date(n_days_to_add, knowledge_date, position_type)
        Return today is position is of settlement, else extend by n days

    generate_account(account_types)
        Select a random account type from a provided set

    generate_return_type()
        Select a random return type from a pre-defined set

    get_random_instrument()
        Return a random instrument from the set of all generated intruments

    persist_record(record)
        Add record to list of those to be persisted

    persist_records(table_name)
        Insert list of records to persist to given table

    retrieve_records(table_name)
        Select all records from given table

    retrieve_batch_records(table_name, amount, start_pos)
        Select sequential batch of records from given table starting at pos

    get_database()
        Get connection to the database

    establish_db_connection()
        Connect to database and return connection

    get_object_config()
        Get json configuration of current object

    get_custom_args()
        Get json configuration of current objects custom arguments
    """

    LONG_SHORT = ['Long', 'Short']
    ACCOUNT_TYPES = ['ICP', 'ECP']
    TRUE_FALSE = [True, False]
    CURRENCIES = ['USD', 'CAD', 'EUR', 'GBP']
    ASSET_CLASSES = ['Stock', 'Cash']
    CREDIT_DEBIT = ['Credit', 'Debit']
    POSITION_TYPES = ['SD', 'TD']
    RETURN_TYPES = ['Outstanding', 'Pending Return', 'Pending Recall',
                    'Partial Return', 'Partial Recall', 'Settled']

    def __init__(self, factory_args, shared_factory_args):
        """ Set configuration, default database connection to None and
        instantiate list of records to persist to be empty. """

        self.__config = factory_args
        self.__shared_args = shared_factory_args
        self.__database = None
        self.__persisting_records = []

    @abstractmethod
    def generate(self, record_count, start_id):
        """ Generate a set number of records for a domain object, where ID's
        are sequential, start from a given id. Concrete implementations
        provided by each domain object """

        pass

    def generate_random_string(self, length,
                               include_letters=True, include_numbers=True):
        """ Generates a random string, of letters or numbers or both.

        Parameters
        ----------
        length : int
            Length of the random string to generate
        include_letters : Boolean
            Boolean flag of whether letters are included in the string
        include_numbers : Boolean
            Boolean flag of whether numbers are included in the string

        Returns
        -------
        String
            Random string of letters or numbers or both
        """

        choices = ''
        if include_letters:
            choices += string.ascii_uppercase

        if include_numbers:
            choices += string.digits

        return ''.join(random.choices(choices, k=length))

    def generate_random_boolean(self):
        """ Return a random boolean value

        Returns
        -------
        Boolean
            Random True or False value
        """

        return random.choice(self.TRUE_FALSE)

    def generate_random_date(self, from_year=2016, to_year=2017,
                                 from_month=1, to_month=12,
                                 from_day=1, to_day=28):
        """ Generates a random date between two given days

        Parameters
        ----------
        from_year : int
            Start year for the range
        to year : int
            End year for the range
        from_month : int
            Start month for the range
        to_month : int
            End month for the range
        from_day : int
            Start day for the range
        to_day : int
            End day for the range

        Returns
        -------
        Date
            Random date between the provided ranges
        """

        year = random.randint(from_year, to_year)
        month = random.randint(from_month, to_month)
        day = random.randint(from_day, to_day)
        return datetime(year, month, day).date()

    def generate_random_integer(self, min=1, max=10000,
                                length=None, negative=False):
        """ Generate a random integer of a given length. If no length given,
        generate a random integer between minimum and maximum.

        Parameters
        ----------
        min : int
            Minimum value of the range
        max : int
            Maximum value of the range
        length : int
            Length of the integer
        negative : Boolean
            Boolean flag indicating if return value should be negative

        Returns
        -------
        int
            Integer between given min, max values, or of given length, and
            negative if specified.
        """

        if length is not None:
            min = 10**(length-1)
            max = (10**length)-1

        value = random.randint(min, max)
        return value if not negative else -value

    def generate_random_decimal(self, min=10, max=10000, dp=2):
        """ Generate a random number between a given range to a given number
        of decimal places.

        Parameters
        ----------
        min : int
            Minimum value of the range
        max : int
            Maximum value of the range
        dp : int
            Number of decimal places to generate the value to

        Returns
        -------
        float
            Randomly generated value between min and max to dp decimal places
        """

        return round(random.uniform(min, max), dp)

    def generate_currency(self):
        """ Generate a random currency from a set list

        Returns
        -------
        String
            Random currency from a pre-defined list
        """

        return random.choice(self.CURRENCIES)

    def generate_asset_class(self):
        """ Generate a random asset class from a set list

        Returns
        -------
        String
            Random asset class from a pre-defined list
        """

        return random.choice(self.ASSET_CLASSES)

    def generate_ric(self, ticker, exchange_code):
        """ Appends two input values to "ticker.exchange_code"

        Parameters
        ----------
        ticker : String
            a ticker
        exchange_code : String
            an exchange code

        Returns
        -------
        String
            Combined "ticker.exchange_code"
        """

        return '{0}.{1}'.format(ticker, exchange_code)

    def generate_isin(self, country_of_issuance, cusip):
        """ Appends two input values to "'country_of_issuance''cusip''4'"

        Parameters
        ----------
        country_of_issuance : String
            a country of issuance code
        cusip : int
            a CUSIP value

        Returns
        -------
        String

        """
        return ''.join([country_of_issuance, str(cusip), '4'])

    def generate_credit_debit(self):
        """ Generate a random credit or debit value

        Returns
        -------
        String
            Random value between credit or debit
        """

        return random.choice(self.CREDIT_DEBIT)

    def generate_long_short(self):
        """ Generate a random long or short value

        Returns
        -------
        String
            Random value between long or short
        """

        return random.choice(self.LONG_SHORT)

    def generate_position_type(self, no_sd=False, no_td=False):
        """ Generate a random position type

        Parameters
        ----------
        no_sd : Boolean
            Boolean flag of whether to include settlement date in choice
        no_td : Boolean
            Boolean flad of whether to include trade date in choice

        Returns
        -------
        String
            Random value between of remaining set of possible position types
        """

        choices = self.POSITION_TYPES
        if no_sd:
            choices.remove('SD')
        if no_td:
            choices.remove('TD')
        return random.choice(choices)

    def generate_knowledge_date(self):
        """ Generate a knowledge day value

        Returns
        -------
        Date
            Todays date
        """

        return datetime.today()

    def generate_effective_date(self, n_days_to_add=3,
                                knowledge_date=None, position_type=None):
        """ Generates an Effective Date value

        Parameters
        ----------
        n_days_to_add : int
            Number of days to add to knowledge date before event takes effect
        knowledge_date : Date
            The knowledge date of the object being generated
        position_type : String
            The position type of the object being generated

        Returns
        -------
        Date
            Future date if input date was trade date, current date if input
            date was settlement.
        """

        return knowledge_date if position_type == 'SD' \
            else knowledge_date + timedelta(days=n_days_to_add)

    def generate_account(self, account_types=ACCOUNT_TYPES):
        """ Generates an account value

        Parameters
        ----------
        account_types : List
            Contains all potential account_types

        Returns
        -------
        String
            Randomly selected account type from list provided/default list
            appended with a 4-digit random string of characters
        """

        account_type = random.choice(account_types)
        random_string = ''.join(random.choices(string.digits, k=4))
        return ''.join([account_type, random_string])

    def generate_return_type(self):
        """ Generate a return type

        Returns
        -------
        String
            Random return type chosen from a pre-determined list
        """

        return random.choice(self.RETURN_TYPES)

    # THESE ARE NON-GENERATING, UTILITY METHODS USED WHERE NECESSARY #

    def get_random_instrument(self):
        """ Returns a random instrument from those generated prior

        Returns
        -------
        List
            Single record from the instruments table of the database
        """

        if self.instruments is None:
            self.instruments = self.retrieve_records('instruments')
        return random.choice(self.instruments)

    def persist_record(self, record):
        """ Adds a given record to the list of records to persist in storage

        Parameters
        ----------
        record : list
            List of records attributes to store for later insertion
        """

        self.__persisting_records.append(record)

    def persist_records(self, table_name):
        """ Insert all records currently set to be persisted into a specified
        table

        Parameters
        ----------
        table_name : String
            Name of the table to persist records to
        """

        if(self.__database is None):
            self.establish_db_connection()
        self.__database.persist_batch(table_name, self.__persisting_records)
        self.__database.commit_changes()

    def retrieve_records(self, table_name):
        """ Selects all records from a given database table

        Parameters
        ----------
        table_name
            Name of the table to retrieve all records of

        Returns
        -------
        SQLite3 Row
            Row object which is iterable, each element contains a Row Object
            the data inwhich can be retrieved as though it's a dictionary
        """

        if(self.__database is None):
            self.establish_db_connection()
        return self.__database.retrieve(table_name)

    def retrieve_batch_records(self, table_name, amount, start_pos):
        """ Selects a batch of records from a given table. Retrieval will
        start from the given position, and take the next amount of records

        Parameters
        ----------
        table_name : String
            Name of the table to retrieve from
        amount : int
            Number of records to retrieve in the batch
        start_pos : int
            Position from which to start the retrieval

        Returns
        -------
        SQLite3 Row
            Row object which is iterable, each element contains a Row Object
            the data inwhich can be retrieved as though it's a dictionary
        """

        if(self.__database is None):
            self.establish_db_connection()
        return self.__database.retrieve_batch(table_name, amount, start_pos)

    def get_database(self):
        """ Returns the database connection object

        Returns
        -------
        SQLite3 Connection
            Connection to the database
        """

        return self.__database

    def establish_db_connection(self):
        """ Establishes and returns the database connection object

        Returns
        -------
        SQLite3 Connection
            Connection to the database
        """

        self.__database = Sqlite_Database()
        return self.__database

    def get_factory_config(self):
        """ Returns the current objects user-specified configuration

        Returns
        -------
        Dict
            Current objects configuration
        """

        return self.__config

    def get_custom_args(self):
        """ Returns the current objects user-specified custom arguments

        Returns
        -------
        Dict
            Current objects custom arguments
        """

        return self.__config['custom_args']

    def get_shared_args(self):
        """ Returns the shared multiprocessing arguments for multiprocessing.

        Returns
        -------
        Dict
            The arguments shared between factories for multiprocessing.
        """
        return self.__shared_args

    def get_record_count(self):
        """ Returns the number of records the factory is to produce.

        Returns
        -------
        int
            The number of records this factory will produce.
        """
        print(self.__config)
        return int(self.__config['fixed_args']['record_count'])

    def set_batch_size(self, batch_size):
        """ Sets the batch size value for the factory.

        Parameters
        ----------
        batch_size : int
            The size of the batch to generate objects in
        """
        self.batch_size = batch_size
