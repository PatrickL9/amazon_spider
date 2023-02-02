# -*- coding: UTF-8 -*-
#!/usr/bin/python3

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import logging
import random
import time
import pymysql
from twisted.enterprise import adbapi
from scrapy.utils.project import get_project_settings

# item 保存到mysql
# 单线程插入mysql
class MysqlPipeline(object):
    """
    同步操作
    """
    def __init__(self):
        # 建立连接
        self.conn = pymysql.connect(host='localhost', user='root', passwd='cqmyglbX91',
                                    db='test', port=3306, charset='utf8mb4')  # 有中文要存入数据库的话要加charset='utf8'
        # 创建游标
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        # sql语句
        insert_sql = """
        insert into amazon_craw_asin_details(asin,asin_url,title,reviews,stars,rank1,
                cat1,rank2,cat2,first_available_date,qna,first_img,price_type,price,total_cat,
                critical_reviews,spider_time) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        # 执行插入数据到数据库操作
        self.cursor.execute(insert_sql, (item['asin'], item['asin_url'], item['title'], item['reviews'], item['stars'],
                            item['rank1'], item['cat1'], item['rank2'], item['cat2'], item['first_available_date'],
                            item['qna'],['first_img'], item['price_type'], item['price'], item['total_cat'],
                            item['critical_reviews'], item['spider_time']))
        # 提交，不进行提交无法保存到数据库
        self.conn.commit()

    def close_spider(self, spider):
        # 关闭游标和连接
        self.cursor.close()
        self.conn.close()

# 异步asyn进程插入mysql
class MysqlasynPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):  # 函数名固定，会被scrapy调用，直接可用settings的值
        """
        数据库建立连接
        :param settings: 配置参数
        :return: 实例化参数
        """
        adbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            charset='utf8mb4',
            port=3306,
            cursorclass=pymysql.cursors.DictCursor  # 指定cursor类型
        )
        # 连接数据池ConnectionPool，使用pymysql或者Mysqldb连接
        dbpool = adbapi.ConnectionPool('pymysql', **adbparams)
        # 返回实例化参数
        return cls(dbpool)

    def process_item(self, item, spider):
        """
        使用twisted将MySQL插入变成异步执行。通过连接池执行具体的sql操作，返回一个对象
        """
        query = self.dbpool.runInteraction(self.do_insert, item)  # 指定操作方法和操作数据
        # 添加异常处理
        query.addCallback(self.handle_error)  # 处理异常

    def do_insert(self, cursor, item):        # 对数据库进行插入操作，并不需要commit，twisted会自动commit
        settings = get_project_settings()
        adbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            charset='utf8mb4',
            port=3306,
            cursorclass=pymysql.cursors.DictCursor  # 指定cursor类型
        )
        # ping一下线程池的mysql库，如果ping不通，整个数据库连接池初始化一遍
        # 百度说mysql连接有效期是8个小时，所以每次插入需要测一下连接（ I doubt it ~~~ ）
        # 不过这里的数据库重新初始化的写法并不好，应该封装一下 by Patrick 20220513
        test_ping = cursor._connection._connection
        try:
            test_ping.ping()
        except:
            logging.warning("数据库ping不通，重新初始化mysql！")
            self.dbpool.close()
            self.dbpool = adbapi.ConnectionPool('pymysql', **adbparams)

        # 插入SQL并执行,twisted会自动commit
        insert_sql = """
        insert into amazon_craw_asin_details(asin,asin_url,title,reviews,stars,rank1,
                cat1,rank2,cat2,first_available_date,qna,first_img,price_type,price,total_cat,
                spider_time,country,store_name,is_fba,description,coupon) 
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
         """
        cursor.execute(insert_sql, (item['asin'], item['asin_url'], item['title'], item['reviews'], item['stars'],
                            item['rank1'], item['cat1'], item['rank2'], item['cat2'], item['first_available_date'],
                            item['qna'], item['first_img'], item['price_type'], item['price'], item['total_cat'],
                            item['spider_time'], item['station'], item['brand'], item['is_fba'],
                            item['description'], item['coupon'])
                       )
        print("数据已插入：" + str(item['asin']) + ": " + str(item['title']))
    def handle_error(self, failure):
        if failure:
            # 打印错误信息
            print(failure)


# item 保存到excel
class excelPipeline:
    def process_item(self, item, spider):
        filepath = 'D:/pythonProject/amazon_spider/结果.xlsx'
        # if os.path.exists(filepath) == False:
        #     os.mknod(filepath)
        with open(filepath, 'a',encoding='utf-8') as f:
            item['asin'] = item.get('asin')
            item['asin_url'] = item.get('asin_url')
            item['spider_time'] = item.get('spider_time')
            item['title'] = item.get('title')
            item['reviews'] = item.get('reviews')
            item['stars'] = item.get('stars')
            item['rank1'] = item.get('rank1')
            item['cat1'] = item.get('cat1')
            item['rank2'] = item.get('rank2')
            item['cat2'] = item.get('cat2')
            item['first_available_date'] = item.get('first_available_date')
            item['qna'] = item.get('qna')
            item['first_img'] = item.get('first_img')
            item['price_type'] = item.get('price_type')
            item['price'] = item.get('price')
            item['total_cat'] = item.get('total_cat')
            item['critical_reviews'] = item.get('critical_reviews')
            txt = str.format('{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n',
                             item['asin'], item['asin_url'],item['spider_time'], item['title'], item['reviews'],
                             item['stars'], item['rank1'], item['cat1'], item['rank2'],
                             item['cat2'], item['first_available_date'], item['qna'],
                             item['first_img'], item['price_type'], item['price'],
                             item['total_cat'], item['critical_reviews'])
            f.write(txt)
            return item

# class RandomDelayMiddleware(object):
#     def __init__(self, delay):
#         self.delay = delay
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         delay = crawler.spider.settings.get("RANDOM_DELAY", 10)
#         if not isinstance(delay, int):
#             raise ValueError("RANDOM_DELAY need a int")
#         return cls(delay)
#
#     def process_request(self, request, spider):
#         delay = random.randint(0, self.delay)
#         logging.debug("### random delay: %s s ###" % delay)
#         time.sleep(delay)
