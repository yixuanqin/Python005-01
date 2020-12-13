### 作业内容
1. 在 Linux 环境下，安装 MySQL5.6 以上版本，修改字符集为 UTF8mb4 并验证，新建一个数据库 testdb，并为该数据库增加远程访问的用户。
    将修改字符集的配置项、验证字符集的 SQL 语句作为作业内容提交
    将增加远程用户的 SQL 语句作为作业内容提交

#### 修改字符集的配置项
为了保证后续数据库的正常使用，需要永久修改配置项。
在MySQL配置文件`/etc/my.cnf`中新增下属配置段后重庆MySQL服务
```
[client]
default_character_set = utf8mb4

[mysql]
default_character_set = utf8mb4

[mysqld]
character_set_server = utf8mb4  
init_connect = 'SET NAMES utf8mb4' 
character_set_client_handshake = FALSE
collation_server = utf8mb4_unicode_ci
```
```
systemctl restart mysqld.service
```

#### 验证字符集的SQL语句
登录MySQL
```
mysql -uroot -p
```
登录后查询变量
``` SQL
mysql> SHOW VARIABLES LIKE '%character%';
+--------------------------------------+----------------------------+
| Variable_name                        | Value                      |
+--------------------------------------+----------------------------+
| character_set_client                 | utf8mb4                    |
| character_set_connection             | utf8mb4                    |
| character_set_database               | utf8mb4                    |
| character_set_filesystem             | binary                     |
| character_set_results                | utf8mb4                    |
| character_set_server                 | utf8mb4                    |
| character_set_system                 | utf8                       |
| character_sets_dir                   | /usr/share/mysql/charsets/ |
| validate_password_special_char_count | 1                          |
+--------------------------------------+----------------------------+
9 rows in set (0.01 sec)

mysql> SHOW VARIABLES LIKE '%collation%';
+----------------------+--------------------+
| Variable_name        | Value              |
+----------------------+--------------------+
| collation_connection | utf8mb4_unicode_ci |
| collation_database   | utf8mb4_unicode_ci |
| collation_server     | utf8mb4_unicode_ci |
+----------------------+--------------------+
3 rows in set (0.00 sec)

```

#### 创建testdb
登录MySQL
```
mysql -uroot -p
```
创建testdb
``` SQL
mysql> CREATE DATABASE testdb;
Query OK, 1 row affected (0.00 sec)

mysql> SHOW CREATE DATABASE testdb;
+----------+-----------------------------------------------------------------------------------------------+
| Database | Create Database                                                                               |+----------+-----------------------------------------------------------------------------------------------+
| testdb   | CREATE DATABASE `testdb` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */ |
+----------+-----------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)

```

#### 增加远程访问用户
登录MySQL
```
mysql -uroot -p
``` 
假设创建远程访问用户test_user, 密码为testpasswd，允许从任意IP访问，对testdb有所有的操作权限
``` SQL
mysql> SET GLOBAL validate_password_policy=LOW;
Query OK, 0 rows affected (0.00 sec)

mysql> CREATE USER 'test_user'@'%' IDENTIFIED BY 'testpasswd';
Query OK, 0 rows affected (0.01 sec)

mysql> GRANT ALL PRIVILEGES ON testdb.* TO  'test_user'@'%';
Query OK, 0 rows affected (0.00 sec)

mysql> FLUSH PRIVILEGES;
Query OK, 0 rows affected (0.00 sec)

mysql> SHOW GRANTS FOR 'test_user'@'%';
+-------------------------------------------------------+
| Grants for test_user@%                                |
+-------------------------------------------------------+
| GRANT USAGE ON *.* TO 'test_user'@'%'                 |
| GRANT ALL PRIVILEGES ON `testdb`.* TO 'test_user'@'%' |
+-------------------------------------------------------+
2 rows in set (0.00 sec)
```

使用test_user登录MySQL验证
```
mysql -utest_user -p
```

``` SQL
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| testdb             |
+--------------------+
2 rows in set (0.00 sec)
```