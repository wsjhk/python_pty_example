# -*- coding:utf-8 -*-

import os
from select import select
from socket import *
import tty
import signal

mode = tty.tcgetattr(0)
tty.setraw(0)
ADDR = ('xxx.xxx.xxx.xxx', 5566)
 
cli = socket(AF_INET, SOCK_STREAM)
 
cli.connect(ADDR)
 
while True:
    if not cli.connect_ex(ADDR):break
    try:
        #将0标准输入注册到select中
        r,w,e = select([0,cli],[],[])
        if cli in r:
            data = cli.recv(1024)
            if data:
                os.write(1,data)
            else:
                pass
        #判断是个标准输入
        if 0 in r:
            cli.send(os.read(0,1024))
    except: 
        tty.tcsetattr(0,tty.TCSAFLUSH,mode)
        raise SystemExit

