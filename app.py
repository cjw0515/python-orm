import sqlalchemy as db
from dotenv import load_dotenv, find_dotenv
import os
import pymysql

load_dotenv(find_dotenv())
db_options = "mysql+pymysql://{user}:{pwd}@{ip}/{db}".format(
    user=os.getenv("USER"),
    pwd=os.getenv("PASSWORD"),
    ip=os.getenv("IP"),
    db=os.getenv("DB"),
)

engine = db.create_engine(db_options)
metadata = db.MetaData
# connection = engine.connect()