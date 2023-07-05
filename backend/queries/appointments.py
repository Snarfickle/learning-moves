from pydantic import BaseModel
from datetime import date, time
from typing import Union, List
from queries.pool import pool


class Error(BaseModel):
    pass


class AppointmentIn(BaseModel):
    user_id: int
    instructor_id: int
    appointment_date: date
    appointment_time: time


class AppointmentOut(BaseModel):
    id: int
    user_id: int
    instructor_id: int
    appointment_date: date
    appointment_time: time


class AppointmentRepo(BaseModel):
    pass
