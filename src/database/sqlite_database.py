import os.path
import sqlite3

import pandas as pd


class Sqlite_Database:
    """ A class wrapping a database. Providing connections to and limited
    querying thereof.

    Attributes
    ----------
    connection : SQlite Connection
        Connection to the database. 30 second timeout.

    Methods
    -------
    populate_prerequisite_table(table_name, file_name)
        Populate a prerequisite table, table_name from a file with name
        and location from the working directory given by file_name.

    persist_batch(table_name, value_lists)
        Insertion of a set of records into a specified table.

    format_list_for_insertion(value_list)
        Utility method for persist methods where given lists are joined into
        a query-friendly format.

    retrieve(table_name)
        Returns all records within a specified table.

    retrieve_batch(table_name, batch_size, offset)
        Retrieves a given number of records from a specified table from a
        given point onward.

    retrieve_column_as_list(table_name, column_name)
        Retrieves one column of records from a given table.

    retrieve_sample(table_name, amount)
        Retrieves a random sample of given size from a specified table.

    get_table_size(table_name)
        Returns the number of records in a specified table.

    drop_table(table_name)
        Deletes a specified table.

    create_table_from_dict(table_name, attribute_dict)
        Creates a new table of given name from a dict of attribute keys
        and type values.

    commit_changes()
        Commit any changes made to the database since opening the connection.

    close_connection()
        Close the connection to the database.

    get_connection()
        Return the database connection. For testing purposes mainly
    """

    def __init__(self):
        """Esablishes a connection to a database on given file_path. If the
        database does not already exist, then the connection is made and
        tables created via hard-coded definitions. These definitions are
        the minimum-required attributes for correct generation of all
        domain objects considering their dependencies.

        Parameters
        ----------
        connection : SQlite Connection
            Connection to the database.
        """

        if (not os.path.isfile("dependencies.db")):
            self.__connection = sqlite3.connect("dependencies.db",
                                                timeout=30.0)
            self.__connection.row_factory = sqlite3.Row

            instrument_def = {"ric": "text",
                              "cusip": "text",
                              "isin": "text",
                              "country_of_issuance": "text"}

            counterparty_def = {"id": "text"}

            swap_contract_def = {"id": "text"}

            swap_position_def = {"swap_contract_id": "text",
                                 "ric": "text",
                                 "position_type": "text",
                                 "effective_date": "text",
                                 "long_short": "text"}

            exchanges_def = {"country_of_issuance": "text",
                             "exchange_code": "text",
                             "currency": "text"}

            tickers_def = {"symbol": "text"}

            tables_dict = {
                "instruments": instrument_def,
                "counterparties": counterparty_def,
                "swap_contracts": swap_contract_def,
                "swap_positions": swap_position_def,
                "exchanges": exchanges_def,
                "tickers": tickers_def
            }

            for table_name, table_def in tables_dict.items():
                self.drop_table(table_name)
                self.create_table_from_dict(table_name, table_def)

            """ Populate exchange info and tickers """
            self.populate_prerequisite_table("exchanges", "exchange_info.csv")
            self.populate_prerequisite_table("tickers", "tickers.csv")

            self.commit_changes()
        else:
            self.__connection = sqlite3.connect("dependencies.db",
                                                timeout=30.0)
            self.__connection.row_factory = sqlite3.Row

    def populate_prerequisite_table(self, table_name, file_name):
        """ Populate a prerequisite table, table_name from a file with name
        and location from the working directory given by file_name.

        Parameters
        ----------
        table_name : String
            The name of the table to insert into
        file_name: String
            Name of the csv file containing data to be inserted. Name should be
            relative to the working directory
        """

        value_list = pd.read_csv(file_name).values.tolist()
        self.persist_batch(table_name, value_list)

    def persist_batch(self, table_name, value_lists):
        """ Insert a given list of records into a specified table of the
        database. Each element of the value_lists list is formatted to be
        syntactically correct for database insertion, and a single query
        ran to insert all formatted rows.

        Parameters
        ----------
        table_name : String
            The name of the table to insert into
        value_lists: List of Lists
            A list containing lists. Each contained list is a record to be
            inserted into to the table. For instance, if value_lists has
            length 20, there will be 20 records added to the table.
            It is structured as:
            [[attr1_1, attr2_1, ..., attN_1],
            [attr1_2, attr2_2, ..., attN_2],
            ...,
            [attr1_X, attr2_X, ..., attN_X]]
        """

        formatted_lists = []
        for list in value_lists:
            formatted_lists.append(self.format_list_for_insertion(list))
        prepared_rows = ",".join(formatted_lists)
        query = " ".join(("INSERT INTO", table_name, "VALUES", prepared_rows))
        self.__connection.execute(query)

    def format_list_for_insertion(self, value_list):
        """ Format a given record to be syntactically correct for insertion
        queries. This assumes that the value being inserted is of type 'text'
        and wraps each value with apostraphes as such.

        Parameters
        ----------
        value_list : List
            A single list representing the record to format.

        Returns
        -------
        String
            Syntactically correct string for insertion of a record .
        """

        values = "','".join(value_list)
        return "".join(("('", values, "')"))

    def retrieve(self, table_name):
        """ Retrieves all records within a given table.

        Parameters
        ----------
        table_name : String
            The name of the table from which to retrieve records

        Returns
        -------
        SQLite3 Row
            Iterable object containing the rows returned by the query
        """

        cur = self.__connection.cursor()
        cur.execute("SELECT * FROM " + table_name)
        rows = cur.fetchall()
        return rows

    def retrieve_on_matching_value(self, table_name, column_name,
                                   column_value):
        cur = self.__connection.cursor()
        cur.execute(
            "SELECT * FROM " + table_name + " WHERE "
            + column_name + " = '" + column_value + "'")
        rows = cur.fetchall()
        return rows

    def retrieve_column_as_list(self, table_name, column_name):
        """ Retrieves one column of records from a given table.

        Parameters
        ----------
        table_name : String
            The name of the table from which to retrieve records
        column_name : String
            The name of the column to retrieve

        Returns
        -------
        SQLite3 Row
            Iterable object containing the row returned by the query
        """

        cur = self.__connection.cursor()
        cur.execute("SELECT " + column_name.upper() + " FROM " + table_name)
        rows = cur.fetchall()
        list = [row[column_name] for row in rows]
        return list

    def retrieve_batch(self, table_name, batch_size, offset):
        """ Retrieves a batch of records from a specified table of a given
        size starting at a given offset.

        Parameters
        ----------
        table_name : String
            Name of the table from which to retrieve records
        batch_size : int
            Amount of records to retrieve in the batch
        offset : int
            The RowID from which to start retrieval

        Returns
        -------
        SQLite3 Row
            Iterable object containing the rows returned by the query
        """

        cur = self.__connection.cursor()
        cur.execute("SELECT * FROM " + table_name + " LIMIT ? OFFSET ?",
                    (batch_size, offset))
        rows = cur.fetchall()
        return rows

    # Retrieve randomly sampled amount of records from a table #
    # Currently Unused #
    def retrieve_sample(self, table_name, amount):
        """ Retrieves a random sample from a specified table of given amount.

        Parameters
        ----------
        table_name : String
            Name of the table from which to retrieve records
        amount : int
            Amount of records to retrieve in the sample

        Returns
        -------
        SQLite3 Row
            Iterable object containing the rows returned by the query
        """

        cur = self.__connection.cursor()
        cur.execute("SELECT * FROM " + table_name + """ ORDER BY
                     RANDOM() LIMIT """ + str(amount))
        rows = cur.fetchall()
        return rows

    def get_table_size(self, table_name):
        """ Returns the number of records held in a specified table

        Parameters
        ----------
        table_name : String
            Name of the table to get the size of

        Returns
        -------
        int
            Number of records held in the specified table
        """

        cur = self.__connection.cursor()
        cur.execute("SELECT max(ROWID) from " + table_name)
        return cur.fetchone()[0]

    def drop_table(self, table_name):
        """ Delete a given table if it exists

        Parameters
        ----------
        table_name : String
            Name of the table to drop
        """

        self.__connection.execute("DROP TABLE IF EXISTS " + table_name)

    # Create table 'table_name' with attributes in 'attribute_dict'
    def create_table_from_dict(self, table_name, attribute_dict):
        """ Create a new table as defined by a given dictionary.

        Progressively build up a query to create a new table. This is done by
        storing components of the final query in a list, before joining them
        together.

        Parameters
        ----------
        table_name : String
            Name of the table to create
        attribute_dictionary : dict
            Keys are attribute names, and values are attribute types
        """

        table_definition = ["CREATE TABLE IF NOT EXISTS " + table_name + " ("]
        attribute_list = []

        for attribute, value in attribute_dict.items():
            attribute_list.append(attribute + " " + value)

        attribute_list = ",".join(attribute_list)
        table_definition.append(attribute_list)
        table_definition.append(")")
        query = "".join(table_definition)

        self.__connection.execute(query)

    def commit_changes(self):
        """ Commit changes to a database, saving them. """
        self.__connection.commit()

    def close_connection(self):
        """ Close the connection to the database. """
        self.__connection.close()

    def get_connection(self):
        """Return the database connection. For testing purposes mainly """
        return self.__connection
