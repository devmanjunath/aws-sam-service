# pylint: disable=broad-except,dangerous-default-value,singleton-comparison
# Copyright 2021 Agnostiq Inc.
#
# This file is part of the Covalent Web Application.
#
# License details to be entered here

"""Contains methods for the hierarchy endpoint"""

from operator import attrgetter
from beanie import Document, PydanticObjectId
from beanie.operators import In
from bson.objectid import ObjectId
from pydantic import BaseModel
from pyparsing import empty
from shared_services.schema.documents import Dispatch, Experiment, Project, Summary
from .dispatch import get_parent_id
from hierarchy_services.api.v1.models.summary import DetailsResponse, SummaryResponse
from shared_services.database.view_models import (DispatchViewModel, ExperimentViewModel,
                                      ProjectViewModel)


async def get_record(item_id: PydanticObjectId, document: Document):
    """Gets a document"""
    doc = await document.get(item_id)
    return doc


class SummaryProjection(BaseModel):
    """Projection model for Summary"""
    itemId: PydanticObjectId


async def search_records(searchstring: str, count: int,
                         offset: int, sort_string: str, item_type=[]):
    """Method to search records"""
    search_text = "'"+searchstring+"'"
    sort = sort_string[1:]
    direction = 1 if sort_string[0:1] == '+' else -1
    mongo_query = [{'$search': {'compound': {'should': [
        {'autocomplete': {'query': search_text, 'path': 'title'}},
        {'autocomplete': {'query': search_text, 'path': 'status'}},
        {'autocomplete': {'query': search_text, 'path': 'lastUpdatedSearch'}},
        {'autocomplete': {'query': search_text, 'path': 'tagSearch'}},
        {'autocomplete': {'query': search_text, 'path': 'startTimeSearch'}},
    ]}}},
        {'$match': {'isActive': True, }},
        {'$skip': offset},
        {'$limit': count},
        {'$sort': {sort: direction}}
    ]
    mongo_query_all = [{'$search': {'compound': {'should': [
        {'autocomplete': {'query': search_text, 'path': 'title'}},
        {'autocomplete': {'query': search_text, 'path': 'status'}},
        {'autocomplete': {'query': search_text, 'path': 'lastUpdatedSearch'}},
        {'autocomplete': {'query': search_text, 'path': 'tagSearch'}},
        {'autocomplete': {'query': search_text, 'path': 'startTimeSearch'}},
    ]}}},
        {'$match': {'isActive': True, }},
        {'$sort': {sort: direction}}
    ]
    id_list = []
    docs = []
    if item_type != []:
        filter_by_query_all = [{'$search': {'compound': {'should': [
            {'autocomplete': {'query': search_text, 'path': 'title'}},
            {'autocomplete': {'query': search_text, 'path': 'status'}},
            {'autocomplete': {'query': search_text, 'path': 'lastUpdatedSearch'}},
            {'autocomplete': {'query': search_text, 'path': 'tagSearch'}},
            {'autocomplete': {'query': search_text, 'path': 'startTimeSearch'}},
        ]}}},
            {'$match': {
                'isActive': True,
                'itemType': {'$in': item_type}}},
            {'$sort': {sort: direction}}
        ]
        filter_by_query = [{'$search': {'compound': {'should': [
            {'autocomplete': {'query': search_text, 'path': 'title'}},
            {'autocomplete': {'query': search_text, 'path': 'status'}},
            {'autocomplete': {'query': search_text, 'path': 'lastUpdatedSearch'}},
            {'autocomplete': {'query': search_text, 'path': 'tagSearch'}},
            {'autocomplete': {'query': search_text, 'path': 'startTimeSearch'}},
        ]}}},
            {'$match': {
                'isActive': True,
                'itemType': {'$in': item_type}}},
            {'$skip': offset},
            {'$limit': count},
            {'$sort': {sort: direction}}
        ]
        all_items = await Summary.find().aggregate(filter_by_query_all,
                                                   projection_model=SummaryProjection).to_list()
        record_count = len(all_items)
        docs = await Summary.find().aggregate(filter_by_query,
                                              projection_model=SummaryProjection).to_list()
    else:
        all_items = await Summary.find().aggregate(mongo_query_all,
                                                   projection_model=SummaryProjection).to_list()
        try:
            record_count = len(all_items)
        except Exception:
            record_count = 0
        docs = await Summary.find().sort(sort_string).\
            limit(count).skip(offset).\
            aggregate(mongo_query, projection_model=SummaryProjection).to_list()
    for doc in docs:
        id_list.append(doc.itemId)
    return id_list, record_count


