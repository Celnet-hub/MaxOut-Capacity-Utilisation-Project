import logging
from datetime import datetime
import os

def get_logger(name: str):
    logger = logging.getLogger(name)

    # Prevent logs from being duplicated across multiple calls (e.g. in Celery workers)
    if logger.hasHandlers():
        return logger
    
    # Set the Base Level to INFO
    logger.setLevel(logging.INFO)
    
    # set logs directory path
    project_root = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(project_root, "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(log_dir, f"{current_date}.log")
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
