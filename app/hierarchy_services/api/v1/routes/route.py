from enum import Enum
from pyparsing import empty
from fastapi import APIRouter, Header, Path
from hierarchy_services.api.v1.services.dispatch import get_grid_view
from hierarchy_services.api.v1.services.summary import return_summary, return_experiment_details, return_project_details
from hierarchy_services.api.v1.models.dispatch import GridResponse
from hierarchy_services.api.v1.models.summary import SummaryResponse, SummaryRequest, SortDirection, DetailsResponse, DetailsRequest

router = APIRouter()

class SortColumn(Enum):
    """Columns to sort the data by"""
    RUNTIME = 'runTime'
    STATUS = 'statusValue'
    LASTUPDATED = 'lastUpdated'
    STARTTIME = 'startTime'
    TITLE = 'titleSearch'


@router.get("/recents/{count}", response_model=GridResponse)
async def list_pinned(count: int = Path(..., ge=1, le=7)):
    """This request will return the recently updated or pinned dispatches"""
    grid_response = await get_grid_view(count)
    return grid_response

@router.post("/summary", response_model=SummaryResponse)
async def return_hierarchy_summary(req: SummaryRequest):
    """Will return a summary view of all items"""
    sort_column = SortColumn[req.sort.name].value
    sort_dir = SortDirection[req.direction.name].value
    sort_string = f"{sort_dir}{sort_column}"
    if req.search is None:
        search_string = empty
    elif req.search.strip() == "":
        search_string = empty
    else:
        search_string = req.search.strip()
    response = await return_summary(req.filterBy.value,
    req.count, req.offset, sort_string, search_string)
    return response

@router.post("/details", response_model=DetailsResponse)
async def return_hierarchy_details(req: DetailsRequest):
    """Will return details of a specific item"""
    sort_column = SortColumn[req.sort.name].value
    if req.direction.name == 'ASCENDING':
        sort_direction = False
    else:
        sort_direction = True
    if req.objectType.value == 'EXPERIMENT':
        response = await return_experiment_details(req.objectId
        , sort_column, sort_direction)
    elif req.objectType.value == 'PROJECT':
        response = await return_project_details(req.objectId
        , sort_column, sort_direction)
    return response

