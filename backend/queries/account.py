from pydantic import BaseModel, EmailStr
from typing import Optional, Union
from queries.pool import pool
from psycopg.rows import dict_row
from jwtdown_fastapi.authentication import Token
from .profile import ProfileOut

class Error(BaseModel):
    message: str

class AccountIn(BaseModel):
    username: str
    email: EmailStr
    password: str

class AccountOut(BaseModel):
    id: int
    username: str
    email: EmailStr

class AccountOutWithPassword(AccountOut):
    password: str

class AccountRepo:
    def create_account(self, account: AccountIn) -> Union[AccountOut, Error]:
        try:
            with pool.connection() as conn:
                # Turn off auto commit to start a transaction block
                conn.autocommit = False
                with conn.cursor(row_factory=dict_row) as db:
                    db.execute(
                        """
                        INSERT INTO accounts (username, email, password)
                        VALUES (%s, %s, %s)
                        RETURNING *;
                        """,
                        [account.username, account.email, account.password]
                    )
                    account_record = db.fetchone()

                    # Create a new profile linked to the new account
                    db.execute(
                        """
                        INSERT INTO profile (account_id, email)
                        VALUES (%s, %s)
                        RETURNING *;
                        """,
                        [account_record['id'], account.email]
                    )
                    profile_record = db.fetchone()

                    # If no errors occurred, commit the transaction
                    conn.commit()

                    # Return both the account and profile information
                    return {
                        'account': AccountOut(**account_record),
                        'profile': ProfileOut(**profile_record)
                    }
        except Exception as error:
            # If an error occurred, rollback the transaction
            conn.rollback()
            print(error)
            return Error(message="Unable to create account in database")
        finally:
            # Always ensure the connection is closed or returned to the connection pool
            conn.close()

    async def get_account(self, account_id: int) -> Union[AccountOut, Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=dict_row) as db:
                    db.execute(
                        """
                        SELECT * FROM accounts
                        WHERE id = %s;
                        """,
                        [account_id]
                    )
                    account_record = db.fetchone()
                    
                    if not account_record:
                        return Error(message="Account not found")

                    return AccountOut(**account_record)

        except Exception as error:
            print(error)
            return Error(message="Unable to get account ID from database")

    async def get_account_by_username(self, username: str) -> Union[AccountOutWithPassword, Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=dict_row) as db:
                    db.execute(
                        """
                        SELECT * FROM accounts
                        WHERE username = %s;
                        """,
                        [username]
                    )
                    account_record = db.fetchone()
                    
                    if not account_record:
                        return Error(message="Account not found here")

                    return AccountOutWithPassword(**account_record)

        except Exception as error:
            print(error)
            return Error(message="Unable to get account username from database")
    
    async def authenticate_user(self, username: str, password: str) -> Union[AccountOutWithPassword, Error]:
        account = await self.get_account_by_username(username)
        if isinstance(account, Error):
            return account
        if account.password != password:
            return Error(message="Incorrect password")
        return account

    def update_account(self, account_id: int, account: AccountIn) -> Union[AccountOut, Error]:
        pass
        # Similar to update_profile in ProfileRepo, but for accounts

    def delete_account(self, account_id: int) -> Union[dict, Error]:
        pass
        # Similar to delete_profile in ProfileRepo, but for accounts
