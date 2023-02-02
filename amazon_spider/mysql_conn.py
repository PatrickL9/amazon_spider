# -*- coding: UTF-8 -*-
#!/usr/bin/python3

import pymysql
from scrapy.utils.project import get_project_settings

class DoMysql:
    def __init__(self):
        settings = get_project_settings()
        # 有中文要存入数据库的话要加charset='utf8'
        self.conn = pymysql.connect(host=settings['MYSQL_HOST'], user=settings['MYSQL_USER'],
                                    passwd=settings['MYSQL_PASSWORD'], db=settings['MYSQL_DBNAME'],
                                    port=settings['MYSQL_PORT'], charset='utf8mb4')

        # 创建游标
        self.cursor = self.conn.cursor()

    # 返回单条数据
    def fetch_one(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    # 返回多条数据
    def fetch_chall(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def fetch_code(self):
        self.cursor.close()
        self.conn.close()

    # 判断是否有数据
    def row_count(self, sql):
        self.cursor.execute(sql)
        return self.cursor.rowcount
