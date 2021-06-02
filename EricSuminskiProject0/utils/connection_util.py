from psycopg2 import connect, OperationalError
import os


def create_connection():
    try:
        conn = connect(
            host=os.environ.get('HOST'),
            database=os.environ.get('DB'),
            user=os.environ.get('DB_USERNAME'),
            password=os.environ.get('DB_PASSWORD'),
            port=os.environ.get('PORT')
        )
        return conn
    except OperationalError as e:
        print(e)

connection = create_connection()
print(connection)
# print()
# print(os.environ.get('HOST'))
# print()
# print(os.environ.get('DB'))
# print()
# print(os.environ.get('DB_USERNAME'))
# print()
# print(os.environ.get('DB_PASSWORD'))
# print()
# print(os.environ.get('PORT'))
