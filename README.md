# 计算机网络课程设计 Web Server

## 一、简要介绍

1. 兼容CGI的多线程静态、动态Web服务框架。

2. 网站的所有资源放在webroot文件夹下

3. 服务器的工作代码是茛目录下的几个.py文件

```
web-server  --源码目录
|
├─ application.py  -- 服务逻辑代码
├─ request.py      -- http请求解析类
├─ response.py     -- http回包类
├─ server.py       -- 主函数
├─ .gitignore
├─ LICENSE
├─ README.md
│      
└─webroot  -- 网站根目录
   ├─ 404.html        -- 默认网页 找不到对应资源
   ├─ ERROR.html      -- 默认网页 出现错误
   ├─ index.html      -- 一个网页
   ├─ calculator.html -- 一个网页
   ├─ query.html      -- 一个网页
   │  
   ├─cgi-bin -- cgi程序
   │   ├─ calculator.py
   │   ├─ query.py
   │   └─ test.py
   │      
   └─log  --日志文件夹
       └─ 2021-10-18.log
```

## 二、使用说明

运行环境：python 3

1. 运行命令：python server.py

2. 使用浏览器访问：[localhost:8888/index.html](localhost:8888/index.html)

## 三、分工

1. http部分框架
2. CGI部分框架
3. 编写动态网页、静态网页
4. 测试、截屏
5. 文档、PPT报告

## 四、 TODO

- [x] 解析POST请求
- [x] 重构HttpRequest
- [x] 发送文件支持（主要指图片文件）
- [ ] 支持ssl
- [ ] 协程异步化