# -*- coding: UTF-8 -*-
#!/usr/bin/python3

# Scrapy settings for amazon_spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# import random
import datetime


BOT_NAME = 'amazon_spider'

SPIDER_MODULES = ['amazon_spider.spiders']
NEWSPIDER_MODULE = 'amazon_spider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'amazon_spider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs

# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 4
#CONCURRENT_REQUESTS_PER_IP = 16
DOWNLOADER_CLIENT_TLS_CIPHERS = "DEFAULT:!DH"
retry_http_codes = [503]
HTTPERROR_ALLOWED_CODES = [403]
RETRY_ENABLED = True
RETRY_TIMES = 1
DOWNLOAD_TIMEOUT = 300
CONCURRENT_REQUESTS = 24

# 生产环境
# MYSQL_HOST = ''
# MYSQL_DBNAME = ''
# MYSQL_USER = ''
# MYSQL_PASSWORD = ''

# 测试环境
MYSQL_HOST = 'localhost'
MYSQL_DBNAME = 'craw_data'
MYSQL_USER = 'root'
MYSQL_PASSWORD = '12345678'
MYSQL_PORT = 3306

# log设置
LOG_LEVEL = 'DEBUG'
to_day = datetime.datetime.now()
log_file_path = 'log/scrapy_{}_{}_{}.log'.format(to_day.year, to_day.month, to_day.day)
LOG_FILE = log_file_path

# Disable cookies (enabled by default)
COOKIES_ENABLED = False
# dont_merge_cookies = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
##  'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
  'accept-encoding': 'gzip, deflate, br',
  'upgrade-insecure-requests': '1',
}
USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11 ",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
    "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (Kresponse, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 ',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
]
##DEFAULT_REQUEST_HEADERS = {
##    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
##    'Accept-Language': 'zh,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
##    'User-Agent': random.choice(USER_AGENT_LIST),
##    'authority': 'www.amazon.com',
##}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'amazon_spider.middlewares.AmazonSpiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOAD_DELAY = 0.8
RANDOMIZE_DOWNLOAD_DELAY = True
# DOWNLOADER_MIDDLEWARES = {
#    'amazon_spider.middlewares.AmazonSpiderDownloaderMiddleware': 543,
# }


DOWNLOADER_MIDDLEWARES = {
    # 'amazon_spider.middlewares.RandomDelayMiddleware': 999,
    'amazon_spider.middlewares.AmazonSpiderDownloaderMiddleware': 543,
    'amazon_spider.middlewares.fail_retry_middleware': 600,
}


# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'amazon_spider.pipelines.excelPipeline': 300,
    'amazon_spider.pipelines.MysqlasynPipeline': 300,
}
# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


count = {'count': 0}
ipPool = []

proxy_url = 'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=460e34f07cf041899a22e79353081288&orderno=YZ2021112078186AsWJy&returnType=1&count=5'

