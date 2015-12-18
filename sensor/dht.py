#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import Adafruit_DHT as dht

class dht11:
    def get_dht(self):
        humidity, temperature = dht.read_retry(dht.DHT11, 4)
        return (humidity, temperature)                  #返回湿度,温度;单位%RH ℃

if __name__ == '__main__':
    dht11 = dht11()
    humidity, temperature = dht11.get_dht()
    print humidity, temperature

