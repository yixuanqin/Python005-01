# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

# class DoubanmoviePipeline:
#     # 每一个item管道组件都会调用该方法，并且必须返回一个item对象实例或raise DropItem异常
#     def process_item(self, item, spider):
#         author = item.get("author", "N/A")
#         rate = item.get("rate", "N/A")
#         content = item.get("content", "N/A")
#         date = item.get("date", "N/A")
#         output = f'|{author}|\t|{content}|\t|{rate}|\t|{date}|\n\n'
#         with open('./doubanmovie.txt', 'a+', encoding='utf-8') as article:
#             article.write(output)
#         return item


class DoubanMySQLPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host = "127.0.0.1", port = 3307, user = "test_user", passwd = "testpasswd", db = "movie_review", charset = "utf8")
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        author = item.get("author", "N/A")
        rate = item.get("rate", "N/A")
        content = item.get("content", "N/A")
        date = item.get("date", "N/A")
        sql = "INSERT INTO the_call(author, rate, content, date) VALUES (%s, %s, %s, %s)"
        self.cur.execute(sql, (author, rate, content, date))
        self.conn.commit()
    
    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
