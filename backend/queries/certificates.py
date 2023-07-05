from pydantic import BaseModel
from typing import Optional, List, Union
from queries.pool import pool
from psycopg.rows import dict_row

class Error(BaseModel):
    message: str
    picture: Optional[str]

class CertificateIn(BaseModel):
    name: str
    description: Optional[str] = None
    course_id: int


class CertificateOut(CertificateIn):
    id: int


class CertificateRepo(BaseModel):
    def get_one(self, certificate_id: int) -> Union[CertificateOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    SELECT *
                    FROM certificates
                    WHERE id = %s
                    """,
                    [certificate_id],
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No certificate found with this ID."}
                return CertificateOut(**record)

    def create_certificate(self, certificate: CertificateIn) -> Union[CertificateOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    INSERT INTO certificates (name, description, course_id)
                    VALUES (%s, %s, %s)
                    RETURNING *;
                    """,
                    [certificate.name, certificate.description, certificate.course_id]
                )
                record = db.fetchone()
                return CertificateOut(**record)

    def get_all_certificates(self) -> Union[List[CertificateOut], dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    SELECT *
                    FROM certificates
                    """
                )
                records = db.fetchall()
                return [CertificateOut(**record) for record in records]

    def update_certificate(self, certificate_id: int, certificate: CertificateIn) -> Union[CertificateOut, dict]:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    UPDATE certificates
                    SET name = %s,
                        description = %s,
                        course_id = %s
                    WHERE id = %s
                    RETURNING *;
                    """,
                    [certificate.name, certificate.description, certificate.course_id, certificate_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No certificate found with this ID."}
                return CertificateOut(**record)

    def delete_certificate(self, certificate_id: int) -> dict:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as db:
                db.execute(
                    """
                    DELETE FROM certificates
                    WHERE id = %s
                    RETURNING *;
                    """,
                    [certificate_id]
                )
                record = db.fetchone()
                if record is None:
                    return {"error": "No certificate found with this ID."}
                return {"message": "Certificate deleted successfully"}
