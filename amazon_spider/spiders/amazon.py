# -*- coding: UTF-8 -*-
#!/usr/bin/python3

import re
import time
from scrapy import Request
from scrapy.spiders import Spider
from amazon_spider.items import AmazonSpiderItem
from amazon_spider.mysql_conn import DoMysql
from amazon_spider.settings import ipPool, count, proxy_url, RETRY_TIMES
import datetime
import requests
import logging
# import random

logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.DEBUG)


class amazon_spider(Spider):
    name = 'amazon_crawl'
    sql_result = []
    sql_result2 = []
    result_count = 0

    def start_requests(self):
        # 第一次请求发起前先填充一下ip池
        self.logger.debug('------------获取首批代理ip----------------')
        ips = requests.get(proxy_url)
        for ip in ips.text.split('\r\n'):
            if len(ip) > 8:
                ipPool.append('http://' + ip)

        sql = '''
           select asin,country from amazon_craw_asin_config 
           group by asin,country
        '''
        sql_check = '''
            select 
            a.asin,a.country 
            from(
                 select 
                 asin,country 
                 from amazon_craw_asin_config
                 group by asin,country
            ) a left join (
                 select 
                 t1.asin,t1.country
                 from amazon_craw_asin_details t1 
                 inner join(
                     select 
                     asin,country,max(spider_time) as spider_time 
                     from amazon_craw_asin_details 
                     where spider_time >= current_date
                     group by asin,country
                     ) t2 on t1.asin = t2.asin and t1.country = t2.country and t1.spider_time = t2.spider_time
                 ) b on a.asin = b.asin and a.country = b.country
            where b.asin is null and b.country is null
            -- group by a.asin,a.country
        '''
        sql_conn = '''
            select asin,country from amazon_craw_asin_config 
            where 1=1
            and CONCAT(asin,country) in(
            'B085ZG29HYIT'
            )
            group by asin,country
        '''
        # 测试 #
        # url_problem = 'https://www.amazon.de/dp/B000MQ7E06'
        # yield Request(url_problem,
        #               meta={'asin': 'B000MQ7E06', 'station': 'DE', 'url': url_problem},
        #               callback=self.parse_de, dont_filter=True)

        query = DoMysql()
        self.sql_result = query.fetch_chall(sql)
        for row in self.sql_result:
            if row[1] == 'US':
                url = 'https://www.amazon.com/dp/' + str(row[0]) + '/?language=en_US'
                yield Request(url, meta={'asin': str(row[0]), 'station': 'US', 'url': url}, callback=self.parse_us)
            elif row[1] == 'DE':
                url = 'https://www.amazon.de/dp/' + str(row[0]) + '/?language=de_DE'
                yield Request(url, meta={'asin': str(row[0]), 'station': 'DE', 'url': url}, callback=self.parse_de)
            elif row[1] == 'IT':
                url = 'https://www.amazon.it/dp/' + str(row[0])
                yield Request(url, meta={'asin': str(row[0]), 'station': 'IT', 'url': url}, callback=self.parse_it)
            elif row[1] == 'FR':
                url = 'https://www.amazon.fr/dp/' + str(row[0])
                yield Request(url, meta={'asin': str(row[0]), 'station': 'FR', 'url': url}, callback=self.parse_fr)
            elif row[1] == 'UK':
                url = 'https://www.amazon.co.uk/dp/' + str(row[0])
                yield Request(url, meta={'asin': str(row[0]), 'station': 'UK', 'url': url}, callback=self.parse_uk)
            elif row[1] == 'ES':
                url = 'https://www.amazon.es/dp/' + str(row[0])
                yield Request(url, meta={'asin': str(row[0]), 'station': 'ES', 'url': url}, callback=self.parse_es)
            elif row[1] == 'JP':
                url = 'https://www.amazon.co.jp/dp/' + str(row[0]) + '/?language=ja_JP&currency=JPY'
                yield Request(url, meta={'asin': str(row[0]), 'station': 'JP', 'url': url}, callback=self.parse_jp)
            elif row[1] == 'CA':
                url = 'https://www.amazon.ca/dp/' + str(row[0]) + '/?language=en_US'
                yield Request(url, meta={'asin': str(row[0]), 'station': 'CA', 'url': url}, callback=self.parse_ca)
            elif row[1] == 'MX':
                url = 'https://www.amazon.com.mx/dp/' + str(row[0])
                yield Request(url, meta={'asin': str(row[0]), 'station': 'MX', 'url': url}, callback=self.parse_mx)

        self.logger.debug('首次爬取完成，开始数据验证重试')
        # time.sleep(900)
        query_check = DoMysql()
        check_times = 1
        while check_times <= 2:
            self.logger.debug('等待900秒后开始验证第 {} 次'.format(str(check_times)))
            time.sleep(900)
            self.logger.debug('等待结束，开始执行重试sql')
            self.sql_result2 = query_check.fetch_chall(sql_check)
            # self.logger.debug('开始重试，需重试 {} 条数据'.format(len(self.sql_result2)))
            # 重新获取代理IP池
            self.logger.debug('------------重新获取代理ip----------------')
            ips = requests.get(proxy_url)
            for ip in ips.text.split('\r\n'):
                if len(ip) > 8:
                    ipPool.append('http://' + ip)

            for row in self.sql_result2:
                if row[1] == 'US':
                    url = 'https://www.amazon.com/dp/' + str(row[0]) + '/?language=en_US'
                    yield Request(url, meta={'asin': str(row[0]), 'station': 'US', 'url': url},
                                  dont_filter=True, callback=self.parse_us)
                elif row[1] == 'DE':
                    url = 'https://www.amazon.de/dp/' + str(row[0]) + '/?language=de_DE'
                    yield Request(url, meta={'asin': str(row[0]), 'station': 'DE', 'url': url},
                                  dont_filter=True, callback=self.parse_de)
                if row[1] == 'IT':
                    url = 'https://www.amazon.it/dp/' + str(row[0])
                    yield Request(url, meta={'asin': str(row[0]), 'station': 'IT', 'url': url},
                                  dont_filter=True, callback=self.parse_it)
                elif row[1] == 'FR':
                    url = 'https://www.amazon.fr/dp/' + str(row[0])
                    yield Request(url, meta={'asin': str(row[0]), 'station': 'FR', 'url': url},
                                  dont_filter=True, callback=self.parse_fr)
                elif row[1] == 'UK':
                    url = 'https://www.amazon.co.uk/dp/' + str(row[0])
                    yield Request(url, meta={'asin': str(row[0]), 'station': 'UK', 'url': url},
                                  dont_filter=True, callback=self.parse_uk)
                elif row[1] == 'ES':
                    url = 'https://www.amazon.es/dp/' + str(row[0])
                    yield Request(url, meta={'asin': str(row[0]), 'station': 'ES', 'url': url},
                                  dont_filter=True, callback=self.parse_es)
                elif row[1] == 'JP':
                    url = 'https://www.amazon.co.jp/dp/' + str(row[0]) + '/?language=ja_JP'
                    yield Request(url, meta={'asin': str(row[0]), 'station': 'JP', 'url': url},
                                  dont_filter=True, callback=self.parse_jp)
                elif row[1] == 'CA':
                    url = 'https://www.amazon.ca/dp/' + str(row[0]) + '/?language=en_US'
                    yield Request(url, meta={'asin': str(row[0]), 'station': 'CA', 'url': url},
                                  dont_filter=True, callback=self.parse_ca)
                elif row[1] == 'MX':
                    url = 'https://www.amazon.com.mx/dp/' + str(row[0])
                    yield Request(url, meta={'asin': str(row[0]), 'station': 'MX', 'url': url},
                                  dont_filter=True, callback=self.parse_mx)
            check_times += 1


    # 美国站点爬取
    def parse_us(self, response):
        item = AmazonSpiderItem()
        response = response.replace(body=response.text.replace('\x00', ''))
        # 检查邮编
        post_code = response.xpath('//span[@class="nav-line-2 nav-progressive-content"]/text()').extract()
        # 检查是否遇到验证码，有验证则返回重试
        # if len(response.text) < 10000:
        #     logger.info("遇到验证码，返回队列重试！" + '\n' + response.meta['url'])
        #     r = response.request.copy()
        #     r.dont_filter = True
        #     ip = random.choice(ipPool)
        #     r.meta['proxy'] = ip
        #     count['count'] += 1
        #     yield r
        if len(response.text) < 10000:
            logger.warning("遇到验证码，跳过！" + '\n' + response.meta['url'])
        ##            logger.warning("遇到验证码，返回队列重试！" + '\n' + response.meta['url'])
        ##            yield scrapy.Request(response.meta['url'],
        ##                                 meta={'asin': response.meta['asin'], 'station': response.meta['station'], 'url': response.meta['url']},
        ##                                 callback=self.parse_us, dont_filter=True)
        else:
            if 'Hong Kong' in ''.join(post_code).strip() or 'China' in ''.join(post_code).strip():
                logger.warning("邮编出错！" + '\n' + response.meta['url'])
            # ASIN
            item['asin'] = response.meta['asin']
            # print(item['asin'])
            item['asin_url'] = response.meta['url']
            # 站点
            item['station'] = response.meta['station']
            # 爬取时间
            item['spider_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 标题
            title = response.xpath('//span[@id="productTitle"]/text()').extract()
            item['title'] = ''.join(title).strip()
            # 品牌名字
            brand_info = response.xpath('//a[@id="bylineInfo"]/text()').extract()
            if 'Store' in ''.join(brand_info):
                item['brand'] = re.findall(r'Visit the (.*) Store', ''.join(brand_info))[0]
            elif 'Brand' in ''.join(brand_info):
                item['brand'] = ''.join(brand_info).split('Brand', 1)[1].replace(':', '').strip()
            else:
                item['brand'] = 'none'
            # 是否FBA
            merchant_infos = response.xpath('//div[@id="merchant-info"]//text()').extract()
            item['is_fba'] = 'none'
            if merchant_infos:
                for merchant_info in merchant_infos:
                    if 'sold by Amazon' in ''.join(merchant_info):
                        item['is_fba'] = '自营'
                        break
                    elif 'Fulfilled by Amazon' in ''.join(merchant_info):
                        item['is_fba'] = 'FBA'
                        break
            else:
                item['is_fba'] = '第三方'
            # 评论数
            reviews = response.xpath(
                '//div[@id="averageCustomerReviews"]'
                '//a[@id="acrCustomerReviewLink"]/span[@id="acrCustomerReviewText"]/text()').extract()
            item['reviews'] = ''.join(reviews).split(' ', 1)[0].replace(',', '')
            # 星级数
            stars = response.xpath(
                '//div[@id="averageCustomerReviews"]//span[@id="acrPopover"]/span/a/i/span/text()').extract()
            item['stars'] = ''.join(stars).strip().split(' ', 1)[0]
            # 取大类排名，大类类目，小类排名，小类类目
            if 'a-section table-padding' in response.text:
                # 排名1，样例：#3,238 in Home & Kitchen，以空格分割，取第一个元素并去除#和逗号
                rank1 = response.xpath(
                    '//*[@id="productDetails_detailBullets_sections1"]/tr/td/span/span[1]/text()[1]').extract()
                item['rank1'] = ''.join(rank1).split(' ', 1)[0].replace('#', '').replace(',', '')
                # 类目1，样例：See Top 100 in Home & Kitchen，取单词in后面的字符串
                cat_1 = response.xpath(
                    '//*[@id="productDetails_detailBullets_sections1"]/tr/td/span/span[1]/a/text()').extract()
                if 'in' in ''.join(cat_1):
                    item['cat1'] = ''.join(cat_1).split('in')[1]
                else:
                    item['cat1'] = ''.join(cat_1)
                # 排名2，样例：#23
                rank2 = response.xpath(
                    '//*[@id="productDetails_detailBullets_sections1"]/tr/td/span/span[2]/text()').extract()
                item['rank2'] = ''.join(rank2).split(' ', 1)[0].replace('#', '').replace(',', '')
                # 类目2，样例：Bed Throws
                cat_2 = response.xpath(
                    '//*[@id="productDetails_detailBullets_sections1"]/tr/td/span/span[2]/a/text()').extract()
                item['cat2'] = ''.join(cat_2)
                # 首次上架日期
                first_available_date = response.xpath(
                    '//th[contains(text(),"Date First Available")]/following-sibling::td/text()').extract()
                item['first_available_date'] = ''.join(first_available_date)
            else:
                rank1 = response.xpath(
                    '//div[@id="detailBulletsWrapper_feature_div"]/ul[1]/li/span//text()[2]').extract()
                item['rank1'] = ''.join(rank1).strip().split(' ', 1)[0].replace('#', '').replace(',', '')
                cat_1 = response.xpath(
                    '//div[@id="detailBulletsWrapper_feature_div"]/ul[1]/li/span/a/text()').extract()
                if 'in' in ''.join(cat_1):
                    item['cat1'] = ''.join(cat_1).split('in')[1]
                else:
                    item['cat1'] = ''.join(cat_1)
                rank2 = response.xpath(
                    '//div[@id="detailBulletsWrapper_feature_div"]/ul/li/span/ul/li/span/text()'
                ).extract()
                item['rank2'] = ''.join(rank2).strip().split(' ', 1)[0].replace('#', '').replace(',', '')
                cat_2 = response.xpath(
                    '//div[@id="detailBulletsWrapper_feature_div"]/ul/li/span/ul/li/span/a/text()').extract()
                item['cat2'] = ''.join(cat_2)
                first_available_date = response.xpath(
                    '//span[contains(text(),"Date First Available")]/following-sibling::span/text()').extract()

                item['first_available_date'] = ''.join(first_available_date)
            # QA问答数
            qna = response.xpath('//*[@id="askATFLink"]/span/text()').extract()
            item['qna'] = ''.join(qna).strip().split(' ', 1)[0]
            # 首图链接
            first_img = response.xpath(
                '//span[@class="a-list-item"]/span[@class="a-declarative"]'
                '/div[@id="imgTagWrapperId"]/img/@src').extract()
            item['first_img'] = ''.join(first_img)
            # 价格标签，区分ourprice和dealprice
            price_tag = response.xpath('//table[contains(@class,"a-lineitem a-align-top")]/'
                                       'tr/td[@class="a-span12"]/span[1]/@id').extract()
            price_type = ''
            if 'ourprice' in ''.join(price_tag):
                price_type = 'ourprice'
            elif 'saleprice' in ''.join(price_tag):
                price_type = 'saleprice'
            elif 'dealprice' in ''.join(price_tag):
                price_type = 'dealprice'
            item['price_type'] = price_type
            # 价格
            price = response.xpath(
                '//*[@id="corePrice_desktop"][1]/div/table/tr/td[2]/span[@class="a-price a-text-price a-size-medium apexPriceToPay"]/span[1]/text()').extract_first()
            price2 = response.xpath(
                '//*[@id="corePriceDisplay_desktop_feature_div"]/div[@class="a-section a-spacing-none aok-align-center"]//span[@class="a-offscreen"]/text()').extract_first()
            if price:
                item['price'] = price.strip()
            elif price2:
                item['price'] = price2.strip()
            else:
                item['price'] = price2
            # 完整类目
            cats1 = response.xpath(
                '//ul[@class="a-unordered-list a-horizontal a-size-small"]/li/span//text()').extract()
            # cats2 = [''.join(i) for i in cats1]
            cats2 = []
            for cat1 in cats1:
                if len(cat1) > 0:
                    cats2.append(cat1.strip())
                    cats2.append(' ')
            item['total_cat'] = ''.join(cats2)
            # 产品卖点
            descriptions = response.xpath('//div[@id="feature-bullets"]/ul//li[not(@id)]/span//text()').extract()
            description = ''
            # print(descriptions)
            for desc in descriptions:
                description = description + '\n' + str(desc).strip()
            item['description'] = description.strip()
            # coupon数据
            coupon = response.xpath('//*[contains(@id,"couponText")]/text()').extract()
            item['coupon'] = ''.join(coupon).strip()
            yield item
            # 评论链接，二级爬取
            # reviews_href = 'https://www.amazon.com/product-reviews/' \
            #                + str(response.meta['asin']) + '/reviewerType=all_reviews'
            # yield scrapy.Request(url=reviews_href, meta={'item': item}, callback=self.parse_reviews_us, dont_filter=True)

    # 德国站点爬取
    def parse_de(self, response):
        item = AmazonSpiderItem()
        response = response.replace(body=response.text.replace('\x00', ''))
        # 检查邮编
        post_code = response.xpath('//span[@class="nav-line-2 nav-progressive-content"]/text()').extract()
        if len(response.text) < 10000:
            logger.warning("遇到验证码，跳过！" + '\n' + response.meta['url'])
        ##            logger.warning("遇到验证码，返回队列重试！" + '\n' + response.meta['url'])
        ##            yield scrapy.Request(response.meta['url'],
        ##                                 meta={'asin': response.meta['asin'], 'station': response.meta['station'], 'url': response.meta['url']},
        ##                                 callback=self.parse_us, dont_filter=True)
        else:
            if 'Hong Kong' in ''.join(post_code).strip() or 'China' in ''.join(post_code).strip():
                logger.warning("邮编出错！" + '\n' + response.meta['url'])
            # ASIN
            item['asin'] = response.meta['asin']
            # print(item['asin'])
            item['asin_url'] = response.meta['url']
            # 站点
            item['station'] = response.meta['station']
            # 爬取时间
            item['spider_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 标题
            title = response.xpath('//span[@id="productTitle"]/text()').extract()
            item['title'] = ''.join(title).strip()
            # 品牌名字
            brand_info = response.xpath('//a[@id="bylineInfo"]/text()').extract()
            if 'Store' in ''.join(brand_info):
                item['brand'] = re.findall(r'Besuche den (.*)-Store', ''.join(brand_info))[0]
            elif 'Marke' in ''.join(brand_info):
                item['brand'] = ''.join(brand_info).split('Marke', 1)[1].replace(':', '').strip()
            else:
                item['brand'] = 'none'
            # 是否FBA
            merchant_infos = response.xpath('//div[@id="merchant-info"]//text()').extract()
            item['is_fba'] = 'none'
            if merchant_infos:
                for merchant_info in merchant_infos:
                    if 'Verkauf und Versand durch Amazon' in ''.join(merchant_info):
                        item['is_fba'] = '自营'
                        break
                    elif 'Versand durch Amazon' in ''.join(merchant_info):
                        item['is_fba'] = 'FBA'
                        break
            else:
                item['is_fba'] = '第三方'
            # 评论数
            reviews = response.xpath(
                '//div[@id="averageCustomerReviews"]//'
                'a[@id="acrCustomerReviewLink"]/span[@id="acrCustomerReviewText"]/text()').extract()
            item['reviews'] = ''.join(reviews).split(' ', 1)[0].replace(',', '').replace('.', '')
            # 星级数
            stars = response.xpath(
                '//div[@id="averageCustomerReviews"]//span[@id="acrPopover"]/span/a/i/span/text()').extract()
            item['stars'] = ''.join(stars).strip().split(' ', 1)[0].replace(',', '.')
            # 取大类排名，大类类目，小类排名，小类类目
            if 'a-section table-padding' in response.text:
                # 排名1，样例：#3,238 in Home & Kitchen，以空格分割，取第一个元素并去除#和逗号
                rank1 = response.xpath(
                    '//*[@id="productDetails_detailBullets_sections1"]/tr/td/span/span[1]/text()[1]').extract()
                item['rank1'] = ''.join(rank1).strip().split('in')[0].replace('Nr.', '').replace(',', '')
                # 类目1，样例：See Top 100 in Home & Kitchen，取单词in后面的字符串
                cat_1 = response.xpath(
                    '//*[@id="productDetails_detailBullets_sections1"]/tr/td/span/span[1]/a/text()').extract()
                if 'in' in ''.join(cat_1):
                    item['cat1'] = ''.join(cat_1).split('in')[1]
                else:
                    item['cat1'] = ''.join(cat_1)
                # 排名2，样例：#23
                rank2 = response.xpath(
                    '//*[@id="productDetails_detailBullets_sections1"]/tr/td/span/span[2]/text()').extract()
                item['rank2'] = ''.join(rank2).strip().split('in')[0].replace('Nr.', '').replace(',', '')
                # 类目2，样例：Bed Throws
                cat_2 = response.xpath(
                    '//*[@id="productDetails_detailBullets_sections1"]/tr/td/span/span[2]/a/text()').extract()
                item['cat2'] = ''.join(cat_2)
                # 首次上架日期
                first_available_date = response.xpath(
                    '//th[contains(text(),"Im Angebot von Amazon.de seit")]/following-sibling::td/text()').extract()
                item['first_available_date'] = ''.join(first_available_date)
            else:
                rank1 = response.xpath(
                    '//div[@id="detailBulletsWrapper_feature_div"]/ul[1]/li/span//text()[2]').extract()
                item['rank1'] = ''.join(rank1).strip().split('in')[0].replace('Nr.', '').replace(',', '')
                cat_1 = response.xpath(
                    '//div[@id="detailBulletsWrapper_feature_div"]/ul[1]/li/span/a/text()').extract()
                if 'in' in ''.join(cat_1):
                    item['cat1'] = ''.join(cat_1).split('in')[1]
                else:
                    item['cat1'] = ''.join(cat_1)
                rank2 = response.xpath(
                    '//div[@id="detailBulletsWrapper_feature_div"]/ul/li/span/ul/li/span/text()'
                ).extract()
                item['rank2'] = ''.join(rank2).strip().split('in')[0].replace('Nr.', '').replace(',', '')
                cat_2 = response.xpath(
                    '//div[@id="detailBulletsWrapper_feature_div"]/ul/li/span/ul/li/span/a/text()').extract()
                item['cat2'] = ''.join(cat_2)
                first_available_date = response.xpath(
                    '//span[contains(text(),"Im Angebot von Amazon.de seit")]/following-sibling::span/text()').extract()

                item['first_available_date'] = ''.join(first_available_date)
            # QA问答数
            qna = response.xpath('//*[@id="askATFLink"]/span/text()').extract()
            item['qna'] = ''.join(qna).strip().split(' ', 1)[0]
            # 首图链接
            first_img = response.xpath(
                '//span[@class="a-list-item"]/span[@class="a-declarative"]/div[@id="imgTagWrapperId"]/img/@src').extract()
            item['first_img'] = ''.join(first_img)
            # 价格标签，区分ourprice和dealprice
            price_tag = response.xpath('//table[contains(@class,"a-lineitem")]/tr/td[@class="a-span12"]/span[1]/@id').extract()
            price_type = ''
            if 'ourprice' in ''.join(price_tag):
                price_type = 'ourprice'
            elif 'saleprice' in ''.join(price_tag):
                price_type = 'saleprice'
            elif 'dealprice' in ''.join(price_tag):
                price_type = 'dealprice'
            item['price_type'] = price_type
            # 价格
            price = response.xpath(
                '//*[@id="corePrice_desktop"][1]/div/table/tr/td[2]/span[@class="a-price a-text-price a-size-medium apexPriceToPay"]/span[1]/text()').extract_first()
            price2 = response.xpath(
                '//*[@id="corePriceDisplay_desktop_feature_div"]/div[@class="a-section a-spacing-none aok-align-center"]//span[@class="a-offscreen"]/text()').extract_first()
            if price:
                item['price'] = price.strip()
            elif price2:
                item['price'] = price2.strip()
            else:
                item['price'] = price2
            # 完整类目
            cats1 = response.xpath('//ul[@class="a-unordered-list a-horizontal a-size-small"]/li/span//text()').extract()
            # cats2 = [''.join(i) for i in cats1]
            cats2 = []
            for cat1 in cats1:
                if len(cat1) > 0:
                    cats2.append(cat1.strip())
                    cats2.append(' ')
            item['total_cat'] = ''.join(cats2)
            # 产品卖点
            descriptions = response.xpath('//div[@id="feature-bullets"]/ul//li[not(@id)]/span//text()').extract()
            # print(descriptions)
            description = ''
            for desc in descriptions:
                description = description + '\n' + str(desc).strip()
            item['description'] = description.strip()
            # coupon数据
            coupon = response.xpath('//*[contains(@id,"couponText")]/text()').extract()
            item['coupon'] = ''.join(coupon).strip()
            yield item
            # 评论链接，二级爬取
            # reviews_href = 'https://www.amazon.de/product-reviews/' \
            #                + str(response.meta['asin']) + '/reviewerType=all_reviews'
            # yield scrapy.Request(url=reviews_href, meta={'item': item}, callback=self.parse_reviews_de, dont_filter=True)

    # 意大利站点爬取
    def parse_it(self, response):
        item = AmazonSpiderItem()
        response = response.replace(body=response.text.replace('\x00', ''))
        # 检查邮编
        post_code = response.xpath('//span[@class="nav-line-2 nav-progressive-content"]/text()').extract()
        if len(response.text) < 10000:
            logger.warning("遇到验证码，跳过！" + '\n' + response.meta['url'])
        ##            logger.warning("遇到验证码，返回队列重试！" + '\n' + response.meta['url'])
        ##            yield scrapy.Request(response.meta['url'],
        ##                                 meta={'asin': response.meta['asin'], 'station': response.meta['station'], 'url': response.meta['url']},
        ##                                 callback=self.parse_us, dont_filter=True)
        else:
            if 'Hong Kong' in ''.join(post_code).strip() or 'China' in ''.join(post_code).strip():
                logger.warning("邮编出错！" + '\n' + response.meta['url'])
            # ASIN
            item['asin'] = response.meta['asin']
            # print(item['asin'])
            item['asin_url'] = response.meta['url']
            # 站点
            item['station'] = response.meta['station']
            # 爬取时间
            item['spider_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 标题
            title = response.xpath('//span[@id="productTitle"]/text()').extract()
            item['title'] = ''.join(title).strip()
            # 品牌名字
            brand_info = response.xpath('//a[@id="bylineInfo"]/text()').extract()
            # print(brand_info)
            if 'Store' in ''.join(brand_info):
                item['brand'] = ''.join(brand_info).split('Visita lo Store di ')[1]
            elif 'Marca' in ''.join(brand_info):
                item['brand'] = ''.join(brand_info).split('Marca', 1)[1].replace(':', '').strip()
            else:
                item['brand'] = 'none'
            # 是否FBA
            dispatch_info = response.xpath(
                '//*[@id="tabular-buybox-truncate-0"]//span[@class="tabular-buybox-text"]//text()'
            ).extract_first()
            sold_info = response.xpath(
                '//*[@id="tabular-buybox-truncate-1"]//span[@class="tabular-buybox-text"]//text()'
            ).extract_first()
            if dispatch_info:
                if 'Amazon' in dispatch_info:
                    if 'Amazon' in sold_info:
                        item['is_fba'] = '自营'
                    else:
                        item['is_fba'] = 'FBA'
                else:
                    item['is_fba'] = '第三方'
            elif title:
                item['is_fba'] = '第三方'
            else:
                item['is_fba'] = ''
            # 评论数
            reviews = response.xpath(
                '//div[@id="averageCustomerReviews"]'
                '//a[@id="acrCustomerReviewLink"]/span[@id="acrCustomerReviewText"]/text()').extract()
            item['reviews'] = ''.join(reviews).split(' ', 1)[0].replace('.', '')
            # 星级数
            stars = response.xpath(
                '//div[@id="averageCustomerReviews"]//span[@id="acrPopover"]/span/a/i/span/text()').extract()
            item['stars'] = ''.join(stars).strip().split(' ', 1)[0].replace(',', '.')
            # 取大类排名，大类类目，小类排名，小类类目
            if 'a-section table-padding' in response.text:
                # 排名1，样例：#3,238 in Home & Kitchen，以空格分割，取第一个元素并去除#和逗号
                rank1 = response.xpath(
                    '//*[@id="productDetails_detailBullets_sections1"]/tr/td/span/span[1]/text()[1]').extract()
                item['rank1'] = ''.join(rank1).strip().split('in')[0].replace('n.', '').replace(',', '')
                # 类目1，样例：See Top 100 in Home & Kitchen，取单词in后面的字符串
                cat_1 = response.xpath(
                    '//*[@id="productDetails_detailBullets_sections1"]/tr/td/span/span[1]/a/text()').extract()
                if 'categoria' in ''.join(cat_1):
                    item['cat1'] = ''.join(cat_1).split('categoria ')[1]
                else:
                    item['cat1'] = ''.join(cat_1)
                # 排名2，样例：#23
                rank2 = response.xpath(
                    '//*[@id="productDetails_detailBullets_sections1"]/tr/td/span/span[2]/text()').extract()
                item['rank2'] = ''.join(rank2).strip().split('in')[0].replace('n.', '').replace(',', '')
                # 类目2，样例：Bed Throws
                cat_2 = response.xpath(
                    '//*[@id="productDetails_detailBullets_sections1"]/tr/td/span/span[2]/a/text()').extract()
                item['cat2'] = ''.join(cat_2)
                # 首次上架日期
                first_available_date = response.xpath(
                    '//th[contains(text(),"Disponibile su Amazon.it a partire dal")]'
                    '/following-sibling::td/text()').extract()
                item['first_available_date'] = ''.join(first_available_date)
            else:
                rank1 = response.xpath(
                    '//div[@id="detailBulletsWrapper_feature_div"]/ul[1]/li/span//text()[2]').extract()
                item['rank1'] = ''.join(rank1).strip().split('in')[0].replace('n.', '').replace(',', '')
                cat_1 = response.xpath(
                    '//div[@id="detailBulletsWrapper_feature_div"]/ul[1]/li/span/a/text()').extract()
                if 'categoria' in ''.join(cat_1):
                    item['cat1'] = ''.join(cat_1).split('categoria ')[1]
                else:
                    item['cat1'] = ''.join(cat_1)
                rank2 = response.xpath(
                    '//div[@id="detailBulletsWrapper_feature_div"]/ul/li/span/ul/li/span/text()'
                ).extract()
                item['rank2'] = ''.join(rank2).strip().split('in')[0].replace('n.', '').replace(',', '')
                cat_2 = response.xpath(
                    '//div[@id="detailBulletsWrapper_feature_div"]/ul/li/span/ul/li/span/a/text()').extract()
                item['cat2'] = ''.join(cat_2)
                first_available_date = response.xpath(
                    '//span[contains(text(),"Disponibile su Amazon.it a partire dal")]'
                    '/following-sibling::span/text()').extract()

                item['first_available_date'] = ''.join(first_available_date)
            # QA问答数
            qna = response.xpath('//*[@id="askATFLink"]/span/text()').extract()
            item['qna'] = ''.join(qna).strip().split(' ', 1)[0]
            # 首图链接
            first_img = response.xpath(
                '//span[@class="a-list-item"]/span[@class="a-declarative"]/div[@id="imgTagWrapperId"]/img/@src').extract()
            item['first_img'] = ''.join(first_img)
            # 价格标签，区分ourprice和dealprice
            price_tag = response.xpath('//table[contains(@class,"a-lineitem a-align-top")]/tr/td[@class="a-span12"]/span[1]/@id').extract()
            price_type = ''
            if 'ourprice' in ''.join(price_tag):
                price_type = 'ourprice'
            elif 'saleprice' in ''.join(price_tag):
                price_type = 'saleprice'
            elif 'dealprice' in ''.join(price_tag):
                price_type = 'dealprice'
            item['price_type'] = price_type
            # 价格
            price = response.xpath(
                '//*[@id="corePrice_desktop"]/div/table/tr/td[2]/span[@class="a-price a-text-price a-size-medium apexPriceToPay"]/span[1]/text()').extract_first()
            price2 = response.xpath(
                '//*[@id="corePriceDisplay_desktop_feature_div"]/div[@class="a-section a-spacing-none aok-align-center"]//span[@class="a-offscreen"]/text()').extract_first()
            if price:
                item['price'] = price.strip()
            elif price2:
                item['price'] = price2.strip()
            else:
                item['price'] = price2

            # 完整类目
            cats1 = response.xpath('//ul[@class="a-unordered-list a-horizontal a-size-small"]/li/span//text()').extract()
            # cats2 = [''.join(i) for i in cats1]
            cats2 = []
            for cat1 in cats1:
                if len(cat1) > 0:
                    cats2.append(cat1.strip())
                    cats2.append(' ')
            item['total_cat'] = ''.join(cats2)
            # 产品卖点
            descriptions = response.xpath('//div[@id="feature-bullets"]/ul//li[not(@id)]/span//text()').extract()
            description = ''
            for desc in descriptions:
                description = description + '\n' + str(desc).strip()
            item['description'] = description.strip()
            # coupon数据
            coupon = response.xpath('//*[contains(@id,"couponText")]/text()').extract()
            # print(coupons)
            item['coupon'] = ''.join(coupon).strip()
            yield item
            # 评论链接，二级爬取
            # reviews_href = 'https://www.amazon.it/product-reviews/' \
            #                + str(response.meta['asin']) + '/reviewerType=all_reviews'
            # yield scrapy.Request(url=reviews_href, meta={'item': item}, callback=self.parse_reviews_de, dont_filter=True)

    # 法国站点爬取
    def parse_fr(self, response):
        item = AmazonSpiderItem()
        response = response.replace(body=response.text.replace('\x00', ''))
        # 检查邮编
        post_code = response.xpath('//span[@class="nav-line-2 nav-progressive-content"]/text()').extract()
        if len(response.text) < 10000:
            logger.warning("遇到验证码，跳过！" + '\n' + response.meta['url'])
        ##            logger.warning("遇到验证码，返回队列重试！" + '\n' + response.meta['url'])
        ##            yield scrapy.Request(response.meta['url'],
        ##                                 meta={'asin': response.meta['asin'], 'station': response.meta['station'], 'url': response.meta['url']},
        ##                                 callback=self.parse_us, dont_filter=True)
        else:
            if 'Hong Kong' in ''.join(post_code).strip() or 'China' in ''.join(post_code).strip():
                logger.warning("邮编出错！" + '\n' + response.meta['url'])
            # ASIN
            item['asin'] = response.meta['asin']
            # print(item['asin'])
            item['asin_url'] = response.meta['url']
            # 站点
            item['station'] = response.meta['station']
            # 爬取时间
            item['spider_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 标题
            title = response.xpath('//span[@id="productTitle"]/text()').extract()
            item['title'] = ''.join(title).strip()
            # 品牌名字
            brand_info = response.xpath('//a[@id="bylineInfo"]/text()').extract()
            # print(brand_info)
            if 'boutique' in ''.join(brand_info):
                item['brand'] = ''.join(brand_info).split('Visiter la boutique ')[1]
            elif 'Marque' in ''.join(brand_info):
                item['brand'] = ''.join(brand_info).split('Marque', 1)[1].replace(':', '').strip()
            else:
                item['brand'] = 'none'
            # 是否FBA
            dispatch_info = response.xpath(
                '//*[@id="tabular-buybox-truncate-0"]//span[@class="tabular-buybox-text"]//text()'
            ).extract_first()
            sold_info = response.xpath(
                '//*[@id="tabular-buybox-truncate-1"]//span[@class="tabular-buybox-text"]//text()'
            ).extract_first()
            if dispatch_info:
                if 'Amazon' in dispatch_info:
                    if 'Amazon' in sold_info:
                        item['is_fba'] = '自营'
                    else:
                        item['is_fba'] = 'FBA'
                else:
                    item['is_fba'] = '第三方'
            elif title:
                item['is_fba'] = '第三方'
            else:
                item['is_fba'] = ''
            # 评论数
            reviews = response.xpath(
                '//div[@id="averageCustomerReviews"]//'
                'a[@id="acrCustomerReviewLink"]/span[@id="acrCustomerReviewText"]/text()').extract()
            item['reviews'] = ''.join(reviews).split(' ', 1)[0].replace('\xa0', '')
            # 星级数
            stars = response.xpath(
                '//div[@id="averageCustomerReviews"]//span[@id="acrPopover"]/span/a/i/span/text()').extract()
            item['stars'] = ''.join(stars).strip().split(' ', 1)[0].replace(',', '.')
            # 取大类排名，大类类目，小类排名，小类类目
            if 'a-section table-padding' in response.text:
                # 排名1，样例：#3,238 in Home & Kitchen，以空格分割，取第一个元素并去除#和逗号
                rank1 = response.xpath(
                    '//*[@id="productDetails_detailBullets_sections1"]/tr/td/span/span[1]/text()[1]').extract()
                item['rank1'] = ''.join(rank1).strip().split('en')[0].replace(',', '')
                # 类目1，样例：See Top 100 in Home & Kitchen，取单词in后面的字符串
                cat_1 = response.xpath(
                    '//*[@id="productDetails_detailBullets_sections1"]/tr/td/span/span[1]/a/text()').extract()
                if 'en' in ''.join(cat_1):
                    item['cat1'] = ''.join(cat_1).split('en')[1]
                else:
                    item['cat1'] = ''.join(cat_1)
                # 排名2，样例：#23
                rank2 = response.xpath(
                    '//*[@id="productDetails_detailBullets_sections1"]/tr/td/span/span[2]/text()').extract()
                item['rank2'] = ''.join(rank2).strip().split('en')[0].replace(',', '')
                # 类目2，样例：Bed Throws
                cat_2 = response.xpath(
                    '//*[@id="productDetails_detailBullets_sections1"]/tr/td/span/span[2]/a/text()').extract()
                item['cat2'] = ''.join(cat_2)
                # 首次上架日期
                first_available_date = response.xpath(
                    '//th[contains(text(),"Date de mise en ligne sur Amazon.fr")]/following-sibling::td/text()').extract()
                item['first_available_date'] = ''.join(first_available_date)
            else:
                rank1 = response.xpath(
                    '//div[@id="detailBulletsWrapper_feature_div"]/ul[1]/li/span//text()[2]').extract()
                item['rank1'] = ''.join(rank1).strip().split('en')[0].replace(',', '')
                cat_1 = response.xpath(
                    '//div[@id="detailBulletsWrapper_feature_div"]/ul[1]/li/span/a/text()').extract()
                if 'in' in ''.join(cat_1):
                    item['cat1'] = ''.join(cat_1).split('en')[1]
                else:
                    item['cat1'] = ''.join(cat_1)
                rank2 = response.xpath(
                    '//div[@id="detailBulletsWrapper_feature_div"]/ul/li/span/ul/li/span/text()'
                ).extract()
                item['rank2'] = ''.join(rank2).strip().split('en')[0].replace(',', '')
                cat_2 = response.xpath(
                    '//div[@id="detailBulletsWrapper_feature_div"]/ul/li/span/ul/li/span/a/text()').extract()
                item['cat2'] = ''.join(cat_2)
                first_available_date = response.xpath(
                    '//span[contains(text(),"Date de mise en ligne sur Amazon.fr")]'
                    '/following-sibling::span/text()').extract()
                item['first_available_date'] = ''.join(first_available_date)
            # QA问答数
            qna = response.xpath('//*[@id="askATFLink"]/span/text()').extract()
            item['qna'] = ''.join(qna).strip().split(' ', 1)[0]
            # 首图链接
            first_img = response.xpath(
                '//span[@class="a-list-item"]/span[@class="a-declarative"]/div[@id="imgTagWrapperId"]/img/@src').extract()
            item['first_img'] = ''.join(first_img)
            # 价格标签，区分ourprice和dealprice
            price_tag = response.xpath('//table[contains(@class,"a-lineitem a-align-top")]/tr/td[@class="a-span12"]/span[1]/@id').extract()
            price_type = ''
            if 'ourprice' in ''.join(price_tag):
                price_type = 'ourprice'
            elif 'saleprice' in ''.join(price_tag):
                price_type = 'saleprice'
            elif 'dealprice' in ''.join(price_tag):
                price_type = 'dealprice'
            item['price_type'] = price_type
            # 价格
            price = response.xpath(
                '//*[@id="corePrice_desktop"]/div/table/tr/td[2]/span[@class="a-price a-text-price a-size-medium apexPriceToPay"]/span[1]/text()').extract_first()
            price2 = response.xpath(
                '//*[@id="corePriceDisplay_desktop_feature_div"]/div[@class="a-section a-spacing-none aok-align-center"]//span[@class="a-offscreen"]/text()').extract_first()
            if price:
                item['price'] = price.strip()
            elif price2:
                item['price'] = price2.strip()
            else:
                item['price'] = price2
            # 完整类目
            cats1 = response.xpath('//ul[@class="a-unordered-list a-horizontal a-size-small"]/li/span//text()').extract()
            # cats2 = [''.join(i) for i in cats1]
            cats2 = []
            for cat1 in cats1:
                if len(cat1) > 0:
                    cats2.append(cat1.strip())
                    cats2.append(' ')
            item['total_cat'] = ''.join(cats2)
            # 产品卖点
            descriptions = response.xpath('//div[@id="feature-bullets"]/ul//li[not(@id)]/span//text()').extract()
            description = ''
            for desc in descriptions:
                description = description + '\n' + str(desc).strip()
            item['description'] = description.strip()
            # coupon数据
            coupon = response.xpath('//*[contains(@id,"couponText")]/text()').extract()
            item['coupon'] = ''.join(coupon).strip()
            yield item
            # 评论链接，二级爬取
            # reviews_href = 'https://www.amazon.fr/product-reviews/' \
            #                + str(response.meta['asin']) + '/reviewerType=all_reviews'
            # yield scrapy.Request(url=reviews_href, meta={'item': item}, callback=self.parse_reviews_de, dont_filter=True)

    # 英国站点爬取
    def parse_uk(self, response):
        item = AmazonSpiderItem()
        response = response.replace(body=response.text.replace('\x00', ''))
        # 检查邮编
        post_code = response.xpath('//span[@class="nav-line-2 nav-progressive-content"]/text()').extract()
        if len(response.text) < 10000:
            logger.warning("遇到验证码，跳过！" + '\n' + response.meta['url'])
        ##            logger.warning("遇到验证码，返回队列重试！" + '\n' + response.meta['url'])
        ##            yield scrapy.Request(response.meta['url'],
        ##                                 meta={'asin': response.meta['asin'], 'station': response.meta['station'], 'url': response.meta['url']},
        ##                                 callback=self.parse_us, dont_filter=True)
        else:
            if 'Hong Kong' in ''.join(post_code).strip() or 'China' in ''.join(post_code).strip():
                logger.warning("邮编出错！" + '\n' + response.meta['url'])
            # ASIN
            item['asin'] = response.meta['asin']
            # print(item['asin'])
            item['asin_url'] = response.meta['url']
            # 站点
            item['station'] = response.meta['station']
            # 爬取时间
            item['spider_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 标题
            title = response.xpath('//span[@id="productTitle"]/text()').extract()
            item['title'] = ''.join(title).strip()
            # 品牌名字
            brand_info = response.xpath('//a[@id="bylineInfo"]/text()').extract()
            # print(brand_info)
            if 'Store' in ''.join(brand_info):
                item['brand'] = re.findall(r'Visit the (.*) Store', ''.join(brand_info))[0]
            elif 'Brand' in ''.join(brand_info):
                item['brand'] = ''.join(brand_info).split('Brand', 1)[1].replace(':', '').strip()
            else:
                item['brand'] = 'none'
            # 是否FBA
            dispatch_info = response.xpath(
                '//*[@id="tabular-buybox-truncate-0"]//span[@class="tabular-buybox-text"]//text()'
            ).extract_first()
            sold_info = response.xpath(
                '//*[@id="tabular-buybox-truncate-1"]//span[@class="tabular-buybox-text"]//text()'
            ).extract_first()
            if dispatch_info:
                if 'Amazon' in dispatch_info:
                    if 'Amazon' in sold_info:
                        item['is_fba'] = '自营'
                    else:
                        item['is_fba'] = 'FBA'
                else:
                    item['is_fba'] = '第三方'
            elif title:
                item['is_fba'] = '第三方'
            else:
                item['is_fba'] = ''
            # 评论数
            reviews = response.xpath(
                '//div[@id="averageCustomerReviews"]'
                '//a[@id="acrCustomerReviewLink"]/span[@id="acrCustomerReviewText"]/text()').extract()
            item['reviews'] = ''.join(reviews).split(' ', 1)[0].replace(',', '')
            # 星级数
            stars = response.xpath(
                '//div[@id="averageCustomerReviews"]//span[@id="acrPopover"]/span/a/i/span/text()').extract()
            item['stars'] = ''.join(stars).strip().split(' ', 1)[0]
            # 取大类排名，大类类目，小类排名，小类类目
            if 'a-section table-padding' in response.text:
                # 排名1，样例：#3,238 in Home & Kitchen，以空格分割，取第一个元素并去除#和逗号
                rank1 = response.xpath(
                    '//*[@id="productDetails_detailBullets_sections1"]/tr/td/span/span[1]/text()[1]').extract()
                item['rank1'] = ''.join(rank1).split(' ', 1)[0].replace('#', '').replace(',', '')
                # 类目1，样例：See Top 100 in Home & Kitchen，取单词in后面的字符串
                cat_1 = response.xpath(
                    '//*[@id="productDetails_detailBullets_sections1"]/tr/td/span/span[1]/a/text()').extract()
                if 'in' in ''.join(cat_1):
                    item['cat1'] = ''.join(cat_1).split('in')[1]
                else:
                    item['cat1'] = ''.join(cat_1)
                # 排名2，样例：#23
                rank2 = response.xpath(
                    '//*[@id="productDetails_detailBullets_sections1"]/tr/td/span/span[2]/text()').extract()
                item['rank2'] = ''.join(rank2).split(' ', 1)[0].replace('#', '').replace(',', '')
                # 类目2，样例：Bed Throws
                cat_2 = response.xpath(
                    '//*[@id="productDetails_detailBullets_sections1"]/tr/td/span/span[2]/a/text()').extract()
                item['cat2'] = ''.join(cat_2)
                # 首次上架日期
                first_available_date = response.xpath(
                    '//th[contains(text(),"Date First Available")]/following-sibling::td/text()').extract()
                item['first_available_date'] = ''.join(first_available_date)
            else:
                rank1 = response.xpath(
                    '//div[@id="detailBulletsWrapper_feature_div"]/ul[1]/li/span//text()[2]').extract()
                item['rank1'] = ''.join(rank1).strip().split(' ', 1)[0].replace('#', '').replace(',', '')
                cat_1 = response.xpath(
                    '//div[@id="detailBulletsWrapper_feature_div"]/ul[1]/li/span/a/text()').extract()
                if 'in' in ''.join(cat_1):
                    item['cat1'] = ''.join(cat_1).split('in')[1]
                else:
                    item['cat1'] = ''.join(cat_1)
                rank2 = response.xpath(
                    '//div[@id="detailBulletsWrapper_feature_div"]/ul/li/span/ul/li/span/text()'
                ).extract()
                item['rank2'] = ''.join(rank2).strip().split(' ', 1)[0].replace('#', '').replace(',', '')
                cat_2 = response.xpath(
                    '//div[@id="detailBulletsWrapper_feature_div"]/ul/li/span/ul/li/span/a/text()').extract()
                item['cat2'] = ''.join(cat_2)
                first_available_date = response.xpath(
                    '//span[contains(text(),"Date First Available")]/following-sibling::span/text()').extract()

                item['first_available_date'] = ''.join(first_available_date)
            # QA问答数
            qna = response.xpath('//*[@id="askATFLink"]/span/text()').extract()
            item['qna'] = ''.join(qna).strip().split(' ', 1)[0]
            # 首图链接
            first_img = response.xpath(
                '//span[@class="a-list-item"]/span[@class="a-declarative"]/div[@id="imgTagWrapperId"]/img/@src').extract()
            item['first_img'] = ''.join(first_img)
            # 价格标签，区分ourprice和dealprice
            price_tag = response.xpath('//table[contains(@class,"a-lineitem a-align-top")]/tr/td[@class="a-span12"]/span[1]/@id').extract()
            price_type = ''
            if 'ourprice' in ''.join(price_tag):
                price_type = 'ourprice'
            elif 'saleprice' in ''.join(price_tag):
                price_type = 'saleprice'
            elif 'dealprice' in ''.join(price_tag):
                price_type = 'dealprice'
            item['price_type'] = price_type
            # 价格
            price = response.xpath(
                '//*[@id="corePrice_desktop"]/div/table/tr/td[2]/span[@class="a-price a-text-price a-size-medium apexPriceToPay"]/span[1]/text()').extract_first()
            price2 = response.xpath(
                '//*[@id="corePriceDisplay_desktop_feature_div"]/div[@class="a-section a-spacing-none aok-align-center"]//span[@class="a-offscreen"]/text()').extract_first()
            if price:
                item['price'] = price.strip()
            elif price2:
                item['price'] = price2.strip()
            else:
                item['price'] = price2

            # 完整类目
            cats1 = response.xpath('//ul[@class="a-unordered-list a-horizontal a-size-small"]/li/span//text()').extract()
            # cats2 = [''.join(i) for i in cats1]
            cats2 = []
            for cat1 in cats1:
                if len(cat1) > 0:
                    cats2.append(cat1.strip())
                    cats2.append(' ')
            item['total_cat'] = ''.join(cats2)
            # 产品卖点
            descriptions = response.xpath('//div[@id="feature-bullets"]/ul//li[not(@id)]/span//text()').extract()
            description = ''
            for desc in descriptions:
                description = description + '\n' + str(desc).strip()
            item['description'] = description.strip()
            # coupon数据
            coupon = response.xpath('//*[contains(@id,"couponText")]/text()').extract()
            item['coupon'] = ''.join(coupon).strip()
            yield item
            # 评论链接，二级爬取
            # reviews_href = 'https://www.amazon.co.uk/product-reviews/' \
            #                + str(response.meta['asin']) + '/reviewerType=all_reviews'
            # yield scrapy.Request(url=reviews_href, meta={'item': item}, callback=self.parse_reviews_us, dont_filter=True)

    # 西班牙站点爬取
    def parse_es(self, response):
        item = AmazonSpiderItem()
        response = response.replace(body=response.text.replace('\x00', ''))
        # 检查邮编
        post_code = response.xpath('//span[@class="nav-line-2 nav-progressive-content"]/text()').extract()
        if len(response.text) < 10000:
            logger.warning("遇到验证码，跳过！" + '\n' + response.meta['url'])
        ##            logger.warning("遇到验证码，返回队列重试！" + '\n' + response.meta['url'])
        ##            yield scrapy.Request(response.meta['url'],
        ##                                 meta={'asin': response.meta['asin'], 'station': response.meta['station'], 'url': response.meta['url']},
        ##                                 callback=self.parse_us, dont_filter=True)
        else:
            if 'Hong Kong' in ''.join(post_code).strip() or 'China' in ''.join(post_code).strip():
                logger.warning("邮编出错！" + '\n' + response.meta['url'])
            # ASIN
            item['asin'] = response.meta['asin']
            # print(item['asin'])
            item['asin_url'] = response.meta['url']
            # 站点
            item['station'] = response.meta['station']
            # 爬取时间
            item['spider_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 标题
            title = response.xpath('//span[@id="productTitle"]/text()').extract()
            item['title'] = ''.join(title).strip()
            # 品牌名字
            brand_info = response.xpath('//a[@id="bylineInfo"]/text()').extract()
            # print(brand_info)
            if 'Store' in ''.join(brand_info):
                item['brand'] = ''.join(brand_info).split('Visita la Store de ')[1]
            elif 'Marca' in ''.join(brand_info):
                item['brand'] = ''.join(brand_info).split('Marca', 1)[1].replace(':', '').strip()
            else:
                item['brand'] = 'none'
            # 是否FBA
            dispatch_info = response.xpath(
                '//*[@id="tabular-buybox-truncate-0"]//span[@class="tabular-buybox-text"]//text()'
            ).extract_first()
            sold_info = response.xpath(
                '//*[@id="tabular-buybox-truncate-1"]//span[@class="tabular-buybox-text"]//text()'
            ).extract_first()
            if dispatch_info:
                if 'Amazon' in dispatch_info:
                    if 'Amazon' in sold_info:
                        item['is_fba'] = '自营'
                    else:
                        item['is_fba'] = 'FBA'
                else:
                    item['is_fba'] = '第三方'
            elif title:
                item['is_fba'] = '第三方'
            else:
                item['is_fba'] = ''
            # 评论数
            reviews = response.xpath(
                '//div[@id="averageCustomerReviews"]'
                '//a[@id="acrCustomerReviewLink"]/span[@id="acrCustomerReviewText"]/text()').extract()
            item['reviews'] = ''.join(reviews).split(' ', 1)[0].replace('.', '')
            # 星级数
            stars = response.xpath(
                '//div[@id="averageCustomerReviews"]//span[@id="acrPopover"]/span/a/i/span/text()').extract()
            item['stars'] = ''.join(stars).strip().split(' ', 1)[0].replace(',', '.')
            # 取大类排名，大类类目，小类排名，小类类目
            if 'a-section table-padding' in response.text:
                # 排名1，样例：#3,238 in Home & Kitchen，以空格分割，取第一个元素并去除#和逗号
                rank1 = response.xpath(
                    '//*[@id="productDetails_detailBullets_sections1"]/tr/td/span/span[1]/text()[1]').extract()
                item['rank1'] = ''.join(rank1).split(' ', 1)[0].replace('nº', '').replace(',', '')
                # 类目1，样例：See Top 100 in Home & Kitchen，取单词in后面的字符串
                cat_1 = response.xpath(
                    '//*[@id="productDetails_detailBullets_sections1"]/tr/td/span/span[1]/a/text()').extract()
                if 'en' in ''.join(cat_1):
                    item['cat1'] = ''.join(cat_1).split('en')[1]
                else:
                    item['cat1'] = ''.join(cat_1)
                # 排名2，样例：#23
                rank2 = response.xpath(
                    '//*[@id="productDetails_detailBullets_sections1"]/tr/td/span/span[2]/text()').extract()
                item['rank2'] = ''.join(rank2).split(' ', 1)[0].replace('nº', '').replace(',', '')
                # 类目2，样例：Bed Throws
                cat_2 = response.xpath(
                    '//*[@id="productDetails_detailBullets_sections1"]/tr/td/span/span[2]/a/text()').extract()
                item['cat2'] = ''.join(cat_2)
                # 首次上架日期
                first_available_date = response.xpath(
                    '//th[contains(text(),"Producto en Amazon.es desde")]/following-sibling::td/text()').extract()
                item['first_available_date'] = ''.join(first_available_date)
            else:
                rank1 = response.xpath(
                    '//div[@id="detailBulletsWrapper_feature_div"]/ul[1]/li/span//text()[2]').extract()
                item['rank1'] = ''.join(rank1).strip().split(' ', 1)[0].replace('nº', '').replace(',', '')
                cat_1 = response.xpath(
                    '//div[@id="detailBulletsWrapper_feature_div"]/ul[1]/li/span/a/text()').extract()
                if 'en' in ''.join(cat_1):
                    item['cat1'] = ''.join(cat_1).split('en')[1]
                else:
                    item['cat1'] = ''.join(cat_1)
                rank2 = response.xpath(
                    '//div[@id="detailBulletsWrapper_feature_div"]/ul/li/span/ul/li/span/text()'
                ).extract()
                item['rank2'] = ''.join(rank2).strip().split(' ', 1)[0].replace('nº', '').replace(',', '')
                cat_2 = response.xpath(
                    '//div[@id="detailBulletsWrapper_feature_div"]/ul/li/span/ul/li/span/a/text()').extract()
                item['cat2'] = ''.join(cat_2)
                first_available_date = response.xpath(
                    '//span[contains(text(),"Producto en Amazon.es desde")]/following-sibling::span/text()').extract()

                item['first_available_date'] = ''.join(first_available_date)
            # QA问答数
            qna = response.xpath('//*[@id="askATFLink"]/span/text()').extract()
            item['qna'] = ''.join(qna).strip().split(' ', 1)[0]
            # 首图链接
            first_img = response.xpath(
                '//span[@class="a-list-item"]/span[@class="a-declarative"]/div[@id="imgTagWrapperId"]/img/@src').extract()
            item['first_img'] = ''.join(first_img)
            # 价格标签，区分ourprice和dealprice
            price_tag = response.xpath('//table[@class="a-lineitem"]/tr/td[@class="a-span12"]/span[1]/@id').extract()
            price_type = ''
            if 'ourprice' in ''.join(price_tag):
                price_type = 'ourprice'
            elif 'saleprice' in ''.join(price_tag):
                price_type = 'saleprice'
            elif 'dealprice' in ''.join(price_tag):
                price_type = 'dealprice'
            item['price_type'] = price_type
            # 价格
            price = response.xpath(
                '//*[@id="corePrice_desktop"]/div/table/tr/td[2]/span[@class="a-price a-text-price a-size-medium apexPriceToPay"]/span[1]/text()').extract_first()
            price2 = response.xpath(
                '//*[@id="corePriceDisplay_desktop_feature_div"]/div[@class="a-section a-spacing-none aok-align-center"]//span[@class="a-offscreen"]/text()').extract_first()
            if price:
                item['price'] = price.strip()
            elif price2:
                item['price'] = price2.strip()
            else:
                item['price'] = price2
            # 完整类目
            cats1 = response.xpath('//ul[@class="a-unordered-list a-horizontal a-size-small"]/li/span//text()').extract()
            # cats2 = [''.join(i) for i in cats1]
            cats2 = []
            for cat1 in cats1:
                if len(cat1) > 0:
                    cats2.append(cat1.strip())
                    cats2.append(' ')
            item['total_cat'] = ''.join(cats2)
            # 产品卖点
            descriptions = response.xpath('//div[@id="feature-bullets"]/ul//li[not(@id)]/span//text()').extract()
            description = ''
            for desc in descriptions:
                description = description + '\n' + str(desc).strip()
            item['description'] = description.strip()
            # coupon数据
            coupon = response.xpath('//*[contains(@id,"couponText")]/text()').extract()
            item['coupon'] = ''.join(coupon).strip()
            yield item
            # 评论链接，二级爬取
            # reviews_href = 'https://www.amazon.es/product-reviews/' \
            #                + str(response.meta['asin']) + '/reviewerType=all_reviews'
            # yield scrapy.Request(url=reviews_href, meta={'item': item}, callback=self.parse_reviews_de, dont_filter=True)

    # 日本站点爬取
    def parse_jp(self, response):
        item = AmazonSpiderItem()
        response = response.replace(body=response.text.replace('\x00', ''))
        # 检查邮编
        post_code = response.xpath('//span[@class="nav-line-2 nav-progressive-content"]/text()').extract()
        if len(response.text) < 10000:
            logger.warning("遇到验证码，跳过！" + '\n' + response.meta['url'])
        ##            logger.warning("遇到验证码，返回队列重试！" + '\n' + response.meta['url'])
        ##            yield scrapy.Request(response.meta['url'],
        ##                                 meta={'asin': response.meta['asin'], 'station': response.meta['station'], 'url': response.meta['url']},
        ##                                 callback=self.parse_us, dont_filter=True)
        else:
            if 'Hong Kong' in ''.join(post_code).strip() or 'China' in ''.join(post_code).strip():
                logger.warning("邮编出错！" + '\n' + response.meta['url'])
            # ASIN
            item['asin'] = response.meta['asin']
            # print(item['asin'])
            item['asin_url'] = response.meta['url']
            # 站点
            item['station'] = response.meta['station']
            # 爬取时间
            item['spider_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 标题
            title = response.xpath('//span[@id="productTitle"]/text()').extract()
            item['title'] = ''.join(title).strip()
            # 品牌名字
            brand_info = response.xpath('//a[@id="bylineInfo"]/text()').extract()
            # print(brand_info)
            if 'ストア' in ''.join(brand_info):
                item['brand'] = ''.join(brand_info).split('の', 1)[0]
            elif 'ブランド' in ''.join(brand_info):
                item['brand'] = ''.join(brand_info).split('ブランド', 1)[1].replace(':', '').strip()
            else:
                item['brand'] = 'none'
            # 是否FBA
            dispatch_info = response.xpath(
                '//*[@id="tabular-buybox-truncate-0"]//span[@class="tabular-buybox-text"]//text()'
            ).extract_first()
            sold_info = response.xpath(
                '//*[@id="tabular-buybox-truncate-1"]//span[@class="tabular-buybox-text"]//text()'
            ).extract_first()
            if dispatch_info:
                if 'Amazon' in dispatch_info:
                    if 'Amazon' in sold_info:
                        item['is_fba'] = '自营'
                    else:
                        item['is_fba'] = 'FBA'
                else:
                    item['is_fba'] = '第三方'
            elif title:
                item['is_fba'] = '第三方'
            else:
                item['is_fba'] = ''
            # 评论数
            reviews = response.xpath(
                '//div[@id="averageCustomerReviews"]'
                '//a[@id="acrCustomerReviewLink"]/span[@id="acrCustomerReviewText"]/text()').extract_first()
            if reviews:
                item['reviews'] = reviews.split('個')[0].replace('.', '')
            else:
                item['reviews'] = ''
            # 星级数
            stars = response.xpath(
                '//div[@id="averageCustomerReviews"]//span[@id="acrPopover"]/span/a/i/span/text()').extract_first()
            if stars:
                item['stars'] = stars.strip().split('星のうち', 1)[1]
            else:
                item['stars'] = ''
            # 取大类排名，大类类目，小类排名，小类类目
            if 'a-section table-padding' in response.text:
                # 排名1，样例：#3,238 in Home & Kitchen，以空格分割，取第一个元素并去除#和逗号
                rank1 = response.xpath(
                    '//*[@id="productDetails_detailBullets_sections1"]/tr/td/span/span[1]/text()[1]').extract()
                item['rank1'] = ''.join(rank1).split('位', 1)[0].replace('-', '').replace(',', '').replace(' ', '')
                # 类目1，样例：See Top 100 in Home & Kitchen，取单词in后面的字符串
                cat_1 = response.xpath(
                    '//*[@id="productDetails_detailBullets_sections1"]/tr/td/span/span[1]/a/text()').extract()
                if '見る' in ''.join(cat_1):
                    item['cat1'] = ''.join(cat_1).split('見る')[1]
                else:
                    item['cat1'] = ''.join(cat_1)
                # 排名2，样例：#23
                rank2 = response.xpath(
                    '//*[@id="productDetails_detailBullets_sections1"]/tr/td/span/span[2]/text()').extract()
                item['rank2'] = ''.join(rank2).split('位', 1)[0].replace('-', '').replace(',', '').replace(' ', '')
                # 类目2，样例：Bed Throws
                cat_2 = response.xpath(
                    '//*[@id="productDetails_detailBullets_sections1"]/tr/td/span/span[2]/a/text()').extract()
                item['cat2'] = ''.join(cat_2)
                # 首次上架日期
                first_available_date = response.xpath(
                    '//th[contains(text(),"Amazon.co.jp での取り扱い開始日")]/following-sibling::td/text()').extract()
                item['first_available_date'] = ''.join(first_available_date)
            else:
                rank1 = response.xpath(
                    '//div[@id="detailBulletsWrapper_feature_div"]/ul[1]/li/span//text()[2]').extract()
                item['rank1'] = ''.join(rank1).strip().split('位', 1)[0].replace('-', '').replace(',', '').replace(' ', '')
                cat_1 = response.xpath(
                    '//div[@id="detailBulletsWrapper_feature_div"]/ul[1]/li/span/a/text()').extract()
                if '見る' in ''.join(cat_1):
                    item['cat1'] = ''.join(cat_1).split('見る')[1]
                else:
                    item['cat1'] = ''.join(cat_1)
                rank2 = response.xpath(
                    '//div[@id="detailBulletsWrapper_feature_div"]/ul/li/span/ul/li/span/text()'
                ).extract()
                item['rank2'] = ''.join(rank2).strip().split('位', 1)[0].replace('-', '').replace(',', '').replace(' ', '')
                cat_2 = response.xpath(
                    '//div[@id="detailBulletsWrapper_feature_div"]/ul/li/span/ul/li/span/a/text()').extract()
                item['cat2'] = ''.join(cat_2)
                first_available_date = response.xpath(
                    '//span[contains(text(),"Amazon.co.jp での取り扱い開始日")]/following-sibling::span/text()').extract()

                item['first_available_date'] = ''.join(first_available_date)
            # QA问答数
            qna = response.xpath('//*[@id="askATFLink"]/span/text()').extract()
            item['qna'] = ''.join(qna).strip().split('が', 1)[0]
            # 首图链接
            first_img = response.xpath(
                '//span[@class="a-list-item"]/span[@class="a-declarative"]/div[@id="imgTagWrapperId"]/img/@src').extract()
            item['first_img'] = ''.join(first_img)
            # 价格标签，区分ourprice和dealprice
            price_tag = response.xpath('//table[contains(@class,"a-lineitem a-align-top")]/tr/td[@class="a-span12"]/span[1]/@id').extract()
            price_type = ''
            if 'ourprice' in ''.join(price_tag):
                price_type = 'ourprice'
            elif 'saleprice' in ''.join(price_tag):
                price_type = 'saleprice'
            elif 'dealprice' in ''.join(price_tag):
                price_type = 'dealprice'
            item['price_type'] = price_type
            # 价格
            price = response.xpath(
                '//*[@id="corePrice_desktop"]/div/table/tr/td[2]/span[@class="a-price a-text-price a-size-medium apexPriceToPay"]/span[1]/text()').extract_first()
            price2 = response.xpath(
                '//*[@id="corePriceDisplay_desktop_feature_div"]/div[@class="a-section a-spacing-none aok-align-center"]//span[@class="a-offscreen"]/text()').extract_first()
            if price:
                item['price'] = price.strip()
            elif price2:
                item['price'] = price2.strip()
            else:
                item['price'] = price2
            # 完整类目
            cats1 = response.xpath('//ul[@class="a-unordered-list a-horizontal a-size-small"]/li/span//text()').extract()
            # cats2 = [''.join(i) for i in cats1]
            cats2 = []
            for cat1 in cats1:
                if len(cat1) > 0:
                    cats2.append(cat1.strip())
                    cats2.append(' ')
            item['total_cat'] = ''.join(cats2)
            # 产品卖点
            descriptions = response.xpath('//div[@id="feature-bullets"]/ul//li[not(@id)]/span//text()').extract()
            description = ''
            for desc in descriptions:
                description = description + '\n' + str(desc).strip()
            item['description'] = description.strip()
            # coupon数据
            coupon = response.xpath('//*[contains(@id,"couponText")]/text()').extract()
            item['coupon'] = ''.join(coupon).strip()
            yield item
            # 评论链接，二级爬取
            # reviews_href = 'https://www.amazon.co.jp/product-reviews/' \
            #                + str(response.meta['asin']) + '/reviewerType=all_reviews/?language=ja_JP'
            # yield scrapy.Request(url=reviews_href, meta={'item': item}, callback=self.parse_reviews_jp, dont_filter=True)

    # 加拿大站点爬取
    def parse_ca(self, response):
        item = AmazonSpiderItem()
        response = response.replace(body=response.text.replace('\x00', ''))
        # 检查邮编
        post_code = response.xpath('//span[@class="nav-line-2 nav-progressive-content"]/text()').extract()
        # 检查是否遇到验证码，有验证则返回重试
        # if len(response.text) < 10000:
        #     logger.info("遇到验证码，返回队列重试！" + '\n' + response.meta['url'])
        #     r = response.request.copy()
        #     r.dont_filter = True
        #     ip = random.choice(ipPool)
        #     r.meta['proxy'] = ip
        #     count['count'] += 1
        #     yield r
        if len(response.text) < 10000:
            logger.warning("遇到验证码，跳过！" + '\n' + response.meta['url'])
        ##            logger.warning("遇到验证码，返回队列重试！" + '\n' + response.meta['url'])
        ##            yield scrapy.Request(response.meta['url'],
        ##                                 meta={'asin': response.meta['asin'], 'station': response.meta['station'], 'url': response.meta['url']},
        ##                                 callback=self.parse_us, dont_filter=True)
        else:
            if 'Hong Kong' in ''.join(post_code).strip() or 'China' in ''.join(post_code).strip():
                logger.warning("邮编出错！" + '\n' + response.meta['url'])
            # ASIN
            item['asin'] = response.meta['asin']
            # print(item['asin'])
            item['asin_url'] = response.meta['url']
            # 站点
            item['station'] = response.meta['station']
            # 爬取时间
            item['spider_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 标题
            title = response.xpath('//span[@id="productTitle"]/text()').extract()
            item['title'] = ''.join(title).strip()
            # 品牌名字
            brand_info = response.xpath('//a[@id="bylineInfo"]/text()').extract()
            if 'Store' in ''.join(brand_info):
                item['brand'] = re.findall(r'Visit the (.*) Store', ''.join(brand_info))[0]
            elif 'Brand' in ''.join(brand_info):
                item['brand'] = ''.join(brand_info).split('Brand', 1)[1].replace(':', '').strip()
            else:
                item['brand'] = 'none'
            # 是否FBA
            merchant_infos = response.xpath('//div[@id="merchant-info"]//text()').extract()
            item['is_fba'] = 'none'
            if merchant_infos:
                for merchant_info in merchant_infos:
                    if 'sold by Amazon' in ''.join(merchant_info):
                        item['is_fba'] = '自营'
                        break
                    elif 'Fulfilled by Amazon' in ''.join(merchant_info):
                        item['is_fba'] = 'FBA'
                        break
            else:
                item['is_fba'] = '第三方'
            # 评论数
            reviews = response.xpath(
                '//div[@id="averageCustomerReviews"]'
                '//a[@id="acrCustomerReviewLink"]/span[@id="acrCustomerReviewText"]/text()').extract()
            item['reviews'] = ''.join(reviews).split(' ', 1)[0].replace(',', '')
            # 星级数
            stars = response.xpath(
                '//div[@id="averageCustomerReviews"]//span[@id="acrPopover"]/span/a/i/span/text()').extract()
            item['stars'] = ''.join(stars).strip().split(' ', 1)[0]
            # 取大类排名，大类类目，小类排名，小类类目
            if 'a-section table-padding' in response.text:
                # 排名1，样例：#3,238 in Home & Kitchen，以空格分割，取第一个元素并去除#和逗号
                rank1 = response.xpath(
                    '//*[@id="productDetails_detailBullets_sections1"]/tr/td/span/span[1]/text()[1]').extract()
                item['rank1'] = ''.join(rank1).split(' ', 1)[0].replace('#', '').replace(',', '')
                # 类目1，样例：See Top 100 in Home & Kitchen，取单词in后面的字符串
                cat_1 = response.xpath(
                    '//*[@id="productDetails_detailBullets_sections1"]/tr/td/span/span[1]/a/text()').extract()
                if 'in' in ''.join(cat_1):
                    item['cat1'] = ''.join(cat_1).split('in')[1]
                else:
                    item['cat1'] = ''.join(cat_1)
                # 排名2，样例：#23
                rank2 = response.xpath(
                    '//*[@id="productDetails_detailBullets_sections1"]/tr/td/span/span[2]/text()').extract()
                item['rank2'] = ''.join(rank2).split(' ', 1)[0].replace('#', '').replace(',', '')
                # 类目2，样例：Bed Throws
                cat_2 = response.xpath(
                    '//*[@id="productDetails_detailBullets_sections1"]/tr/td/span/span[2]/a/text()').extract()
                item['cat2'] = ''.join(cat_2)
                # 首次上架日期
                first_available_date = response.xpath(
                    '//th[contains(text(),"Date First Available")]/following-sibling::td/text()').extract()
                item['first_available_date'] = ''.join(first_available_date)
            else:
                rank1 = response.xpath(
                    '//div[@id="detailBulletsWrapper_feature_div"]/ul[1]/li/span//text()[2]').extract()
                item['rank1'] = ''.join(rank1).strip().split(' ', 1)[0].replace('#', '').replace(',', '')
                cat_1 = response.xpath(
                    '//div[@id="detailBulletsWrapper_feature_div"]/ul[1]/li/span/a/text()').extract()
                if 'in' in ''.join(cat_1):
                    item['cat1'] = ''.join(cat_1).split('in')[1]
                else:
                    item['cat1'] = ''.join(cat_1)
                rank2 = response.xpath(
                    '//div[@id="detailBulletsWrapper_feature_div"]/ul/li/span/ul/li/span/text()'
                ).extract()
                item['rank2'] = ''.join(rank2).strip().split(' ', 1)[0].replace('#', '').replace(',', '')
                cat_2 = response.xpath(
                    '//div[@id="detailBulletsWrapper_feature_div"]/ul/li/span/ul/li/span/a/text()').extract()
                item['cat2'] = ''.join(cat_2)
                first_available_date = response.xpath(
                    '//span[contains(text(),"Date First Available")]/following-sibling::span/text()').extract()

                item['first_available_date'] = ''.join(first_available_date)
            # QA问答数
            qna = response.xpath('//*[@id="askATFLink"]/span/text()').extract()
            item['qna'] = ''.join(qna).strip().split(' ', 1)[0]
            # 首图链接
            first_img = response.xpath(
                '//span[@class="a-list-item"]/span[@class="a-declarative"]'
                '/div[@id="imgTagWrapperId"]/img/@src').extract()
            item['first_img'] = ''.join(first_img)
            # 价格标签，区分ourprice和dealprice
            price_tag = response.xpath('//table[contains(@class,"a-lineitem a-align-top")]/'
                                       'tr/td[@class="a-span12"]/span[1]/@id').extract()
            price_type = ''
            if 'ourprice' in ''.join(price_tag):
                price_type = 'ourprice'
            elif 'saleprice' in ''.join(price_tag):
                price_type = 'saleprice'
            elif 'dealprice' in ''.join(price_tag):
                price_type = 'dealprice'
            item['price_type'] = price_type
            # 价格
            price = response.xpath(
                '//*[@id="corePrice_desktop"][1]/div/table/tr/td[2]/span[@class="a-price a-text-price a-size-medium apexPriceToPay"]/span[1]/text()').extract_first()
            price2 = response.xpath(
                '//*[@id="corePriceDisplay_desktop_feature_div"]/div[@class="a-section a-spacing-none aok-align-center"]//span[@class="a-offscreen"]/text()').extract_first()
            if price:
                item['price'] = price.strip()
            elif price2:
                item['price'] = price2.strip()
            else:
                item['price'] = price2
            # 完整类目
            cats1 = response.xpath(
                '//ul[@class="a-unordered-list a-horizontal a-size-small"]/li/span//text()').extract()
            # cats2 = [''.join(i) for i in cats1]
            cats2 = []
            for cat1 in cats1:
                if len(cat1) > 0:
                    cats2.append(cat1.strip())
                    cats2.append(' ')
            item['total_cat'] = ''.join(cats2)
            # 产品卖点
            descriptions = response.xpath('//div[@id="feature-bullets"]/ul//li[not(@id)]/span//text()').extract()
            description = ''
            # print(descriptions)
            for desc in descriptions:
                description = description + '\n' + str(desc).strip()
            item['description'] = description.strip()
            # coupon数据
            coupon = response.xpath('//*[contains(@id,"couponText")]/text()').extract()
            item['coupon'] = ''.join(coupon).strip()
            yield item

    def parse_mx(self, response):
        item = AmazonSpiderItem()
        response = response.replace(body=response.text.replace('\x00', ''))
        # 检查邮编
        post_code = response.xpath('//span[@class="nav-line-2 nav-progressive-content"]/text()').extract()
        if len(response.text) < 10000:
            logger.warning("遇到验证码，跳过！" + '\n' + response.meta['url'])
        ##            logger.warning("遇到验证码，返回队列重试！" + '\n' + response.meta['url'])
        ##            yield scrapy.Request(response.meta['url'],
        ##                                 meta={'asin': response.meta['asin'], 'station': response.meta['station'], 'url': response.meta['url']},
        ##                                 callback=self.parse_us, dont_filter=True)
        else:
            if 'Hong Kong' in ''.join(post_code).strip() or 'China' in ''.join(post_code).strip():
                logger.warning("邮编出错！" + '\n' + response.meta['url'])
            # ASIN
            item['asin'] = response.meta['asin']
            # print(item['asin'])
            item['asin_url'] = response.meta['url']
            # 站点
            item['station'] = response.meta['station']
            # 爬取时间
            item['spider_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 标题
            title = response.xpath('//span[@id="productTitle"]/text()').extract()
            item['title'] = ''.join(title).strip()
            # 品牌名字
            brand_info = response.xpath('//a[@id="bylineInfo"]/text()').extract()
            # print(brand_info)
            if 'Store' in ''.join(brand_info):
                item['brand'] = ''.join(brand_info).split('Visita la Store de ')[1]
            elif 'Marca' in ''.join(brand_info):
                item['brand'] = ''.join(brand_info).split('Marca', 1)[1].replace(':', '').strip()
            else:
                item['brand'] = 'none'
            # 是否FBA
            dispatch_info = response.xpath(
                '//*[@id="tabular-buybox-truncate-0"]//span[@class="tabular-buybox-text"]//text()'
            ).extract_first()
            sold_info = response.xpath(
                '//*[@id="tabular-buybox-truncate-1"]//span[@class="tabular-buybox-text"]//text()'
            ).extract_first()
            if dispatch_info:
                if 'Amazon' in dispatch_info:
                    if 'Amazon' in sold_info:
                        item['is_fba'] = '自营'
                    else:
                        item['is_fba'] = 'FBA'
                else:
                    item['is_fba'] = '第三方'
            elif title:
                item['is_fba'] = '第三方'
            else:
                item['is_fba'] = ''
            # 评论数
            reviews = response.xpath(
                '//div[@id="averageCustomerReviews"]'
                '//a[@id="acrCustomerReviewLink"]/span[@id="acrCustomerReviewText"]/text()').extract()
            item['reviews'] = ''.join(reviews).split(' ', 1)[0].replace('.', '')
            # 星级数
            stars = response.xpath(
                '//div[@id="averageCustomerReviews"]//span[@id="acrPopover"]/span/a/i/span/text()').extract()
            item['stars'] = ''.join(stars).strip().split(' ', 1)[0].replace(',', '.')
            # 取大类排名，大类类目，小类排名，小类类目
            if 'a-section table-padding' in response.text:
                # 排名1，样例：#3,238 in Home & Kitchen，以空格分割，取第一个元素并去除#和逗号
                rank1 = response.xpath(
                    '//*[@id="productDetails_detailBullets_sections1"]/tr/td/span/span[1]/text()[1]').extract()
                item['rank1'] = ''.join(rank1).split(' ', 1)[0].replace('nº', '').replace(',', '')
                # 类目1，样例：See Top 100 in Home & Kitchen，取单词in后面的字符串
                cat_1 = response.xpath(
                    '//*[@id="productDetails_detailBullets_sections1"]/tr/td/span/span[1]/a/text()').extract()
                if 'en' in ''.join(cat_1):
                    item['cat1'] = ''.join(cat_1).split('en')[1]
                else:
                    item['cat1'] = ''.join(cat_1)
                # 排名2，样例：#23
                rank2 = response.xpath(
                    '//*[@id="productDetails_detailBullets_sections1"]/tr/td/span/span[2]/text()').extract()
                item['rank2'] = ''.join(rank2).split(' ', 1)[0].replace('nº', '').replace(',', '')
                # 类目2，样例：Bed Throws
                cat_2 = response.xpath(
                    '//*[@id="productDetails_detailBullets_sections1"]/tr/td/span/span[2]/a/text()').extract()
                item['cat2'] = ''.join(cat_2)
                # 首次上架日期
                first_available_date = response.xpath(
                    '//th[contains(text(),"Producto en Amazon.es desde")]/following-sibling::td/text()').extract()
                item['first_available_date'] = ''.join(first_available_date)
            else:
                rank1 = response.xpath(
                    '//div[@id="detailBulletsWrapper_feature_div"]/ul[1]/li/span//text()[2]').extract()
                item['rank1'] = ''.join(rank1).strip().split(' ', 1)[0].replace('nº', '').replace(',', '')
                cat_1 = response.xpath(
                    '//div[@id="detailBulletsWrapper_feature_div"]/ul[1]/li/span/a/text()').extract()
                if 'en' in ''.join(cat_1):
                    item['cat1'] = ''.join(cat_1).split('en')[1]
                else:
                    item['cat1'] = ''.join(cat_1)
                rank2 = response.xpath(
                    '//div[@id="detailBulletsWrapper_feature_div"]/ul/li/span/ul/li/span/text()'
                ).extract()
                item['rank2'] = ''.join(rank2).strip().split(' ', 1)[0].replace('nº', '').replace(',', '')
                cat_2 = response.xpath(
                    '//div[@id="detailBulletsWrapper_feature_div"]/ul/li/span/ul/li/span/a/text()').extract()
                item['cat2'] = ''.join(cat_2)
                first_available_date = response.xpath(
                    '//span[contains(text(),"Producto en Amazon.es desde")]/following-sibling::span/text()').extract()

                item['first_available_date'] = ''.join(first_available_date)
            # QA问答数
            qna = response.xpath('//*[@id="askATFLink"]/span/text()').extract()
            item['qna'] = ''.join(qna).strip().split(' ', 1)[0]
            # 首图链接
            first_img = response.xpath(
                '//span[@class="a-list-item"]/span[@class="a-declarative"]/div[@id="imgTagWrapperId"]/img/@src').extract()
            item['first_img'] = ''.join(first_img)
            # 价格标签，区分ourprice和dealprice
            price_tag = response.xpath('//table[@class="a-lineitem"]/tr/td[@class="a-span12"]/span[1]/@id').extract()
            price_type = ''
            if 'ourprice' in ''.join(price_tag):
                price_type = 'ourprice'
            elif 'saleprice' in ''.join(price_tag):
                price_type = 'saleprice'
            elif 'dealprice' in ''.join(price_tag):
                price_type = 'dealprice'
            item['price_type'] = price_type
            # 价格
            price = response.xpath(
                '//*[@id="corePrice_desktop"]/div/table/tr/td[2]/span[@class="a-price a-text-price a-size-medium apexPriceToPay"]/span[1]/text()').extract_first()
            price2 = response.xpath(
                '//*[@id="corePriceDisplay_desktop_feature_div"]/div[@class="a-section a-spacing-none aok-align-center"]//span[@class="a-offscreen"]/text()').extract_first()
            if price:
                item['price'] = price.strip()
            elif price2:
                item['price'] = price2.strip()
            else:
                item['price'] = price2
            # 完整类目
            cats1 = response.xpath('//ul[@class="a-unordered-list a-horizontal a-size-small"]/li/span//text()').extract()
            # cats2 = [''.join(i) for i in cats1]
            cats2 = []
            for cat1 in cats1:
                if len(cat1) > 0:
                    cats2.append(cat1.strip())
                    cats2.append(' ')
            item['total_cat'] = ''.join(cats2)
            # 产品卖点
            descriptions = response.xpath('//div[@id="feature-bullets"]/ul//li[not(@id)]/span//text()').extract()
            description = ''
            for desc in descriptions:
                description = description + '\n' + str(desc).strip()
            item['description'] = description.strip()
            # coupon数据
            coupon = response.xpath('//*[contains(@id,"couponText")]/text()').extract()
            item['coupon'] = ''.join(coupon).strip()
            yield item

    # 美国站评论页爬取
    def parse_reviews_us(self, response):
        item = response.meta['item']
        critical_reviews = response.xpath(
            '//div[@id="cm_cr-review_list"]/div[@data-hook="review"]/div/div/div[@class="a-row"]/a/@title').extract()
        crs = 0
        for cr in critical_reviews:
            if float(''.join(cr).strip().split(' ', 1)[0]) <= 3:
                crs += 1
        # print('首页差评数： ' + str(crs))
        item['critical_reviews'] = crs
        # print("评论数已爬取：" + str(item['critical_reviews']))
        yield item

    # 德国站点评论数爬取
    def parse_reviews_de(self, response):
        item = response.meta['item']
        critical_reviews = response.xpath(
            '//div[@id="cm_cr-review_list"]/div[@data-hook="review"]/div/div/div[@class="a-row"]/a/@title').extract()
        crs = 0
        for cr in critical_reviews:
            if float(''.join(cr).strip().replace(',', '.').split(' ', 1)[0]) <= 3:
                crs += 1
        # print('首页差评数： ' + str(crs))
        item['critical_reviews'] = crs
        # print("评论数已爬取：" + str(item['critical_reviews']))
        yield item

    # 日报点评论数爬取
    def parse_reviews_jp(self, response):
        item = response.meta['item']
        critical_reviews = response.xpath(
            '//div[@id="cm_cr-review_list"]/div[@data-hook="review"]/div/div/div[@class="a-row"]'
            '/a/i[@data-hook="review-star-rating"]/span/text()').extract()
        # print(critical_reviews)
        crs = 0
        for cr in critical_reviews:
            if float(''.join(cr).strip().split('星のうち', 1)[1]) <= 3:
                crs += 1
        # print('首页差评数： ' + str(crs))
        item['critical_reviews'] = crs
        # print("评论数已爬取：" + str(item['critical_reviews']))
        yield item
