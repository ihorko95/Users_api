import psycopg2
import datetime
from passlib.hash import pbkdf2_sha256
from pg_database import DATABASE_URL

try:
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()

    postgres_insert_query = """ INSERT INTO users(id, name,email,password,register_date) VALUES (%s,%s,%s,%s,%s)"""
    ctime = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    for i in range(1, 4):
        values = (f'uuid4-user{i}', f'user{i}', f'user{i}@gmail.com', pbkdf2_sha256.hash(f'user{i}'), ctime)
        cursor.execute(postgres_insert_query, values)

    connection.commit()
    print("Records inserted successfully into users table")

except (Exception, psycopg2.Error) as error:
    print("Failed to insert record into users table", error)

finally:
    # closing database connection.
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
