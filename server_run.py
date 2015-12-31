#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import time,sys,serial,os
import json

from sensor.dht import dht11
from sensor.pm import ttl_pm
from sensor.weather import weather


def remote_cp(Dict):
    fr = './json.data'
    with open(fr, 'w') as f:
        f.write(json.dumps(Dict))
        f.close()
    os.system('scp %s yjiang@10.207.0.184:~/weather/' % fr)
    #print json_data


try:
    pm = ttl_pm('/dev/ttyUSB0', 2400)
    wt = weather()
    dht11 = dht11()
    while True:
        #获取室外天气
        wt_str = wt.get_weather()

        #获取室内温度湿度
        humidity, temperature = dht11.get_dht()

        #获取PM2.5
        vout, dustdensity = pm.show()

        data = {
            'humidity' : humidity,
            'temperature' : temperature,
            'vout' : vout,
            'dustdensity' : dustdensity,
            'weather': wt_str,
            'time' : time.strftime('%Y-%m-%d %H:%M:%S')
        }
        print json.dumps(data)
        remote_cp(data)
        time.sleep(1)

except KeyboardInterrupt:
    ser.close()
