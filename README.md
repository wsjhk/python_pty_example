# python_pty_example

1）pty_server.py和pty.client.py配合使用，只支持单连接，不支持多连接。并且连接后窗口大小固定，不可调，支持vim,top等动态实时命令的使用。对于一般的远程使用已足够，可实现类似SSH远程客户端连接应用开发。

2）pseudo_terminals_in_python.py文件是支持窗口大小调整的，功能更加强大，配合websocket可实现浏览器终端。

3）pty_*和pseudo_terminals_in_python.py都是使用了python的pty模块(pty.py)实现Linux的master-slave虚拟设备对的创建，原理是一样的。

