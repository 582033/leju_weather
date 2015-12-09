#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import time,sys,serial,os
import Adafruit_DHT as dht
import json
import requests
from bs4 import BeautifulSoup


# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=2400,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout = 1
)

def num_format(num_hex):
    num_int = int(num_hex, 16)
    return float(format(num_int, '.10f'))

def get_vout(hex_str):
    #0005004d52ffaa
    #找到数据开始位aa
    index = hex_str.find('aa')
    #获取Vout_h索引位置
    if index==12:
        Vout_h_index = 0
    else:
        Vout_h_index = index + 2
    #获取Vout_l索引位置
    if Vout_h_index==12:
        Vout_l_index = 0
    else:
        Vout_l_index = Vout_h_index + 2

    #开始计算
    Vout_h = num_format(hex_str [Vout_h_index:Vout_h_index+2])
    Vout_l = num_format(hex_str [Vout_l_index:Vout_l_index+2])

    Vout = ((Vout_h * 256) + Vout_l) / 1024 * 5     #输入电压
    Vout = round(Vout, 3)
    return Vout

def show():
    byteData = ser.read(7)                          # read one, blocking
    byteData += ser.read(ser.inWaiting()).encode('hex')
    line = byteData.encode('hex')

    A = 550                                         #比例系数,由用户自定义
    Vout = get_vout(line)                           #输入电压
    #Vout = ((Vout_h * 256) + Vout_l) / 1024 * 5    #输入电压
    Dustdensity = int(A * Vout)                     #灰尘密度,单位 ug/m3
    return (Vout, Dustdensity)

def get_dht():
    humidity, temperature = dht.read_retry(dht.DHT11, 4)
    return (humidity, temperature)                  #返回湿度,温度;单位%RH ℃


def remote_cp(Dict):
    fr = '/root/json.data'
    with open(fr, 'w') as f:
        f.write(json.dumps(Dict))
        f.close()
    os.system('scp %s yjiang@10.207.0.184:~/weather/' % fr)
    #print json_data

def get_weather():
    url = 'http://beijing.tianqi.com/dongchengqu/'
    content = BeautifulSoup(requests.get(url).content)

    return content.find(class_='fuzhitxt')['value']


try:
    weather = get_weather()
    while True:
        humidity, temperature = get_dht()
        vout, dustdensity = show()
        data = {
            'humidity' : humidity,
            'temperature' : temperature,
            'vout' : vout,
            'dustdensity' : dustdensity,
            'weather': weather
        }
        print json.dumps(data)
        remote_cp(data)
        time.sleep(1)

except KeyboardInterrupt:
    ser.close()
