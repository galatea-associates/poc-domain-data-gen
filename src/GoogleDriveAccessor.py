from Kafka_Python.Runnable import Runnable

from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from CSVReader import CSVReader

import io
import os
import argparse
from enum import Enum
from multiprocessing import Lock

SCOPES = 'https://www.googleapis.com/auth/drive'


class FileState(Enum):
    NOT_STARTED = 1
    DOWNLOADING = 2
    DOWNLOADED = 3


class SetActions(Enum):
    START_DOWNLOADING = 1
    WAIT_FOR_DOWNLOAD = 2
    START_PROCESSING = 3


class GoogleDriveAccessor(Runnable):
    def __init__(self, folder_id=None, output_folder="data",
                 file_name=None, file_type="CSV"):
        self.__folder_ID = folder_id
        self.__output_folder = self.__process_path(path=output_folder)
        self.__service = None
        self.__file_name = file_name
        self.__file_type = file_type
        self.__file_download_status = None
        self.__lock = Lock()
        self.__data_loader = None

    def __check_download_status(self):
        if os.path.isfile(self.__output_folder + self.__file_name):
            return FileState.DOWNLOADED
        else:
            return FileState.NOT_STARTED

    def __auth_gdrive(self):
        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
            creds = tools.run_flow(flow, store)
        self.__service = build('drive', 'v3', http=creds.authorize(Http()))

    def __get_files_in_folder(self, folder):
        results = self.__service.files().list(
            q=' "'+folder+'" in parents', fields="files(*)").execute()
        return results.get('files', [])

    def __download_items(self, items):
        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                file_name = item['name']
                if not file_name == self.__file_name:
                    continue
                file_id = item['id']
                request = self.__service.files().get_media(fileId=file_id)
                fh = io.FileIO(self.__output_folder + file_name, 'w')
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                    print("Download %d%%." % int(status.progress() * 100))

    def __process_path(self, path):
        if not path.endswith(os.path.sep):
            path += os.path.sep
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def __process_args(self, args):
        if args is None:
            return

        if "Folder ID" in args.keys():
            self.__folder_ID = args["Folder ID"]
        
        if "Output Directory" in args.keys():
            self.__output_folder = self.__process_path(path=args["Output Directory"])

        if "File Name" in args.keys():
            self.__file_name = args["File Name"]
        
        if "File Type" in args.keys():
            self.__file_type = args["File Type"]

        if self.__file_download_status is None:
            self.__file_download_status = self.__check_download_status()

    def __set_downloading_state(self, state):
        self.__file_download_status = state

    def __get_downloading_state(self):
        return self.__file_download_status

    def __download_from_gdrive(self):
        self.__auth_gdrive()

        items = self.__get_files_in_folder(folder=self.__folder_ID)

        self.__download_items(items=items)

    def __process_data(self, args):
        return self.__data_loader.run(args)

    def __get_current_action(self):
        set_action = None
        while set_action in [SetActions.WAIT_FOR_DOWNLOAD, None]:
            with self.__lock:
                set_action = {
                    FileState.DOWNLOADED: SetActions.START_PROCESSING,
                    FileState.DOWNLOADING: SetActions.WAIT_FOR_DOWNLOAD,
                    FileState.NOT_STARTED: SetActions.START_DOWNLOADING
                    }[self.__get_downloading_state()]
                if set_action == SetActions.START_DOWNLOADING:
                    self.__set_downloading_state(FileState.DOWNLOADING)
        return set_action

    def __get_data_loader(self):
        return {
            "CSV": CSVReader()
        }[self.__file_type]

    # In DataConfiguration.py, 'Data Args' field should look like:
    # {"Output Directory": "data",
    #  "Folder ID": "2342342341fsdfs342sdf",
    #  "File Name": "prices.csv",
    #  "File Type": "CSV",
    #  "Data Loader Config": {
    #                           "File": "data/prices.csv",
    #                           "Format": "CSV",
    #                           "Chunk Size": 1,
    #                           "Loop on end": True
    #                           }
    # }
    def run(self, args=None):
        if self.__data_loader is not None:
            return self.__process_data(args["Data Loader Config"])

        self.__process_args(args=args)

        set_action = self.__get_current_action()
        
        if set_action == SetActions.START_DOWNLOADING:
            self.__download_from_gdrive()
            self.__set_downloading_state(FileState.DOWNLOADED)

        with self.__lock:
            if self.__data_loader is None:
                self.__data_loader = self.__get_data_loader()

        return self.__process_data(args["Data Loader Config"])


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--folder_id', type=str, required=True,
        help="The ID of the folder where the file is located on google drive.")
    parser.add_argument(
        '--output_folder', type=str, default="data",
        help="The folder where the data will be downloaded to")
    parser.add_argument(
        '--file_name', type=str,
        help="The name of the file to download")
    parser.add_argument(
        '--file_type', type=str, default="CSV",
        help="The type of the file, eg CSV")
    return parser.parse_args()


def format_args(output_dir, folder_id, file_name, file_type):
    return {
        "Output Directory": output_dir,
        "Folder ID": folder_id,
        "File Name": file_name,
        "File Type": file_type,
        "Data Loader Config": {
                                "File": output_dir + "/" + file_name,
                                "Format": file_type,
                                "Chunk Size": 1,
                                "Loop on end": True
                                }
    }


if __name__ == "__main__":
    args = get_args()
    formatted_args = format_args(output_dir=args.output_folder,
                                 folder_id=args.folder_id,
                                 file_name=args.file_name,
                                 file_type=args.file_type)
    print(GoogleDriveAccessor().run(args=formatted_args))
