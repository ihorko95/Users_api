import databases, sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = 'postgresql://manager:manager@localhost:5432/dbusers'
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    'users',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.String, primary_key=True),
    sqlalchemy.Column('name', sqlalchemy.String),
    sqlalchemy.Column('email', sqlalchemy.String, unique=True),
    sqlalchemy.Column('password', sqlalchemy.String),
    sqlalchemy.Column('register_date', sqlalchemy.String),
)
engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)
Base = declarative_base()
