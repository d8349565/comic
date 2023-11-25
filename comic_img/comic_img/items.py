# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ComicImgItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    introduction = scrapy.Field()
    chapter_num = scrapy.Field()
    chapter_title = scrapy.Field()
    chapter_url = scrapy.Field()
    pic_num = scrapy.Field()
    pic_url = scrapy.Field()
    comic_cover = scrapy.Field()
