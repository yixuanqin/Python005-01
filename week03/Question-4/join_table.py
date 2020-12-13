#!/usr/bin/python3
from configparser import ConfigParser
from datetime import datetime
import pymysql
from sqlalchemy import create_engine, DateTime, Table, Float, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sys

def load_config(config_path, section):
        # Read database config from config file
        try:
            config = ConfigParser(allow_no_value = False)
            config.read(config_path)
        except Exception as e:
            sys.exit(e)
        if config.has_section(section):
            items = config.items(section)
            return dict(items)
        else:
            raise Exception('{0} not found in the {1} file'.format(section, config_path))

Base = declarative_base()

class Test_table_1(Base):
    __tablename__ = 'Table1'
    id = Column(Integer(), primary_key=True)
    name = Column(String(50))
    # name = Column(String(50), index=True)

    def __repr__(self):
        return "Test_table_1(id='{self.id}', " \
            "name={self.name})".format(self=self)

class Test_table_2(Base):
    __tablename__ = 'Table2'
    id = Column(Integer(), primary_key=True)
    name = Column(String(50))
    # name = Column(String(50), index=True)

    def __repr__(self):
        return "Test_table_2(id='{self.id}', " \
            "name={self.name})".format(self=self)


config_path = "./mysql.ini"
section = "default"
db_config = load_config(config_path, section)
# Init a database connection
dburl = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4".format(
                                                            db_config['username'], 
                                                            db_config['password'], 
                                                            db_config['host'],
                                                            db_config['port'],
                                                            db_config['database'],
                                                            )
engine = create_engine(dburl, echo=True, encoding="utf-8")
Base.metadata.create_all(engine)

# 创建session
SessionClass = sessionmaker(bind=engine)
session = SessionClass()

# 给Table1增加数据
table_1_list = []
table_1_list.append(Test_table_1(name='table1_table2'))
table_1_list.append(Test_table_1(name='table1'))
for record in table_1_list:
        session.add(record)

# 给Table2增加数据
table_2_list = []
table_2_list.append(Test_table_2(name='table1_table2'))
table_2_list.append(Test_table_2(name='table2'))
table_2_list.append(Test_table_2(name='table2'))
for record in table_2_list:
    session.add(record)

# 删除Table2中不要的数据
query = session.query(Test_table_2)
query = query.filter(Test_table_2.id == 2)
# session.delete(query.one())
query.delete()

session.commit()
session.close()