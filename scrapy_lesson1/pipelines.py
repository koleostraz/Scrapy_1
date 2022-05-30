# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke


class ScrapyLesson1Pipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.books

    def process_item(self, item, spider):
        try:
            item['_id'] = self.process_art(item['art'])
            del item['art']
            if item['old_price'] is not None:
                item['old_price'] = self.process_price(item['old_price'], 1)
            item['cur'], item['new_price'] = self.process_price(item['new_price'])
            item['rating'] = self.process_rating(item['rating'])

            collection = self.mongobase[spider.name]
            try:
                collection.insert_one(item)
            except:
                dke
                print(f'Duplicate key error in {item["url"]}')

            return item
        except:
            print(f'smth wrong in item {item["url"]}')

    def process_art(self, art):
        try:
            art = art.split(sep=': ')
            _id = art[-1]
            return _id
        except:
            print('smth wrong in art')

    def process_price(self, price, mode=0):
        try:
            price = price.replace('\xa0', '')
            price = price.split(sep=' ')
            if mode == 0:
                cur = price[-2]
                price = float(price[1])
                return cur, price
            else:
                price = float(price[1])
                return price
        except:
            cur = None
            price = None
            print('smth wrong in price')
            return cur, price

    def process_rating(self, rating):
        try:
            rating = rating.replace(' ', '')
            rating = rating.replace(',', '.')
            rating = float(rating)
            return rating
        except:
            print('smth wrong in rating')