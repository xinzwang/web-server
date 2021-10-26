from application import WSGIServer

if __name__ == '__main__':
    # 创建服务器对象
    wsgiServer = WSGIServer()
    wsgiServer.load_cert_chain( certfile='./webroot/cert/server.crt',
                                keyfile= './webroot/cert/server_nopass.key')
    wsgiServer.startServer()
    pass
