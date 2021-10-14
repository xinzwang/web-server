import os
import socket
from concurrent.futures import ThreadPoolExecutor

from http_server import http_context


class server_helper:
    # 网站配置
    port = 0
    web_path = ""

    # 默认主页
    index_404 = ""

    def __init__(self, port=8888, web_path=""):
        super().__init__()
        self.port = port
        self.web_path = web_path

        f = open(self.web_path+"/404.html", "r",  encoding="utf-8")
        self.index_404 = f.read()
        f.close()

    def listen(self):
        # 创建线程池
        thread_pool = ThreadPoolExecutor(
            max_workers=64, thread_name_prefix="server_")
        # 初始化套接字
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("", self.port))
        server_socket.listen(64)  # 最大连接数

        print("Listen port:", self.port)

        while True:
            client_socket, client_address = server_socket.accept()
            print("conn: [ip:%s, port:%s]" % client_address)

            thread_pool.submit(self.server_handler,
                               client_socket)  # 提交线程池任务

    def server_handler(self, client_socket):
        ctx = http_context(client_socket)

        # 1. 反序列化，解析请求
        ctx.parse()

        # 2. 分析请求类型
        method = ctx.get_method()
        url = ctx.get_url()
        if method == "GET":

        elif method == "POST":

        else:
            ctx.set(404, {}, self.index_404)

        # 3. 路径判断
        if not os.path.isfile(self.web_path + url):    # 路径不存在
            ctx.set(404, {}, self.index_404)

        # 4. 执行操作
        f = open(self.web_path + "/index.html", "r", encoding="utf-8")
        body = f.read()
        f.close()

        # 5. 回包
        ctx.set(200, {}, body).response()
