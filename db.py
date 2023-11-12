
import psycopg2
import json
from psycopg2 import pool

# Load database credentials from the JSON file
with open('env/development.json') as config_file:
    config = json.load(config_file)

print("xxxxxxxxxxxxxxxxxxxxxxxxxxx >>>>>>>>>>>>>>>>>>>>>>>>> ", config)
# Create a connection pool
db_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,  # Minimum number of connections in the pool
    maxconn=10,  # Maximum number of connections in the pool
    database=config["services"]["pgsql"]["database"],
    user=config["services"]["pgsql"]["user"],
    password=config["services"]["pgsql"]["password"],
    host=config["services"]["pgsql"]["host"],
    port=config["services"]["pgsql"]["port"]
)

print("PGSQL Connected >>>>>>>>>>>>>>>>>>> xxxxxxxxxxxxxxx", db_pool)


def get_connection():
    return db_pool.getconn()


def close_connection(conn):
    db_pool.putconn(conn)
