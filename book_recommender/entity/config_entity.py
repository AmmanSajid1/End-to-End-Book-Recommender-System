from collections import namedtuple

DataIngestionConfig = namedtuple("DatasetConfig", ["dataset_download_url", "raw_data_dir", "ingested_dir"])

DataValidationConfig = namedtuple("DataValidationConfig", ["clean_data_dir",
                                                           "books_csv_file",
                                                           "ratings_csv_file",
                                                           "serialized_objects_dir",])

DataTransformationConfig = namedtuple("DataTransformationConfig", ["clean_data_file_path",
                                                                   "transformed_data_dir"])


ModelTrainerConfig = namedtuple("ModelTrainerConfig", ["trained_model_dir", "trained_model_name", "pivot_table_dir"])