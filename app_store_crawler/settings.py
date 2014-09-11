# -*- coding: utf-8 -*-

# Scrapy settings for app_store_crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'app_store_crawler'

SPIDER_MODULES = ['app_store_crawler.spiders']
NEWSPIDER_MODULE = 'app_store_crawler.spiders'
COOKIES_ENABLED=False
DOWNLOAD_DELAY=0.5

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'app_store_crawler (+http://www.yourdomain.com)'

#USER_AGENT='Mozilla/5.0'
DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
    'app_store_crawler.comm.rotate_useragent.RotateUserAgentMiddleware' :400,
    'app_store_crawler.comm.proxy.RetryChangeProxyMiddleware': 600
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'google_play_crawler (+http://www.yourdomain.com)'

DUPEFILTER_CLASS='app_store_crawler.app_dup_filter.AppURLFilter'

#MEMDEBUG_NOTIFY = ['maxwell.mao@hotmail.com']

