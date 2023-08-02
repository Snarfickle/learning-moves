import os
from fastapi import Depends
from jwtdown_fastapi.authentication import Authenticator
from queries.account import AccountRepo, AccountOut, AccountOutWithPassword
from datetime import timedelta




class MyAuthenticator(Authenticator):
    

    async def get_account_data(
        self,
        username: str,
        accounts: AccountRepo,
    ):
        # Use your repo to get the account based on the
        # username (which could be an email)
        return await accounts.get_account_by_username(username)

    def get_account_getter(
        self,
        accounts: AccountRepo = Depends(),
    ):
        # Return the accounts. That's it.
        return accounts

    def get_hashed_password(self, account: AccountOutWithPassword):
        # Return the encrypted password value from your
        # account object
        print("account for password:", account)
        return account.password

    def get_account_data_for_cookie(self, account: AccountOut):
        # Return the username and the data for the cookie.
        # You must return TWO values from this method.
        return account.username, AccountOut(**account.dict())


two_hours = timedelta(hours = 2)

authenticator = MyAuthenticator(
    os.environ["SIGNING_KEY"],
    exp=two_hours,)
