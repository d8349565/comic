# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from comic_img.model import Pic, session_0
class ComicImgPipeline:
    def __init__(self):
        self.session = session_0()
        self.li = []
    def process_item(self, item, spider):
        name = f"{int(item['pic_url'].split('/')[-1].split('.')[0]):03d}.jpg"
        num = f"{item['chapter_num']:03d}"
        Chapter_title = f"{num}_{item['chapter_title'].strip()}"
        pic = Pic(Comic_name=item['name'], target_url=item['pic_url'], Chapter_title=Chapter_title, name=name,
                  Comic_cover=item['comic_cover'], Chapter_url=item['chapter_url'])

        self.li.append(pic)
        # print(len(self.li)%-200)
        if len(self.li)%-500==0:
            # self.session.add_all(self.li)
            self.session.bulk_save_objects(self.li)
            self.session.commit()
            self.li = []

        return item
    def close_spider(self, spider):
        self.session.bulk_save_objects(self.li)
        self.session.commit()  # 提交到数据库
        self.session.close()