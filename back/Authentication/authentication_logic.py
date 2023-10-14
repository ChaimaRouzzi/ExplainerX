from fastapi import APIRouter, Depends, HTTPException, status
import jwt
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from Data_Gathering.db_connection import connect_to_db
from fastapi.security import OAuth2PasswordBearer


SECRET_KEY = "cairocoders123456789"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 800

dummy_user = {
    "email": "cairocoders",
    "password": "123456ednalan",
}

login_router = APIRouter()


class Loginclass(BaseModel):
    email: str
    password: str
    role:str


@login_router.post("/authenticate")
async def login_user(login_item: Loginclass, connection=Depends(connect_to_db)):
    data = jsonable_encoder(login_item)

    query = "SELECT user_id, password, role, name FROM users WHERE email = $1"
    result = await connection.fetchrow(query, data['email'])

    if result and result['password'] == data['password'] and result['role']==data['role']:
        user_id = result['user_id']
        role = result['role']
        name = result['name']
        encoded_jwt = jwt.encode({"user_id": user_id}, SECRET_KEY, algorithm=ALGORITHM)
        return {'token': encoded_jwt, 'user_id': user_id, 'role': role, 'name': name}
    else:
        raise HTTPException(status_code=401, detail="Login failed")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_current_active_user(current_user: int = Depends(get_current_user)):
    return current_user
