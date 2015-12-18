#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import time,sys,serial,os

class ttl_pm:
    def __init__(self, port, baudrate):
        self.ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout = 1
        )

    def __del__(self):
        self.ser.close()

    def num_format(self, num_hex):
        num_int = int(num_hex, 16)
        return float(format(num_int, '.10f'))

    def get_vout(self, hex_str):
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
        Vout_h = self.num_format(hex_str [Vout_h_index:Vout_h_index+2])
        Vout_l = self.num_format(hex_str [Vout_l_index:Vout_l_index+2])

        Vout = ((Vout_h * 256) + Vout_l) / 1024 * 5     #输入电压
        Vout = round(Vout, 3)
        return Vout

    def show(self):
        byteData = self.ser.read(7)                          # read one, blocking
        byteData += self.ser.read(self.ser.inWaiting()).encode('hex')
        line = byteData.encode('hex')

        A = 550                                         #比例系数,由用户自定义
        Vout = self.get_vout(line)                           #输入电压
        #Vout = ((Vout_h * 256) + Vout_l) / 1024 * 5    #输入电压
        Dustdensity = int(A * Vout)                     #灰尘密度,单位 ug/m3
        return (Vout, Dustdensity)

if __name__ == '__main__':
    pm = ttl_pm('/dev/ttyUSB0', 2400)
    vout, dustdensity = pm.show()
    print "%s ug/m3" % dustdensity
