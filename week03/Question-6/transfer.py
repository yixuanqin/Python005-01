#!/usr/bin/python3
from configparser import ConfigParser
from datetime import datetime 
import pymysql
from sqlalchemy import Date, DateTime, create_engine, DECIMAL, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
import sys

Base = declarative_base()
# Create table class
class User_table(Base):
    __tablename__ = 'user'
    user_id = Column(Integer(), primary_key = True, nullable = False, autoincrement = True)
    username = Column(String(15), nullable = False, unique = True)
    created_on = Column(DateTime(), default = datetime.now)
    
    def __repr__(self):
        return "user(user_id = '{self.user_id}', " \
            "username = '{self.username}', " \
            "created_on = {self.created_on})".format(self = self)

class Account_table(Base):
    __tablename__ = 'account'
    account_id = Column(Integer(), primary_key = True, nullable = False, autoincrement = True)
    user_id = Column(Integer(), nullable = False)
    total_amount = Column(DECIMAL(20,3), nullable = False)
    created_on = Column(DateTime(), default = datetime.now)
    updated_on = Column(DateTime(), default = datetime.now,
                        onupdate = datetime.now)
    
    def __repr__(self):
        return "account(account_id = '{self.account_id}', " \
            "total_amount = '{self.total_amount}', " \
            "updated_on = {self.updated_on})".format(self=self)

class Transfer_table(Base):
    __tablename__ = 'transfer'
    record_id = Column(Integer(), primary_key = True, nullable = False, autoincrement = True)
    transfer_id = Column(Integer(), nullable = False)
    receive_id = Column(Integer(), nullable = False)
    amount = Column(DECIMAL(21,3), nullable = False)
    created_on = Column(DateTime(), default = datetime.now)
    
    def __repr__(self):
        return "transfer(id='{self.id}', " \
            "transfer_id = '{self.transfer_id}', " \
            "receive_id = '{self.receive_id}', " \
            "amount = '{self.amount}', " \
            "created_on = {self.created_on})".format(self=self)

class TransferApp:
    def __init__(self, config_path, section):
        self.config_path = config_path
        self.section = section
        self.db_config = self.load_config()
        self.engine = self.init_connection()
        self.session = self.init_session()
    
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
        engine = create_engine(dburl, echo = False, encoding = "utf-8")
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

    def create_user(self, username, init_amount):
        if init_amount < 0:
            sys.exit("初始余额需要大于0, 当前提供的初始值为: {}".format(init_amount))
        session = self.init_session()
        try:
            user_record = session.query(User_table).filter(User_table.username == username).first()
            if not user_record:
                new_user = User_table(username = username)
                session.add(new_user)
                session.commit()
                print("创建用户: {}".format(username))
            else:
                print("用户: {} 已存在, 无需再次创建".format(username))
            user_record = session.query(User_table).filter(User_table.username == username).first()
            user_id = user_record.user_id
            account_record = session.query(Account_table).filter(Account_table.user_id == user_id).first()
            if not account_record:
                new_account = Account_table(user_id = user_id, total_amount = init_amount)
                session.add(new_account)
                session.commit()
                print("创建账户: {}, 初始余额为: {}".format(username, init_amount))
            else:
                print("账户: {}, ID: {} 已存在, 无需再次创建".format(username, account_record.account_id))
        except Exception as e:
                session.rollback()
                print(e)
        finally:
            if not session:
                session.close()

    def create_transfer_record(self, transfer_id, receive_id, amount):
        session = self.init_session()
        try:
            new_transfer_record = Transfer_table(
                            transfer_id = transfer_id,
                            receive_id = receive_id,
                            amount = amount)
            session.add(new_transfer_record)
            session.commit()
            print("已新增转账记录—— transfer_id: {}, receive_id: {}, amount: {}".format(transfer_id, receive_id, amount))
        except Exception as e:
            session.rollback()
            print(e)
        finally:
            if not session:
                session.close()
        
    def query_user(self, username):
        session = self.init_session()
        try:
            result = session.query(User_table).filter(User_table.username == username).first()
            if result:
                print("用户信息: {}".format(result))
                account_result = session.query(Account_table).filter(Account_table.user_id == result.user_id).first()
                print("账户信息: {}".format(account_result))
            else:
                print("用户 {} 不存在, 查询失败".format(username))
        except Exception as e:
            print(e)
        finally:
            if not session:
                session.close()

    def modify_account(self, username, amount):
        session = self.init_session()
        try:
            result = session.query(User_table).filter(User_table.username == username).first()
            if result:
                    account_query = session.query(Account_table.total_amount).filter(Account_table.user_id == result.user_id)
                    total_account = account_query[0].total_amount + amount
                    if total_account < 0:
                        print('{}账户中当前余额为: {}，无法提取: {}'.format(username, account_query[0].total_amount, abs(amount)))
                        return False
                    account_query.update({Account_table.total_amount: total_account})
                    session.commit()
                    if amount >= 0:
                        print("已经新增{}至{}的账户, 当前余额为: {}".format(amount, username, total_account))
                    else:
                        print("已经从{}的账户提取{}, 当前余额为: {}".format(username, abs(amount), total_account))
                    return True
            else:
                print("用户 {} 不存在, 请先注册账户".format(username))
                return False
        except Exception as e:
            session.rollback()
            print(e)
            return False
        finally:
            if not session:
                session.close()

    def transfer_account(self, from_user, to_user, amount):
        # 禁止给自己转账
        if from_user == to_user:
            print("不能转账给自己!")
            return False
        # 转账金额应该大于0
        if amount <= 0:
            print("转账金额要大于0: {}".format(amount))
            return False
        session = self.init_session()
        try:
            # session.begin(subtransactions = True)
            from_user_record = session.query(User_table).filter(User_table.username == from_user).first()
            # 检查转账用户是否存在
            if not from_user_record:
                print("转账用户不存在: {}".format(from_user))
                return False
            to_user_record = session.query(User_table).filter(User_table.username == to_user).first()
            # 检查接收用户是否存在
            if not to_user_record:
                print("接收用户不存在: {}".format(to_user))
                return False
            # 进行账户金额增减
            transfer_result = self.modify_account(from_user, -amount)
            if transfer_result:
                receive_result = self.modify_account(to_user, amount)
                # 新增转账记录
                if receive_result:
                    self.create_transfer_record(from_user_record.user_id, to_user_record.user_id, amount)
        except Exception as e:
            session.rollback()
            print(e)
        finally:
            if not session:
                session.close()
        

if __name__ == "__main__":
    config_path = "./mysql.ini"
    section = "default"
    # Create instance
    transfer_ins = TransferApp(config_path, section)
    # Create database
    transfer_ins.create_table()
    # Create new account
    transfer_ins.create_user('张三', 2000)
    transfer_ins.create_user('李四', 1000)
    # Query user
    transfer_ins.query_user('张三')
    transfer_ins.query_user('李四')
    # Transfer
    transfer_ins.transfer_account('张三', '李四', 100)
    # transfer_ins.transfer_account('李四', '张三', 100)
