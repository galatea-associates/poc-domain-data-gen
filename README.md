# fuse-test-data-gen
This project serves two functions:
- Provides the ability to generate meaningful domain objects to be used for testing purposes
- Provides the ability to export test domain objects using a variety of formats (AVRO, JSON, XML etc)

This readme will contain an index to features and their location in code.

## Overview

### Domain Objects

A domain object is an entity that represents a real-world business object, such as a position or a trade.

Each domain object is represented by a single Python module containing a single Python class, these modules reside in the "domainobjects" package.  Each class extends the abstract class "Generatable", which defines a single abstract method "get_template".  If you wish to add a new domain object, simply create a new python module containing a single class which extends the "Generatable" abstract class and implements the abstract method "get_template".  The "get_template" method should return a dictionary that represents the structure of the domain object.  Functions found inside the "common_data_generator" module can be referenced here.

### Domain Objects Data Dictionary

A data dictionary for all currently supported domain objects will be created and put here in the near future.

### File Builders

A file builder is a self contained piece of functionality which, given a dataset, will build a file according to a specified data format and output that file to a specified location.  

Each file builder is represented by a single Python module containing a single Python class, these modules reside in the "filebuilders" package.  Each class extends the abstract class "FileBuilder", which defines a single abstract method "build".  Initially, file builders will be created for JSON, CSV and XML.  If you wish to add a new file builder, simply create a new python module inside the "filebuilders" package containing a single class which extends the "FileBuilder" abstract class and implements the abstract method "build".  The "build" method should accept a list of dictionaries (one dictionary per domain object) and use that dataset to generate a file.

### Configuration

The entire tool is driven by a JSON config file which contains a list of all domain objects and all file builders.  Each domain object needs to contain the following config keys:

```json
{
    "module_name":"front_office_position",
    "class_name":"FrontOfficePosition",
    "file_count":"1",
    "objects_per_file":"10",
    "file_name":"front_office_positions",
    "file_builder_name":"CSV",
    "output_directory":"out",
    "upload_to_google_drive":"false"
}
```

Note the naming convention for the module and class names, these reflect the PEP 8 coding style.  The "file_builder_name" value must reflect the "name" attribute of one of the file builder.

Each file builder needs to contain the following config keys:

```json
{
    "name" : "CSV",
    "module_name":"csv_builder",
    "class_name":"CSVBuilder",
    "file_extension":".csv"        
}
```

### Running the data generator
- Clone the repo
- Set up the python environment: ```pip install -r requirements.txt```
- Run src/app.py: ```python src/app.py```

### Common Data Generator   
The common data generator class contains functions to generate data that is shared across domain objects.  Templates for domain objects should reference functions within the common data generator class.
