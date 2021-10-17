import socket
import threading
from response import HttpResponse
from request import HttpRequest

# WSGI服务器


class WSGIServer():

    def __init__(self, host='localhost', port=8080, connectSize=100):
        '''
        :param port: 服务器的端口号
        :param connectSize: 默认的并发数量
        '''
        self.__host = host
        self.__port = port
        self.__connectSize = connectSize
        pass

    def startServer(self):
        '''
        服务启动主程序
        :return:
        '''
        server = None
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((self.__host, self.__port))
            server.listen(self.__connectSize)
            print("======服务器启动成功：http://" +
                  self.__host + ":" + str(self.__port))
            while True:

                clientConn, clientAddr = server.accept()  # 等待客户端请求
                # 启动独立的线程，处理每一次用户请求
                wt = WorkThread(clientConn, clientAddr)
                wt.start()
                pass
        except socket.gaierror as g:
            print(g)
        finally:
            if server:
                server.close()
        pass

    pass


class WorkThread(threading.Thread):
    def __init__(self, connection, addr, bufferSize=8096):
        threading.Thread.__init__(self)
        self.__connection = connection
        self.__addr = addr
        self.__bufferSize = bufferSize
        pass

    def run(self):
        receiveMsg = self.__connection.recv(self.__bufferSize)
        receiveMsg = receiveMsg.decode("utf-8")
        print(receiveMsg)
        request = HttpRequest()
        request = request.parseRequest(receiveMsg)
        response = HttpResponse()
        url = 'templates/index.html'
        if request['url'] == "/":
            url = 'templates/index.html'
        else:
            url = 'templates' + request['url']

        if(request['url'] != '/favicon.ico'):
            try:
                responseText = response.responseHeader() + "\n" + response.responseBody(url)
            except Exception:
                responseText = response.resopnseError()+'\n'+'404'
            print(responseText)
            self.__connection.send(responseText.encode("utf-8"))
            self.__connection.close()

        pass
    pass
