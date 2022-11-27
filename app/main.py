import logging
from logging.config import fileConfig
from fastapi import FastAPI
from mangum import Mangum
from os import path
import numpy

app = FastAPI()

log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logger.conf')
fileConfig(log_file_path, disable_existing_loggers=False)

logger = logging.getLogger(__name__)


@app.get("/")
def index():
    logger.warning("logging from the root logger")
    print(numpy)
    return {"message": "hello"}


handler = Mangum(app)
