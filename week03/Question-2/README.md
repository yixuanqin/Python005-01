2. 使用 sqlalchemy ORM 方式创建如下表，使用 PyMySQL 对该表写入 3 条测试数据，并读取:
    用户 id、用户名、年龄、生日、性别、学历、字段创建时间、字段更新时间
    将 ORM、插入、查询语句作为作业内容提交


本作业在`candidate.py`中，通过`class CandidateTable`实现
1. ORM
```
# 定义Table
Base = declarative_base()
class Candidate_table(Base):

# 定义CandidateTable这个类
class CandidateTable
# 创建Table
create_table
```

2. 插入
```
# 准备一个字典组成的列表，遍历列表的每一个字典，将字典内的值匹配到每个表的值后，插入表
insert_data(candidate_list)
```

3. 查询
```
# 查询表内数据
query_all_data()
```