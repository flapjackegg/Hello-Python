# -*- coding: utf-8 -*-
import scrapy
from shiyanlougithub.items import ShiyanlougithubItem


class ReposSpider(scrapy.Spider):
    name = 'repos'
    # allowed_domains = ['https://github.com/shiyanlou']
    start_urls = ['http://https://github.com/shiyanlou/']

    @property
    def start_urls(self):
        url_tmpl = 'https://github.com/shiyanlou?page={}&tab=repositories'
        return (url_tmpl.format(i) for i in range(1, 5))

    def parse(self, response):
        for repo in response.xpath('//*[@id="user-repositories-list"]/ul/li'):
            item = ShiyanlougithubItem()
            item['name'] = repo.xpath('div/h3/a/text()').re_first('\w+')
            item['update_time'] = repo.xpath(
                'div/relative-time/@datetime').extract_first()
            repo_urls = response.urljoin(
                repo.xpath('div/h3/a/@href').extract_first())
            request = scrapy.Request(repo_urls, callback=self.parse_repo_page)
            request.meta['item'] = item
            yield request

    def parse_repo_page(self, response):
        item = response.meta['item']
        item['commits'] = response.xpath(
            '//div[@class="stats-switcher-wrapper"]/ul/li[1]/a/span/text()'
        ).re_first('[^\d]*(\d*)[^\d*]')
        item['branches'] = response.xpath(
            '//div[@class="stats-switcher-wrapper"]/ul/li[2]/a/span/text()'
        ).re_first('[^\d]*(\d*)[^\d*]')
        item['releases'] = response.xpath(
            '//div[@class="stats-switcher-wrapper"]/ul/li[3]/a/span/text()'
        ).re_first('[^\d]*(\d*)[^\d*]')
        yield item
