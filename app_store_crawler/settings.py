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

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'app_store_crawler (+http://www.yourdomain.com)'
