# -*- coding: utf-8 -*-
from scrapy import Selector, Request
from scrapy.spiders import CrawlSpider
from webtoon.items import  WebtoonItem, DetailWabtoonItem


class WebtoonSpider(CrawlSpider):
    name="tudou.webtoon"
    #将首页获取到的漫画信息根据ID保存至dict中，进入详细页面获取漫画更新
    # 和介绍信息后根据ID取出对应首页中获取的漫画信息合成完整的漫画信息item
    headPageWebtoonItemDict=dict()
    start_urls=['http://www.webtoons.com/zh-hans/genre']
    def  parse(self, response):
        sel= Selector(response)
        h2_categories=sel.xpath('//div[@class="card_wrap genre"]/h2')
        ul_webtoons=sel.xpath('//div[@class="card_wrap genre"]/ul')
        for index in range(len(h2_categories)):
            # 循环遍历每个分类信息
            category= h2_categories[index]
            li_webtoons=ul_webtoons[index].xpath('li')
            for li_webtoon in  li_webtoons:
                a_webtoon=li_webtoon.xpath('a')

                webtoonItem=WebtoonItem()
                webtoonItem['category']=category.xpath('text()').extract()[0]
                webtoonItem['content_url']=a_webtoon.xpath('attribute::href').extract()[0]
                webtoonItem['title_no']=str(webtoonItem['content_url']).split('=')[-1]
                webtoonItem['img_url']=a_webtoon.xpath('img/attribute::src').extract()[0]
                webtoonItem['subj']=a_webtoon.xpath('div/p[@class="subj"]/text()').extract()[0]
                webtoonItem['author']=a_webtoon.xpath('div/p[@class="author"]/text()').extract()[0]
                grade_area = a_webtoon.xpath('div/p[@class="grade_area"]/em/text()').extract()
                if(grade_area):
                    webtoonItem['grade']=grade_area[0]
                else:
                    webtoonItem['grade']=''
                txt_ico_hot=a_webtoon.xpath('div/p[@class="icon_area"]/span[@class="txt_ico_hot"]/text()').extract()
                txt_ico_up=a_webtoon.xpath('div/p[@class="icon_area"]/span[@class="txt_ico_up"]/text()').extract()
                txt_ico_completed=a_webtoon.xpath('div/p[@class="icon_area"]/span[@class="txt_ico_completed"]/text()').extract()

                if(txt_ico_hot):
                    webtoonItem['txt_ico_hot']=True
                else:
                    webtoonItem['txt_ico_hot']=False

                if(txt_ico_up):
                    webtoonItem['txt_ico_up']=True
                else:
                    webtoonItem['txt_ico_up']=False

                if(txt_ico_completed):
                    webtoonItem['txt_ico_completed'] = True
                else:
                    webtoonItem['txt_ico_completed'] = False

                self.headPageWebtoonItemDict[webtoonItem['title_no']]=webtoonItem
                #进入漫画内容页面爬取信息
                yield  Request(webtoonItem['content_url'],callback=self.pareContentUrl)

    def  pareContentUrl(self, response):
        selector=Selector(response)
        webtoonItem= self.headPageWebtoonItemDict[str(response.url).split('=')[-1]]
        webtoonItem['update_time']=selector.xpath('//p[@class="day_info"]/text()').extract()[0]
        webtoonItem['dec']=selector.xpath('//p[@class="summary"]/text()').extract()[0]

        if(self.name=='tudou.webtoon'):
            yield  self.headPageWebtoonItemDict.pop(str(response.url).split('=')[-1])
        #爬取漫画剧集列表
        else:
            yield  Request(webtoonItem['content_url']+'&page=1', callback=self.pareWebtoonList)

    def  pareWebtoonList(self, response):
        isLastPage=False
        currentPage=int(str(response.url).split('=')[-1])#从url中获取当前爬取的pagenumber
        detailWabtoonItem=DetailWabtoonItem()
        selector=Selector(response)
        webtoons=selector.xpath('//div[@class="detail_lst"]/ul/li')
        for webtoon in  webtoons:
            contentUrl=webtoon.xpath('a/attribute::href').extract()[0]
            title_no= str(response.url).split('&')[0].split('=')[-1]
            thmb = webtoon.xpath('a/span[1]/img/attribute::src').extract()[0]
            subJ = webtoon.xpath('a/span[2]/span/text()').extract()[0]
            date = webtoon.xpath('a/span[4]/text()').extract()[0]
            like_are=webtoon.xpath('a/span[5]/text()').extract()
            tx=webtoon.xpath('a/span[6]/text()').extract()[0][1:]
            if like_are:
                like_are = like_are[0]
            else:
                like_are = ''
            detailWabtoonItem['title_no']=title_no
            detailWabtoonItem['contentUrl']=contentUrl
            detailWabtoonItem['thmbUrl']=thmb
            detailWabtoonItem['date']=date
            detailWabtoonItem['like_are']=like_are
            detailWabtoonItem['subJ']=subJ
            detailWabtoonItem['tx']=tx
            if(int(tx)==1):
                #当漫画标题为第一集表示抓取到最后一页
                isLastPage=True

            yield detailWabtoonItem
        #判断是否将漫画列表所有页全部获取完
        if(isLastPage==False):
            currentPage+=1
            #拼接下一页url
            nextLink=str(response.url).split('&')[0]+'&page='+str(currentPage)
            yield Request(nextLink,callback=self.pareWebtoonList)


    #初始化详细漫画页面爬取所需信息
    def __initDetailWabtoonPage(self):

        self.isLastPage=False # 是否到达最后一页

        self.currentPage=1 # 记录爬取的当前页

        self.begUrl=self.webtoonItem['content_url']+'&page=' #漫画详细列表第一页

    def __margeWebtoonItem(self):
        print("======================================================================")
        for index in  len(self.headPageWebtoonItems):
            webtoonItemFromHeadPage=self.headPageWebtoonItems[index]
            webtoonItemFromDetailPage=self.detailPageWebtoonItems[index]

            webtoonItemFromHeadPage['update_time']=webtoonItemFromDetailPage['update_time']
            webtoonItemFromHeadPage['dec']=webtoonItemFromDetailPage['dec']

            yield  webtoonItemFromHeadPage
