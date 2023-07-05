from pydantic import BaseModel, EmailStr
from typing import Optional, List, Union
from enum import Enum
from queries.pool import pool
from psycopg.rows import dict_row


class Error(BaseModel):
    message: str
    picture: Optional[str]

class ProfileType(str, Enum):
    student = 'student'
    teacher = 'teacher'

class ProfileIn(BaseModel):
    account_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    type: Optional[str] = None
    phone_number: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    certificates: Optional[str] = None
    profile_picture: Optional[str] = None
    about_me: Optional[str] = None


class ProfileOut(ProfileIn):
    id: int

class ProfileRepo(BaseModel):
    def get_one(self, profile_id: int) -> Union[ProfileOut, Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=dict_row) as db:
                    db.execute(
                        """
                        SELECT *
                        FROM profile
                        WHERE id =%s
                        """,
                        [profile_id],
                    )
                    record = db.fetchone()
                    if record is None:
                        return Error(picture="https://skrift.io/media/3cdf1cxr/missing-files.jpg" ,message="There is no profile with that ID")
                    return ProfileOut(**record)
        except Exception as error:
            print(error)
            return Error( picture="https://images5.fanpop.com/image/photos/28100000/I-dunno-lol-random-28130691-500-412.jpg" ,message="unable to pull profile form database")
    
    def update_profile(self, profile_id: int, profile: ProfileIn) -> Union[ProfileOut, Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=dict_row) as db:
                    db.execute(
                        """
                        UPDATE profile
                        SET first_name = %s,
                            last_name = %s,
                            email = %s,
                            type = %s,
                            phone_number = %s,
                            city = %s,
                            state = %s,
                            certificates = %s,
                            profile_picture = %s,
                            about_me = %s
                        WHERE id = %s
                        RETURNING *;
                        """,
                        [profile.first_name, profile.last_name, profile.email, profile.type, profile.phone_number, 
                        profile.city, profile.state, profile.certificates, profile.profile_picture, profile.about_me, profile_id]
                    )
                    record = db.fetchone()
                    if record is None:
                        return Error(picture="https://skrift.io/media/3cdf1cxr/missing-files.jpg" ,message="There is no profile with that ID")
                    return ProfileOut(**record)
        except Exception as error:
            print(error)
            return Error(picture="https://images5.fanpop.com/image/photos/28100000/I-dunno-lol-random-28130691-500-412.jpg", message="Unable to update profile in database")
    
    def get_all_profiles(self) -> Union[List[ProfileOut], Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=dict_row) as db:
                    db.execute(
                        """
                        SELECT *
                        FROM profile
                        """
                    )
                    records = db.fetchall()
                    return [ProfileOut(**record) for record in records]
        except Exception as error:
            print(error)
            return Error(picture="https://images5.fanpop.com/image/photos/28100000/I-dunno-lol-random-28130691-500-412.jpg" ,message="Unable to fetch profiles from database")

    def create_profile(self, profile: ProfileIn) -> Union[ProfileOut, Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=dict_row) as db:
                    db.execute(
                        """
                        INSERT INTO profile (first_name, last_name, email, type, phone_number, city, state, certificates, profile_picture, about_me)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING *;
                        """,
                        [profile.first_name, profile.last_name, profile.email, profile.type, profile.phone_number, 
                         profile.city, profile.state, profile.certificates, profile.profile_picture, profile.about_me]
                    )
                    record = db.fetchone()
                    return ProfileOut(**record)
        except Exception as error:
            print(error)
            return Error(picture="https://images5.fanpop.com/image/photos/28100000/I-dunno-lol-random-28130691-500-412.jpg" ,message="Unable to create profile in database")

    def delete_profile(self, profile_id: int) -> Union[dict, Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=dict_row) as db:
                    db.execute(
                        """
                        DELETE FROM profile
                        WHERE id = %s
                        RETURNING *;
                        """,
                        [profile_id]
                    )
                    record = db.fetchone()
                    if record is None:
                        return Error(picture="https://skrift.io/media/3cdf1cxr/missing-files.jpg" ,message="There is no profile with that ID")
                    return {"message": "Profile deleted successfully"}
        except Exception as error:
            print(error)
            return Error(picture="https://images5.fanpop.com/image/photos/28100000/I-dunno-lol-random-28130691-500-412.jpg" ,message="Unable to delete profile from database")
