"""
cd ./comic/comic_img
scrapy crawl baozi --nolog
"""
import scrapy
import re
from comic_img.items import ComicImgItem

class BaoziSpider(scrapy.Spider):
    name = "baozi"
    ALLOWED_DOMAINS = []
    start_urls = ["https://cn.webmota.com/comic/wolaiziyouxi-mokf_c"]

    def start_requests(self):
        self.headers = {
            'authority': 'cn.baozimh.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
            'referer': 'https://cn.baozimh.com/'
        }
        for url in self.start_urls:
            yield scrapy.Request(url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        node_list1 = response.xpath('//*[@id="chapter-items"]/div')
        node_list2 = response.xpath('//*[@id="chapters_other_list"]/div')
        node_list3 = response.xpath('//*[@id="layout"]/div[2]/div[3]/div/div[4]/div')
        node_list = node_list1 + node_list2 + node_list3
        total = len(node_list1 + node_list2)
        name = response.xpath('//*[@id="layout"]/div[2]/div[1]/div[3]/div/div[2]/div/h1/text()').extract_first()
        cover = response.xpath('/html/body/div/div/div/div[2]/div[1]/div[1]/@style').extract_first()
        cover = re.findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", cover)[0].rstrip("');")
        print(f'开始爬取《{name}》,总计：{total}',cover)
        for node in node_list:
            url = response.urljoin(node.xpath('./a/@href').extract_first())
            title = node.xpath('./a/div/span/text()').extract_first()
            # print(title,url)
            request = scrapy.Request(url=url, callback=self.parse_detail, headers=self.headers,
                                     meta={'name': name, 'cover': cover, 'title': title, 'url': url})
            yield request
            # break

    def parse_detail(self, response):
        node_list = response.xpath('//*[@id="layout"]/div/div[2]/ul/div')
        for num, node in enumerate(node_list):
            if node.xpath('./amp-img/@data-src').extract_first():
                pic_url = node.xpath('./amp-img/@data-src').extract_first()
                item = ComicImgItem()
                item['name'] = response.meta['name']
                item['comic_cover'] = response.meta['cover']
                item['chapter_title'] = response.meta['title']
                item['chapter_url'] = response.meta['url']
                item['chapter_num'] = int(item['chapter_url'].split('=')[-1])
                item['pic_num'] = pic_url.split('/')[-1]
                item['pic_url'] = pic_url
                yield item
        part_url = response.xpath('//*[@id="layout"]/div/div[6]/a/@href').extract_first()
        try:
            p = response.xpath('//*[@id="layout"]/div/div[6]/a/text()').extract_first().strip()
        except AttributeError:
            p = None
        # print(p,part_url)
        if p != '点击进入下一话':
            next_url = response.urljoin(part_url)
            # 构建请求对象，并且返回给引擎
            yield scrapy.Request(
                url=next_url,
                callback=self.parse_detail,
                meta=response.meta
                # dont_filter = True,
                # 如果不能翻页，设置不过滤网站
            )


if __name__ == '__main__':
    from scrapy.cmdline import execute

    execute(['scrapy', 'crawl', 'baozi', '--nolog'])
    # execute(['scrapy', 'crawl', 'baozi'])
