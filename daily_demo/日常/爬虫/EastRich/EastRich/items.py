# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EastrichItem(scrapy.Item):
    news_title = scrapy.Field()
    news_url = scrapy.Field()
    content = scrapy.Field()
    news_time = scrapy.Field()
    news_source = scrapy.Field()
    # image_address = scrapy.Field()
