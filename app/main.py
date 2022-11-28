import logging
from logging.config import fileConfig
from fastapi import FastAPI
from mangum import Mangum
from os import path
from shared_files.cust_func import hello

app = FastAPI()

log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logger.conf')
fileConfig(log_file_path, disable_existing_loggers=False)

logger = logging.getLogger(__name__)


@app.get("/")
def index():
    logger.warning("logging from the root logger")
    return {"message": "Welcome to AWS SAM Project"}

@app.get("/hello")
def hello_root():
    logger.warning("printing hello from layers")
    res = hello()
    return {"message": res}


handler = Mangum(app)
