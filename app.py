import sqlalchemy as db
from dotenv import load_dotenv, find_dotenv
import os
import pymysql
"""
tutorial : https://towardsdatascience.com/sqlalchemy-python-tutorial-79a577141a91
"""
load_dotenv(find_dotenv())
db_options = "mysql+pymysql://{user}:{pwd}@{ip}/{db}".format(
    user=os.getenv("USER"),
    pwd=os.getenv("PASSWORD"),
    ip=os.getenv("IP"),
    db=os.getenv("DB"),
)

engine = db.create_engine(db_options)
connection = engine.connect()
metadata = db.MetaData()
# 데이터베이스 생성
"""
engine.execute("CREATE DATABASE IF NOT EXISTS {db};".format(db="test_db"))
"""
# 1. create table
"""
emp = db.Table('test_emp', metadata,
               db.Column('Id', db.Integer()),
               db.Column('name', db.String(255), nullable=False),
               db.Column('salary', db.Float(), default=100.0),
               db.Column('active', db.Boolean(), default=True)
               )

metadata.create_all(engine)
"""
# 2. viewing table details
"""
test_emp = db.Table('test_emp', metadata, autoload=True, autoload_with=engine)
"""

#   2-1. Print the column names
"""
print(test_emp.columns.keys())
"""

# 2-2. Print full table metadata
"""
print(repr(metadata.tables['census']))
"""

# 3. inserting data

"""
query = db.insert(emp).values(Id=1, name='naveen', salary=60000.00, active=True)
ResultProxy = connection.execute(query)
"""


#   3-1. Inserting many records at ones

"""
query = db.insert(emp)
values_list = [{'Id':'2', 'name':'ram', 'salary':80000, 'active':False},
               {'Id':'3', 'name':'ramesh', 'salary':70000, 'active':True}]
ResultProxy = connection.execute(query,values_list)
"""

# 4. querying
#    ResultProxy : .excute()가 리턴하는 객체. 다양한 방법으로 데이터를 가져올 수 있다.
#    ResultSet   : ResultProxy의 .fetchall()같은 패치 메서드가 리턴하는 실제 데이터.

"""
test_emp = db.Table('test_emp', metadata, autoload=True, autoload_with=engine)

query = db.select([test_emp])
ResultProxy = connection.execute(query)
ResultSet = ResultProxy.fetchall()
print(ResultSet[:3])
"""
# 4-1. filtering data
test_emp = db.Table('test_emp', metadata, autoload=True, autoload_with=engine)

#   4-1-1. where
query = db.select([test_emp]).where(test_emp.columns.name=='naveen')
ResultProxy = connection.execute(query)
ResultSet = ResultProxy.fetchall()
print(ResultSet)

#   4-1-2. in
query = db.select([test_emp]).where(test_emp.columns.name.in_(['naveen', 'ram']))
ResultProxy = connection.execute(query)
ResultSet = ResultProxy.fetchall()
print(ResultSet)

#   4-1-3. and, or, net
query = db.select([test_emp]).where(
    db.and_(test_emp.columns.name == 'ram',
            test_emp.columns.active != 1
            )
)
ResultProxy = connection.execute(query)
ResultSet = ResultProxy.fetchall()
print(ResultSet)

#   4-1-4. order by
query = db.select([test_emp]).order_by(db.desc(test_emp.columns.salary), db.desc(test_emp.columns.Id))
ResultProxy = connection.execute(query)
print(ResultSet)
ResultSet = ResultProxy.fetchall()

#   4-1-5. functions
query = db.select([db.func.sum(test_emp.columns.salary)])
ResultProxy = connection.execute(query)
ResultSet = ResultProxy.fetchall()
print(ResultSet)

#   4-1-6. group by
query = db.select([db.func.sum(test_emp.columns.salary).label('salary_t'), test_emp.columns.active])\
    .group_by(test_emp.columns.active)
ResultProxy = connection.execute(query)
ResultSet = ResultProxy.fetchall()
print(ResultSet)

#   4-1-7. distinct
query = db.select([test_emp.columns.active.distinct()])
ResultProxy = connection.execute(query)
ResultSet = ResultProxy.fetchall()
print(ResultSet)
