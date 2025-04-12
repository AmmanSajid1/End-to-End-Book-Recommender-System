import logging
import os 
from datetime import datetime 

# Create a directory for logs if it doesn't exist
LOG_DIR = "logs"
LOG_DIR = os.path.join(os.getcwd(), LOG_DIR)

# Create the directory if it doesn't exist
os.makedirs(LOG_DIR, exist_ok=True)

# Create file name with current date and time
CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d %H-%M-%S')}"
file_name = f"log_{CURRENT_TIME_STAMP}.log"

# Create the full path for the log file
log_file_path = os.path.join(LOG_DIR, file_name)

logging.basicConfig(
    filename=log_file_path,
    filemode='w',
    format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s',
    level=logging.NOTSET
)


