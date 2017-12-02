# -*- coding: utf-8 -*-
import scrapy
from shiyanlougithub.items import ShiyanlougithubItem


class ReposSpider(scrapy.Spider):
    name = 'repos'
    allowed_domains = ['https://github.com/shiyanlou']
    start_urls = ['http://https://github.com/shiyanlou/']

    @property
    def start_urls(self):
        url_tmpl = 'https://github.com/shiyanlou?page={}&tab=repositories'
        return (url_tmpl.format(i) for i in range(1, 5))

    def parse(self, response):
        for repo in response.xpath('//*[@id="user-repositories-list"]/ul/li'):
            item = ShiyanlougithubItem({
                'name':
                repo.xpath(
                    'div/h3/a/text()'
                ).re_first('\w+'),
                'update_time':
                repo.xpath(
                    'div/relative-time/@datetime'
                ).extract_first()
            })
            yield item
