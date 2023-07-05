from fastapi import APIRouter, Depends, HTTPException
from typing import Union, List, Dict
from queries.appointments import Error, AppointmentIn, AppointmentOut, AppointmentRepo
from authenticator import authenticator

router = APIRouter()

@router.post("/appointments", response_model=AppointmentOut)
def create_appointment(
    appointment: AppointmentIn,
    repo: AppointmentRepo = Depends(AppointmentRepo),
    account_data: Dict = Depends(authenticator.get_current_account_data),
):
    result = repo.create_appointment(appointment)
    if isinstance(result, Error):
        raise HTTPException(status_code=400, detail=result.dict())
    return result

@router.get("/appointments/{appointment_id}", response_model=AppointmentOut)
def get_one_appointment(
    appointment_id: int,
    repo: AppointmentRepo = Depends(AppointmentRepo),
    account_data: Dict = Depends(authenticator.get_current_account_data),
):
    result = repo.get_one(appointment_id)
    if isinstance(result, Error):
        raise HTTPException(status_code=404, detail=result.dict())
    return result

@router.put("/appointments/{appointment_id}", response_model=AppointmentOut)
def update_appointment(
    appointment_id: int,
    appointment: AppointmentIn,
    repo: AppointmentRepo = Depends(AppointmentRepo),
    account_data: Dict = Depends(authenticator.get_current_account_data),
):
    result = repo.update_appointment(appointment_id, appointment)
    if isinstance(result, Error):
        raise HTTPException(status_code=400, detail=result.dict())
    return result

@router.delete("/appointments/{appointment_id}", response_model=Dict)
def delete_appointment(
    appointment_id: int,
    repo: AppointmentRepo = Depends(AppointmentRepo),
    account_data: Dict = Depends(authenticator.get_current_account_data),
):
    result = repo.delete_appointment(appointment_id)
    if isinstance(result, Error):
        raise HTTPException(status_code=404, detail=result.dict())
    return result

@router.get("/appointments", response_model=List[AppointmentOut])
def get_all_appointments(
    repo: AppointmentRepo = Depends(AppointmentRepo), 
    account_data: Dict = Depends(authenticator.get_current_account_data),
):
    result = repo.get_all_appointments()
    if isinstance(result, Error):
        raise HTTPException(status_code=400, detail=result.dict())
    return result
