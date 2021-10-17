class HttpRequest():
    # 标头
    def parseRequest(self, requestText):
        request = {}
        array = requestText.split('\r\n')[0].split(' ')

        request['method'] = array[0]
        if(request['method'] == 'POST'):
            params_list = array[1][2:].split('&')
            request['body'] = {
                'params': {}
            }
            for param in params_list:
                param = param.split('=')
                key, value = param[0], param[1]
                request['body']['params'][key] = value
        elif(request['method'] == 'GET'):
            request['url'] = array[1]
            pass
        request['httptype'] = array[2]
        request['cookies'] = {}

        return request
        pass
    pass
