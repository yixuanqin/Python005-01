5. 使用 MySQL 官方文档，学习通过 sql 语句为上题中的 id 和 name 增加索引，并验证。根据执行时间，增加索引以后是否查询速度会增加？请论述原因，并思考什么样的场景下增加索引才有效。

> 执行结果如下。对于本题中的表，执行结果显示增加索引后查询速度没有增加。每一个索引在InnoDB里面对应一棵B+树，而基于非主键索引的查询需要多扫描一棵索引树。根据下面explain运行的结果，本题中查询时使用了非主键索引，并且使用的表结构简单，数据量非常小，遍历索引的时间和直接查询表的时间没有区别。当表结构复杂且数据量很大的时候，增加索引能提升查询速度。

``` SQL
mysql> explain SELECT Table1_index.id, Table1_index.name, Table2_index.id, Table2_index.name FROM Table1_index INNER JOIN Table2_index ON Table1_index.id = Table2_index.id;
+----+-------------+--------------+------------+--------+----------------------------+----------------------+---------+------------------------+------+----------+-------------+
| id | select_type | table        | partitions | type   | possible_keys              | key                  | key_len | ref                    | rows | filtered | Extra       |
+----+-------------+--------------+------------+--------+----------------------------+----------------------+---------+------------------------+------+----------+-------------+
|  1 | SIMPLE      | Table1_index | NULL       | index  | PRIMARY,ix_Table1_index_id | ix_Table1_index_name | 203     | NULL                   |    2 |   100.00 | Using index |
|  1 | SIMPLE      | Table2_index | NULL       | eq_ref | PRIMARY,ix_Table2_index_id | PRIMARY              | 4       | testdb.Table1_index.id |    1 |   100.00 | NULL        |
+----+-------------+--------------+------------+--------+----------------------------+----------------------+---------+------------------------+------+----------+-------------+
2 rows in set, 1 warning (0.00 sec)
```

#### 添加索引的SQL语句
```
# Unique Index
ALTER TALBE 'Table1' ADD UNIQUE KEY('id')

# Primary Key Index
ALTER TABLE 'Table1' ADD PRIMARY KEY （'id')  

# Simple Index
ALTER TABLE 'Table1' ADD INDEX index_name('id') 

# Fulltext Index
ALTER TABLE 'Table1' ADD FULLTEXT ('id') 

```
#### 创建Table
``` SQL
mysql> SHOW CREATE TABLE Table1_index;
+--------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table        | Create Table                                                                                                                                                                                                                                                                                                           |
+--------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table1_index | CREATE TABLE `Table1_index` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_Table1_index_id` (`id`),
  KEY `ix_Table1_index_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci |
+--------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.01 sec)

mysql> SHOW CREATE TABLE Table2_index;
+--------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table        | Create Table                                                                                                                                                                                                                                                                                                           |
+--------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table2_index | CREATE TABLE `Table2_index` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_Table2_index_name` (`name`),
  KEY `ix_Table2_index_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci |
+--------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

#### INNER JOIN
``` SQL
mysql> SELECT Table1_index.id, Table1_index.name, Table2_index.id, Table2_index.name
    -> FROM Table1_index
    -> INNER JOIN Table2_index
    -> ON Table1_index.id = Table2_index.id;
+----+---------------+----+---------------+
| id | name          | id | name          |
+----+---------------+----+---------------+
|  1 | Table1_table2 |  1 | Table1_table2 |
+----+---------------+----+---------------+
1 row in set (0.00 sec)
```

#### LEFT JOIN
``` SQL
mysql> SELECT Table1_index.id, Table1_index.name, Table2_index.id, Table2_index.name
    -> FROM Table1_index
    -> LEFT JOIN Table2_index
    -> ON Table1_index.id = Table2_index.id;
+----+---------------+------+---------------+
| id | name          | id   | name          |
+----+---------------+------+---------------+
|  2 | Table1        | NULL | NULL          |
|  1 | Table1_table2 |    1 | Table1_table2 |
+----+---------------+------+---------------+
2 rows in set (0.00 sec)

```

#### RIGHT JOIN

``` SQL
mysql> SELECT Table1_index.id, Table1_index.name, Table2_index.id, Table2_index.name
    -> FROM Table1_index
    -> RIGHT JOIN Table2_index
    -> ON Table1_index.id = Table2_index.id;
+------+---------------+----+---------------+
| id   | name          | id | name          |
+------+---------------+----+---------------+
|    1 | Table1_table2 |  1 | Table1_table2 |
| NULL | NULL          |  3 | table2        |
+------+---------------+----+---------------+
2 rows in set (0.00 sec)

```