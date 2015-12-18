#!/usr/bin/env bash

#-d 选项是启动一个守护进程
#-m 是分配给Memcache使用的内存数量，单位是MB，默认64MB
#-M return error on memory exhausted (rather than removing items)
#-u 是运行Memcache的用户，如果当前为root 的话，需要使用此参数指定用户
#-l 是监听的服务器IP地址，默认为所有网卡
#-p 是设置Memcache的TCP监听的端口，最好是1024以上的端口
#-c 选项是最大运行的并发连接数，默认是1024
#-P 是设置保存Memcache的pid文件
#-f chunk size growth factor (default: 1.25)
#-I Override the size of each slab page. Adjusts max item size(1.4.2版本新增)

memcached -u root -d
