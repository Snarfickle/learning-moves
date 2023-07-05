from pydantic import BaseModel
from typing import Optional, List, Union
from queries.pool import pool
from psycopg.rows import dict_row


class Error(BaseModel):
    message: str
    picture: Optional[str]


class AppointmentIn(BaseModel):
    id: int
    user_id: int
    instructor_id: int
    date: str
    time: str
    address: str
    city: str
    state: str
    zip: str
    country: str


class AppointmentOut(AppointmentIn):
    id: int


class AppointmentRepo(BaseModel):
    def get_one(self, appointment_id: int) -> Union[AppointmentOut, Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=dict_row) as db:
                    db.execute(
                        """
                        SELECT *
                        FROM appointments
                        WHERE id = %s
                        """,
                        [appointment_id],
                    )
                    record = db.fetchone()
                    if record is None:
                        return Error(picture="https://skrift.io/media/3cdf1cxr/missing-files.jpg", message="There is no appointment with that ID")
                    return AppointmentOut(**record)
        except Exception as error:
            print(error)
            return Error(picture="https://images5.fanpop.com/image/photos/28100000/I-dunno-lol-random-28130691-500-412.jpg", message="Unable to pull appointment from database")

    def update_appointment(self, appointment_id: int, appointment: AppointmentIn) -> Union[AppointmentOut, Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=dict_row) as db:
                    db.execute(
                        """
                        UPDATE appointments
                        SET user_id: %s,
                            instructor_id: %s,
                            date = %s,
                            time = %s,
                            address = %s,
                            city = %s,
                            state = %s,
                            zip = %s,
                            country = %s
                        WHERE id = %s
                        RETURNING *;
                        """,
                        [appointment.user_id, appointment.instructor_id, appointment.date, appointment.time, appointment.address, appointment.city, appointment.state,
                         appointment.zip, appointment.country, appointment_id]
                    )
                    record = db.fetchone()
                    if record is None:
                        return Error(picture="https://skrift.io/media/3cdf1cxr/missing-files.jpg", message="There is no appointment with that ID")
                    return AppointmentOut(**record)
        except Exception as error:
            print(error)
            return Error(picture="https://images5.fanpop.com/image/photos/28100000/I-dunno-lol-random-28130691-500-412.jpg", message="Unable to update appointment in database")

    def get_all_appointments(self) -> Union[List[AppointmentOut], Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=dict_row) as db:
                    db.execute(
                        """
                        SELECT *
                        FROM appointments
                        """
                    )
                    records = db.fetchall()
                    return [AppointmentOut(**record) for record in records]
        except Exception as error:
            print(error)
            return Error(picture="https://images5.fanpop.com/image/photos/28100000/I-dunno-lol-random-28130691-500-412.jpg", message="Unable to fetch appointments from database")

    def create_appointment(self, appointment: AppointmentIn) -> Union[AppointmentOut, Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=dict_row) as db:
                    db.execute(
                        """
                        INSERT INTO appointments (date, time, address, city, state, zip, country)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING *;
                        """,
                        [appointment.user_id, appointment.instructor_id, appointment.date, appointment.time, appointment.address, appointment.city, appointment.state,
                         appointment.zip, appointment.country]
                    )
                    record = db.fetchone()
                    return AppointmentOut(**record)
        except Exception as error:
            print(error)
            return Error(picture="https://images5.fanpop.com/image/photos/28100000/I-dunno-lol-random-28130691-500-412.jpg", message="Unable to create appointment in database")

    def delete_appointment(self, appointment_id: int) -> Union[dict, Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=dict_row) as db:
                    db.execute(
                        """
                        DELETE FROM appointments
                        WHERE id = %s
                        RETURNING *;
                        """,
                        [appointment_id]
                    )
                    record = db.fetchone()
                    if record is None:
                        return Error(picture="https://skrift.io/media/3cdf1cxr/missing-files.jpg", message="There is no appointment with that ID")
                    return {"message": "Appointment deleted successfully"}
        except Exception as error:
            print(error)
            return Error(picture="https://images5.fanpop.com/image/photos/28100000/I-dunno-lol-random-28130691-500-412.jpg", message="Unable to delete appointment from database")
