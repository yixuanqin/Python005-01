

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanmovieItem(scrapy.Item):
    # define the fields for your item here like:
    author = scrapy.Field()
    rate = scrapy.Field()
    content = scrapy.Field()
    date = scrapy.Field()
