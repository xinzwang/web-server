class HttpRequest():
#标头
    def parseRequest(self, requestText):
        params = {}
        array = requestText.split('\r\n')[0].split(' ')

        params['method'] = array[0]
        params['url'] = array[1]
        params['httptype'] = array[2]
        params['cookies'] = {}

        return params
        pass
    pass