cookie_us = [
    "session-id=147-6719954-4248045; session-id-time=2082787201l; i18n-prefs=USD; skin=noskin; ubid-main=131-5343993-4790506; session-token=3yq6jlG9N26du5b8MQZkdafmmYvkjBdH2yeBz//II7I8+yfAF+wud6RVGrAT8vYoBpH5cyiKYGcgGOBwgDxc9Dz23g8z7fooFx/9Iw0Pb437X8FKbfIdkBqcNJN37We+x0HpiQ9EGb2dp8siBXvuAGhajW/UCyqKPxk3I5x/pVPttE31ia9nG3ciFZ3hTr2ifPLgHpG6IqtCjNxXEKlUP4YVYSUQmvoTzTDUTH2qsow=; csm-hit=tb:s-B4SCBBSCK59MF9QFXP53|1672816665659&t:1672816665659&adb:adblk_no",
]
cookie_de = [
    "session-id=261-8408151-6254714; session-id-time=2082787201l; i18n-prefs=EUR; ubid-acbde=257-1970195-4510835; lc-acbde=de_DE; session-token=8em64RKE31UcpFI+DY7ZgI8ItZIFiTWBDs9RcGmiznukXd31li4L1mOakSzI6YtaUxDo1dHCoa/Esp6paKfSOoODEkmwzVMAQsLtFyGnRpralRTDEf8LWiplJ38kU6Zn//fC4VHE1JQQq2cH4rJH7o0bap/SGOMnJLLU+mhEqUedJcnbRGSVTP/Jj5gJcnkzLcjCNOEfA24S3YGFUUqLW8hcLB0Rd4bQaHZ0LtawKis=; csm-hit=tb:s-TCQT4WT8J7VGWV7ZHMVF|1672816989795&t:1672816989795&adb:adblk_no",
]
cookie_es = [
    "session-id=258-2839381-2120349; session-id-time=2082787201l; i18n-prefs=EUR; ubid-acbes=261-6759534-5782310; session-token=teV9UMNXfYPwYxOYA3mL2pTdQHbc8JzAhhapp8ZHB77n+hwRPZ3KTPES+yhiuWuY6V+nDF/xazeiIqHueZ1hVzMP4NmCPRaBjK0cCVq2Txr3nYr0f3PR5bGD1zmleqSWki8AZstXcVt+AH4R9pvysp7qZ2ue93MemWAnuPC/gkgHnHI+FmRQH7k0Oj59mMR4QuZW7oSA32l7Hkhq8NelAtgZiopSOY4xBnidY2qt4K8=; csm-hit=tb:s-ZKR51H2A1WMRM41AN480|1672817168157&t:1672817168157&adb:adblk_no",
]
cookie_it = [
    "session-id=259-8594502-3890115; session-id-time=2082787201l; i18n-prefs=EUR; ubid-acbit=262-5537385-0107161; session-token=rnBIN9EV6YQIhMuQy9j45kdaDG8p0LHtmSc5MOcFL1WRYXmD+f6gCqJlQ+/PCb3UHpjlk2E2IiqOZK49JpcbLcps4HLcpyGa/0Uu5/naA+ezuUBq6jLTIup4Q5UxGu4nEr4AVmWdeHLekFO4aI/90bmomBsrIwVIw4HI2gyTsY9TnQ0/rObnRDL/rUNui6Bs6U6cS9hzPFBiLCh8jbf69+bT6khrxbBfnKCmhaOEkds=; csm-hit=tb:s-2PCE5GM622HMA9XYCMGK|1672817348566&t:1672817348567&adb:adblk_no",
]
cookie_fr = [
    "session-id=261-0020452-2915429; session-id-time=2082787201l; i18n-prefs=EUR; ubid-acbfr=261-8869012-8055317; session-token=uif+eAXWfMdxuPoshSSUhXkqg98QVYQW6D1qoQ3BT8CE5j70M+3uCVybTMY4jSPXyWonrfH2gITM7XDMSpZodyNf64koO2dL+gFAE/78Ih6vBX/ROxYfltZbLxET/EBontLRiPaI8c/WzK5ve6dsuu9JPzEQJ2dv2PzxKmhFJRNIKS7NAr0NYhsdi66FQF8zx7265vz6t8OHC8a4pXCjvsjTE5/JttQ7+/gQ7iRlM30=; csm-hit=tb:s-XWNJAT0JGSG22D198J2J|1672817450094&t:1672817450094&adb:adblk_no",
]
cookie_uk = [
    "session-id=259-5626504-7267823; session-id-time=2082787201l; i18n-prefs=GBP; ubid-acbuk=258-3939217-3920232; session-token=y/ptpFerQJKhDE2eKLcb1Zze8Xn1eUZsEu5L6NxgG51qEcbF0uBBGP+6AHRcBexB8/u80J50AAIrb/tAgK0ZN3SIzyxiRGDeJ5GLBWUytidWBnEzuQyGJPyzcr/GHRCHROjwMgMMi45LEbKdEsncZCdv19qHOZM+NEHeQCy2fr6JEuyx2ry7cbfk2GV1uGXiCg94gl8G3pHKfbJTV+PE6QTWbmtrp94e9Zz04iibeU4=; csm-hit=tb:s-FVWK17HRP4YQMVMX3481|1672817550853&t:1672817550853&adb:adblk_no",
]
cookie_jp = [
    "session-id=355-1510070-9181653; i18n-prefs=JPY; skin=noskin; ubid-acbjp=358-2295867-2654851; session-token=Dwu/wQ1M9v9XDSth+6fGagVyHvANztupnxx75y6shIYgUh2fBQZBFwZ3NHi1ihxbZ8KiCQEmKyQ5ETY3Z927iQaPQg5Crrlml0AenBMTMuu36/Ve0TPu2d+eBLD1sE7hHigxFw+kvvDUiwUdMFTPoQZg2oJnzHm5s18F8YbSAH0EouDh5yuS5tG77PJtLrS59//l9z2fC6GiOGhreT7oFIr+WMgsROH2ROuKNHBJd3k=; session-id-time=2082787201l; lc-acbjp=ja_JP; csm-hit=tb:s-CKKP5WZMH3DVNG2Z8SD5|1672817698872&t:1672817699689&adb:adblk_no",
]
cookie_ca = [
    "session-id=135-8254159-5671745; session-id-time=2082787201l; i18n-prefs=CAD; ubid-acbca=135-6657064-2469964; session-token=bMij5IYsUWHuu0XiUBFk5koH+/IA/b4Wt5BJKeISu5dmphSzTgF6uldPJ14Sxjo6KP0NuvMuAgD04vqqezW8pkJQTzxq8b3vFMmdykrL8QhzSoPvGIkeh6rtzmJvkXayhBM+h8cabxkikhwpiPbWTXir7WLmRa+vfnp5tpWgxIwMSugfcNN21BzK99qIGBiZx/jfc3N24DUVZyeKCW4HZz6J3aPrx561fXcnTRfYf3o=; csm-hit=tb:EG2HPRXEF4RQ8QQ2S288+s-84B8QYSZ046P8FVK0DBZ|1675235227446&t:1675235227446&adb:adblk_yes",
]
cookie_mx = [
    "session-id=146-6540191-2985150; session-id-time=2082787201l; i18n-prefs=MXN; ubid-acbmx=132-8256847-5754533; session-token=l6D3/VNgbnRnq/bNZ1aJYffmlXcA7qXdavc/QeIk/mO4k74zfD04HSF6CvIU1i4ZJlLtpKqOkZ1J7RaqKbWn9OOVdCnr29rW9BZfkIEL8Li23NcKm4Eu/Y7ixsy5OJ9uB/p3FYquWjagerz+S1WwRlYisCbgL8UFAFsWmpwMp9/3wkJXptJ3u0KeNDzKNMd9VWQmrSTTOY7z5a/dPenQSsUkrCDNMCaTTbFKkoBkuWI=; csm-hit=tb:JRNJBMK0WVE6946RZ2RP+s-Q3GSA69Y5C7HAQ0G0015|1675235548826&t:1675235548826&adb:adblk_no",
]
