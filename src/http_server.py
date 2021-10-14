

class http_req:
    method = ""
    url = ""
    version = ""
    head = {}
    body = ""

    def __init__(self, req_str):
        super().__init__()

        head_body = req_str.split("\r\n\r\n")
        head = head_body[0].split("\r\n")

        req_line = head[0].split(" ")

        req_head = {}
        for i in range(len(head)):
            if i == 0:
                continue
            k, v = head[i].split(": ")

            req_head[k] = v

        self.method = req_line[0]
        self.url = req_line[1]
        self.version = req_line[2]
        self.head = req_head
        self.body = head_body[1]

    def get_url(self):
        return self.url


class http_rsp:
    start_line = "HTTP/1.1 200 OK\r\n"
    headers = "Server: My server\r\n"

    def __init__(self, code=200):
        if code == 200:
            self.start_line = "HTTP/1.1 200 OK\r\n"
        elif code == 400:
            self.start_line = "HTTP/1.1 400 OK\r\n"
        elif code == 403:
            self.start_line = "HTTP/1.1 403 OK\r\n"
        elif code == 404:
            self.start_line = "HTTP/1.1 404 OK\r\n"
