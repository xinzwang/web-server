import time
import socket
import threading
import ssl
from subprocess import Popen, PIPE

from response import HttpResponse
from request import HttpRequest

# WSGI服务器


WEB_ROOT = "./webroot"
LOG_ROOT = "./webroot/log"


class WSGIServer():

    def __init__(self, host='0.0.0.0', port=443, connectSize=100):
        '''
        :param port: 服务器的端口号
        :param connectSize: 默认的并发数量
        '''
        self.__host = host
        self.__port = port
        self.__connectSize = connectSize
        pass

    def load_cert_chain(self, certfile, keyfile):
        '''
        :certfile: 证书公钥
        :keyfile: 证书私钥
        '''
        self.__context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.__context.load_cert_chain(certfile, keyfile)

    def startServer(self):
        '''
        服务启动主程序
        :return:
        '''
        server = None
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((self.__host, self.__port))
            server.listen(self.__connectSize)

            with self.__context.wrap_socket(server, server_side=True) as ssl_server:
                print("======服务器启动成功：https://" +
                      self.__host + ":" + str(self.__port)+"======")
                while True:
                    try:
                        clientConn, clientAddr = ssl_server.accept()  # 等待客户端请求
                        # 启动独立的线程，处理每一次用户请求
                        wt = WorkThread(clientConn, clientAddr)
                        wt.start()
                    except Exception:
                        pass
        except Exception as e:
            print(str(e.args))
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

        self.log(self.__addr, receiveMsg)  # 记录日志
        print(receiveMsg)

        request = HttpRequest()
        request = request.parseRequest(receiveMsg)
        response = HttpResponse(self.__connection)
        if request == {}:
            response.setCode(404)
            response.setData_From_Url(WEB_ROOT+"/404.html")
            response.response()
            return

        # 2.url
        if(request['url'] == '/'):
            request['url'] = '/index.html'
        elif(request['url'] == '/favicon.ico'):
            request['url'] = '/pic/favicon.ico'
        url = request['url']

        # 3.method
        responseText = ""
        if request['method'] == "GET":
            try:
                response.setCode(200)
                response.setData_From_Url(WEB_ROOT+url)
            except Exception:
                response.setCode(404)
                response.setData_From_Url(WEB_ROOT+"/404.html")
        elif request['method'] == "POST":
            if url[0:8] == "/cgi-bin":
                appName = url.split("/")[2]

                argvList = []
                for k in request['params']:
                    argvList.append(request['params'][k])

                cmd = ["python", WEB_ROOT+"/cgi-bin/{}.py".format(appName)]
                for a in argvList:
                    cmd.append(a)
                cmd.append(request['body'])

                process = Popen(cmd, stdout=PIPE, stderr=PIPE)
                stdout, stderr = process.communicate()
                print(stdout)
                print(stderr)

                response.setCode(200)
                response.setData(stdout)
            else:
                response.setCode(404)
                response.setData_From_Url(WEB_ROOT+"/404.html")
        elif request['method'] == "HEAD":
            pass
        else:
            pass

        # 4.response
        response.response()

    def log(self, addr, data):
        date = time.strftime("%Y-%m-%d")
        path = LOG_ROOT+'/' + date+'.log'

        date = time.strftime("%Y-%m-%d %H:%M:%S")
        d = data.replace('\r\n', ' ')
        s = "[\'" + date + "\'] " + str(addr) + " " + d+"\n"

        f = open(path, 'a')
        f.write(s)
        f.close()
