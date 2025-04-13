import os
import sys 
import pickle 
import streamlit as st
import numpy as np
from book_recommender.logger.logger import logging 
from book_recommender.exception.exception_handler import AppException
from book_recommender.pipeline.training_pipeline import TrainingPipeline
from book_recommender.config.configuration import AppConfiguration

class Recommendation:
    def __init__(self, app_config = AppConfiguration()):
        try:
            self.recommendation_config = app_config.get_recommendation_config()
        except Exception as e:
            raise AppException(e, sys) from e
        
    def fetch_poster(self, suggestion):
        try:
            book_name = []
            ids_index = []
            poster_url = []
            book_pivot = pickle.load(open(self.recommendation_config.book_pivot_serialized_objects, 'rb'))
            ratings_and_books = pickle.load(open(self.recommendation_config.ratings_and_books_serialized_objects, 'rb'))

            for book_id in suggestion:
                book_name.append(book_pivot.index[book_id])

            for name in book_name[0]:
                ids = np.where(ratings_and_books['title'] == name)[0][0]
                ids_index.append(ids)

            for idx in ids_index:
                url = ratings_and_books.iloc[idx]['image_url']
                poster_url.append(url)

            return poster_url
        
        except Exception as e:
            raise AppException(e, sys) from e
        
    def recommend_book(self, book_name):
        try:
            books_list = []
            model = pickle.load(open(self.recommendation_config.trained_model_path, 'rb'))
            book_pivot = pickle.load(open(self.recommendation_config.book_pivot_serialized_objects, 'rb'))
            book_id = np.where(book_pivot.index == book_name)[0][0]
            distances, suggestions = model.kneighbors(book_pivot.iloc[book_id, :].values.reshape(1, -1), n_neighbors=6)

            poster_url = self.fetch_poster(suggestions)

            for i in range(len(suggestions)):
                books = book_pivot.index[suggestions[i]]
                for j in books:
                    books_list.append(j)

            return books_list, poster_url
        
        except Exception as e:
            raise AppException(e, sys) from e
        
    def train_engine(self):
        try:
            obj = TrainingPipeline()
            obj.start_training_pipeline()
            st.text("Training completed successfully")
            logging.info(f"Recommendation Engine Trained Successfully")
        except Exception as e:
            raise AppException(e, sys) from e
        
    def recommendations_engine(self, selected_books):
        try:
            recommended_books, poster_url = self.recommend_book(selected_books)
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.text(recommended_books[1])
                st.image(poster_url[1])

            with col2:
                st.text(recommended_books[2])
                st.image(poster_url[2])

            with col3:
                st.text(recommended_books[3])
                st.image(poster_url[3])

            with col4:
                st.text(recommended_books[4])
                st.image(poster_url[4])

            with col5:
                st.text(recommended_books[5])
                st.image(poster_url[5])
        except Exception as e:
            raise AppException(e, sys) from e
        
    
if __name__ == "__main__":
    try:
        st.header("ML Based Book Recommender System")
        st.text("This is a collaborative filtering based book recommender system")

        obj = Recommendation()

        # Training
        if st.button("Train Recommender System"):
            obj.train_engine()

        book_names = pickle.load(open(os.path.join('templates', 'book_names.pkl'), 'rb'))
        selected_books = st.selectbox(
            "Typw or select a book from the dropdown",
            book_names
        )

        if st.button("Show Recommendations"):
            obj.recommendations_engine(selected_books)

    except Exception as e:
        raise AppException(e, sys) from e
