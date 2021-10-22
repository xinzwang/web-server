class HttpRequest():
    # 标头
    def parseRequest(self, requestText):
        request = {}

        if requestText == "":
            return request

        # parse http header
        a = requestText.split("\r\n\r\n")
        head = a[0]
        if len(a) > 1:
            body = a[1]
            request['body'] = body

        b = head.split("\r\n")
        request_line = b[0]

        request['head'] = {}
        for i in range(1, len(b)):
            k, v = b[i].split(': ')
            request['head'][k] = v

        c = request_line.split(" ")
        request['method'] = c[0]
        request['version'] = c[2]

        d = c[1].split("?")
        request['url'] = d[0]

        request['params'] = {}
        if len(d) > 1:
            e = d[1].split('&')
            for l in e:
                k, v = l.split('=')
                request['params'][k] = v

        request['cookies'] = {}

        # return
        if request['method'] == 'GET':
            pass
        elif request['method'] == 'POST':
            pass
        else:
            pass

        return request
