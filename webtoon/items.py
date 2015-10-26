# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from  scrapy import  Item

from  scrapy import  Field

class WebtoonItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #漫画类别
    category=Field()
    #漫画ID
    title_no=Field()
    #漫画详细页面url
    content_url	=Field()
    #漫画图片url
    img_url	=Field()
    #漫画名称
    subj=Field()
    #漫画作者
    author=Field()
    #漫画评价
    grade=Field()
    #漫画热度
    txt_ico_hot=Field()
    #漫画是否完结
    txt_ico_completed=Field()
    #漫画是否更新
    txt_ico_up=Field()
    #漫画详细介绍
    dec=Field()
    #漫画更新时间
    update_time=Field()

    def __getattribute__(self, name):               # 获取属性的方法
        return object.__getattribute__(self, name)

    def __setattr__(self, name, value):
        self.__dict__[name] = value


class DetailWabtoonItem(Item):
    #漫画列表缩略图url
    thmbUrl=Field()
    #剧集主题
    subJ=Field()
    #更新日期
    date=Field()
    #喜爱人数
    like_are= Field()
    #第几集
    tx=Field()
    #漫画内容地址
    contentUrl= Field()
    #漫画id
    title_no=Field()