async def return_summary_all(count: int, offset: int, sort_string: str, search_string: str):
    """Returns all summary records"""
    record_count = 0
    items = []
    if search_string is empty:
        record_count = await Summary.find({"$and": [{Summary.isHierarchyView: True}, {Summary.isActive: True}]}).count()
        summaries = await Summary.find({"$and": [{Summary.isHierarchyView: True}, {Summary.isActive: True}]}).\
            sort(sort_string).limit(count).skip(offset).to_list()
    else:
        summaries = []
        id_list, record_count = await search_records(search_string, count,
                                                     offset, sort_string)
        summaries = await Summary.find(In(Summary.itemId, id_list)).sort(sort_string).to_list()
    for item in summaries:
        if item.itemType == 'Dispatch':
            dispatch_doc = await Dispatch.get(item.itemId)
            dispatch_master = await get_parent_id(dispatch_doc)
            dispatch = DispatchViewModel(dispatch_doc, dispatch_master)
            items.append(dispatch)
        elif item.itemType == 'Experiment':
            experiment_doc = await Experiment.get(item.itemId)
            experiment = ExperimentViewModel(experiment_doc)
            items.append(experiment)
        else:
            project_doc = await Project.get(item.itemId)
            project = ProjectViewModel(project_doc)
            items.append(project)
    return items, record_count


async def return_all_dispatches(count: int, offset: int, sort_string: str, search_string):
    """Returns all dispatches"""
    dispatch_list = []
    if search_string is empty:
        dispatches = await Dispatch.find({"$and": [{Dispatch.isArchived: False}, {Dispatch.isDeleted: False}]}).sort(sort_string).skip(offset).limit(count).to_list()
        record_count = await Dispatch.find({"$and": [{Dispatch.isArchived: False}, {Dispatch.isDeleted: False}]}).count()
    else:
        dispatches = []
        id_list, record_count = await search_records(search_string,
                                                     count, offset, sort_string, ['Dispatch'])
        dispatches = await Dispatch.find(In(Dispatch.id, id_list)).sort(sort_string).to_list()
    for dispatch in dispatches:
        dispatch_master = await get_parent_id(dispatch)
        dispatch_view_model = DispatchViewModel(dispatch, dispatch_master)
        dispatch_list.append(dispatch_view_model)
    return dispatch_list, record_count


async def check_if_experiment_is_parent(item_id):
    """Checks if experiment is parent for a specific dispatch"""
    try:
        ObjectId(item_id)
        experiment = await Experiment.get(item_id)
        if experiment is None:
            return False
        else:
            return True
    except Exception:
        return False


async def check_if_project_is_parent(item_id):
    """Checks if project is parent for a given dispatch"""
    project = await Project.get(item_id)
    if project is None:
        return False
    else:
        return True


async def return_experiments(count: int, offset: int, sort_string: str, search_string: str):
    """Returns all experiments"""
    experiments = []
    if search_string is empty:
        experiment_docs = await Experiment.find({"$and": [{Experiment.isArchived: False}, {Experiment.isDeleted: False}]}).sort(sort_string).\
            skip(offset).limit(count).to_list()
        for experiment in experiment_docs:
            exp = ExperimentViewModel(experiment)
            experiments.append(exp)
        record_count = await Experiment.find({"$and": [{Experiment.isArchived: False}, {Experiment.isDeleted: False}]}).count()
    else:
        id_list, record_count = await search_records(search_string,
                                                     count, offset, sort_string, ['Experiment'])
        summaries = await Summary.find(In(Summary.itemId, id_list)).sort(sort_string).to_list()
        for item in summaries:
            if item.itemType == 'Dispatch':
                dispatch_doc = await Dispatch.get(item.itemId)
                is_experiment_parent = await check_if_experiment_is_parent(dispatch_doc.parent)
                if is_experiment_parent is True:
                    dispatch = DispatchViewModel(dispatch_doc)
                    experiments.append(dispatch)
            elif item.itemType == 'Experiment':
                experiment_doc = await Experiment.get(item.itemId)
                experiment = ExperimentViewModel(experiment_doc)
                experiments.append(experiment)
    return experiments, record_count


