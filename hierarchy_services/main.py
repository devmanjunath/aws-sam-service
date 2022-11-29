from fastapi import FastAPI
from hierarchy_services.api.v1.routes.route import router
from shared_services.database import database
from hierarchy_services.api.v1.services import config_service
from shared_services.schema.documents import Dispatch, Experiment, Project, Summary
from beanie import init_beanie
app = FastAPI()

@app.on_event("startup")
async def startup_event():
    config_service.load_config()
    client = await database.get_client()
    db = await database.get_database()
    await init_beanie(
        database=client[db], document_models=[Dispatch, Experiment, Project, Summary]
    )

app.include_router(router, prefix="/api/v1")