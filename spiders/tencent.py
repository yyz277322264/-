# -*- coding: utf-8 -*-
import scrapy
from Tencent.items import TencentItem

class TencentSpider(scrapy.Spider):
    # 爬虫名
    name = 'tencent'
    # 爬虫爬数据的域范围
    allowed_domains = ['tencent.com']
    # 需要拼接的url
    base_url='http://hr.tencent.com/position.php?&start='
    offset=0
    # 爬虫启动时 读取的url列表
    start_urls=[base_url+str(offset)]


    def parse(self, response):
        node_list=response.xpath("//tr[@class='even'] | //tr[@class='odd']")
        item=TencentItem()
        for node in node_list:
            item=TencentItem()
            positionName=node.xpath("./td[1]/a/text()").extract()
            positionLink=node.xpath("./td[1]/a/@href").extract()
            if len(node.xpath("./td[2]/text()")):
                positionType=node.xpath("./td[2]/text()").extract()
                item['positionType']=positionType[0]
            else:
                item['positionType']=''
            positionNumber=node.xpath("./td[3]/text()").extract()
            positionLocation=node.xpath("./td[4]/text()").extract()
            positionTime=node.xpath("./td[5]/text()").extract()
            item['positionName']=positionName[0]
            item['positionLink']=positionLink[0]
            
            item['positionNumber']=positionNumber[0]
            item['positionLocation']=positionLocation[0]
            item['positionTime']=positionTime[0]
            yield item
        # if self.offset<2190:
        #     self.offset+=10
        #     url=self.base_url+str(self.offset)
        #     yield  scrapy.Request(url,callback=self.parse)
        if not len(response.xpath("//a[@class='noactive' and @id='next']")):
            url=response.xpath("//a[@id='next']/@href").extract()[0]
            # //a[@id='next']/@href
            # //a[@class='noactive' and @id='next']
            yield scrapy.Request("http://hr.tencent.com/"+url,callback=self.parse)

# 爬虫总结
# scrapy stratproject xxxx
# scrapy genspider “http://xxxxxx.com
# 编写 item.py 明确需要提取的数据
# 编写spiders/xxx.py 编写爬虫文件 处理请求和响应 以及提取数据yield item
# 编写pipeline.py 编写管道文件 处理spider返回的item数据
# 启动管道组件 以及其他相关设置 setting.py 文件打开管道 禁止协议
# scrapy crawl xxxx 执行爬虫