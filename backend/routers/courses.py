from fastapi import APIRouter, Depends, HTTPException
from typing import Union, List, Dict
from queries.course import Error, CourseIn, CourseOut, CourseRepo
from authenticator import authenticator

router = APIRouter()

@router.post("/courses", response_model=CourseOut)
def create_course(
    course: CourseIn,
    repo: CourseRepo = Depends(CourseRepo),
    account_data: Dict = Depends(authenticator.get_current_account_data),
):
    result = repo.create_course(course)
    if isinstance(result, Error):
        raise HTTPException(status_code=400, detail=result.dict())
    return result

@router.get("/courses/{course_id}", response_model=CourseOut)
def get_one_course(
    course_id: int,
    repo: CourseRepo = Depends(CourseRepo),
    account_data: Dict = Depends(authenticator.get_current_account_data),
):
    result = repo.get_one(course_id)
    if isinstance(result, Error):
        raise HTTPException(status_code=404, detail=result.dict())
    return result

@router.put("/courses/{course_id}", response_model=CourseOut)
def update_course(
    course_id: int,
    course: CourseIn,
    repo: CourseRepo = Depends(CourseRepo),
    account_data: Dict = Depends(authenticator.get_current_account_data),
):
    result = repo.update_course(course_id, course)
    if isinstance(result, Error):
        raise HTTPException(status_code=400, detail=result.dict())
    return result

@router.delete("/courses/{course_id}", response_model=Dict)
def delete_course(
    course_id: int,
    repo: CourseRepo = Depends(CourseRepo),
    account_data: Dict = Depends(authenticator.get_current_account_data),
):
    result = repo.delete_course(course_id)
    if isinstance(result, Error):
        raise HTTPException(status_code=404, detail=result.dict())
    return result

@router.get("/courses", response_model=List[CourseOut])
def get_all_courses(
    repo: CourseRepo = Depends(CourseRepo), 
    account_data: Dict = Depends(authenticator.get_current_account_data),
):
    result = repo.get_all_courses()
    if isinstance(result, Error):
        raise HTTPException(status_code=400, detail=result.dict())
    return result
