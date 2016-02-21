from hospitals.items import HospitalsItem
from scrapy import Spider, log, Request

class HospitalSpider(Spider):
    name = "hospitals"
    start_urls=["http://www.beckershospitalreview.com/lists/100-great-hospitals-in-america-2015.html"]


    def parse(self,response):
        elements = response.css("#left-column div:nth-child(2) p:not(:first-child)")
        for el in elements:
            selector = el.css("strong::text").extract()
            if len(selector)!=0:
                name = ''.join(selector[:len(selector)-1])
                if len(name)!=0:
                    item = HospitalsItem()
                    item['name']=name
                    yield item
