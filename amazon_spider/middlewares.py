# -*- coding: UTF-8 -*-
#!/usr/bin/python3

import logging
import random
from scrapy import signals
import requests
import time
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
# from ..usergents import USER_AGENT_LIST
from scrapy.utils.project import get_project_settings
from .settings import ipPool, count, proxy_url, \
    cookie_de, cookie_us, cookie_fr, cookie_es, cookie_it, cookie_jp, cookie_uk, \
    cookie_ca, cookie_mx
from twisted.internet.error import TimeoutError, TCPTimedOutError
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


# class AmazonSpiderSpiderMiddleware:
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the spider middleware does not modify the
#     # passed objects.
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s
#
#     def process_spider_input(self, response, spider):
#         # Called for each response that goes through the spider
#         # middleware and into the spider.
#
#         # Should return None or raise an exception.
#         return None
#
#     def process_spider_output(self, response, result, spider):
#         # Called with the results returned from the Spider, after
#         # it has processed the response.
#
#         # Must return an iterable of Request, or item objects.
#         for i in result:
#             yield i
#
#     def process_spider_exception(self, response, exception, spider):
#         # Called when a spider or process_spider_input() method
#         # (from other spider middleware) raises an exception.
#
#         # Should return either None or an iterable of Request or item objects.
#         pass
#
#     def process_start_requests(self, start_requests, spider):
#         # Called with the start requests of the spider, and works
#         # similarly to the process_spider_output() method, except
#         # that it doesn’t have a response associated.
#
#         # Must return only requests (not items).
#         for r in start_requests:
#             yield r
#
#     def spider_opened(self, spider):
#         spider.logger.info('Spider opened: %s' % spider.name)
#
# class UserAgentDownloadMiddleware(object):
#     """
#     随机使用 User Agent 中间件
#     """
#     def process_request(self, request, spider):
#         """
#         每次请求都会添加一个随机的 UA
#         :param request:
#         :param spider:
#         :return:
#         """
#         settings = get_project_settings()
#         user_agent = random.choice(settings['USER_AGENT_LIST'])
#         request.headers['User-Agent'] = user_agent
#         spider.logger.debug("[User-Agent] ", user_agent)
#
#     def process_response(self, request, response, spider):
#         # if response.status != 200:
#         #     proxy = self.get_random_proxy()
#         #     print("this is response ip:" + proxy)
#         #     # 对当前reque加上代理
#         #     request.meta['proxy'] = proxy
#         #     settings = get_project_settings()
#         #     user_agent = random.choice(settings['USER_AGENT_LIST'])
#         #     request.headers['User-Agent'] = user_agent
#         #     return request
#         return response


class AmazonSpiderDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        """
        每次请求都会添加一个随机的 UA
        :param request:
        :param spider:
        :return:
        """
        settings = get_project_settings()
        user_agent = random.choice(settings['USER_AGENT_LIST'])
        request.headers['User-Agent'] = user_agent
        print("[User-Agent]: {}".format(user_agent))
        spider.logger.debug("[User-Agent]: {}".format(user_agent))
        if '.com/' in request.url:
            request.headers['cookie'] = random.choice(cookie_us)
        elif '.de/' in request.url:
            request.headers['cookie'] = random.choice(cookie_de)
        elif '.es/' in request.url:
            request.headers['cookie'] = random.choice(cookie_es)
        elif '.fr/' in request.url:
            request.headers['cookie'] = random.choice(cookie_fr)
        elif '.it/' in request.url:
            request.headers['cookie'] = random.choice(cookie_it)
        elif '.co.uk/' in request.url:
            request.headers['cookie'] = random.choice(cookie_uk)
        elif '.co.jp/' in request.url:
            request.headers['cookie'] = random.choice(cookie_jp)
        elif '.ca/' in request.url:
            request.headers['cookie'] = random.choice(cookie_ca)
        elif '.mx/' in request.url:
            request.headers['cookie'] = random.choice(cookie_mx)

        if '.co.jp/' not in request.url and 'reviews' not in request.url:
        #and request.meta.get('dont_filter', False):
            # 随机选中一个ip
            ip = random.choice(ipPool)
            spider.logger.debug('更换IP:' + str(ip) + '-----' + str(count['count']))
            print('当前ip', ip, '-----', count['count'])
            # 更换request的ip----------这句是重点
            request.meta['proxy'] = ip
            # 如果循环大于某个值,就清理ip池,更换ip的内容
            if count['count'] > 75:
                spider.logger.debug("-----------重新请求新一批代理IP-----------------")
                count['count'] = 0
                ipPool.clear()
                ips = requests.get(proxy_url)
                for ip in ips.text.split('\r\n'):
                    if len(ip) > 8:
                        ipPool.append('http://' + ip)
            # 每次访问,计数器+1
            count['count'] += 1
        return None

        # return None


    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        # 更换代理
        # if response.status != 200 or len(response.text) < 10000:
        #     proxy = self.get_proxy()
        #     spider.logger.debug("更换IP: {}".format(proxy))
        #     # 对当前reque加上代理
        #     request.meta['proxy'] = 'http://' + proxy
        #     request.meta['dont_filter'] = True
        #     settings = get_project_settings()
        #     user_agent = random.choice(settings['USER_AGENT_LIST'])
        #     request.headers['User-Agent'] = user_agent
        #     return request
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        
        # 针对超时和无响应的reponse,获取新的IP,设置到request中，然后重新发起请求
        if isinstance(exception, TimeoutError) :
            if '.co.jp/' not in request.url and 'reviews' not in request.url:
                # and request.meta.get('dont_filter', False):
                # 随机选中一个ip
                ip = random.choice(ipPool)
                spider.logger.debug('访问超时更换IP:' + str(ip) + '-----' + str(count['count']))
                print('当前ip', ip, '-----', count['count'])
                # 更换request的ip----------这句是重点
                request.meta['proxy'] = ip
                # 如果循环大于某个值,就清理ip池,更换ip的内容
                if count['count'] > 75:
                    spider.logger.debug("-----------重新请求新一批代理IP-----------------")
                    count['count'] = 0
                    ipPool.clear()
                    ips = requests.get(proxy_url)
                    for ip in ips.text.split('\r\n'):
                        if len(ip) > 8:
                            ipPool.append('http://' + ip)
                # 每次访问,计数器+1
                count['count'] += 1
                return request
        elif isinstance(exception, TCPTimedOutError):
            if '.co.jp/' not in request.url and 'reviews' not in request.url:
                # and request.meta.get('dont_filter', False):
                # 随机选中一个ip
                ip = random.choice(ipPool)
                spider.logger.debug('TCP超时更换IP:' + str(ip) + '-----' + str(count['count']))
                print('当前ip', ip, '-----', count['count'])
                # 更换request的ip----------这句是重点
                request.meta['proxy'] = ip
                # 如果循环大于某个值,就清理ip池,更换ip的内容
                if count['count'] > 75:
                    spider.logger.debug("-----------重新请求新一批代理IP-----------------")
                    count['count'] = 0
                    ipPool.clear()
                    ips = requests.get(proxy_url)
                    for ip in ips.text.split('\r\n'):
                        if len(ip) > 8:
                            ipPool.append('http://' + ip)
                # 每次访问,计数器+1
                count['count'] += 1
                return request
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class fail_retry_middleware(RetryMiddleware):
    logger = logging.getLogger(__name__)

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        if response.status in self.retry_http_codes and '.co.jp/' not in request.url:
            reason = response_status_message(response.status)
            # 随机选中一个ip
            ip = random.choice(ipPool)
            spider.logger.debug('异常重试更换IP:' + str(ip) + '-----' + str(count['count']))
            print('当前ip', ip, '-----', count['count'])
            # 更换request的ip----------这句是重点
            request.meta['proxy'] = ip
            # 如果循环大于某个值,就清理ip池,更换ip的内容
            if count['count'] > 10:
                spider.logger.debug("-----------重新请求新一批代理IP-----------------")
                count['count'] = 0
                ipPool.clear()
                ips = requests.get(proxy_url)
                for ip in ips.text.split('\r\n'):
                    if len(ip) > 8:
                        ipPool.append('http://' + ip)
            # 每次访问,计数器+1
            count['count'] += 1
            return self._retry(request,reason, spider) or response
        return response
