from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from app_store_crawler.items import AppItem
'''
        https://itunes.apple.com/us/app
'''

class AppStoreSpider(CrawlSpider):
    name='app_store'
    allowed_domains=['itunes.apple.com']
    start_urls=[
        "https://itunes.apple.com/us/app/7-minute-workout/id650762525?mt=8"
#        "https://itunes.apple.com/us/genre/ios/id36?mt=8",
#        "https://itunes.apple.com/gb/genre/ios/id36?mt=8",
#        "https://www.apple.com/itunes/charts/free-apps/",
#        "https://www.apple.com/itunes/charts/paid-apps/",
    ]
    rules = (
        Rule(SgmlLinkExtractor(allow=('/??/app/*', )), callback='parseApp', follow=True),
        )

    def parseApp(self, response):
        print '[Inside app]'
        hxs = HtmlXPathSelector(response)
        item = AppItem()
        item['url']=response.url
        item['name']=hxs.select('//div[@id="title"]/div[1]/h1/text()').extract()
        more_app_by=hxs.select('//div[@class="extra-list more-by"]/ul/li')
#        for li in more_app_by:
        for app_url in hxs.select('//a[@class="artwork-link"]/@href').extract():
            print app_url
            yield Request(app_url, callback=self.parseApp)


