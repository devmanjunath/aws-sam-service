from shared_services.schema.documents import Dispatch, Experiment
from hierarchy_services.api.v1.models.dispatch import GridResponse, PinDispatchViewModel


async def get_parent_id(dispatch):
    """Gets grandparent for a dispatch"""
    if dispatch.parent:
        experiment_parent_id = await Experiment.get(dispatch.parent)
        if experiment_parent_id:
            return experiment_parent_id.parent
        return None
    return None


async def get_grid_view(count: int):
    """Loads grid view"""
    dispatch_list = []
    # pinned_dispatches = await Dispatch.find(Dispatch.isPinned == True and Dispatch.isArchived == False and Dispatch.isDeleted == False).sort(-Dispatch.lastUpdated).limit(count).to_list()
    pinned_dispatches = await Dispatch.find({"$and": [{Dispatch.isPinned: True},
                                                      {Dispatch.isArchived: False},
                                                      {Dispatch.isDeleted: False}]}).\
        sort(-Dispatch.lastUpdated).limit(count).to_list()
    for dispatch in pinned_dispatches:
        disp = PinDispatchViewModel(dispatch)
        disp.master = await get_parent_id(dispatch)
        dispatch_list.append(disp)
    if len(dispatch_list) < count:
        # unpinned_dispatches = await Dispatch.find(Dispatch.isPinned == False and Dispatch.isArchived == False and Dispatch.isDeleted == False).sort(-Dispatch.lastUpdated).limit(count-len(dispatch_list)).to_list()
        unpinned_dispatches = await Dispatch.find({"$and": [{Dispatch.isPinned: True},
                                                            {Dispatch.isArchived: False},
                                                            {Dispatch.isDeleted: False}]}).\
            sort(-Dispatch.lastUpdated).limit(count-len(dispatch_list)).to_list()
        for dispatch in unpinned_dispatches:
            disp = PinDispatchViewModel(dispatch)
            disp.master = await get_parent_id(dispatch)
            dispatch_list.append(disp)
    return GridResponse(gridMessage="Pinned/Recent dispatches", count=count,
                        recents=dispatch_list)
