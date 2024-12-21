import os
import sys
import logging

logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"
log_dir = "logs"
log_filepath = os.join(log_dir, "running_log")
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    Level = logging.INFO,
    format= logging_str,

    handlers=[
        logging.FileHandeler(log_filepath),
        logging.streamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("cnnClassifierLogger")