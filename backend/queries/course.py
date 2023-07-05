from pydantic import BaseModel
from typing import Optional, List, Union
from queries.pool import pool
from psycopg.rows import dict_row

class Error(BaseModel):
    message: str
    picture: Optional[str]

class CourseIn(BaseModel):
    title: str
    description: Optional[str] = None
    instructor_id: int
    cost: float
    duration: str
    materials: Optional[str] = None


class CourseOut(CourseIn):
    id: int


class CourseRepo(BaseModel):
    def get_one(self, course_id: int) -> Union[CourseOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    SELECT *
                    FROM course
                    WHERE id = %s
                    """,
                    [course_id],
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No course found with this ID."}
                return CourseOut(**record)

    def create_course(self, course: CourseIn) -> Union[CourseOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    INSERT INTO course (title, description, instructor_id, cost, duration, materials)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING *;
                    """,
                    [course.title, course.description, course.instructor_id, course.cost, course.duration, course.materials]
                )
                record = db.fetchone()
                return CourseOut(**record)

    def get_all_courses(self) -> Union[List[CourseOut], dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    SELECT *
                    FROM course
                    """
                )
                records = db.fetchall()
                return [CourseOut(**record) for record in records]

    def update_course(self, course_id: int, course: CourseIn) -> Union[CourseOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    UPDATE course
                    SET title = %s,
                        description = %s,
                        instructor_id = %s,
                        cost = %s,
                        duration = %s,
                        materials = %s
                    WHERE id = %s
                    RETURNING *;
                    """,
                    [course.title, course.description, course.instructor_id, course.cost, course.duration, course.materials, course_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No course found with this ID."}
                return CourseOut(**record)

    def delete_course(self, course_id: int) -> dict:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    DELETE FROM course
                    WHERE id = %s
                    RETURNING *;
                    """,
                    [course_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No course found with this ID."}
                return {"message": "Course deleted successfully"}
