from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from app_store_crawler.items import AppItem
import json
'''
        https://itunes.apple.com/us/app
'''

class AppStoreSpider(CrawlSpider):
    name='app_store'
    allowed_domains=['itunes.apple.com']
    start_urls=[
#        "https://itunes.apple.com/us/app/7-minute-workout/id650762525?mt=8"
#        "https://itunes.apple.com/us/genre/ios/id36?mt=8",
#        "https://itunes.apple.com/gb/genre/ios/id36?mt=8",
#        "https://itunes.apple.com/us/genre/ios-books/id6018?mt=8"
        "http://www.apple.com/choose-your-country/"
#        "https://www.apple.com/itunes/charts/free-apps/",
#        "https://www.apple.com/itunes/charts/paid-apps/",
    ]
#    rules = (
##        Rule(SgmlLinkExtractor(allow=('/??/app/*', )), callback='parseApp', follow=True),
#        Rule(SgmlLinkExtractor(allow=('/us/genre/ios-books/id6018?mt=8')), callback='parseCategory', follow=True),
#        )

    def parse(self, response):
        '''
            choose the country of markets
        '''
        for country in response.xpath('//div[@id="content" and @class="content selfclear"]/div/ul/li/a/@href'):
            c_url='https://itunes.apple.com'+country.extract()+'genre/ios-books/id6018?mt=8'
            print '[Country]', c_url
            yield Request(c_url, callback=self.parseMarket)

    def parseMarket(self, response):
        '''
            parsing the total categories of app store
        '''
        print '[Parse]', response.url
        for category in response.xpath('//div[@id="genre-nav" and @class="nav"]/div/ul/li/a/@href'):
            cateURL=category.extract()
            print cateURL
            yield Request(cateURL, callback=self.parseCategory)

    def parseCategory(self, response):
        '''
            parsing the link to the alphabeta pages of each category
        '''
        print '[Parse Category AlphaBeta]'
        for alphabeta in response.xpath('//ul[@class="list alpha"]/li/a/@href'):
            abURL=alphabeta.extract()
            print abURL
            yield Request(abURL, callback=self.parseCategoryPage)

    def parseCategoryPage(self, response):
        '''
            parsing the link to the pages of each category
        '''
        print '[Parse Category Page]', response.url
        for page in response.xpath('//ul[@class="list paginate"]/li/a/@href')[:-1]:
            pageURL=page.extract()
            print pageURL
            yield Request(pageURL, callback=self.parseCategoryPageApp)

    def parseCategoryPageApp(self, response):
        '''
            parsing the link to the app on each page of each category
        '''
        print '[Parse Category Page App]', response.url
        for app in response.xpath('//div[@id="selectedcontent" and @class="grid3-column"]/div/ul/li/a/@href'):
            appURL=app.extract()
            print appURL
            yield Request(appURL, callback=self.parseApp)

    def parseApp(self, response):
        item = AppItem()
        info={}
        info['url']=item['url']=response.url
        name=response.xpath('//div[@id="title"]/div[1]/h1/text()[1]').extract()
        if name:
            info['name']=item['name']=name[0]
        else:
            info['name']=item['name']=''

#        print 'Name', response.xpath('//div[@id="title"]/div[1]/h1/text()').extract()[0]
        desc=response.xpath('//div[@class="product-review"]/p').extract()
        if desc:
            info['description']=item['description']=desc[0]
        else:
            info['description']=item['description']=''

        l_index=0
        for link in response.xpath('//div[@class="app-links"]/a/@href'):
            if l_index==0:
                info['app_link_first']=item['app_link_first']=link.extract()
            else:
                info['app_link_second']=item['app_link_second']=link.extract()
            l_index+=1

#       item['app_link_first']=response.xpath('//div[@class="app-links"]/a[1]/@href').extract()[0]
#       item['app_link_second']=response.xpath('//div[@class="app-links"]/a[2]/@href').extract()[0]
        cate=response.xpath('//div[@id="left-stack"]/div/ul/li[@class="genre"]/a/text()[1]').extract()
        if cate:
            info['category']=item['category']=cate[0]
        else:
            info['category']=item['category']=''

#        item['update']=
        price=response.xpath('//div[@class="price"]/text()').extract()
        if price:
            info['price']=item['price']=price[0]
        else:
            info['price']=item['price']=''

        size=response.xpath('//div[@id="left-stack"]/div/ul[@class="list"]/li[5]/text()').extract()
        if size:
            info['size']=item['size']=[0]
        else:
            info['size']=item['size']=''

        version=response.xpath('//div[@id="left-stack"]/div/ul[@class="list"]/li[4]/text()').extract()
        if version:
            info['version']=item['version']=version[0]
        else:
            info['version']=item['version']=''
        
        lang=response.xpath('//div[@id="left-stack"]/div/ul[@class="list"]/li[@class="language"]/text()').extract()
        if lang:
            info['lang']=item['lang']=lang[0]
        else:
            info['lang']=item['lang']=''

        seller=item['seller']=response.xpath('//div[@id="left-stack"]/div/ul[@class="list"]/li[7]/text()').extract()
        if seller:
            info['seller']=seller[0]
        else:
            info['seller']=''

        comp=response.xpath('//div[@id="left-stack"]/div/p/text()').extract()
        if comp:
            info['compatibility']=item['compatibility']=comp[0]
        else:
            info['compatibility']=item['compatibility']=''

        release=response.xpath('//div[@id="left-stack"]/div/ul[@class="list"]/li[@class="release-date"]').extract()
        if release:
            info['release_date']=item['release_date']=release[0]
        else:
            info['release_date']=item['release_date']=''

        cur_rate=response.xpath('//div[@class="extra-list customer-ratings"]/div[2]/span[@class="rating-count"]/text()[2]').extract()
        if cur_rate:
            info['current_rating_num']=item['current_rating_num']=cur_rate[0].split()[0]
        else:
            info['current_rating_num']=item['current_rating_num']=0


        rate=0
        for c_x in response.xpath('//div[@class="extra-list customer-ratings"]/div[2]/div/span/@class'):
            c=c_x.extract()
            if c=="rating-star":
                rate+=1
            elif c=="rating-star half":
                rate+=0.5
        info['current_rating']=item['current_rating']=rate

        all_rate=response.xpath('//div[@class="extra-list customer-ratings"]/div[4]/span/text()[2]').extract()
        if all_rate:
            info['all_rating_num']=item['all_rating_num']=all_rate[0].split([0])
        else:
            info['all_rating_num']=item['all_rating_num']=0

        rate=0
        for c in response.xpath('//div[@class="extra-list customer-ratings"]/div[4]/div/span/@class/text()'):
            if c=="rating-star":
                rate+=1
            elif c=="rating-star half":
                rate+=0.5
        info['all_rating']=item['all_rating']=rate
    
        print '[App Details]', json.dumps(info)
#        pass
#        more_app_by=hxs.select('//div[@class="extra-list more-by"]/ul/li')
##        for li in more_app_by:
#        for app_url in hxs.select('//a[@class="artwork-link"]/@href').extract():
#            print app_url
#            yield Request(app_url, callback=self.parseApp)
        for app in response.xpath('//div[@class="lockup small application"]/a[@class="artwork-link"]/@href'):
            yield Request(app.extract(), callback=self.parseApp)


