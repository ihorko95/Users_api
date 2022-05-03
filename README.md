# UsersListAPI
* FastAPI app;
* PostgreSQL integration using SQLAlchemy;
* Pipenv environment;
* Dockerfile and docker-compose integrations;
## How to start?
1. [download zip code](https://github.com/ihorko95/Users_api/archive/refs/heads/main.zip)  or clone the reposetory<br><br>
2. Launch docker-compose:
```bash
docker-compose up -d --build
```

3. Profit. Project is going to be available on http://0.0.0.0:8008 <br><br>
4. (*Manualy*) Add initial data to database:
   ```bash 
   docker exec -it userslist python pg_insertdata.py
   ```
#### Initialized table contains:  
| ID          | NAME  | EMAIL           | PASSWORD     |REG_DATE
|-------------|:-----:|:---------------:|:------------:|:----------:|
| uuid4-user1 | user1 | user1@gmail.com | `hash(user1)`|`date.now`
| uuid4-user2 | user2 | user2@gmail.com | `hash(user2)`|`date.now`
| uuid4-user3 | user3 | user3@gmail.com | `hash(user3)`|`date.now`
###### Column `ID` of initialized data, was not generated. It is for friendly using. Use `uuid4-user1` for  CRUD.