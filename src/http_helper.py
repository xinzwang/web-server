import socket
from multiprocessing import Process


class http_helper:
    port = 0

    def __init__(self, port=8888):
        super().__init__()
        self.port = port

    def listen(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("", self.port))
        server_socket.listen(128)  # 最大连接数

        while True:
            client_socket, client_address = server_socket.accept()
            print("conn: [ip:%s, port:%s]" % client_address)

            client_handler_process = Process(
                target=self.client_handler, args=(client_socket,))
            client_handler_process.start()
            client_socket.close()

    def client_handler(self, client_socket):
        request_data = client_socket.recv(1024)
        print("req data:", request_data)

        # 构造响应数据
        response_start_line = "HTTP/1.1 200 OK\r\n"
        response_headers = "Server: My server\r\n"
        response_body = "<h1>Python HTTP Test</h1>"
        response = response_start_line + response_headers + "\r\n" + response_body

        # 向客户端返回响应数据
        client_socket.send(bytes(response, "utf-8"))

        # 关闭客户端连接
        client_socket.close()
