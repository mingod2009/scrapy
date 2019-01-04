# -*- coding: utf-8 -*-
import scrapy
import urlparse
import socket
import datetime

from properties.items import PropertiesItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join


class BasicSpider(scrapy.Spider):
    name = "basic"
    allowed_domains = ["web"]
    #start_urls = (
    #    'http://web:9312/properties/property_000000.html',
    #    'http://web:9312/properties/property_000001.html',
    #)
    start_urls = [i.strip() for i in open('urls.txt').readlines()]

    def parse(self, response):
        '''
            This function parse a property page.
            @url http://web:9312/properties/property_000001.html
            @returns items 1
            @scrapes title price description address image_urls
            @scrapes url project spider server date
        '''
        item = PropertiesItem()
        l = ItemLoader(item=item, response=response)
        l.add_xpath('title','//*[@itemprop="name"][1]/text()', MapCompose(unicode.strip, unicode.title))
        l.add_xpath('price', '//*[@itemprop="price"][1]/text()', MapCompose(lambda i: i.replace(',',''), float) ,re='[,.0-9]+')
        l.add_xpath('description', '//*[@itemprop="description"][1]/text()', MapCompose(unicode.strip), Join())
        l.add_xpath('address', '//*[@itemtype="http://schema.org/Place"][1]/text()', MapCompose(unicode.strip))
        l.add_xpath('image_urls', '//*[@itemprop="image"][1]/@src', MapCompose(lambda i: urlparse.urljoin(response.url, i)))

        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.datetime.now())

        #item['title'] = response.xpath('//*[@itemprop="name"][1]/text()').extract()
        #self.log("title: %s" % response.xpath('//*[@itemprop="name"][1]/text()').extract())

        #item['price'] = response.xpath('//*[@itemprop="price"][1]/text()').extract()
        #self.log("price: %s" % response.xpath('//*[@itemprop="price"][1]/text()').extract())

        #item['description'] = response.xpath('//*[@itemprop="description"][1]/text()').extract()
        #self.log("description: %s" % response.xpath('//*[@itemprop="description"][1]/text()').extract())

        #item['address'] = response.xpath('//*[@itemtype="http://schema.org/Place"][1]/text()').extract()
        #self.log("address: %s" % response.xpath('//*[@itemtype="http://schema.org/Place"][1]/text()').extract())

        #item['image_urls'] = response.xpath('//*[@itemprop="image"][1]/@src').extract()
        #self.log("image_urls: %s" % response.xpath('//*[@itemprop="image"][1]/@src').extract())
        
        return l.load_item()
