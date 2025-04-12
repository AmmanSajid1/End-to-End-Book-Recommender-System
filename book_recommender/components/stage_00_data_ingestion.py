import os
import sys 
import urllib 
import urllib.request
import zipfile 
from book_recommender.logger.logger import logging 
from book_recommender.exception.exception_handler import AppException
from book_recommender.config.configuration import AppConfiguration

class DataIngestion:
    def __init__(self, app_config = AppConfiguration()):
        try:
            logging.info(f"{'='*20}Data Ingestion log started.{'='*20}")
            self.data_ingestion_config = app_config.get_data_ingestion_config()
        except Exception as e:
            raise AppException(e, sys) from e
        

    def download_data(self):
        """
        Download the dataset from the given URL and save it to the specified directory.
        """
        try:
            dataset_url = self.data_ingestion_config.dataset_download_url
            zip_download_dir = self.data_ingestion_config.raw_data_dir
            os.makedirs(zip_download_dir, exist_ok=True)
            data_file_name = os.path.basename(dataset_url)
            zip_file_path = os.path.join(zip_download_dir, data_file_name)
            logging.info(f"Downloading dataset from {dataset_url} to {zip_file_path}")
            urllib.request.urlretrieve(dataset_url, zip_file_path)
            logging.info(f"Dataset downloaded successfully to {zip_file_path}")
            return zip_file_path 
        
        except Exception as e:
            raise AppException(e, sys) from e
        
    def extract_data(self, zip_file_path: str):
        """
        Extract the contents of the downloaded zip file.
        """
        try:
            ingested_dir = self.data_ingestion_config.ingested_dir
            os.makedirs(ingested_dir, exist_ok=True)
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(ingested_dir)
            logging.info(f"Extracting zip file {zip_file_path} to {ingested_dir}")
            logging.info(f"Data extracted successfully to {ingested_dir}")
        except Exception as e:
            raise AppException(e, sys) from e
        
    def initiate_data_ingestion(self):
        """
        Initiate the data ingestion process by downloading and extracting the dataset.
        """
        try:
            zip_file_path = self.download_data()
            self.extract_data(zip_file_path)
            logging.info(f"{'='*20}Data Ingestion log completed.{'='*20} \n\n")
        except Exception as e:
            raise AppException(e, sys) from e
