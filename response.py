class HttpResponse():
    conn = None
    code = 404
    data = ""
    data_type = ""

    def __init__(self, conn):
        self.conn = conn

    def setCode(self, code):
        self.code = code

    def setData(self, data):
        self.data = data

    def setData_From_Url(self, url):
        with open(url, 'rb') as fp:
            body = fp.read()
        self.data = body
        if(url[-4:] == '.jpg'):
            self.data_type = 'image/jpeg'
        elif (url[-4:] == '.png'):
            self.data_type = 'image/png'
        elif (url[-4:] == '.ico'):
            self.data_type = 'image/x-icon'
        elif(url[-4:] == '.css'):
            self.data_type = 'text/css'
        else:
            self.data_type = 'text/html'
        return body

    def response(self):
        header = ""
        if self.code == 200:
            header = "http/1.1 200 OK\r\n" + \
                "Content-Type: {data_type};charset=UTF-8\r\n".format(data_type=self.data_type) + \
                "X-Ua-Compatible: IE=Edge,chrome=1\r\n"
        else:
            header = "http/1.1 404 NOT FOUND\r\n" + \
                "Content-Type: text/html;charset=UTF-8\r\n" + \
                "X-Ua-Compatible: IE=Edge,chrome=1\r\n"
        rsp = (header+"\r\n").encode("utf8") + self.data

        self.conn.send(rsp)
        self.conn.close()
