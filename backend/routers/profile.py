from fastapi import APIRouter, Depends
from typing import Union, List, Optional, Dict
from queries.profile import Error, ProfileIn, ProfileOut, ProfileRepo
from authenticator import authenticator


router = APIRouter()

@router.post("/profiles", response_model=Union[ProfileOut, Error])
def create_profile(
    profile: ProfileIn,
    repo: ProfileRepo = Depends(ProfileRepo),
    account_data: Dict = Depends(authenticator.get_current_account_data),
):
    return repo.create_profile(profile)

@router.get("/profiles", response_model=Union[List[ProfileOut], Error])
def get_all_profiles(
    repo: ProfileRepo = Depends(ProfileRepo), 
    account_data: Dict = Depends(authenticator.get_current_account_data),
):
    return repo.get_all_profiles()
