from fastapi import  APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from  sqlalchemy.orm import  Session

from .. import  database, schemas, models, utils, auth2

router = APIRouter(
    prefix='/login', tags=['Authentication']
)

@router.post('/', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm =Depends(),db: Session = Depends(database.get_db)):
    userLogin = db.query(models.User).filter(
        models.User.email == user_credentials.username
    ).first()

    if not  userLogin:
        raise  HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")

    dbUtils = utils.verify(user_credentials.password, userLogin.password)

    if not dbUtils:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")

    #Create a token
    access_token = auth2.create_access_token(data = { 'user_id': userLogin.id})

    return  {"access_token" : access_token, "token_type": "bearer"}




