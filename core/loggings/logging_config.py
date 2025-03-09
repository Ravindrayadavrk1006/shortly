import logging
import logging.config
import logging.handlers
import os


log_dir = 'logs/'
log_file = 'url_shorter.log'
log_path = os.path.join(log_dir, log_file)
os.makedirs(log_dir, mode = 777, exist_ok= True)

logging_config = {
    "version":1,
    "formatters":{
        "standard":{
            "format": "%(asctime)s [%(levelname)s] %(module)s: %(message)s"
        },
        "detailed":{
            "format": "%(asctime)s [%(levelname)s] %(module)s (%(filename)s:%(lineno)d): %(message)s"
        }
    },
    "handlers":{
        "console":{
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard"
        },
        "file":{
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": log_path,
            "maxBytes": 1024*1024*5,
            "formatter": "detailed"

        }
    },
    "root":{
        "level": "DEBUG",
        "handlers":["console", "file"]
    }
}


#setting up logger
logging.config.dictConfig(logging_config)
#get the root logger
logger = logging.getLogger()
