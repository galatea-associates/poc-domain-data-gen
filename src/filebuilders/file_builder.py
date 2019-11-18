import abc
import os
from datetime import datetime

class FileBuilder(abc.ABC):
    """ A base class for all file builders. Contains utility functions for
    uploading to google drive, opening and closing files, and various others
    for file extension-specific requirements. Defines an abstract method for
    which a concrete implementation is provided in all children.

    Attributes
    ----------
    file_name : String
        Initially, the domain object, later extended to combine this with
        the sequential naming formatting and file extension.
    file_extension : String
        The output file type
    google_drive_connector : Google_Drive_Connector
        Instantiated connector object for uploading to a pre-defined google
        drive directory.
    output_dir : String
        The directory files are to be written to
    root_element_name : string
        For XML formatting, the top-most, all-encapsulating tag.
    item_name : String
        For XML formatting, the tag surrounding each written object.

    Methods
    -------
    build(file_number, data, upload_to_google_drive) : Abstract
        An abstract class defining the name and mathod variables for all
        child-implemented build methods.
    upload_to_google_drive(local_folder_name, file_name)
        Create a given directory/file_name structure in a remote directory on
        google drive and upload data.
    open_file()
        Opens the current file
    close_file()
        Closes the current file
    get_output_directory()
        Returns the output directory
    get_file_name()
        Returns the file name
    get_google_drive_connector()
        Returns the google drive connector object
    get_root_element_name()
        Returns the name of XML parent tags
    get_item_name()
        Returns the name of each XML item
    """

    def __init__(self, google_drive_connector, domain_object_config):
        """ Initialises various values required for correct behaviour when
        writing out to files.

        Parameters
        ----------
        google_drive_connector : Google_Drive_Connector
            Instantiated connector object for uploading to a pre-defined
            google drive directory.
        domain_object_config : Dict
            Dictionary containing the parsed json user-defined configuration
            for the current object.
        """

        file_type = domain_object_config['output_file_type']
        file_name = domain_object_config['file_name']
        file_extension = file_type.lower()

        self.__google_drive_connector = google_drive_connector
        self.__file_name = file_name + '_{}.' + file_extension
        self.__output_dir = domain_object_config['output_directory']

        if file_type == 'XML':
            file_specific_config = domain_object_config['file_type_args']
            self.__root_element_name = \
                file_specific_config['xml_root_element']
            self.__item_name = file_specific_config['xml_item_name']

    @abc.abstractmethod
    def build(self, file_number, data, upload_to_google_drive):
        """ Method called to write given data to a file. The file name
        includes the given number for sequential writing. If uploading to
        google drive, copies of file are made locally too.

        Parameters
        ----------
        file_number : int
            The current file number to be writing to
        data : List
            List of records to be writen to file
        upload_to_google_drive : Boolean
            Boolean flag on whether to upload the results to google drive
        """
        pass

    def upload_to_google_drive(self, local_folder_name, file_name):
        """ Checks whether a directory structure exists within a pre-defined
        google drive location, creating such if need be, and uploads the file
        there, or updates an existing one.

        Parameters
        ----------
        local_folder_name : String
            Directory on local machine where results have been written to
        file_name : String
            Name of file on local machine
        """
        root_folder_id = self.__google_drive_connector.root_folder_id
        todays_date = datetime.today().strftime('%Y-%m-%d')

        # Check if a folder for today's date exists, create if it doesn't
        folder_id = self.__google_drive_connector\
            .get_folder_id(todays_date, root_folder_id)
        if folder_id == None:
            folder_id = self.__google_drive_connector\
                .create_folder(todays_date, root_folder_id)

        # Check if the file already exists, create it if not
        file_id = self.__google_drive_connector\
            .get_file_id(file_name, folder_id)
        if file_id == None:
            self.__google_drive_connector\
                .create_file(local_folder_name, file_name, folder_id)
        else:
            self.__google_drive_connector\
                .update_file(local_folder_name, file_name, file_id)

    def open_file(self):
        """ Open a file of initialised directory and name """
        self.file = open(os.path.join(self.__output_dir,
                                      self.__file_name), 'a+')

    def close_file(self):
        """ Close the file opened as by open_file """
        self.file.close()

    def get_output_directory(self):
        """ Return the directory where files are output to

        Returns
        -------
        String
            Current output directory of written files
        """
        return self.__output_dir

    def get_file_name(self):
        """ Return the name of current file

        Returns
        -------
        String
            Current file name
        """
        return self.__file_name

    def get_google_drive_connector(self):
        """ Return the google drive connector object

        Returns
        -------
        Google_Drive_Connector
            Configured google drive connector
        """
        return self.__google_drive_connector

    def get_root_element_name(self):
        """ Return the XML root element name

        Returns
        -------
        String
            The XML root element name
        """
        return self.__root_element_name

    def get_item_name(self):
        """ Return the XML item name
        Returns
        -------
        String
            The XML item name
        """
        return self.__item_name
