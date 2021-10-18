import socket
import threading
from subprocess import Popen, PIPE

from response import HttpResponse
from request import HttpRequest

# WSGI服务器


WEB_ROOT = "./webroot"


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
                  self.__host + ":" + str(self.__port)+"======")
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
        # 1.解析请求
        receiveMsg = self.__connection.recv(self.__bufferSize)
        receiveMsg = receiveMsg.decode("utf-8")
        print(receiveMsg)
        request = HttpRequest()
        request = request.parseRequest(receiveMsg)
        response = HttpResponse()

        # 2.url
        url = request['url']
        # if request['url'] == "/":  # 默认网页
        #     url = WEB_ROOT + '/index.html'
        # else:
        #     url = WEB_ROOT + request['url']

        # 3.method
        responseText = ""
        if request['method'] == "GET":
            if(request['url'] == '/favicon.ico'):
                responseText = response.responseHeader() + "\n" + \
                    response.responseBody(WEB_ROOT+"/404.html")
            try:
                responseText = response.responseHeader() + "\n" + response.responseBody(url)
            except Exception:
                responseText = response.responseHeader() + "\n" + \
                    response.responseBody(WEB_ROOT+"/404.html")
            print(responseText)

        elif request['method'] == "POST":
            if url[0:8] == "/cgi-bin":
                appName = url.split("/")[2]

                argvList = []
                for k in request['params']:
                    argvList.append(request['params'][k])

                cmd = ["python", WEB_ROOT+"/cgi-bin/{}.py".format(appName)]
                for a in argvList:
                    cmd.append(a)

                process = Popen(cmd, stdout=PIPE, stderr=PIPE)

                stdout, stderr = process.communicate()
                print(stdout)
                print(stderr)
            pass
        elif request['method'] == "HEAD":
            pass
        else:
            pass

        # 4.response
        self.__connection.send(responseText.encode("utf-8"))
        self.__connection.close()

    pass
