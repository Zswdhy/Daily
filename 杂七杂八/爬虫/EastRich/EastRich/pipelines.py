# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from openpyxl import Workbook


class EastrichPipeline:

    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(["网页地址", "新闻标题", "正文", "发布时间", "文章来源"])

    def process_item(self, item, spider):
        line = [item["news_url"],
                item["news_title"],
                item["content"],
                item["news_time"],
                item["news_source"]
                ]
        self.ws.append(line)
        self.wb.save("eastRich.xlsx")
        return item
