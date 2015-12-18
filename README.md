基于树莓派及粉尘传感器(GP2Y1051AU0F) 温度湿度传感器(DHT11)的检测装置


###设备列表
    * 树莓派2B
    * 粉尘传感器(GP2Y1051AU0F)
    * 温度湿度传感器(DHT11)


###数据服务端
    - server_run.py
    - json.data

> 获取各项监测数值并把数据写入json.data,通过scp命令复制到WEB服务器端
> 使用memcached每一小时抓取一次weather,防屏蔽


###WEB服务端
    - index.php
    - json.data

> 通过`php -S 0.0.0.0:7777`使用php脚本开启简易HTTP服务,用于访问 index.php 展示数据
> index.php 从`json.data`文件获取数据进行展示
