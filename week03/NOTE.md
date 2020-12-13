# 学习笔记
## SQL 语法以及 MySQL 数据库的安装和配置
企业级MySQL的Linux环境部署：
注意操作系统的平台：32位、64位
注意安装的MySQL版本：MySQL企业版、社区版、MariaDB
注意安装后避免yum/apt自动更新
注意数据库安全性

## 安装MySQL-Community-Server
### 查看系统架构
```
arch
cat /etc/redhat-release
```
下载MySQL的rpm安装包并安装
```
yum install *.rpm
rpm -qa |grep -i 'mysql'
```

> mysql 5.7 初始化的root密码在/var/log/mysqld.log
> 初次登录后需要修改，否则无法进行其他操作
``` SQL
# revise password
ALTER USER 'root'@'localhost' IDENTIFIED BY 'xxxxxx';
FLUSH PRIVILEGES;

# check variable
SHOW VARIABLES like '%character%';
# 查看校对规则
SHOW VARIABLES like '%collation_%';

# check create databases
SHOW CREATE DATABASE db1;
```
## 详解开发中涉及到的字符集问题
- MySQL中的utf8不是UTF-8字符集
- utf8只支持三个字节字符，而汉字需要占用四个字节
- UTF-8支持四子节字符，在mysql中表示位utf8mb4
- MySQL校对规则是用于字符比较和排序的一套规则
- collation中规则如果是_ci结尾，表示大小写不敏感；如果是_cs结尾，表示大小写敏感
``` SQL
character_set_client        # 客户端连接MySQL使用的字符集
character_set_connection    # 应用连接MySQL使用的字符集
character_set_database      # 当前选中的数据库使用的字符集
character_set_filesystem    # 
character_set_results       # 显示查询结果时使用的字符集
character_set_server        # MySQL内部默认操作的字符集
character_set_system        # MySQL中字段名称使用的字符集
character_sets_dir          # 
```

## 多种方式连接MySQL
注意：
- MySQLdb是python2的依赖包，适用于MySQL5.5和python2.7
- python3安装的MySQLdb包叫做mysqlclient，但是加载仍旧使用 `import MySQLdb` 
- DB API: pymysql, mysql-connector-python --> 面向过程; ORM: sqlalchemy
- 使用ORM方式和数据库交互有四个要求
    - 创建的base实例必须继承自sqlalchemy.ext.declarative.declarative_base()
    - 创建表时可以通过class，但是必须包括表名称  __tablename__=xxx 
    - 表中必须包含至少一个属性，即需要包含至少一个 Column 
    - 表中至少包含一个主键

## 必要的SQL知识
SQL语言按照功能划分:
- DQL：Data Query Language，数据查询语言，开发工程师学习的重点
- DDL：Data Definition Language，数据定义语言，操作库和表结构
- DML：Data Manipulation Language，数据操作语言，操作表中记录
- DCL：Data Control Language，数据控制语言，安全和访问权限控制

创建表需要注意的问题
- 创建的表之前是否存在
- 反引号避免有字段使用单引号/双引号
- 定义字符集和校对规则
- 创建数据表的数量越少越好
- 字段越少越好，越简单越好
- 表的联合主键越少越好
- 在数据量较小且性能要求不高的情况下可以使用foriegn key，对外的系统foriegn key要在应用层处理

SELECT查询时关键字的顺序
``` SQL
SELECT...FROM...WHERE...GROUP BY...HAVING...ORDERED BY...LIMIT
```
生产环境因为列数较多，一般禁用SELECT *
WHERE字段避免全表扫描，一般需要增加索引
``` SQL
SELECT DISTINCT book_id, book_name, count(*) as number   # 5
FROM book JOIN author ON book.sn_id = author.sn_id       # 1
WHERE pages > 500                                        # 2
GROUP BY book.book_id                                    # 3
HAVING number > 10                                       # 4
ORDER BY number                                          # 6
LIMIT 5                                                  # 7
```

## MySQL的聚合函数
SQL的函数分类：算数函数、字符串函数、日期函数、转换函数、聚合函数
聚合函数
- COUNT()     计算行数
- MAX()          最大值
- MIN()           最小值
- SUM()          求和
- AVG()           平均值
聚合函数忽略空行
对一组数据进行汇总，输入是一组数据，输出是单个值
WHERE 过滤数据仅作用于表的每一行，在使用 GROUP BY 后再使用 HAVING 过滤时是作用于所分的组

## 子查询和join关键字解析
子查询：需要从查询结果中再次进行查询，才能得到想要的结果
子查询要关注的问题：
关联子查询和非子查询的区别
 
关联子查询何时使用IN，何时使用EXISTS
小表驱动大表

## 事务的特性和隔离级别
事务的特点：要么全执行，要么不执行
事务的特性——ACID
- Atomicity：原子性，指不可分割的
- Consistency：一致性，事务从一种一致的状态，变为另一种一致的状态
- Isolation：隔离性，每个事务彼此间是独立的
- Durablity：持久性，事务提交后数据修改是持久的

事务的隔离级别：
- 读未提交：允许读到未提交的数据
- 读已提交：只能读到已提交的内容
- 可重复读：同一事务在相同查询条件下两次查询结果数据一致
- 可串行化：事务进行串行化，但是牺牲了并发的性能
- 隔离级别越高，数据共享性越低，可并发性就越低

使用 PyMySQL 进行数据库的连接、库表操作、事务与异常处理等
- INSERT
- SELECT
- UPDATE
- DELETE

## 多文件插入MySQL && 如何设计一个良好的数据库连接配置文件
- executemany 可用于更新多条MySQL记录
- ini文件可以包括多个section，每个section中用 key = value 配置参数
- ini配置文件的设计
    - 可读性
    - 配置简单明确
    - 适用于单机应用

## 使用SQLAlchemy与MySQL交互
ORM好处：
- 数据分层，业务逻辑层(class)、持久层(ORM)和数据库层，让开发仅需要关注业务逻辑

ORM缺点：
- 需要把定义好的类实例化，需要把session功能转换为SQL，存在性能损耗
- ORM抽象出来的功能不能完全覆盖所有的SQL





