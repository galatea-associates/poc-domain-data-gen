import sqlite3
class Sqlite_Database:

    def __init__(self):
        # Establish connection #
        # Can connect to ::memory:: if using an in-memory database #
        # TODO: Configuration options for in-memory databases #
        self.__connection = sqlite3.connect("dependencies.db")
        self.__connection.row_factory = sqlite3.Row
        
        # Define list of database table dictionaries for domain objects requiring persistence #
        instrument_def = {"ric":"text", "cusip":"text","isin":"text"}
        counterparty_def = {"id":"text"}
        swap_contract_def = {"id":"text"}
        swap_position_def = {"swap_contract_id":"text", "ric":"text", "position_type":"text", "effective_date":"text","long_short":"text"}
        
        tables_dict = {
            "instruments":instrument_def,
            "counterparties":counterparty_def,
            "swap_contracts":swap_contract_def,
            "swap_positions":swap_position_def            
        }

        for table_name, table_def in tables_dict.items():
            self.drop_table(table_name)
            self.create_table_from_dict(table_name, table_def)
        
        self.commit_changes()

    # Takes table with N attributes & X rows for insertion formatted as:
    # [[attr1_1, attr2_1, ... , attN_1], [attr1_2, attr2_2, ... , attN_2], ... , [att1_X, att2_X, ... , arrN_X]]
    # And inserts them into the table in a single query
    def persist_batch(self, table_name, value_lists):
        formatted_lists = []
        for list in value_lists:
            formatted_lists.append(self.format_list_for_insertion(list))
        prepared_rows = ",".join(formatted_lists)
        query = " ".join(("INSERT INTO",table_name,"VALUES",prepared_rows))
        self.__connection.execute(query)

    # Persist a single row to a given table with a list of given attributes as above #
    def persist(self, table_name, value_list):
        formatted_values = self.format_list_for_insertion(value_list)
        query = " ".join(("INSERT INTO",table_name,"VALUES",formatted_values))
        self.__connection.execute(query)

    # Assumes 'text' input type, wrapping each input value with ' ' #
    def format_list_for_insertion(self, value_list):
        values = "','".join(value_list)
        return "".join(("('",values,"')"))

    # Retrieve all records from a specified table
    def retrieve(self, table_name):
        cur = self.__connection.cursor()
        cur.execute("SELECT * FROM "+table_name)
        rows = cur.fetchall()
        return rows

    # Retrieve a batch of records from specified table. Batch size is specified, as is the offset to start from #
    def retrieve_batch(self, table_name, batch_size, offset):
        cur = self.__connection.cursor()
        cur.execute("SELECT * FROM "+table_name+" LIMIT ? OFFSET ?",(batch_size, offset))
        rows = cur.fetchall()
        return rows

    # Retrieve a specified, randomly sampled, amount of records from a specified table #
    # Currently Unused #
    def retrieve_sample(self, table_name, amount):
        cur = self.__connection.cursor()
        cur.execute("SELECT * FROM "+table_name+""" WHERE id IN 
                    (SELECT id FROM """+table_name+" ORDER BY RANDOM() LIMIT "+amount)
        rows = cur.fetchall()
        return rows

    # Delete specified table from the database
    def drop_table(self, table_name):
        self.__connection.execute("DROP TABLE IF EXISTS "+table_name)

    # Create a new table called 'table_name' with attributes as specified within 'attribute_dict'
    def create_table_from_dict(self, table_name, attribute_dict):
        table_definition = ["CREATE TABLE "+table_name+" ("] # Build up query here
        attribute_list = []                                  # Add attributes here to later ",".join together
        
        for attribute, value in attribute_dict.items():
            attribute_list.append(attribute+" "+value)    
        
        attribute_list = ",".join(attribute_list)
        table_definition.append(attribute_list)
        table_definition.append(")")
        query = "".join(table_definition)

        self.__connection.execute(query)

    def commit_changes(self):
        self.__connection.commit()