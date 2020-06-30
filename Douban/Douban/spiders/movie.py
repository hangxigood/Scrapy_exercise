import scrapy
from scrapy import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from Douban.items import DoubanItem


class MovieSpider(CrawlSpider):
    name = 'movie'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']
    rules = (
        Rule(LinkExtractor(allow=(r'https://movie.douban.com/top250\?start=\d+.*'))),
        Rule(LinkExtractor(allow=(r'https://movie.douban.com/subject/\d+')), callback='parse_item'),
    )

    def parse_item(self, response):
        sel = Selector(response)
        item = DoubanItem() # 以下爬出的内容中文编码有问题，需要转化
        item['name']=sel.xpath('//*[@id="content"]/h1/span[1]/text()').extract()
        item['year']=sel.xpath('//*[@id="content"]/h1/span[2]/text()').re(r'\((\d+)\)')
        item['score']=sel.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()')
        item['director']=sel.xpath('//*[@id="info"]/span[1]/span[2]/a/text()')
        item['classification']= sel.xpath('//span[@property="v:genre"]/text()')
        item['actor']= sel.xpath('//*[@id="info"]/span[3]/span[2]/text()') # 输出全是 '/'，需要修正
        return item