import logging 
import os
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s:')

project_name = "book_recommender"

list_of_files = [
    f"{project_name}/__init__.py",
    f"{project_name}/components/__init__.py",
    f"{project_name}/components/stage_00_data_ingestion.py",
    f"{project_name}/components/stage_01_data_validation.py",
    f"{project_name}/components/stage_02_data_transformation.py",
    f"{project_name}/components/stage_03_model_trainer.py",
    f"{project_name}/config/__init__.py",
    f"{project_name}/config/configuration.py",
    f"{project_name}/constants/__init__.py",
    f"{project_name}/entity/__init__.py",
    f"{project_name}/entity/config_entity.py",
    f"{project_name}/exception/__init__.py",
    f"{project_name}/exception/exception_handler.py",
    f"{project_name}/logger/__init__.py",
    f"{project_name}/logger/logger.py",
    f"{project_name}/pipeline/__init__.py",
    f"{project_name}/pipeline/training_pipeline.py",
    f"{project_name}/utils/__init__.py",
    f"{project_name}/utils/utils.py",
    ".dockerignore",
    "app.py",
    "Dockerfile",
    "setup.py",
    
]

for filepath in list_of_files:
    filepath = Path(filepath)
    
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir}")

    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        with open(filepath, 'w') as file:
            pass
        logging.info(f"Creating file: {filename}")

    else:
        logging.info(f"{filename} already exists") 
