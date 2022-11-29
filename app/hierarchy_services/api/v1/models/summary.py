import datetime
import re
from enum import Enum
from typing import Optional
import pydantic
from bson.objectid import ObjectId
from pydantic import BaseModel, conint, validator
from shared_services.data_model.response_model import CaseInsensitiveEnum


class SortBy(CaseInsensitiveEnum):
    """Values to sort data by"""
    RUNTIME = 'RUNTIME'
    STATUS = 'STATUS'
    LASTUPDATED = 'LASTUPDATED'
    STARTTIME = 'STARTTIME'

    TITLE = 'TITLE'

class SortDirection(CaseInsensitiveEnum):
    """Values to decide sort direction"""
    ASCENDING = 'ASC'
    DESCENDING = 'DESC'


class FilterBy(CaseInsensitiveEnum):
    """Values to filter data by"""
    ALL = 'ALL'
    EXPERIMENTS = 'EXPERIMENTS'
    DISPATCHES = 'DISPATCHES'
    PROJECTS = 'PROJECTS'


class SummaryResponse(BaseModel):
    """Summary Response"""
    count: int
    items: list

class SummaryRequest(BaseModel):
    """Summary Request Model"""
    count: conint(gt=0, lt=100)
    offset: Optional[conint(gt=-1)] = 0
    search: Optional[str] = None
    filterBy: Optional[FilterBy] = FilterBy.ALL
    sort: Optional[SortBy] = SortBy.LASTUPDATED
    direction: Optional[SortDirection] = SortDirection.DESCENDING


class DetailsResponse(BaseModel):
    """Details Response"""
    count: int
    items: list

class DetailsType(CaseInsensitiveEnum):
    """Value to get the details of an item"""
    EXPERIMENT = 'EXPERIMENT'
    PROJECT = 'PROJECT'

class DetailsRequest(BaseModel):
    """Details Request Model"""
    sort: Optional[SortBy] = SortBy.LASTUPDATED
    direction: Optional[SortDirection] = SortDirection.DESCENDING
    objectId: str
    objectType: DetailsType
