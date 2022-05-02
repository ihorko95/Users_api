import datetime
import uuid
from fastapi import APIRouter, status
from users.schemas import UserList, User, UserUpdate, UserPut
from typing import List
from pg_database import users, database
from passlib.hash import pbkdf2_sha256

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
async def user_detail(userid: str):
    query = users.select().where(users.c.id == userid)
    return await database.fetch_one(query)


@router.post('/user', response_model=UserList, tags=["User"], status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    gen_ID = str(uuid.uuid4())
    ctime = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    query = users.insert().values(
        id=gen_ID,
        name=user.name,
        email=user.email,
        password=pbkdf2_sha256.hash(user.password),
        register_date=ctime
    )
    await database.execute(query)
    return {
        'id': gen_ID,
        **user.dict(),
        'register_date': ctime
    }


@router.put('/user/{userId}', response_model=UserPut, tags=["User"])
async def update_user(userid: str, user: UserUpdate):
    query = users.update().where(users.c.id == userid).values(
        id=userid,
        name=user.name if user.name else None,
        email=user.email if user.email else None,
        password=pbkdf2_sha256.hash(user.password) if user.password else None,
        register_date=user.register_date if user.register_date else None,
    )
    await database.execute(query)

    return await user_detail(userid)


@router.patch('/user/{userId}', response_model=UserUpdate, tags=["User"])
async def patch_user(userid: str, user: UserUpdate):
    query = users.update().where(users.c.id == userid).values(
        id=userid,
        name=user.name if user.name else users.c.name,
        email=user.email if user.email else users.c.email,
        password=pbkdf2_sha256.hash(user.password) if user.password else users.c.password,
        register_date=user.register_date if user.register_date else users.c.register_date,
    )
    await database.execute(query)

    return await user_detail(userid)


@router.delete("/user/{userId}", tags=["User"])
async def delete_user(userid: str):
    query = users.delete().where(users.c.id == userid)
    await database.execute(query)

    return {
        "status": True,
        "message": "User deleted successfully."
    }
