import yaml
import sys 
from book_recommender.exception.exception_handler import AppException


def read_yaml_file(file_path: str) -> dict:
    """
    Reads a YAML file and returns its contents as a dictionary.

    Parameters:
        file_path (str): The path to the YAML file.

    Returns:
        dict: The contents of the YAML file.
    """
    try:
        with open(file_path, 'rb') as file:
            content = yaml.safe_load(file)
        return content
    except Exception as e:
        raise AppException(e, sys) from e
    


    

