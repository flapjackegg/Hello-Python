#!/usr/bin/env python3
# encoding: utf-8

import scrapy

class SlyGithub(scrapy.Spider):
    name = "SlyGithub"

    @property
    def start_urls(self):
        url_tmpl = "https://github.com/shiyanlou?page={}&tab=repositories"
        return (url_tmpl.format(i) for i in range(1, 5))

    def parse(self, response):
        for repos in response.xpath('//*[@id="user-repositories-list"]/ul/li'):
            yield {
                'name': repos.xpath('div/h3/a/text()').re_first('\w+'),
                'update_time': repos.xpath('div/relative-time/@datetime').extract_first()
            }