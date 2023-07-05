from fastapi import APIRouter, Depends, HTTPException
from typing import Union, List, Dict
from queries.certificates import Error, CertificateIn, CertificateOut, CertificateRepo
from authenticator import authenticator

router = APIRouter()

@router.post("/certificates", response_model=CertificateOut)
def create_certificate(
    certificate: CertificateIn,
    repo: CertificateRepo = Depends(CertificateRepo),
    account_data: Dict = Depends(authenticator.get_current_account_data),
):
    result = repo.create_certificate(certificate)
    if isinstance(result, Error):
        raise HTTPException(status_code=400, detail=result.dict())
    return result

@router.get("/certificates/{certificate_id}", response_model=CertificateOut)
def get_one_certificate(
    certificate_id: int,
    repo: CertificateRepo = Depends(CertificateRepo),
    account_data: Dict = Depends(authenticator.get_current_account_data),
):
    result = repo.get_one(certificate_id)
    if isinstance(result, Error):
        raise HTTPException(status_code=404, detail=result.dict())
    return result

@router.put("/certificates/{certificate_id}", response_model=CertificateOut)
def update_certificate(
    certificate_id: int,
    certificate: CertificateIn,
    repo: CertificateRepo = Depends(CertificateRepo),
    account_data: Dict = Depends(authenticator.get_current_account_data),
):
    result = repo.update_certificate(certificate_id, certificate)
    if isinstance(result, Error):
        raise HTTPException(status_code=400, detail=result.dict())
    return result

@router.delete("/certificates/{certificate_id}", response_model=Dict)
def delete_certificate(
    certificate_id: int,
    repo: CertificateRepo = Depends(CertificateRepo),
    account_data: Dict = Depends(authenticator.get_current_account_data),
):
    result = repo.delete_certificate(certificate_id)
    if isinstance(result, Error):
        raise HTTPException(status_code=404, detail=result.dict())
    return result

@router.get("/certificates", response_model=List[CertificateOut])
def get_all_certificates(
    repo: CertificateRepo = Depends(CertificateRepo), 
    account_data: Dict = Depends(authenticator.get_current_account_data),
):
    result = repo.get_all_certificates()
    if isinstance(result, Error):
        raise HTTPException(status_code=400, detail=result.dict())
    return result
