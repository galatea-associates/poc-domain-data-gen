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

### Specifying a custom config file
By default, the application will run using the config.json file in the root of the src directory.  It is possible to maintain multiple config files and specify which to use via an optional command line argument.  For example, running the data generator as follows will use a custom JSON config file:

```python src/app.py --config src/my_custom_config.json```

Your custom config will need to contain at least one domain object configuration and one file builder configuration as show in the configuration section above.

### Running the data generator
- Clone the repo
- Set up the python environment: ```pip install -r requirements.txt```
- Run src/app.py: ```python src/app.py```

#### Command Line Arguments


| Argument Name         | Optional? | Default Value | Description   |
| ---                   | ---       | ---           | ---           |
| --config              | Yes       | src\config.json
| --file-builder-name   | Yes       | JSON
| --output-directory    | Yes       | root |
| --upload-to-gdrive    | Yes       | 
| --gdrive-root         | Yes       |

- --config', default=os.path.join('src', 'config.json'), help='JSON config file location')    
- --file-builder-name', default='JSON', help='Name of the file builder module to use')
- --output-directory', default='out', help='Local output directory')
- --upload-to-gdrive', default='false', help='Upload to Google Drive (true/false)')
- --gdrive-root', default='root', help='Google Drive root folder ID')

### Common Data Generator   
The common data generator class contains functions to generate data that is shared across domain objects.  Templates for domain objects should reference functions within the common data generator class.

### Uploading to Google Drive
The uploading of files to Google is optional and controlled at the domain object level.  This is configured by the "upload_to_google_drive" value (true or false), shown in the domain object configuration JSON above.

An optional command line parameter --g-drive-root can be supplied, which represents the Google Drive ID of a folder where you would like the files uploaded to.  If this parameter isn't supplied, the files will be uploaded to the root of your own Google drive.

When files are uploaded to Google drive, they will be uploaded into a folder with today's date (YYYY-MM-DD) as the name.  If the folder doesn't exist for today, it will be created.  If you are re-uploading the same files on a date where they have already been uploaded, the existing version(s) will be kept using the Google Drive versioning functionality.  To see the version history of a given file, you can right-click on a file in Google Drive and select "Manage Versions".

When uploading to Google Drive for the first time, you will be required to login using your Galatea Google account, a browser window should automatically load to allow you do this.  Once you have done this, an authentication token file "token.pickle" will be downloaded onto your machine.  When running the service remotely, it is important to ensure that a valid token.pickle file exists in the same directory as the application.

TODO: Investigate the use of the Google service accounts for Google Drive connectivity

### Jenkins Build
The Galatea Jenkins server can be found at: https://jenkins.fuse.galatea-associates.com/.
The FUSE-Test-Data-Gen job is the job for this project.
#### Pipeline
The Jenkinsfile defines a pipeline of the stages Jenkins will perform, the order in which to perform them, the commands required to execute them, as well as any options and environment details. The current stages in this project are:
##### Install Requirements
Runs ```pip install -r requirements.txt``` to install the necessary plugins to the virtual environment.
##### Run Unit Tests
Executes the tests as supplied in the ```tests/unit/``` directory. Names of test files must be preceeded with ```test_```
#### Discovery Method
The discovery method is set within the configuration of the job itself rather than any external file. It is currently set to scan the repo & run once daily if not otherwise executed. Branches are automatically detected if they contain a Jenkinsfile. 
