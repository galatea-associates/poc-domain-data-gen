# fuse-test-data-gen
This project serves two functions:
- Provides the ability to generate meaningful domain objects to be used for testing & POC purposes
- Provides the ability to export these domain objects using a variety of formats (CSV, JSON, XML etc)

This readme will contain an index to features and their location in code.

## Overview

### Domain Objects

A domain object is an entity that represents a real-world business object, such as a position or a trade.

Each domain object is represented by a single Python module containing a single Python class. These modules reside within the "domainobjects" package. Each class extends the abstract class "Generatable", which defines a single abstract method "generate". This method takes 2 variables as arguments, the number of an object to generate, and the ID from which to start from where sequential IDs are relevant. 

To add a new domain object, create a new python module containing an implementation of the "generate" method. Generate methods should return a list of dictionaries, where these dictionaries represent a single domain object. Functions found inside the "Generatable" class are inherited here for ease, these are frequently occuring random generation methods used elsewhere. 

To generate said new domain object, include a definition for its generation parameters in the configuration file, and processing, generation and writing to a desired format will be handled.

### Domain Objects Data Dictionary

See here a list of all domain objects currently supported. For a breakdown of their attributes, see the documentation at: https://docs.google.com/document/d/1IB_-k16uhSBJWg2_s0pD2Vh3WZjTFALFYV6Ip9jM_4Q/edit?usp=sharing

    * Back Office Position
    * Cash Balance
    * Cash Flow
    * Counterpartie
    * Depot Position
    * Front Office Position
    * Instrument
    * Order Execution
    * Price
    * Stock Loan Position
    * Swap Contract
    * Swap Position

Additionally, there are a number of inter-object dependencies listed in the table below. Where these arise, the dependent objects require that their dependencies first be generated. This is implicitly ensured via the ordering of the configuration file, but more detail is included in the Configuration section.

Domain Object | Dependencies
------------- | ------------
Back Office Position | Instrument
Depot Position | Instrument
Front Office Position | Instrument
Order Execution | Instrument
Price | Instrument
Stock Loan Position | Instrument
Swap Contract | Counterparty
Swap Position | Swap Contract
Cash Flow | Swap Position

### File Builders

A file builder is a self contained piece of fucntionality which, given a list of records, writes a file according to a specified data format and outputs this to a specified location.

Each file builder is reprsented by a single Python module containing a single Python class. These modules reside within the "filebuilders" package. Each class extends the abstract class "Filebuilder", which defines a single abstract method "build". Initially, file builders have been created for JSON, JSONL, CSV and XML formats. To add a new file builder, create a new python module inside of the "filebuilders" package containing a single class extending "FileBuilder" and implements the abstract method "build". This method should accept a list of dictionaries, and the current file number, and uses this to create a file names as per the given number.

## Installation
A comprehensive overview for:
* The installation process from this repo can be found at: https://docs.google.com/document/d/1RkBaUWfWJPAKJjRUYGRjpISV6IhRxZ-YjoIS4c9HAqg/edit#heading=h.2ucndgcbljzx 
* Running the generator from a Docker image can be found at: https://docs.google.com/document/d/1AsAcaHiI23mQeq7vs5J2c4M2nlssotJTWMpLn_xj7Sc/edit#heading=h.lnuycosihik6 under Quickstart Guides

### Cloned Repo
Once the repo has been cloned locally, there are some pre-execution steps required:

- Clone the repo
- Set up the python environment: ```pip install -r requirements.txt```
    - ujson requires ```Microsoft Visual C++ 14.0```. This can be downloaded from: ```https://visualstudio.microsoft.com/visual-cpp-build-tools/```. Newer versions are also sufficient.

By default, the application runs using the config.json file at the root of the src directory. This will generate 500 of each domain object, as well as, on average, 5000 swap contracts, 2.4 million swap positions, and 3.4 million cashflows and is run via the command line argument:

```python src/app.py``` 

Alternatively, you can specify your own configuration file as per the guidelines set out below and running:

```python src/app.py --config src/my_custom_config.json```

Your custom config will need to contain at least one domain object configuration and one file builder configuration as show in the configuration section below.

### Docker
TODO: Complete once the company repo is set up.
TODO: Transpose information from Dockerumentation to here.
If running from a Docker container, all prerequisites will be set up for you, further instruction as to running from a Docker container is outlined at the end of: 

### Configuration

The entire tool is driven by a JSON config file which contains a list of all domain objects and all file builders.  

#### Domain Object Config

Each domain object needs to contain the following config keys:

```json
{
    "module_name":"instrument",
    "class_name":"Instrument",
    "record_count":"10",
    "max_objects_per_file":"1000000",
    "file_name":"instruments",
    "root_element_name":"instruments",
    "item_name":"instrument",
    "file_builder_name":"XML",
    "output_directory":"out",
    "upload_to_google_drive":"false",
    "dummy_fields":[
        { "data_type": "string", "field_count" : "50" },
        { "data_type": "numeric", "field_count" : "50" }
    ],
    "custom_args":{}
}
```

Attribute | Changeable? | Meaning
--------- | ----------- | --------
Module_Name | No | File path in directory used to find domain object module.
Class_Name | No | File path in directory used to find domain object class.
Record_Count | Yes | Number of records to generate for this domain object.
Max_Objects_Per_File | Yes | Number of records to save to each file.
File_Name | Yes | Prefix of the file to save records too. Sequentially numbered.
Root_Element_Name | Yes | For XML, the top-most tag of the file.
Item_Name | Yes | For XML, the tag around each record.
File_Builder_Name | Yes | File format to output records as.
Output_Directory | Yes | The output directory.
Upload_To_Google_Drive | Yes | Flag of whether to upload or not. __Not merged yet(?).__
Dummy_Fields | Yes | Description of the dummy data to generate for each record. __Not merged yet(?).__
Custom_Args | Yes | Custom arguments, these vary per object and are explained below.

Note the naming convention for the module and class names, these reflect the PEP 8 coding style.  The "file_builder_name" value must reflect the "name" attribute of one of the file builder.

#### File Builder Config

Each file builder needs to contain the following config keys:

```json
{
    "name" : "CSV",
    "module_name":"csv_builder",
    "class_name":"CSVBuilder",
    "file_extension":".csv"        
}
```

Pre-existing filebuilder descriptions should remain unedited and only serve as a basis from which to implement your own file builders.

Attribute | Changeable? | Decription
--------- | ----------- | ----------
Name | No | How this builder is to be referenced in config.
Module_Name | No | File path in directory used to find file builder module.
Class_Name | No | File path in directory used to find file builder class.
File_Extension | No | The file extension of written files.

#### Shared Config

Factors pertaining to generation of all objects, may require some trial and error for optimal performance. __Must be set.__ These are to be set in a "shared_args" section of config. 

```json
"shared_args": {
    "gen_pools": 2,
    "write_pools": 1,
    "job_size": 100000
}
```

Attribute | Description
--------- | -----------
gen_pools | Number of Processes used when generating.
write_pools | Number of Processes used when writing to file.
job_size | Number of records assigned to each Process to generate.
