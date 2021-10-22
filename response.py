class HttpResponse():
    conn = None
    code = 404
    data = ""

    def __init__(self, conn):
        self.conn = conn

    def setCode(self, code):
        self.code = code

    def setData(self, data):
        self.data = data

    def setData_From_Url(self, url):
        with open(url, 'r', encoding="utf-8") as fp:
            body = fp.read()
        self.data = body
        return body

    def response(self):
        header = ""
        if self.code == 200:
            header = "http/1.1 200 OK\r\n" + \
                "Content-Type: text/html\r\n" + \
                "X-Ua-Compatible: IE=Edge,chrome=1\r\n"
        else:
            header = "http/1.1 404 NOT FOUND\r\n" + \
                "Content-Type: text/html\r\n" + \
                "X-Ua-Compatible: IE=Edge,chrome=1\r\n"

        rsp = header + "\n" + str(self.data)

        self.conn.send(rsp.encode("utf-8"))
        self.conn.close()
