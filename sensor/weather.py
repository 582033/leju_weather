#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import memcache
import time

class weather():
    def __init__(self):
        self.mc = memcache.Client(['127.0.0.1:11211'], debug=True)
        self.cache_key = 'dongcheng_weather'
        self.cacht_time = 3600
        self.indent_timeout = True

    def get_weather(self):
        return self.__cache_get(self.cache_key)


    def __get_weather(self):
        url = 'http://beijing.tianqi.com/dongchengqu/'
        headers = {
            'Accept-Language' : 'zh-CN,zh;q=0.8',
            'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36',
            'Host' : 'beijing.tianqi.com',
            'Cookie' : 'bdshare_firstime=1451003806108; cs_prov=01; cs_city=0101; ccity=101011501; a8205_pages=175; a8205_times=1; Hm_lvt_ab6a683aa97a52202eab5b3a9042a8d2=1451003806; Hm_lpvt_ab6a683aa97a52202eab5b3a9042a8d2=1451004424'
        }
        #content = BeautifulSoup(requests.get(url, headers=headers, timeout=(10, 3600)).content)
        try:
            content = BeautifulSoup(requests.get(url, headers=headers, timeout=10).content)
            self.indent_timeout = False
        except requests.exceptions.ConnectTimeout as e:
            #标识超时,
            self.__get_weather()
            time.sleep(3600)

        return content.find(class_='fuzhitxt')['value']

    def __cache_set(self, weather_str):
        self.mc.set(self.cache_key, weather_str, self.cacht_time)

    def __cache_get(self, key):
        cache_val = self.mc.get(self.cache_key)
        if self.indent_timeout is True:
            return '获取室外数据超时'
        if cache_val is None:
            weather_str = self.__get_weather()
            self.__cache_set(weather_str)
            return weather_str
        else:
            return cache_val




if __name__ == '__main__':
    wt = weather()
    print wt.get_weather()
