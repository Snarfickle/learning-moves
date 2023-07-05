from pydantic import BaseModel
from typing import Optional, List, Union
from queries.pool import pool
from psycopg.rows import dict_row

class Error(BaseModel):
    message: str
    picture: Optional[str]

class ResourceIn(BaseModel):
    name: str
    description: Optional[str] = None
    course_id: int
    material_id: int


class ResourceOut(ResourceIn):
    id: int


class ResourceRepo(BaseModel):
    def get_one(self, resource_id: int) -> Union[ResourceOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    SELECT *
                    FROM resources
                    WHERE id = %s
                    """,
                    [resource_id],
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No resource found with this ID."}
                return ResourceOut(**record)

    def create_resource(self, resource: ResourceIn) -> Union[ResourceOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    INSERT INTO resources (name, description, course_id, material_id)
                    VALUES (%s, %s, %s, %s)
                    RETURNING *;
                    """,
                    [resource.name, resource.description, resource.course_id, resource.material_id]
                )
                record = db.fetchone()
                return ResourceOut(**record)

    def get_all_resources(self) -> Union[List[ResourceOut], dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    SELECT *
                    FROM resources
                    """
                )
                records = db.fetchall()
                return [ResourceOut(**record) for record in records]

    def update_resource(self, resource_id: int, resource: ResourceIn) -> Union[ResourceOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    UPDATE resources
                    SET name = %s,
                        description = %s,
                        course_id = %s,
                        material_id = %s
                    WHERE id = %s
                    RETURNING *;
                    """,
                    [resource.name, resource.description, resource.course_id, resource.material_id, resource_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No resource found with this ID."}
                return ResourceOut(**record)

    def delete_resource(self, resource_id: int) -> dict:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    DELETE FROM resources
                    WHERE id = %s
                    RETURNING *;
                    """,
                    [resource_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No resource found with this ID."}
                return {"message": "Resource deleted successfully"}
