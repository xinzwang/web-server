class HttpResponse():
    # 请求头
    def responseHeader(self):  # 200情况
        header = "http/1.1 200 OK\r\n" + \
                 "Content-Type: text/html\r\n" + \
                 "X-Ua-Compatible: IE=Edge,chrome=1\r\n"
        return header
        pass

    # 请求头
    def resopnseError(self):  # 404情况
        header = "http/1.1 404 NOT FOUND\r\n" + \
                 "Content-Type: text/html\r\n" + \
                 "X-Ua-Compatible: IE=Edge,chrome=1\r\n"
        return header
        pass

    # 请求体
    def responseBody(self, url):
        body = ""
        with open(url, 'r', encoding="utf-8") as fp:
            body = fp.read()
        return body
        pass
    pass
