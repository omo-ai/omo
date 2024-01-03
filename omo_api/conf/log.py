
import logging
import os
import errno
import pathlib

def mkdir_p(path):
    try:
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    except OSError as exc:  # Python ≥ 2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        # possibly handle other errno cases here, otherwise finally:
        else:
            raise

class MakeFileHandler(logging.FileHandler):
    def __init__(self, filename, mode='a', encoding=None, delay=0):            
        mkdir_p(os.path.dirname(filename))
        logging.FileHandler.__init__(self, filename, mode, encoding, delay)

log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",

        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "answer_question": {
            "formatter": "default",
            "class": "omo_api.conf.log.MakeFileHandler",
            "filename": "/mnt/efs/logs/answer_question.log",
        }
    },
    "loggers": {
        "": {
            "handlers": ["default"],
            "level": "DEBUG"
        },
        "answer_question": { 
            "handlers": ["answer_question"],
            "level": "DEBUG"
        }
    },
}