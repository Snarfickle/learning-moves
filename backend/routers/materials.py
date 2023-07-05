from fastapi import APIRouter, Depends, HTTPException
from typing import Union, List, Dict
from queries.materials import Error, MaterialIn, MaterialOut, MaterialRepo
from authenticator import authenticator

router = APIRouter()

@router.post("/materials", response_model=MaterialOut)
def create_material(
    material: MaterialIn,
    repo: MaterialRepo = Depends(MaterialRepo),
    account_data: Dict = Depends(authenticator.get_current_account_data),
):
    result = repo.create_material(material)
    if isinstance(result, Error):
        raise HTTPException(status_code=400, detail=result.dict())
    return result

@router.get("/materials/{material_id}", response_model=MaterialOut)
def get_one_material(
    material_id: int,
    repo: MaterialRepo = Depends(MaterialRepo),
    account_data: Dict = Depends(authenticator.get_current_account_data),
):
    result = repo.get_one(material_id)
    if isinstance(result, Error):
        raise HTTPException(status_code=404, detail=result.dict())
    return result

@router.put("/materials/{material_id}", response_model=MaterialOut)
def update_material(
    material_id: int,
    material: MaterialIn,
    repo: MaterialRepo = Depends(MaterialRepo),
    account_data: Dict = Depends(authenticator.get_current_account_data),
):
    result = repo.update_material(material_id, material)
    if isinstance(result, Error):
        raise HTTPException(status_code=400, detail=result.dict())
    return result

@router.delete("/materials/{material_id}", response_model=Dict)
def delete_material(
    material_id: int,
    repo: MaterialRepo = Depends(MaterialRepo),
    account_data: Dict = Depends(authenticator.get_current_account_data),
):
    result = repo.delete_material(material_id)
    if isinstance(result, Error):
        raise HTTPException(status_code=404, detail=result.dict())
    return result

@router.get("/materials", response_model=List[MaterialOut])
def get_all_materials(
    repo: MaterialRepo = Depends(MaterialRepo), 
    account_data: Dict = Depends(authenticator.get_current_account_data),
):
    result = repo.get_all_materials()
    if isinstance(result, Error):
        raise HTTPException(status_code=400, detail=result.dict())
    return result
