import logging
from logging.config import fileConfig
from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

fileConfig("logger.conf", disable_existing_loggers=False)

logger = logging.getLogger(__name__)


@app.get("/")
def index():
    logger.warning("logging from the root logger")
    return {"message": "Welcome"}


handler = Mangum(app)
