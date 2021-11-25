from application import WSGIServer

ENABLE_HTTPS = False
if __name__ == '__main__':
    # 创建服务器对象
    wsgiServer = WSGIServer(enable_https=ENABLE_HTTPS, port=14001)

    wsgiServer.startServer()
    pass
