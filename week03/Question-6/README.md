6. 张三给李四通过网银转账 100 极客币，现有数据库中三张表：

    一张为用户表，包含用户 ID 和用户名字
    另一张为用户资产表，包含用户 ID 用户总资产
    第三张表为审计用表，记录了转账时间，转账 id，被转账 id，转账金额

请合理设计三张表的字段类型和表结构；
请实现转账 100 极客币的 SQL(可以使用 pymysql 或 sqlalchemy-orm 实现)，张三余额不足，转账过程中数据库 crash 等情况需保证数据一致性。



### 三张表
``` SQL
+-------+-------------+
| Table | Create Table|
+-------+-------------+
| user  | CREATE TABLE `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(15) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_on` datetime DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci |
+-------+-------------+

+-------+-------------+
| Table | Create Table|
+-------+-------------+
| transfer | CREATE TABLE `transfer` (
  `record_id` int(11) NOT NULL AUTO_INCREMENT,
  `transfer_id` int(11) NOT NULL,
  `receive_id` int(11) NOT NULL,
  `amount` decimal(21,3) NOT NULL,
  `created_on` datetime DEFAULT NULL,
  PRIMARY KEY (`record_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci |
+-------+-------------+

+-------+-------------+
| Table | Create Table|
+-------+-------------+
| user  | CREATE TABLE `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(15) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_on` datetime DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci |
+-------+-------------+

```

### 转账函数
`transfer.py`中的`transfer_account`函数