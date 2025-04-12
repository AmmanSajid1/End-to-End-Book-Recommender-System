import os
import sys 
import pickle 
import pandas as pd 
from book_recommender.exception.exception_handler import AppException
from book_recommender.logger.logger import logging 
from book_recommender.config.configuration import AppConfiguration


class DataTransformation:
    def __init__(self, app_config = AppConfiguration()):
        try:
            self.data_transformation_config = app_config.get_data_transformation_config()
            self.data_validation_config = app_config.get_data_validation_config()
        except Exception as e:
            raise AppException(e, sys) from e
        
    
    def transform_data(self):
        try:
            df = pd.read_csv(self.data_transformation_config.clean_data_file_path)
            
            # Create the pivot table
            pivot_table = df.pivot_table(index='title', columns='user_id', values='rating', fill_value=0)
            logging.info(f"Shape of the pivot table: {pivot_table.shape}")

            # Save serialized pivot table
            os.makedirs(self.data_validation_config.serialized_objects_dir, exist_ok=True)
            pickle.dump(pivot_table, open(os.path.join(self.data_validation_config.serialized_objects_dir, 'book_pivot.pkl'), "wb"))
            logging.info(f"Saved serialized pivot table at: {self.data_validation_config.serialized_objects_dir}")

            # Keep book names
            book_names = pivot_table.index 

            # Save serialized book names for web app
            os.makedirs(self.data_validation_config.serialized_objects_dir, exist_ok=True)
            pickle.dump(book_names, open(os.path.join(self.data_validation_config.serialized_objects_dir, 'book_names.pkl'), "wb"))
            logging.info(f"Saved serialized book names at: {self.data_validation_config.serialized_objects_dir}")

        except Exception as e:
            raise AppException(e, sys) from e
        

    def initiate_data_transformation(self):
        try:
            logging.info(f"{'='*20} Data Transformation log started {'='*20}")
            self.transform_data()
            logging.info(f"{'='*20} Data Transformation log completed {'='*20}")
        except Exception as e:  
            raise AppException(e, sys) from e
