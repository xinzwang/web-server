
class http_context:
    '''配置'''
    http_version = "HTTP/1.1"

    '''套接字'''
    socket = 0

    '''http请求包'''
    req_method = ""
    req_url = ""
    req_version = ""
    req_head = {}
    req_body = ""

    '''http返回包'''
    rsp_code = 200
    rsp_state = "OK"
    rsp_header = {}
    rsp_body = ""

    def __init__(self, socket):
        super().__init__()
        self.socket = socket

    def parse(self):
        """解析请求"""
        req_str = self.socket.recv(1024).decode()
        head_body = req_str.split("\r\n\r\n")
        head = head_body[0].split("\r\n")

        req_line = head[0].split(" ")

        req_head = {}
        for i in range(len(head)):
            if i == 0:
                continue
            k, v = head[i].split(": ")
            req_head[k] = v

        self.req_method = req_line[0]
        self.req_url = req_line[1]
        self.req_version = req_line[2]
        self.req_head = req_head
        self.req_body = head_body[1]

    def get_url(self):
        return self.req_url

    def get_method(self):
        return self.req_method

    def set(self, code=200, header={}, body=""):
        self.rsp_code = code

        for h in header:
            if h in self.rsp_header:
                self.rsp_header[h] = header[h]
            else:
                self.rsp_header[h] = header[h]

        self.rsp_body = body
        return self

    def response(self):
        start_line = self.http_version + " " + \
            str(self.rsp_code) + " " + "self.rsp_state\r\n"

        headers = ""
        for h in self.rsp_header:
            headers += str(h) + ": " + self.rsp_header[h] + "\r\n"

        rsp = start_line + headers + "\r\n" + self.rsp_body

        self.socket.send(bytes(rsp, "utf-8"))
        self.socket.close()
