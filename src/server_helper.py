import socket
from concurrent.futures import ThreadPoolExecutor

import http_server


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
        # 1. 接收数据，反序列化
        req_str = client_socket.recv(1024).decode()
        req = http_server.http_req(req_str)

        # 2. 路径分析
        url = req.get_url()
        if not os.path.is_file(self.web_path + url):    # 路径不存在
            http_server.http_rsp()

        # 构造响应数据

        f = open(self.web_path + "/index.html", "r", encoding="utf-8")
        response_body = f.read()
        f.close()

        # response_body = "<h1>Hello</h1>"
        response = response_start_line + response_headers + "\r\n" + response_body

        # 向客户端返回响应数据
        client_socket.send(bytes(response, "utf-8"))

        # 关闭客户端连接
        client_socket.close()
