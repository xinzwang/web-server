import time
import socket
import threading
import ssl
import asyncio

from subprocess import Popen, PIPE

from response import HttpResponse
from request import HttpRequest

# WSGI服务器


WEB_ROOT = "./webroot"
LOG_ROOT = "./webroot/log"

connectNum = 0
lock = threading.Lock()


class WSGIServer():

    def __init__(self, host='0.0.0.0', port=14001, connectSize=10, enable_https=False):
        '''
        :param port: 服务器的端口号
        :param connectSize: 默认的并发数量
        '''
        self.__host = host
        self.__port = port
        self.__connectSize = connectSize
        self.enable_https = enable_https
        if enable_https:
            self.load_cert_chain(certfile='./webroot/cert/server.crt',
                                 keyfile='./webroot/cert/server_nopass.key')
        pass

    def load_cert_chain(self, certfile, keyfile):
        '''
        :certfile: 证书公钥
        :keyfile: 证书私钥
        '''
        self.__context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.__context.load_cert_chain(certfile, keyfile)

    async def __server(self):
        global connectNum
        global lock
        '''
        服务的主要实现
        :return:
        '''
        server = None
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((self.__host, self.__port))
            server.listen(self.__connectSize)
            print("======服务器启动成功：https://" +
                  self.__host + ":" + str(self.__port)+"======")

            if self.enable_https:
                with self.__context.wrap_socket(server, server_side=True) as ssl_server:
                    while True:
                        try:
                            if connectNum < self.__connectSize:
                                clientConn, clientAddr = ssl_server.accept()  # 等待客户端请求
                                # 启动独立的线程，处理每一次用户请求
                                wt = WorkCoroutine(clientConn, clientAddr)
                                asyncio.ensure_future(wt.handle())
                                # 交出执行权！！
                                await asyncio.sleep(0)
                                print('handle a client. connect number:',
                                      connectNum)
                            else:
                                clientConn, clientAddr = ssl_server.accept()  # 等待客户端请求
                                # 启动独立的线程，处理每一次用户请求
                                wt = WorkCoroutine(clientConn, clientAddr)
                                asyncio.ensure_future(wt.handle("Full"))
                                # 交出执行权！！
                                await asyncio.sleep(0)
                                print(
                                    'client list full. connect number:', connectNum)
                        except Exception:
                            pass
            else:
                while True:
                    clientConn, clientAddr = server.accept()
                    lock.acquire()
                    connectNum += 1
                    lock.release()
                    if connectNum < self.__connectSize:
                        # 启动独立的线程，处理每一次用户请求
                        wt = WorkCoroutine(clientConn, clientAddr)
                        asyncio.ensure_future(wt.handle())
                        # 交出执行权！！
                        await asyncio.sleep(0)
                        print('handle a client. connect number:', connectNum)
                    else:
                        # 达到最大协程数
                        wt = WorkCoroutine(clientConn, clientAddr)
                        asyncio.ensure_future(wt.handle("Full"))
                        # 交出执行权！！
                        await asyncio.sleep(0)
                        print('client list full. connect number:', connectNum)

        except Exception as e:
            print(str(e.args))
        finally:
            if server:
                server.close()

    def startServer(self):
        '''
        启动异步服务
        :return:
        '''
        asyncio.run(self.__server())


class WorkCoroutine:
    def __init__(self, connection, addr, bufferSize=8096):
        self.__connection = connection
        self.__addr = addr
        self.__bufferSize = bufferSize
        pass

    async def handle(self, msg=""):
        global connectNum
        global lock
        try:
            # 1.解析请求
            receiveMsg = self.__connection.recv(self.__bufferSize)
            receiveMsg = receiveMsg.decode("utf-8")

            self.log(self.__addr, receiveMsg)  # 记录日志
            print(receiveMsg)

            request = HttpRequest()
            request = request.parseRequest(receiveMsg)
            response = HttpResponse(self.__connection)

            # 达到最大协程，直接返回
            if msg == "Full":
                response = HttpResponse(self.__connection)
                response.setCode(404)
                response.setData_From_Url(WEB_ROOT+'/ERROR.html')
                response.response()
                lock.acquire()
                connectNum -= 1
                lock.release()
                return
            if request == {}:
                response.setCode(404)
                response.setData_From_Url(WEB_ROOT+"/404.html")
                response.response()
                lock.acquire()
                connectNum -= 1
                lock.release()
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
        except Exception as e:
            print(str(e.args))

        lock.acquire()
        connectNum -= 1
        lock.release()
        return

    def log(self, addr, data):
        date = time.strftime("%Y-%m-%d")
        path = LOG_ROOT+'/' + date+'.log'

        date = time.strftime("%Y-%m-%d %H:%M:%S")
        d = data.replace('\r\n', ' ')

        lock.acquire()
        s = "[\'" + date + "\'] " + \
            str(addr) + "(connNum:"+str(connectNum)+") " + d+"\n"
        lock.release()

        f = open(path, 'a')
        f.write(s)
        f.close()
