from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv(".env")

import os

USER = os.getenv("db_ADMIN")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")


def create_mysql_engine(user, password, host, port, database):
    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{int(port)}/{database}")
    return engine


ENGINE = create_mysql_engine(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        database=DATABASE
    ) 
