import sqlite3

class Sqlite_Database:

    def __init__(self):
        # Establish connection
        self.__connection = sqlite3.connect("dependencies.db")
        self.__connection.row_factory = sqlite3.Row
        
        # Define list of database table dictionaries for data requiring persistence#
        instrument_dict = {"ric":"text", "cusip":"text","isin":"text"}
        counterparty_dict = {"id":"integer"}
        swap_contract_dict = {"id":"integer"}
        swap_position_dict = {"swap_contract_id":"integer", "ric":"text", "position_type":"text", "effective_date":"text","long_short":"text"}
        
        tables_dict = {
            "instruments":instrument_dict,
            "counterparties":counterparty_dict,
            "swap_contracts":swap_contract_dict,
            "swap_positions":swap_position_dict            
        }

        for table_name, table_dict in tables_dict.items():
            self.drop_table(table_name)
            self.create_table_from_dict(table_name, table_dict)
        
        self.commit_changes()

    # Just table name and (PRE)formatted row as input, for an example of formatting see a persisted domain object
    # TODO: Format in here instead
    def persist_to_database(self, table_name, row):
        query = "INSERT INTO "+table_name+" VALUES "+row
        self.__connection.execute(query)

    # Retrieve all records from a specified table
    def retrieve_from_database(self, table_name):
        cur = self.__connection.cursor()
        cur.execute("SELECT * FROM "+table_name)
        rows = cur.fetchall()
        return rows

    # Retrieve all records from a specified table to be iterated through X at a time
    def retrieve_batch_from_database(self, table_name, batch_size, offset):
        cur = self.__connection.cursor()
        cur.execute("SELECT * FROM "+table_name+" LIMIT ? OFFSET ?",(batch_size, offset))
        rows = cur.fetchall()
        return rows

    # Retrieve a specified, randomly sampled, amount of records from a specified table 
    def retrieve_sample_from_database(self, table_name, amount):
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
        attribute_list = [] # Add attributes here to later ",".join together
        
        for attribute, value in attribute_dict.items():
            attribute_list.append(attribute+" "+value)    
        
        attribute_list = ",".join(attribute_list)
        table_definition.append(attribute_list)
        table_definition.append(")")
        query = "".join(table_definition)

        self.__connection.execute(query)

    def commit_changes(self):
        self.__connection.commit()