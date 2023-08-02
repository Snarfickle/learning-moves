from fastapi import APIRouter, Depends, HTTPException
from typing import Union, List, Dict
from queries.profile import Error, ProfileIn, ProfileOut, ProfileRepo
from authenticator import authenticator

router = APIRouter()

@router.post("/profiles", response_model=ProfileOut)
def create_profile(
    profile: ProfileIn,
    repo: ProfileRepo = Depends(ProfileRepo),
    account_data: Dict = Depends(authenticator.get_current_account_data),
):
    result = repo.create_profile(profile)
    if isinstance(result, Error):
        raise HTTPException(status_code=400, detail=result.dict())
    return result

@router.get("/profiles/{profile_id}", response_model=ProfileOut)
def get_one_profile(
    profile_id: int,
    repo: ProfileRepo = Depends(ProfileRepo),
    account_data: Dict = Depends(authenticator.get_current_account_data),
):
    result = repo.get_one(profile_id)
    if isinstance(result, Error):
        raise HTTPException(status_code=404, detail=result.dict())
    return result

@router.put("/profiles/edit/{profile_id}", response_model=ProfileOut)
def update_profile(
    profile_id: int,
    profile: ProfileIn,
    repo: ProfileRepo = Depends(ProfileRepo),
    account_data: Dict = Depends(authenticator.get_current_account_data),
):
    result = repo.update_profile(profile_id, profile)
    if isinstance(result, Error):
        raise HTTPException(status_code=400, detail=result.dict())
    return result

@router.delete("/profiles/{profile_id}", response_model=Dict)
def delete_profile(
    profile_id: int,
    repo: ProfileRepo = Depends(ProfileRepo),
    account_data: Dict = Depends(authenticator.get_current_account_data),
):
    result = repo.delete_profile(profile_id)
    if isinstance(result, Error):
        raise HTTPException(status_code=404, detail=result.dict())
    return result

@router.get("/profiles", response_model=List[ProfileOut])
def get_all_profiles(
    repo: ProfileRepo = Depends(ProfileRepo), 
    account_data: Dict = Depends(authenticator.get_current_account_data),
):
    result = repo.get_all_profiles()
    if isinstance(result, Error):
        raise HTTPException(status_code=400, detail=result.dict())
    return result
