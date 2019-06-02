# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ThomannItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    categorie = scrapy.Field()
    guitar_type = scrapy.Field()
    guitar = scrapy.Field() 
    price = scrapy.Field()
    manufacturer = scrapy.Field()
    author = scrapy.Field()
    review = scrapy.Field()
    stars_gesamt = scrapy.Field()
    stars_features = scrapy.Field()
    stars_sound = scrapy.Field()
    stars_verarbeitung = scrapy.Field()
    key_features = scrapy.Field()

    pass

class ThomannItemShort(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    main_categorie = scrapy.Field()
    sub_categorie = scrapy.Field()
    product = scrapy.Field() 
    price = scrapy.Field()
    manufacturer = scrapy.Field()
    author = scrapy.Field()
    review = scrapy.Field()
    stars_gesamt = scrapy.Field()

    pass
