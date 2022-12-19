# logger設定
import os
import time
import datetime
from logging import getLogger, StreamHandler, FileHandler, DEBUG, INFO, Formatter
from dotenv import load_dotenv
load_dotenv

class ElapsedFormatter:
    def __init__(self):
        self.start_time = time.time()

    def format(self, record):
        elapsed_seconds = record.created - self.start_time
        elapsed = datetime.timedelta(seconds = elapsed_seconds)
        return "{} \t {}".format(elapsed, record.getMessage())

def init_logger(exp_name, loglevel="INFO"):
    t_delta = datetime.timedelta(hours=9)  # 9時間
    JST = datetime.timezone(t_delta, 'JST')  # UTCから9時間差の「JST」タイムゾーン
    dt = datetime.datetime.now(JST)
    exe_start_time = dt.strftime('%Y%m%d%H%M%S')

    log_dir = os.path.join(os.getenv("OUTPUT_DIR"), exp_name, "log")
    log_file = os.path.join(log_dir, f"log_{exe_start_time}.log")
    os.makedirs(log_dir, exist_ok=True)

    logger = getLogger(os.getenv("COMPETITION") + exp_name)
    if loglevel == "DEBUG":
        logger.setLevel(DEBUG)
    elif loglevel == "INFO":
        logger.setLevel(INFO)

    logger.handlers.__init__()
    stream_handler = StreamHandler()
    stream_handler.setFormatter(ElapsedFormatter())
    logger.addHandler(stream_handler)
    
    file_handler = FileHandler(log_file, mode="a")
    file_handler.setFormatter(ElapsedFormatter())
    logger.addHandler(file_handler)

    return logger