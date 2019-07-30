# Ensure that prior functionality is maintained across new iterations
# Update these to reflect any additional functionality

# To add additional file types into the testing framework:
#   1) Have it be supported within the main application
#   2) Create a test_config_newfiletype.json configuration file
#   3) Add the new file type to the list below

# CB: Parse the output files into a standard format and have comparison logic in a separately defined function.

import os, logging
import csv, json, xmlutils

def main():
    clean_output_directory()
    
    domain_objects = get_domain_objects()
    file_types = get_file_types()
    config_file_paths = get_config_file_paths(file_types)
    
    generate_output_files_from_config(config_file_paths)

    test_csv(config_file_paths['csv'], domain_objects)
    


# Return a list of file types supported & to be tested. 
def get_file_types():
    #return ['json','jsonl','xml','csv']
    # Temporary return value for ease & speed:
    return ['csv']

# Return a list of domain objects supported by the generator
def get_domain_objects():
    return [
        'back_office_positions',
        'cash_balances',
        'cashflows',
        'counterparties',
        'depot_postions',
        'front_office_positions',
        'instruments',
        'order_executions',
        'prices',
        'stock_loan_positions',
        'swap_contracts',
        'swap_positions'
        ]

# Create a new list with a 1-to-1 correspondence to the input file types containing file path to said files
# Naming convention predetermined, based on the .json files which require testing.
def get_config_file_paths(file_types):
    config_files = dict()
    for file_type in file_types:
        config_files[file_type] = "tests/resources/test_config_"+file_type+".json"
    return config_files

# Delete files inside of a given directory
# Code from: https://stackoverflow.com/questions/185936/how-to-delete-the-contents-of-a-folder-in-python
def clean_output_directory(directory="tests/output/"):
    for the_file in os.listdir(directory):
        file_path = os.path.join(directory, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            log_error("Error removing file: "+file_path)
            print(e)

# Generate files for all JSON / JSONL / XML / CSV Formats - report any with errors
# Config input directory hardcoded to be: tests/resources
# Output directory hardcoded within config files to be: tests/output/
# Subshell execution of app.py method from: https://stackoverflow.com/questions/7974849/how-can-i-make-one-python-file-run-another
def generate_output_files_from_config(config_files):
    for file_type in config_files:
        # Outcode captured as no direct terminal output seen from subshell execution
        outcode = os.system("python src/app.py --config "+config_files[file_type])
        if outcode == 1:
            log_error("Error generating Domain Object(s) for configuration file: "+config_files[file_type])

## Tests ##
# TODO: Implement Testing for other file types
# TODO: Achieved via conversion to CSV and running through the same tests. 

def test_csv(config_file_path, domain_objects):
    with open(config_file_path) as config_file:
        config = json.load(config_file)

    
    

## Generalised Tests ##
# Approach is to convert file formats into CSVs and perform any testing on these 

def test_lengths():
    print("Testing Lengths\n")

def test_dependencies():
    # Of the current (30/07/2019) Domain Objects there are dependencies on 3 objects & 5 attributes total:
    #   instrument[RIC]     : stock_loan_position, order_execution, cash_flow, front_office_position, swap_position
    #   instrument[CUSIP]   : back_office_position
    #   instrument[ISIN]    : depot_position
    #   swap_contract[ID]   : swap_position
    #   counterparty[ID]    : swap_contract
    print("Testing Dependencies\n")

## Utility Functions ##
def log_info(message):
    logging.info(message)

def log_error(message):
    logging.error(message)

if __name__ == '__main__':   
    main()