import scrapy 

class BabynamesSpider(scrapy.Spider):
    name = "babynames"

    def start_requests(self):
        urls = []
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            urls.append(f'https://hamariweb.com/names/muslim-girl-names-starting-with-{letter}/page-1')
            urls.append(f'https://hamariweb.com/names/muslim-boy-names-starting-with-{letter}/page-1')

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        gender = 'boy' if 'boy' in response.url.split('/')[-2] else 'girl'
        rows = response.xpath("//table[@class='table']/tr[not(@class='tbl_header')]")
        for row in rows:
            yield {
                'name': row.xpath('./td/a/text()').get(),
                'meaning': row.xpath('./td/text()').get(),
                'gender': gender,
                'ethnicity': "muslim"
            }

        next_page = response.xpath("//nav[@class='pagination']/a[contains(text(), 'Next')]/@href").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