async def return_projects(count: int, offset: int, sort_string: str, search_string: str):
    """Returns all projects"""
    project_list = []
    if search_string is empty:
        record_count = await Project.find({"$and": [{Project.isArchived: False}, {Project.isDeleted: False}]}).count()
        projects = await Project.find({"$and": [{Project.isArchived: False}, {Project.isDeleted: False}]}).sort(sort_string).skip(offset).limit(count).to_list()
        for item in projects:
            project = ProjectViewModel(item)
            project_list.append(project)
    else:
        id_list, record_count = await search_records(search_string,
                                                     count, offset, sort_string, ['Project'])
        projects = await Summary.find(In(Summary.itemId, id_list)).sort(sort_string).to_list()
        for item in projects:
            if item.itemType == 'Dispatch':
                dispatch_doc = await Dispatch.get(item.itemId)
                is_project_parent = await check_if_project_is_parent(dispatch_doc.parent)
                if is_project_parent:
                    dispatch = DispatchViewModel(dispatch_doc)
                    project_list.append(dispatch)
            elif item.itemType == 'Experiment':
                experiment_doc = await Experiment.get(item.itemId)
                is_project_parent = await check_if_project_is_parent(experiment_doc.parent)
                if is_project_parent:
                    experiment = ExperimentViewModel(experiment_doc)
                    project_list.append(experiment)
            else:
                project_doc = await Project.get(item.itemId)
                project = ProjectViewModel(project_doc)
                project_list.append(project)
    return project_list, record_count


async def return_experiment_details(experiment_id, sort_column: str, sort_direction: bool):
    """Returns experiment details"""
    try:
        ObjectId(experiment_id)
    except Exception:
        return DetailsResponse(count=0, dispatches=[], experiments=[])
    dispatch_list = []
    experiment = await Experiment.find({"_id": ObjectId(experiment_id)},
                                       fetch_links=True).first_or_none()
    if experiment is None:
        return DetailsResponse(count=0, dispatches=[], experiments=[])
    for dispatch in experiment.dispatches:
        if dispatch.isDeleted == False and dispatch.isArchived == False:
            dispatch_master = await get_parent_id(dispatch)
            dispatch_model = DispatchViewModel(dispatch, dispatch_master)
            dispatch_list.append(dispatch_model)
    dispatch_list.sort(key=attrgetter(sort_column), reverse=sort_direction)
    return DetailsResponse(count=len(dispatch_list),
                           items=dispatch_list)


async def return_project_details(project_id, sort_column: str, sort_direction: bool):
    """Returns project details"""
    try:
        ObjectId(project_id)
    except Exception:
        return DetailsResponse(count=0, dispatches=[], experiments=[])
    item_list = []
    project = await Project.find({"_id": ObjectId(project_id)}, fetch_links=True).first_or_none()
    if project is None:
        return DetailsResponse(count=0, dispatches=[], experiments=[])
    for dispatch in project.dispatches:
        if dispatch.isDeleted == False and dispatch.isArchived == False:
            dispatch_master = await get_parent_id(dispatch)
            disp = DispatchViewModel(dispatch, dispatch_master)
            item_list.append(disp)
    for experiment in project.experiments:
        if experiment.isDeleted == False and experiment.isArchived == False:
            exp = ExperimentViewModel(experiment)
            item_list.append(exp)
    item_list.sort(
        key=attrgetter(sort_column), reverse=sort_direction)
    return DetailsResponse(count=len(item_list), items=item_list)


async def return_summary(filter_by: str, count: int, offset: int,
                         sort_string: str, search_string: str):
    """Returns summary response to the api"""
    items = []
    record_count = 0
    if filter_by == 'ALL':
        items, record_count = await return_summary_all(count, offset, sort_string, search_string)
    elif filter_by == 'EXPERIMENTS':
        items, record_count = await return_experiments(count, offset, sort_string, search_string)
    elif filter_by == 'DISPATCHES':
        items, record_count = await return_all_dispatches(count, offset, sort_string, search_string)
    elif filter_by == 'PROJECTS':
        items, record_count = await return_projects(count, offset, sort_string, search_string)
    return SummaryResponse(count=record_count, items=items)
