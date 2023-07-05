from fastapi import (
    APIRouter, 
    Depends, 
    HTTPException, 
    status, 
    Response, 
    Request)
from typing import Union
from pydantic import BaseModel
from jwtdown_fastapi.authentication import Token
from authenticator import authenticator
from queries.account import ( 
    AccountIn, 
    AccountOut, 
    AccountRepo)
from queries.profile import (
    ProfileOut,
    ProfileRepo
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
        print("Account under router create: ", account)
    except Exception as e:
        print("error:", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot create an account with those credentials",
        )
    form = AccountForm(username=account_info.username, password=plain_password, email=account_info.email)
    token = await authenticator.login(response, request, form, accountsRepo)
    return AccountToken(account=account['account'], **token.dict())

@router.get("/token", response_model=Union[AccountToken, None])
async def get_token(
    request: Request,
    account: AccountOut = Depends(authenticator.try_get_current_account_data),
    profileRepo: AccountRepo = Depends(),
) -> Union[AccountToken, None]:
    if account and authenticator.cookie_name in request.cookies:
        print(account)
        accountFromDB = profileRepo.get_one(account["id"])
        return {
            "access_token": request.cookies[authenticator.cookie_name],
            "type": "Bearer",
            "account": accountFromDB,
        }
