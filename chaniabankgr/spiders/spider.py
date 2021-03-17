import scrapy

from scrapy.loader import ItemLoader

from ..items import ChaniabankgrItem
from itemloaders.processors import TakeFirst


class ChaniabankgrSpider(scrapy.Spider):
	name = 'chaniabankgr'
	start_urls = ['https://www.chaniabank.gr/']

	def parse(self, response):
		post_links = response.xpath('//a[@class="btn-link"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1[@class="font-weight-bold mb-4"]/text()').get()
		description = response.xpath('//div[@class="font-weight-light"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="font-weight-light h4"]/text()').get()

		item = ItemLoader(item=ChaniabankgrItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
