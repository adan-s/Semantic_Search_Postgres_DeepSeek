import logging
import os

DEBUG = os.getenv("DEBUG_MODE", "True").lower() == "true"
APPLICATION_ROOT = os.getenv("APPLICATION_APPLICATION_ROOT", "")
HOST = os.getenv("APPLICATION_HOST", "127.0.0.1")
PORT = int(os.getenv("APPLICATION_PORT", "3000"))

logging.basicConfig(
    filename=os.getenv("APP_LOG", "app.log"),
    level=logging.DEBUG,
    format="%(levelname)s: %(asctime)s \
        pid:%(process)s module:%(module)s %(message)s",
    datefmt="%d/%m/%y %H:%M:%S",
)
