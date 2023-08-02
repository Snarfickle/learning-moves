from fastapi import (
    APIRouter, 
    Depends, 
    HTTPException, 
    status, 
    Response, 
    Request)
from typing import Union, List, Dict
from pydantic import BaseModel
from jwtdown_fastapi.authentication import Token
from authenticator import authenticator
from queries.account import ( 
    AccountIn, 
    AccountOut, 
    AccountRepo,
)


class AccountForm(BaseModel):
    username: str
    email: str
    password: str

class AccountToken(Token):
    account: AccountOut

class HttpError(BaseModel):
    detail: str


router = APIRouter()

@router.post("/accounts", response_model=Union[AccountToken, None])
async def create_account(
    account_info: AccountIn,
    request: Request,
    response: Response,
    accountsRepo: AccountRepo = Depends(),
):
    plain_password = account_info.password
    hashed_password = authenticator.hash_password(account_info.password)

    try:
        account_info.password = hashed_password
        account = accountsRepo.create_account(account_info)
    except Exception as e:
        print("error:", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot create an account with those credentials",
        )
    form = AccountForm(username=account_info.username, password=plain_password, email=account_info.email)
    token = await authenticator.login(response, request, form, accountsRepo)
    return AccountToken(account=account['account'], **token.dict())

@router.get("/accounts/", response_model=Union[AccountToken, None])
async def get_account_info(
    request: Request,
    account: AccountOut = Depends(authenticator.try_get_current_account_data),
    profileRepo: AccountRepo = Depends(),
    account_data: Dict = Depends(authenticator.get_current_account_data),
) -> Union[AccountToken, None]:
    if account and authenticator.cookie_name in request.cookies:
        accountFromDB = await profileRepo.get_account(account["id"])        
        access_token = request.cookies.get(authenticator.cookie_name)
        return AccountToken(account=accountFromDB, access_token=access_token)
    else:
        print("account: ", account)
        print("request: ", request)
        print("authenticator.cookie_name: ", authenticator.cookie_name)
        print("request.cookies: ", request.cookies)
        print("unable to provide the account data") 
