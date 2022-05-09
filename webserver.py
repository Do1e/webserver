import sys
from socket import *
from threading import Thread
from time import time, localtime, strftime
import os
import urllib.parse
from ls_site import lsSite

sitepath = sys.argv[2]          # 网页根目录
cTime = 0                       # 上次修改时间
fp = open(os.path.join(sitepath, "..", "site.log"), "a")

# 线程函数
def serverfun(conn, addr):
    try:
        message = str(conn.recv(10000), "utf-8")
        filename = message.split()[1]
        if(filename[-1] == "/"):  # 访问根目录重定向为index.html
            filename += "index.html"
        global cTime
        if(filename[-10:] == "index.html" and cTime < os.path.getctime(sitepath)):
            cTime = os.path.getctime(sitepath)
            ls = lsSite(sitepath)
            ls.run()
            fp.write(strftime('%Y-%m-%d %H:%M:%S', localtime(time())) + " list file\n")
        filename = sitepath + filename
        filename = urllib.parse.unquote(filename)  # 中文网页支持
        if(os.path.isdir(filename)):
            if(filename[-1] == "/"):
                filename += "index.html"
            else:
                filename += "/index.html"
        fp.write("visit file: " + filename + "\n")
        fp.flush()
        f = open(filename, "rb")
        outputdata = f.readlines()
        # 发送HTML报头
        conn.send("HTTP/1.1 200 OK\r\n".encode("utf-8"))
        conn.send("\r\n".encode("utf-8"))
        # 发送网页内容
        for line in outputdata:
            conn.send(line)
        # 结束
        conn.send("\r\n".encode("utf-8"))
        f.close()
        conn.close()
        fp.write(strftime('%Y-%m-%d %H:%M:%S', localtime(time())) + " disconnect - " + str(addr) + "\n")
        fp.flush()
    except IOError:  # 打开文件失败，发送404错误
        fp.write(strftime('%Y-%m-%d %H:%M:%S', localtime(time())) + " 404 - " + str(addr) + "\n")
        f = open(sitepath + "/404.html", "rb")
        outputdata = f.readlines()
        conn.send("HTTP/1.1 404 Not Found\r\n".encode("utf-8"))
        conn.send("\r\n".encode("utf-8"))
        for line in outputdata:
            conn.send(line)
        conn.send("\r\n".encode("utf-8"))
        f.close()
        conn.close()
        fp.write(strftime('%Y-%m-%d %H:%M:%S', localtime(time())) + " disconnect - " + str(addr) + "\n")
        fp.flush()
    except IndexError:
        fp.write(strftime('%Y-%m-%d %H:%M:%S', localtime(time())) + " indexError - " + str(message) + "\n")

if __name__ == "__main__":
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # 停止之后不占用端口，可以立即重用
    serverSocket.bind(('', int(sys.argv[1])))             # 监听端口(注：HTTP默认端口为80)
    serverSocket.listen(10)         # 最大连接数10
    fp.write(strftime('%Y-%m-%d %H:%M:%S', localtime(time())) + " server start" + "\n")
    fp.flush()
    while True:
        try:
            connectionSocket, addr = serverSocket.accept()
            fp.write(strftime('%Y-%m-%d %H:%M:%S', localtime(time())) + " connect - " + str(addr) + "\n")
            fp.flush()
            t = Thread(target=serverfun, args=(connectionSocket, addr))
            t.start()    # 有新的连接时创建一个新的线程
        except KeyboardInterrupt:   # 捕获Ctrl+C，关闭服务器
            fp.write(strftime('%Y-%m-%d %H:%M:%S', localtime(time())) + " server close" + "\n\n")
            fp.flush()
            serverSocket.close()
            fp.close()