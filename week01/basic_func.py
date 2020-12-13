import inspect
import logging
import os
import pathlib
from datetime import *

def record(function_name):
    log_folder_name = "-".join(["python", datetime.now().strftime("%Y%m%d")])
    log_name = ".".join([function_name, "log"])
    log_folder_path = os.path.join("/var/log", log_folder_name)
    if not os.path.exists(log_folder_path):
        os.makedirs(log_folder_path)
    log_path = os.path.join(log_folder_path, log_name)
    #log_path = log_name
    logging.basicConfig(filename = log_path, 
                        level = logging.DEBUG, 
                        datefmt = "%Y-%m-%d %H:%M:%S",
                        format = '%(asctime)s [%(levelname)s] %(message)s'
                        )
    logging.info("%s is being called", function_name)

def print_current_time():
    record(inspect.currentframe().f_code.co_name)
    print("Current time is", datetime.now())
    

if __name__ == "__main__":
    print_current_time()