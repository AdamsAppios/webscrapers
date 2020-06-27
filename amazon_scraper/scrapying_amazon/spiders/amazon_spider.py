# -*- coding: utf-8 -*-
import scrapy
from ..items import ScrapyingAmazonItem


class AmazonSpiderSpider(scrapy.Spider):
    name = 'amazon_spider'
    allowed_domains = ['amazon.com']
    page_number = 2
    start_urls = [
        'https://www.amazon.com/s?k=electronics+books&i=stripbooks-intl-ship&ref=nb_sb_noss_2']

    def parse(self, response):
        items = ScrapyingAmazonItem()
        for slavecss in response.css("span div.s-latency-cf-section"):
            product_name = slavecss.css(
                "a span.a-text-normal").css('::text').extract()
            product_author = slavecss.css(
                "div.sg-row:nth-child(1) div.a-color-secondary>a.a-link-normal").getall()
            product_price = slavecss.css(
                "span span.a-price-whole").get()
            product_imagelink = slavecss.css(
                "div img.s-image::attr(src)").extract()
            # define the fields for your item here like:
            items["product_name"] = product_name
            items["product_author"] = product_author
            items["product_price"] = product_price
            items["product_imagelink"] = product_imagelink
            yield items
        next_page = 'https://www.amazon.com/s?k=electronics+books&i=stripbooks-intl-ship&page={0}&qid=1593248439&ref=sr_pg_2'.format(
            AmazonSpiderSpider.page_number)
        if AmazonSpiderSpider.page_number <= 10:
            AmazonSpiderSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)
