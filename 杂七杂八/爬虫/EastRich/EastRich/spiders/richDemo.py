import scrapy
import time
from ..items import EastrichItem
# from cryptography import x509


class RichdemoSpider(scrapy.Spider):
    name = 'richDemo'
    allowed_domains = ['finance.eastmoney.com']
    start_urls = ['http://finance.eastmoney.com/a/cgnjj.html']

    # http: // finance.eastmoney.com / a / cgnjj.html
    # http://finance.eastmoney.com/a/cgnjj_2.html
    def __init__(self):
        self.url = "http://finance.eastmoney.com/a/cgnjj.html"
        self.offset = 0

    def parse(self, response):
        all_div = response.xpath('//div[@class="text text-no-img"]')
        for item in all_div:
            news_url = item.xpath('./p[@class="title"]/a/@href').extract()[0]
            yield scrapy.Request(news_url, callback=self.parse_item)
            time.sleep(0.5)
        if self.offset < 10:
            self.offset += 1
            left = "http://finance.eastmoney.com/a/cgnjj_"
            right = ".html"
            self.url = left + str(self.offset) + right
            print(self.url)
            yield scrapy.Request(self.url, callback=self.parse)

    def parse_item(self, response):
        item = EastrichItem()
        url = response.url
        title = response.xpath('//div[@class="newsContent"]/h1/text()').extract()[0]
        time1 = response.xpath('//div[@class="time"]/text()').extract()[0]
        source = response.xpath('//p[@class="em_media"]/text()').extract()[0]
        content = response.xpath('//div[@class="Body"]//p/text()').extract()
        content = "".join(content)
        print("url", url)
        print("title", title)
        print("time1", time1)
        print("source", source)
        print("content", content)
        print("-" * 120)

        item["news_url"] = url
        item["news_title"] = title
        item["news_time"] = time1
        item["news_source"] = source
        item["content"] = content
        yield item
