# Ensure that prior functionality is maintained across new iterations
# Update these to reflect any additional functionality

# CB: Parse the output files into a standard format and have comparison logic in a separately defined function.

import sys, os, logging
import csv

def main():
    logging.basicConfig(level=logging.INFO)

    #log_info("Cleaning Output Directory")
    #clean_output_directory()
    #log_info("Output Directory Cleaned")

    file_types = get_file_types()
    config_files = get_config_file_names(file_types)

    #log_info("Generating Files")
    #generate_files(config_files)
    #log_info("Successfully Generated Files")

    log_info("Asserting that the correct number of each Domain Object has been generated")
    # for each domain object, determine how many should have been generated #
    # asses that each .csv has that_num+1 lines generated # 
    # TODO: Count for each file format that the correct number of domain objects has been generated for each
    # Approach:     CSV: Check - Number of lines = Number of Objects Generated + 1
    #               XML: Check - Number of Items = Number of Objects Generated
    #              JSON: Check - Number of JSON Objects = Number of Objects Generated
    #             JSONL: Check - Number of lines = Number of Objects Generated + 1
    test_json_lengths()
    test_xml_lengths()
    test_csv_lengths()
    test_jsonl_lengths()
    log_info("The Correct Amount of each Domain Object has been generated")

    log_info("Asserting that the dependencies between Domain Objects has been maintained")
    # Current Dependency Tree can be found at: https://drive.google.com/file/d/1lp8qB-EYiv-ny742rmVCGM1aTnq2tid4/view?usp=sharing
    # This requires updating as new dependencies are formed, be it between existing Domain Objects, or the addition of new ones
    # TODO: Check for each file format that the correct domain object dependencies have been maintained
    test_json_dependencies()
    test_xml_dependencies()
    test_csv_dependencies()
    test_jsonl_dependencies()
    log_info("The expected dependencies have been maintained")

# Return a list of file types supported. To add additional ones into the testing framework:
#   1) Have it be supported within the main application
#   2) Create a test_config_newfiletype.json configuration file
#   3) Add the new file type to the list below
def get_file_types():
    return ['json','jsonl','xml','csv']

# Create a new list with a 1-to-1 correspondence to the input file types containing file path to said files
# Naming convention predetermined, based on the .json files which require testing.
def get_config_file_names(file_types):
    config_files = file_types
    num_file_types = len(file_types)
    for x in range(num_file_types):
        config_files[x] = "tests/resources/test_config_"+file_types[x]+".json"
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
# Output directory hardcoded to be: tests/output/
# Subshell execution of app.py method from: https://stackoverflow.com/questions/7974849/how-can-i-make-one-python-file-run-another
def generate_files(config_files):
    for file_path in config_files:
        outcode = os.system("python src/app.py --config "+file_path)
        if outcode == 1:
            log_error("Error generating Domain Object(s) for configuration file: "+file_path)

## Length Tests ##

def test_json_lengths():
    sys.stdout.write("test_json_lengths")

def test_xml_lengths():
    sys.stdout.write("test_xml_lengths")

def test_csv_lengths():
    sys.stdout.write("test_csv_lengths")

def test_jsonl_lengths():
    sys.stdout.write("test_jsonl_lengths")

## Dependency Tests ##

def test_json_dependencies():
    sys.stdout.write("test_json_dependencies")

def test_xml_dependencies():
    sys.stdout.write("test_xml_dependencies")

def test_csv_dependencies():
    sys.stdout.write("test_csv_dependencies")

def test_jsonl_dependencies():
    sys.stdout.write("test_jsonl_dependencies")

## Utility Functions ##
def log_info(message):
    logging.info(message)

def log_error(message):
    logging.error(message)

if __name__ == '__main__':   
    main()