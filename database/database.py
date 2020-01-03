from sqlite3 import connect
from os.path import exists
from pandas import read_csv


class Database:

    def __init__(self):
        self.__conn = None
        if not exists("dependencies.db"):
            self.__create_database()

    def execute_query(self, query):
        cursor = self.__get_conn().cursor()
        cursor.execute(query)
        rows_retrieved = cursor.fetchall()
        if rows_retrieved:
            if len(rows_retrieved) == 1 and len(rows_retrieved[0]) == 1:
                # 1 row containing 1 value
                # (ie a list containing a single 1-tuple)
                return rows_retrieved[0][0]
            elif len(rows_retrieved) == 1:
                # one row with n values (ie a list containing a single n-tuple)
                return rows_retrieved[0]
            else:
                return rows_retrieved

    def commit(self):
        self.__get_conn().commit()

    def get_random_value(self, table_name, column_name="*"):
        query = f"SELECT {column_name} FROM {table_name} " + \
                "ORDER BY RANDOM() LIMIT 1"
        return self.execute_query(query)

    def __create_database(self):

        table_definitions = {
            "tickers": "symbol text",
            "exchanges":
                "country_of_issuance text, exchange_code text, currency text",
            "instruments":
                "instrument_id text, cusip text, isin text, market text",
            "accounts":
                "account_id text, account_type text, iban text"
        }

        for table_name, table_definition in table_definitions.items():
            self.__drop_table(table_name)
            self.__create_table(table_name, table_definition)

        self.__populate_table_from_csv("exchanges", "exchanges.csv")
        self.__populate_table_from_csv("tickers", "tickers.csv")

        self.commit()

    def __get_conn(self):
        if not self.__conn:
            self.__conn = connect("dependencies.db", timeout=30.0)
        return self.__conn

    def __create_table(self, table_name, table_definition):
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({table_definition})"
        self.execute_query(query)

    def __drop_table(self, table_name):
        query = f"DROP TABLE IF EXISTS {table_name}"
        self.execute_query(query)

    def __populate_table_from_csv(self, table_name, file_name):
        table_contents = read_csv(file_name).values.tolist()

        values = ", ".join(
            [
                "('" + row[0].replace("\t", "', '") + "')"
                for row in table_contents
            ]
        )

        query = f"INSERT INTO {table_name} VALUES {values}"
        self.execute_query(query)
