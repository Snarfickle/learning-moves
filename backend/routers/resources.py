from fastapi import APIRouter, Depends, HTTPException
from typing import Union, List, Dict
from queries.resources import Error, ResourceIn, ResourceOut, ResourceRepo
from authenticator import authenticator

router = APIRouter()

@router.post("/resources", response_model=ResourceOut)
def create_resource(
    resource: ResourceIn,
    repo: ResourceRepo = Depends(ResourceRepo),
    account_data: Dict = Depends(authenticator.get_current_account_data),
):
    result = repo.create_resource(resource)
    if isinstance(result, Error):
        raise HTTPException(status_code=400, detail=result.dict())
    return result

@router.get("/resources/{resource_id}", response_model=ResourceOut)
def get_one_resource(
    resource_id: int,
    repo: ResourceRepo = Depends(ResourceRepo),
    account_data: Dict = Depends(authenticator.get_current_account_data),
):
    result = repo.get_one(resource_id)
    if isinstance(result, Error):
        raise HTTPException(status_code=404, detail=result.dict())
    return result

@router.put("/resources/{resource_id}", response_model=ResourceOut)
def update_resource(
    resource_id: int,
    resource: ResourceIn,
    repo: ResourceRepo = Depends(ResourceRepo),
    account_data: Dict = Depends(authenticator.get_current_account_data),
):
    result = repo.update_resource(resource_id, resource)
    if isinstance(result, Error):
        raise HTTPException(status_code=400, detail=result.dict())
    return result

@router.delete("/resources/{resource_id}", response_model=Dict)
def delete_resource(
    resource_id: int,
    repo: ResourceRepo = Depends(ResourceRepo),
    account_data: Dict = Depends(authenticator.get_current_account_data),
):
    result = repo.delete_resource(resource_id)
    if isinstance(result, Error):
        raise HTTPException(status_code=404, detail=result.dict())
    return result

@router.get("/resources", response_model=List[ResourceOut])
def get_all_resources(
    repo: ResourceRepo = Depends(ResourceRepo), 
    account_data: Dict = Depends(authenticator.get_current_account_data),
):
    result = repo.get_all_resources()
    if isinstance(result, Error):
        raise HTTPException(status_code=400, detail=result.dict())
    return result
