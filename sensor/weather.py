#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
from werkzeug.contrib.cache import FileSystemCache
import time

class weather():
    def __init__(self):
        self.cache = FileSystemCache('/tmp/leju_weather_cache_dir')
        self.weather_cache_key = 'dongcheng_weather'
        self.aqi_cache_key = 'aqicn_num'
        self.cache_time = 3600

    def get_weather(self):
        weather = self.__cache_get(self.weather_cache_key)
        aqi = self.__cache_get(self.aqi_cache_key)
        return [weather, aqi]


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
            content = BeautifulSoup(requests.get(url, headers=headers, timeout=10).content, "html.parser")
            return content.find(class_='fuzhitxt')['value']
        except requests.exceptions.ConnectTimeout as e:
            #超时信息存入缓存3600秒
            #self.__get_weather()
            return '获取室外数据超时'

    def __get_usa_aqi(self):
        url = 'http://aqicn.org/city/beijing/'
        headers = {
            'Accept-Language' : 'zh-CN,zh;q=0.8',
            'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36',
            'Host' : 'aqicn.org',
            'Cookie' : 'waqi-m-history=[{%22url%22:%22http://aqicn.org/city/beijing/chaoyangaotizhongxin/cn/m/%22%2C%22id%22:%22@450%22%2C%22name%22:%22%E6%9C%9D%E9%98%B3%E5%A5%A5%E4%BD%93%E4%B8%AD%E5%BF%83%22%2C%22time%22:%222016-09-21T02:59:23.642Z%22}%2C{%22url%22:%22http://aqicn.org/city/beijing/us-embassy/cn/m/%22%2C%22id%22:%22@3303%22%2C%22name%22:%22%E5%8C%97%E4%BA%AC%E7%BE%8E%E5%9B%BD%E5%A4%A7%E4%BD%BF%E9%A6%86%22%2C%22time%22:%222016-09-21T02:59:04.177Z%22}]; __uvt=; __atuvc=2%7C42; waqi-w-station={%22url%22:%22http://aqicn.org/city/beijing/%22%2C%22name%22:%22Beijing%22%2C%22idx%22:1451%2C%22time%22:%222016-11-16T02:07:56.247Z%22}; waqi-w-history=[{%22url%22:%22http://aqicn.org/city/beijing/%22%2C%22name%22:%22Beijing%22%2C%22idx%22:1451%2C%22time%22:%222016-11-16T02:07:56.247Z%22}%2C{%22url%22:%22http://aqicn.org/city/beijing/us-embassy/%22%2C%22name%22:%22Beijing%20US%20Embassy%22%2C%22idx%22:3303%2C%22time%22:%222016-11-14T23:39:31.677Z%22}]; __utma=42180789.1319042313.1474426745.1479166782.1479261892.7; __utmb=42180789.2.10.1479261892; __utmc=42180789; __utmz=42180789.1479166782.6.4.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); uvts=5AqenfALEYF052Ho'
        }
        #content = BeautifulSoup(requests.get(url, headers=headers, timeout=(10, 3600)).content)
        try:
            content = BeautifulSoup(requests.get(url, headers=headers, timeout=10).content, "html.parser")
            return "大使馆AQI: %s" % content.select('#aqiwgtvalue')[0].get_text().encode('utf-8')
        except requests.exceptions.ConnectTimeout as e:
            #超时信息存入缓存3600秒
            #self.__get_weather()
            return '获取大使馆AQI数据超时'

    def __cache_get(self, cache_key):
        cache_val = self.cache.get(cache_key)
        if cache_val is None:
            if cache_key == 'dongcheng_weather':
                string = self.__get_weather()
            else:
                string = self.__get_usa_aqi()
            self.cache.set(cache_key, string, self.cache_time)
            return string
        else:
            return cache_val




if __name__ == '__main__':
    wt = weather()
    print wt.get_weather()[0]
