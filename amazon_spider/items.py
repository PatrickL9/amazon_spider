# -*- coding: UTF-8 -*-
#!/usr/bin/python3

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    asin = scrapy.Field()
    asin_url = scrapy.Field()
    title = scrapy.Field()
    reviews = scrapy.Field()
    stars = scrapy.Field()
    rank1 = scrapy.Field()
    cat1 = scrapy.Field()
    rank2 = scrapy.Field()
    cat2 = scrapy.Field()
    first_available_date = scrapy.Field()
    qna = scrapy.Field()
    first_img = scrapy.Field()
    price_type = scrapy.Field()
    price = scrapy.Field()
    total_cat = scrapy.Field()
    critical_reviews = scrapy.Field()
    spider_time = scrapy.Field()
    station = scrapy.Field()
    brand = scrapy.Field()
    is_fba = scrapy.Field()
    description = scrapy.Field()
    coupon = scrapy.Field()
    pass
