__author__ = 'Administrator'
from  scrapy import  cmdline
''' make the program run'''
cmdline.execute("scrapy crawl tudou.webtoon.detailpage".split())