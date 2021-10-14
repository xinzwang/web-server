from application import WSGIServer

if __name__ == '__main__':
    # 创建服务器对象
    wsgiServer = WSGIServer()
    wsgiServer.startServer()
    pass