import os
import sys 
import pickle
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
from book_recommender.exception.exception_handler import AppException
from book_recommender.logger.logger import logging 
from book_recommender.config.configuration import AppConfiguration

class ModelTrainer:
    def __init__(self, app_config = AppConfiguration()):
        try:
           self.model_trainer_config = app_config.get_model_trainer_config()
        except Exception as e:
            raise AppException(e, sys) from e
        

    def train(self):
        try:
            # loading pivot table data
            book_pivot = pickle.load(open(self.model_trainer_config.pivot_table_dir, 'rb'))
            # Create CSR matrix from the pivot table
            book_sparse = csr_matrix(book_pivot)

            # Train model
            model = NearestNeighbors(algorithm='brute')
            model.fit(book_sparse)

            # Save model object for recommendations
            os.makedirs(self.model_trainer_config.trained_model_dir, exist_ok=True)
            file_name = os.path.join(self.model_trainer_config.trained_model_dir, self.model_trainer_config.trained_model_name)
            pickle.dump(model, open(file_name, 'wb'))
            logging.info(f"Model saved at {file_name}")

        except Exception as e:
            raise AppException(e, sys) from e
        
    
    def initiate_model_trainer(self):
        try:
            logging.info(f"{'='*20} Model Trainer log started{'='*20}")
            self.train()
            logging.info(f"{'='*20} Model Trainer log completed{'='*20}")

        except Exception as e:
            raise AppException(e, sys) from e
