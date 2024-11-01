"""The  three main components of JWT token is are: HEADER, PAYLOAD and SIGNATURE"""
from  jose import  JWSError, jwt
from datetime import  timedelta, datetime
from . import  schemas, database, models
from  fastapi import  Depends, status, HTTPException
from  fastapi.security import  OAuth2PasswordBearer
from sqlalchemy.orm import  Session
from .config import settings

#To generate a token we need
# 1. SECRETE_KEY
#2. ALGORITHM
#3  Expiration Time

# to get a string like this run:
# openssl rand - hex 32
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data: dict):
    encode_token = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encode_token.update({'exp': expire})

    encoded_jwt = jwt.encode(encode_token, SECRET_KEY, algorithm=ALGORITHM)
    return  encoded_jwt

def verify_access_token(token: str, credential_exception):
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if not  id:
            raise credential_exception

        token_data = schemas.TokenData(id = id)
    except Exception:
        raise  credential_exception

    return  token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db) ):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"could not validate credentials",
                                         headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credential_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user