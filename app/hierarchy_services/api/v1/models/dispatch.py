
from pydantic import BaseModel
from shared_services.schema.documents import Dispatch


class GridResponse(BaseModel):
    """Grid Response"""
    gridMessage: str
    count: int
    recents: list

class PinDispatchViewModel:
    """Pinned Dispatch View Model"""
    def __init__(self, dispatch: Dispatch):
        self.id = dispatch.id
        self.title = dispatch.title
        self.totalElectrons = dispatch.totalElectrons
        self.completedElectrons = dispatch.completedElectrons
        self.status = dispatch.status
        self.startTime = dispatch.startTime
        self.lastUpdated = dispatch.lastUpdated
        self.parentId = str(dispatch.parent)
        self.isPinned = dispatch.isPinned
        self.tags = dispatch.tags
        self.runTime = dispatch.runTime
        self.master = None
