from pydantic import BaseModel
from typing import Optional, List, Union
from queries.pool import pool
from psycopg.rows import dict_row


class MaterialIn(BaseModel):
    name: str
    info: Optional[str] = None
    quantity: int
    cost: float
    free: bool
    owner_id: int


class MaterialOut(MaterialIn):
    id: int


class MaterialRepo(BaseModel):
    def get_one(self, material_id: int) -> Union[MaterialOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    SELECT *
                    FROM materials
                    WHERE id = %s
                    """,
                    [material_id],
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No material found with this ID."}
                return MaterialOut(**record)

    def create_material(self, material: MaterialIn) -> Union[MaterialOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    INSERT INTO materials (name, info, quantity, cost, free, owner_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING *;
                    """,
                    [material.name, material.info, material.quantity, material.cost, material.free, material.owner_id]
                )
                record = db.fetchone()
                return MaterialOut(**record)

    def get_all_materials(self) -> Union[List[MaterialOut], dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    SELECT *
                    FROM materials
                    """
                )
                records = db.fetchall()
                return [MaterialOut(**record) for record in records]

    def update_material(self, material_id: int, material: MaterialIn) -> Union[MaterialOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    UPDATE materials
                    SET name = %s,
                        info = %s,
                        quantity = %s,
                        cost = %s,
                        free = %s,
                        owner_id = %s
                    WHERE id = %s
                    RETURNING *;
                    """,
                    [material.name, material.info, material.quantity, material.cost, material.free, material.owner_id, material_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No material found with this ID."}
                return MaterialOut(**record)

    def delete_material(self, material_id: int) -> dict:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    DELETE FROM materials
                    WHERE id = %s
                    RETURNING *;
                    """,
                    [material_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No material found with this ID."}
                return {"message": "Material deleted successfully"}
