import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from embbank.items import Article


class embbankSpider(scrapy.Spider):
    name = 'embbank'
    start_urls = ['https://www.emb.bank/about/bank-news']

    def parse(self, response):
        articles = []
        title_index = len(articles)+1
        num_titles = len(response.xpath('//h3').getall())
        while title_index <= num_titles:
            item = ItemLoader(Article())
            item.default_output_processor = TakeFirst()

            title = response.xpath(f'(//h3)[{title_index}]/text()').get()
            if title:
                title = title.strip()
            while not title and title_index <= num_titles:
                title_index += 1
                title = response.xpath(f'(//h3)[{title_index}]/text()').get()
                if title:
                    title = title.strip()

            content = response.xpath(f'(//div[@data-content="content"])[2]//p[count(preceding-sibling::h3)={title_index}]//text()').getall()
            content = [text for text in content if text.strip() and '{' not in text]
            content = "\n".join(content).strip()
            date = content.split()[0]
            title_index += 1

            item.add_value('title', title)
            item.add_value('date', date)
            item.add_value('content', content)

            yield item.load_item()



