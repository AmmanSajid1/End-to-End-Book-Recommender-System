import os 
import sys 
import ast 
import pandas as pd 
import pickle 
from book_recommender.logger.logger import logging 
from book_recommender.exception.exception_handler import AppException
from book_recommender.config.configuration import AppConfiguration


class DataValidation:
    def __init__(self, app_config = AppConfiguration()):
        try:
            self.data_validation_config = app_config.get_data_validation_config()
        except Exception as e:
            raise AppException(e, sys) from e
        
    
    def preprocess_data(self):
        try:
            ratings = pd.read_csv(self.data_validation_config.ratings_csv_file, sep=';', encoding='latin-1', on_bad_lines='skip')
            books = pd.read_csv(self.data_validation_config.books_csv_file, sep=';', encoding='latin-1', on_bad_lines='skip')

            logging.info(f"Shape of ratings data: {ratings.shape}")
            logging.info(f"Shape of books data: {books.shape}")

            # Here the Large Image URL column is important for the poster so we will keep it
            books = books[['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher', 'Image-URL-L']]
            # Let's rename the columns
            books.rename(columns={'Book-Title': 'title', 'Book-Author': 'author', 
                                  'Year-Of-Publication': 'year', 'Publisher': 'publisher', 
                                  'Image-URL-L': 'image_url'}, inplace=True)
            
            ratings.rename(columns={'User-ID': 'user_id',
                              'Book-Rating': 'rating'}, inplace=True)
            
            # Keep users who have rated at least 100 books
            at_least_100 = ratings["user_id"].value_counts()[ratings["user_id"].value_counts() >= 100].index.tolist()
            ratings = ratings[ratings["user_id"].isin(at_least_100)]
            
            # Now merge ratings with books
            ratings_and_books = ratings.merge(books, on="ISBN")
            
            # Add number of ratings for each book
            number_rating = ratings_and_books.groupby("title")["rating"].count().reset_index()
            number_rating.rename(columns={"rating": "number_of_ratings"}, inplace=True)
            ratings_and_books = ratings_and_books.merge(number_rating, on="title")

            # Keep books that have at least 50 ratings
            ratings_and_books = ratings_and_books[ratings_and_books["number_of_ratings"] >= 50]

            # Drop duplicates
            ratings_and_books.drop_duplicates(subset=["user_id", "title"], inplace=True)
            logging.info(f"Shape of final cleaned data: {ratings_and_books.shape}")

            # Save the cleaned data for transformation
            os.makedirs(self.data_validation_config.clean_data_dir, exist_ok=True)
            ratings_and_books.to_csv(os.path.join(self.data_validation_config.clean_data_dir, "clean_data.csv"), index=False)
            logging.info(f"Saved ckeaned data to {self.data_validation_config.clean_data_dir}")

            # Save the serialized cleaned data for web app
            os.makedirs(self.data_validation_config.serialized_objects_dir, exist_ok=True)
            pickle.dump(ratings_and_books, open(os.path.join(self.data_validation_config.serialized_objects_dir, "clean_data.pkl"), "wb"))
            logging.info(f"Saved serialized cleaned data to {self.data_validation_config.serialized_objects_dir}")

        except Exception as e:
            raise AppException(e, sys) from e
        

    def initiate_data_validation(self):
        try:
            logging.info(f"{'='*20} Data Validation log started{'='*20}")
            self.preprocess_data()
            logging.info(f"{'='*20} Data Validation log completed{'='*20}")
        except Exception as e:
            raise AppException(e, sys) from e