import inspect
import logging
import os
import pathlib
from datetime import *
from functools import wraps
import sys

def log_record(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        log_folder_name = "-".join(["python", datetime.now().strftime("%Y%m%d")])
        log_name = ".".join([func.__name__, "log"])
        log_folder_path = os.path.join("/tmp", log_folder_name)
        if not os.path.exists(log_folder_path):
            os.makedirs(log_folder_path)
        log_path = os.path.join(log_folder_path, log_name)
        logging.basicConfig(filename = log_path, 
                        level = logging.DEBUG, 
                        datefmt = "%Y-%m-%d %H:%M:%S",
                        format = '%(asctime)s [%(levelname)s] %(message)s'
                        )
        try:
            return func(*args, **kwargs)
        finally:
            print("logging to {}".format(log_path))
            logging.info("%s is being called", func.__name__)
    return wrapper

@log_record 
def display_item(input_list):
    for item in input_list:
        print(item)

if __name__ == "__main__":
    input_list = [x * 10 for x in range(5)]
    display_item(input_list)