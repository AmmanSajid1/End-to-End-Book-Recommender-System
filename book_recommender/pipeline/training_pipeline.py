from book_recommender.components.stage_00_data_ingestion import DataIngestion
from book_recommender.components.stage_01_data_validation import DataValidation
from book_recommender.components.stage_02_data_transformation import DataTransformation
from book_recommender.exception.exception_handler import AppException
import sys

class TrainingPipeline:
    def __init__(self):
        self.data_ingestion = DataIngestion()
        self.data_validation = DataValidation()
        self.data_transformation = DataTransformation()

    def start_training_pipeline(self):
        try:
            self.data_ingestion.initiate_data_ingestion()
            self.data_validation.initiate_data_validation()
            self.data_transformation.initiate_data_transformation()



        except Exception as e:
            raise AppException(e, sys) from e