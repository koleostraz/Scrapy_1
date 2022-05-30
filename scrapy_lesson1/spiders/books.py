import scrapy
from scrapy.http import HtmlResponse
from scrapy_lesson1.items import ScrapyLesson1Item
from pprint import pprint


class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['book24.ru']
    urls_list = []
    for p in range(24):
        url = f'https://book24.ru/search/page-{p}/?q=%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5'
        urls_list.append(url)
    pprint(urls_list)
    start_urls = urls_list

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[contains(text(),'Вперед')]/@href").extract()
        pprint(next_page)
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[contains(@class, 'product-card__name smartLink')]/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):
        name = response.xpath('//li[contains(@class, "_last-item")]/span/text()').get()
        author = response.xpath('//div[@class="product-characteristic__item"]//span[contains(text(), "Автор:")]/../../div[@class="product-characteristic__value"]//text()').get()
        url = response.url
        try:
            old_price = response.xpath('//span[contains(@class, "product-sidebar-price__price-old")]/text()').get()
        except:
            old_price = None
        new_price = response.xpath('//div[contains(@class, "product-sidebar-price__main-price")]//text()').get()
        art = response.xpath('//p[@class="product-detail-page__article"]/text()').get()
        rating = response.xpath('//span[@class="rating-widget__main-text"]/text()').get()
        yield ScrapyLesson1Item(name=name, author=author, url=url, old_price=old_price,
                                new_price=new_price, art=art, rating=rating)
