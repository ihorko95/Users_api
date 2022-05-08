import datetime
import uuid
from fastapi import APIRouter, Query, status, HTTPException
from users.schemas import pattern, UserList, User, UserUpdate, UserPut
from typing import List
from pg_database import users, database
from passlib.hash import pbkdf2_sha256


def password_hash(password: str) -> str:
    return pbkdf2_sha256.hash(password)[21:-1]


db = APIRouter()


@db.on_event("startup")
async def startup():
    await database.connect()


@db.on_event("shutdown")
async def shutdown():
    await database.disconnect()


router = APIRouter(
    prefix="/users",
)


@router.get('/user-list', response_model=List[UserList], tags=["User List"])
async def users_list():
    query = users.select()
    return await database.fetch_all(query)


@router.get("/user/{userId}", response_model=UserList, tags=["User"])
async def user_detail(userid: str =
                      Query(...,
                            regex=pattern['id'],
                            description="Enter user ID",
                            alias="ID"
                            )):
    query = users.select().where(users.c.id == userid)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404,
                            detail=[{"loc": ["string", 0], "msg": "User not found", "type": "ValueError"}])
    return {
        **dict(result.items())
    }


@router.post('/user', response_model=UserList, tags=["User"], status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    query = users.select()  # better select one field
    result = await database.fetch_all(query)
    for rec in result:
        if user.email == tuple(rec.values())[2]:
            raise HTTPException(status_code=409,
                                detail=[{"loc": ["string", 0], "msg": "Email is already exist.", "type": "ValueError"}])
    gen_ID = str(uuid.uuid4())
    ctime = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    query = users.insert().values(
        id=gen_ID,
        name=user.name,
        email=user.email,
        password=password_hash(user.password),
        register_date=ctime
    )
    await database.execute(query)
    return {
        'id': gen_ID,
        **user.dict(),
        'register_date': ctime
    }


@router.put('/user/{userId}', response_model=UserList, tags=["User"])
async def update_user(user: User, userid: str =
Query(...,
      regex=pattern['id'],
      description="Enter user ID",
      alias="ID"
      )):
    query = users.select()  # better select two fields
    result = await database.fetch_all(query)
    for rec in result:
        if user.email == tuple(rec.values())[2] and userid != tuple(rec.values())[0]:
            raise HTTPException(status_code=409,
                                detail=[{"loc": ["string", 0], "msg": "Email is already used.", "type": "ValueError"}])
    query = users.update().where(users.c.id == userid).values(
        id=userid,
        name=user.name,
        email=user.email,
        password=password_hash(user.password),
    )
    await database.execute(query)
    return await user_detail(userid)


@router.patch('/user/{userId}', response_model=UserUpdate, tags=["User"])
async def patch_user(user: UserUpdate, userid: str =
Query(...,
      regex=pattern['id'],
      description="Enter user ID",
      alias="ID"
      )):
    query = users.select()  # better select two fields
    result = await database.fetch_all(query)
    for rec in result:
        if user.email == tuple(rec.values())[2] and userid != tuple(rec.values())[0]:
            raise HTTPException(status_code=409,
                                detail=[{"loc": ["string", 0], "msg": "Email is already used.", "type": "ValueError"}])
    query = users.update().where(users.c.id == userid).values(
        id=userid,
        name=user.name if user.name else users.c.name,
        email=user.email if user.email else users.c.email,
        password=password_hash(user.password) if user.password else users.c.password,
        register_date=user.register_date if user.register_date else users.c.register_date,
    )
    await database.execute(query)

    return await user_detail(userid)


@router.delete("/user/{userId}", tags=["User"])
async def delete_user(userid: str =
                      Query(...,
                            regex=pattern['id'],
                            description="Enter user ID",
                            alias="ID"
                            )):
    query = users.select().where(users.c.id == userid)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404,
                            detail=[{"loc": ["string", 0], "msg": "User not found", "type": "ValueError"}])
    query = users.delete().where(users.c.id == userid)
    await database.execute(query)

    return {
        "status": True,
        "message": "User deleted successfully."
    }



async def create_user1(user: User):
    query = users.select()  # better select one field
    result = await database.fetch_all(query)
    for rec in result:
        if user.email == tuple(rec.values())[2]:
            raise HTTPException(status_code=409,
                                detail=[{"loc": ["string", 0], "msg": "Email is already exist.", "type": "ValueError"}])
    gen_ID = str(uuid.uuid4())
    ctime = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    query = users.insert().values(
        id=gen_ID,
        name=user.name,
        email=user.email,
        password=password_hash(user.password),
        register_date=ctime
    )
    await database.execute(query)
    return {
        'id': gen_ID,
        **user.dict(),
        'register_date': ctime
    }