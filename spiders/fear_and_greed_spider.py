import scrapy
from bs4 import BeautifulSoup

class FearandGreedSpider(scrapy.Spider): # inherit Spider
    name="FearandGreed"

    url='https://edition.cnn.com/markets/fear-and-greed'

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)


    def parse(self,response):
        
        feat_and_greed_gauge =(response.css('[class="market-fng-gauge__dial-number-value"]::text').getall())[0]
        feat_and_greed=response.css('[data-uri="cms.cnn.com/_components/paragraph/instances/market-fng-market-1@published"]::text').getall()[0]
        if feat_and_greed_gauge.strip():
            pass
        else:
            feat_and_greed_gauge="Not Found"
        print("VIA REQUESTS")
        print(f"{feat_and_greed} Index:{feat_and_greed_gauge}")
        

from scrapy import Spider, Request
from scrapy_playwright.page import PageMethod

class PlaywrightFearandGreedSpider(scrapy.Spider): # inherit Spider
    name="PlaywrightFearandGreed"

    url='https://edition.cnn.com/markets/fear-and-greed'

    def start_requests(self):
        #yield scrapy.Request(url=self.url, callback=self.parse)
        yield scrapy.Request(self.url, meta={"playwright": True, "playwright_include_page": True,
                                             "playwright_page_goto_kwargs": {
            "wait_until": "networkidle", # this waits till network is idle
        },
        "playwright_page_methods": [
                PageMethod("screenshot", path="fear-and-greed.png", full_page=True),
                PageMethod("wait_for_selector", 'a[class="market-fng-gauge__text"]'), # wait till gauge text is displayed
                PageMethod("wait_for_selector", '[class="market-fng-gauge__dial-number-value"]'), # wait till gauge value is displayed
            ],
        },callback=self.parse)


    async def parse(self,response):
        
        feat_and_greed_gauge =(response.css('[class="market-fng-gauge__dial-number-value"]::text').getall())[1]
       
        feat_and_greed_gauge_text= response.css('a[class="market-fng-gauge__text"]').getall()[0]

        soup = BeautifulSoup(feat_and_greed_gauge_text, 'html.parser')
        feat_and_greed_gauge_text=soup.a.text

        feat_and_greed=response.css('[data-uri="cms.cnn.com/_components/paragraph/instances/market-fng-market-1@published"]::text').getall()[0]

        if feat_and_greed_gauge.strip():
            pass
        else:
            feat_and_greed_gauge="Not Found"
        print("VIA PLAYWRIGHT")
        print(f"{feat_and_greed} Index:{feat_and_greed_gauge} ==> {feat_and_greed_gauge_text}")
       
 
      



    