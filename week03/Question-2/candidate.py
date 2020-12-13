#!/usr/bin/python3
from configparser import ConfigParser
from datetime import datetime 
import pymysql
from sqlalchemy import Date, DateTime, create_engine, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sys

Base = declarative_base()
# Create candidate table class
class Candidate_table(Base):
    __tablename__ = 'candidate'
    user_id = Column(Integer(), primary_key = True)
    username = Column(String(15), nullable = False, unique = True)
    gender = Column(String(10), nullable = False)
    age = Column(Integer(), nullable = False)
    birthday = Column(Date(), nullable = False)
    edu_degree = Column(String(20), nullable = False)
    created_on = Column(DateTime(), default = datetime.now)
    updated_on = Column(DateTime(), default = datetime.now,
                        onupdate=datetime.now)
    def __repr__(self):
        return "Candidate_table(user_id = '{self.user_id}', " \
            "username = '{self.username}', " \
            "gender = '{self.gender}', " \
            "age = '{self.age}', " \
            "birthday = '{self.birthday}', " \
            "edu_degree = '{self.edu_degree}', " \
            "created_on = '{self.created_on}', " \
            "updated_on = '{self.updated_on})'".format(self = self)

class CandidateTable:
    def __init__(self, config_path, section):
        self.config_path = config_path
        self.section = section
        self.db_config = self.load_config()
        self.engine = self.init_connection()
    
    def load_config(self):
        # Read database config from config file
        try:
            config = ConfigParser(allow_no_value = False)
            config.read(self.config_path)
        except Exception as e:
            sys.exit(e)
        if config.has_section(self.section):
            items = config.items(self.section)
            return dict(items)
        else:
            raise Exception('{0} not found in the {1} file'.format(self.section, self.config_path))
    
    def init_connection(self):
        # Init a database connection
        dburl = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4".format(
                                                                    self.db_config['username'], 
                                                                    self.db_config['password'], 
                                                                    self.db_config['host'],
                                                                    self.db_config['port'],
                                                                    self.db_config['database'],
                                                                    )
        engine = create_engine(dburl, echo=True, encoding="utf-8")
        return engine

    def init_session(self):
        # Init a database session for query
        SessionClass = sessionmaker(bind = self.engine)
        session = SessionClass()
        return session
    
    def create_table(self):
        try:
            Base.metadata.create_all(self.engine)
        except Exception as e:
            sys.exit(e)

    def insert_data(self, candidate_list):
        session = self.init_session()
        # Insert data from list
        try:
            for candidate_info in candidate_list:
                # Insert only when username does not exist
                if not session.query(Candidate_table).filter(Candidate_table.username == candidate_info['username']):
                    candidate = Candidate_table(username = candidate_info['username'], 
                                                gender = candidate_info['gender'],
                                                age = candidate_info['age'],
                                                birthday = candidate_info['birthday'],
                                                edu_degree = candidate_info['edu_degree']
                                                )
                    session.add(candidate)
            session.commit()
            session.close()
        except Exception as e:
            sys.exit(e)
        

    def query_all_data(self):
        # Query 3 records
        session = self.init_session()
        try:
            for result in session.query(Candidate_table).limit(3):
                print(result)
            session.close()
        except Exception as e:
            sys.exit(e)



if __name__ == "__main__":
    config_path = "./mysql.ini"
    section = "default"
    # Create instance
    candidate_ins = CandidateTable(config_path, section)
    # Create Database
    candidate_ins.create_table()
    # Insert data
    candidate_list = []
    candidate_list.append({'username': 'Lily', 'gender': 'female', 'age': 25, 'birthday': '1995-08-15', 'edu_degree': 'master'})
    candidate_list.append({'username': 'Henry', 'gender': 'male', 'age': 26, 'birthday': '1994-12-20', 'edu_degree': 'phd'})
    candidate_list.append({'username': 'Yolanda', 'gender': 'female', 'age': 24, 'birthday': '1996-02-10', 'edu_degree': 'balcher'})
    candidate_ins.insert_data(candidate_list)
    # print(candidate_list)
    # Query all data
    candidate_ins.query_all_data()