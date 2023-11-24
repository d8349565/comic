import scrapy


class BaoziSpider(scrapy.Spider):
    name = "baozi"
    allowed_domains = ["cn.baozimh.com"]
    start_urls = ["https://cn.webmota.com/comic/yaoshenji-taxuedongman"]

    def start_requests(self):
        headers = {
            'authority': 'cn.baozimh.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            # 'cookie': 'bs0=%5B%7B%22wolaizixukong-heiniaoshe%22%3A0%7D%2C%7B%22yaoshenji-taxuedongman%22%3A0%7D%2C%7B%22wolaiziyouxi-mokf%22%3A0%7D%5D; _ga=amp-Bm-_BHC7IcIbL-d0x_qsjQ; cf_clearance=CKuPk9keQ3gMRZM7c2YpkWL3Y2pdAbaxYXQ1gFnTHBI-1691332803-0-1-319a8775.505a375f.669bd895-250.0.0',
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
            yield scrapy.Request(url, headers=headers, callback=self.parse)

    def parse(self, response):
        print(response)
        node_list1 = response.xpath('//*[@id="chapter-items"]/div')
        node_list2 = response.xpath('//*[@id="chapters_other_list"]/div')
        node_list3 = response.xpath('//*[@id="layout"]/div[2]/div[3]/div/div[4]/div')
        node_list = node_list1 + node_list2 + node_list3
        total = len(node_list1 + node_list2)
        name = response.xpath('//*[@id="layout"]/div[2]/div[1]/div[3]/div/div[2]/div/h1/text()').extract_first()
        cover = response.xpath('/html/body/div/div/div/dsiv[2]/div[1]/div[3]/div/div[1]/amp-img/@src').extract_first()
        print(f'开始爬取《{name}》,总计：{total}')
        for node in node_list:
            url = response.urljoin(node.xpath('./a/@href').extract_first())
            title = node.xpath('./a/div/span/text()').extract_first()
            print(title,url)
            # print(url not in Chapter_urls)

if __name__ == '__main__':
    from scrapy.cmdline import execute

    execute(['scrapy', 'crawl', 'baozi','--nolog'])
    # execute(['scrapy', 'crawl', 'baozi'])
