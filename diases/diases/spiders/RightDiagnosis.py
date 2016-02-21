from scrapy import Spider, log, Request
from urlparse import urljoin
from diases.items import DiasesItem

class RightDiagnosisSpider(Spider):
    name = "right-diagnosis-spider"
    start_urls = ["http://www.rightdiagnosis.com/diseasecenter.htm"]

    def parse(self, response):
        elements = response.xpath('//div[@class="list_box"]/div/ol/li[position()>2]')
        for element in elements:
            url = element.xpath("a/@href").extract()[0]
            url = urljoin(response.url, url)
            disease_name = element.xpath("a/text()").extract()[0]
            yield Request(url, callback=self.parse_disease, dont_filter=True, meta={'disease_name':disease_name})

    def parse_disease(self, response):
        disease_name = response.meta['disease_name']
        url = response.xpath('//div[@id="tabmenu"]/ul/li[2]/a/@href').extract()[0]
        symptoms_url = urljoin(response.url, url)
        yield Request(symptoms_url, callback=self.parse_symptoms, dont_filter=True, meta={'disease_name':disease_name})

    def parse_symptoms(self, response):
        item = DiasesItem()
        item['disease_name'] = response.meta['disease_name']
        symptoms = response.xpath('//a[@id="symptom_list"]/following-sibling::ul[1]//li[not(ul) and position()!=last()]/a//text()').extract()
        item['symptoms'] = symptoms
        yield item
