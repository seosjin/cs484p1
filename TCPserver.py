from socket import *
import os
import time
from time import mktime
from datetime import datetime
from wsgiref.handlers import format_date_time


serverPort = 8080
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

def setHeader(x, f = ""):
    #https://stackoverflow.com/questions/237079/how-to-get-file-creation-modification-date-times-in-python for modified time
    timeMod = "Last-Modified: " + str(format_date_time(mktime(time.localtime(os.path.getmtime(f))))) + "\n"
    #https://stackoverflow.com/questions/225086/rfc-1123-date-representation-in-python for time
    timeNow = "Date: " + str(format_date_time(mktime(datetime.now().timetuple()))) + "\n"

    connection = "Connection: close\n"

    contentType = "Content-Type: "
    ext = f.split('.')[-1]
    if ext == "html":
        contentType += "text/html\n"
        length = "Content-Length: " + str(len(open(f,'r').read()))
    elif ext == "css":
        contentType += "text/css\n"
        length = "Content-Length: " + str(len(open(f,'r').read()))
    else:
        contentType += "image/jpeg\n"
        length = "Content-Length: " + str(len(open(f,'rb').read()))

    status = "HTTP/1.1 "
    if x == 200:
        status += "200 OK\n"
    elif x == 301:
        status += "301 Moved Permanently\n"
    else:
        status += "404 Not Found\n"
        contentType = "Content-Type: text/html\n"
        header = status + timeNow + conenction + contentType + length
        header += str(len(header))
        return header
    
    header = status + timeNow + timeMod + connection + contentType + length

    return header

def validRequest(x, files):
    if x == '/' or x == "test1.html":
        return 1
    if x[1:] == "white.html":
        return 3
    for i in range(0, len(files)):
        if x[1:] in files[i].replace("\\","/"):
            return i
    return -1

while True:
    connectionSocket, addr = serverSocket.accept()
    message = connectionSocket.recv(1024).decode()
    parsed = message.split('\r\n')
    files = []
    for dirpath, dirnames, filenames in os.walk("./proj1files"):
        for filename in [f for f in filenames]:
            files.append(os.path.join(dirpath, filename))

    try:
        iOfFile = validRequest(parsed[0].split(' ')[1], files)
        if iOfFile == -1:
            header = setHeader(404)
            connectionSocket.send((header + "\n\n" + f).encode())
            conenctionSocket.close()
            continue
        if iOfFile == 1 or iOfFile == 3:
            header = setHeader(301,files[iOfFile])
        else:
            header = setHeader(200,files[iOfFile])
        if "jpg" in files[iOfFile] or "jpeg" in files[iOfFile]:
            f = open(files[iOfFile],'rb').read()
            connectionSocket.send((header + "\n\n").encode() + f)
        else:
            f = open(files[iOfFile],'r').read()
            connectionSocket.send((header + "\n\n" + f).encode())
        
    except:
        continue
    connectionSocket.close()





        
