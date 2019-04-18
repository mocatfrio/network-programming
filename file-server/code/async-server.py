import asyncore
import socket
import os
import shutil
import sys
import threading


def response_listdir(param):
    param = param.split("/listdir/")
    if(len(param)>1):
        try :
            l = "\n".join(str(x) for x in os.listdir(param[1]))
        except :
            l = "Not found"
    else:
        l = "\n".join(str(x) for x in os.listdir(os.curdir))

    print l
    hasil = "HTTP/1.1 200 OK\r\n" \
            "Content-Type: text/plain\r\n" \
            "Content-Length: "+str(len(l))+"\r\n" \
            "\r\n" \
            + l
    return hasil


def response_download(param):
    url, filename = param.split('=')
    print filename
    file = open(filename, 'rb').read()
    panjang = len(file)
    hasil = "HTTP/1.1 200 OK\r\n" \
            "Content-Type:  multipart/form-data\r\n" \
            "Content-Length: {}\r\n" \
            "\r\n" \
            "{}".format(panjang, file)
    return hasil

def response_delete(param):
    url, filename = param.split('=')
    try:
        os.system('rm ' + filename)
        hasil = "HTTP/1.1 200 OK\r\n" \
            "Content-Type: text/plain\r\n" \
            "Content-Length: 7\r\n" \
            "\r\n" \
            "Deleted"
    except:
        hasil = "HTTP/1.1 200 OK\r\n" \
                "Content-Type: text/plain\r\n" \
                "Content-Length: 13\r\n" \
                "\r\n" \
                "Cannot delete"
    return hasil

def response_deletedir(param):
    url, filename = param.split('=')
    try :
        shutil.rmtree(filename)
        hasil = "HTTP/1.1 200 OK\r\n" \
            "Content-Type: text/plain\r\n" \
            "Content-Length: 7\r\n" \
            "\r\n" \
            "Deleted"
    except :
        hasil = "HTTP/1.1 200 OK\r\n" \
                "Content-Type: text/plain\r\n" \
                "Content-Length: 13\r\n" \
                "\r\n" \
                "Cannot delete"

    return hasil

def response_move(param):
    url, source, dest = param.split('=')
    try:
        os.system('mv ' + source + ' ' + dest)
        hasil = "HTTP/1.1 200 OK\r\n" \
            "Content-Type: text/plain\r\n" \
            "Content-Length: 5\r\n" \
            "\r\n" \
            "Moved"
    except:
        hasil = "HTTP/1.1 200 OK\r\n" \
                "Content-Type: text/plain\r\n" \
                "Content-Length: 11\r\n" \
                "\r\n" \
                "Cannot move"
    return hasil

def response_createdir(param):
    url, dirname = param.split('=')
    try:
        os.system('mkdir ' + dirname)
        hasil = "HTTP/1.1 200 OK\r\n" \
            "Content-Type: text/plain\r\n" \
            "Content-Length: 17\r\n" \
            "\r\n" \
            "directory created"
    except:
        hasil = "HTTP/1.1 200 OK\r\n" \
                "Content-Type: text/plain\r\n" \
                "Content-Length: 23\r\n" \
                "\r\n" \
                "Cannot create directory"
    return hasil

def uploader():
    file = open('page.html', 'r').read()
    panjang = len(file)
    hasil = "HTTP/1.1 200 OK\r\n" \
            "Content-Type: text/html\r\n" \
            "Content-Length: {}\r\n" \
            "\r\n" \
            "{}".format(panjang, file)
    return hasil

class ClientHandler(asyncore.dispatcher):
    def __init__(self, sock):
        asyncore.dispatcher.__init__(self, sock=sock)
        self.request_message = ""
        self.reply_message = ""
        return

    def handle_write(self):
        pass

    def handle_close(self):
        pass
        # fungsi melayani client

    def handle_read(self):
        data = self.recv(64)
        #data = bytes.decode(data)
        self.request_message = self.request_message + data

        if (len(data)<64):
            if self.request_message.startswith("POST") :
                filename = self.request_message.split('filename="')
                filename = filename[1]
                index = filename.find('"')
                filename = filename[:index:]
                f = open(filename, "wb")
                request_message = self.request_message.split("Content-Type: ")
                request_message = request_message[2]
                print request_message[-60::]
                index = request_message.find("\r\n\r\n")
                request_message = request_message[index + 4::]
                request_message = request_message.split("\n\r\n------WebKitForm")
                f.write(request_message[0])
                f.close()

            baris = self.request_message.split("\r\n")
            baris_request = baris[0]
            print baris_request

            a, url, c = baris_request.split(" ")

            if (url.startswith("/download")):
                respon = response_download(url)
            elif (url.startswith("/deletedir")):
                respon = response_deletedir(url)
            elif (url.startswith("/delete")):
                respon = response_delete(url)
            elif (url.startswith("/createdir")):
                respon = response_createdir(url)
            elif (url.startswith("/move")):
                respon = response_move(url)
            elif (url.startswith('/listdir')):
                respon = response_listdir(url)
            elif (url == '/upload'):
                respon = uploader()
            elif (url == '/submit'):
                respon = "HTTP/1.1 200 OK\r\n" \
                         "Content-Type: text/plain\r\n" \
                         "Content-Length: 13\r\n" \
                         "\r\n" \
                         "File uploaded"
            elif (url == '/'):
                respon = "HTTP/1.1 200 OK\r\n" \
                         "Content-Type: text/plain\r\n" \
                         "Content-Length: 19\r\n" \
                         "\r\n" \
                         "Connected to server"
            else:
                respon = "HTTP/1.1 200 OK\r\n" \
                         "Content-Type: text/plain\r\n" \
                         "Content-Length: 9\r\n" \
                         "\r\n" \
                         "Not found"


            self.request_message = ""
            self.send(respon)
            self.close()


class WebServer(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_connect(self):
        pass

    def handle_expt(self):
        self.close()

    def handle_read(self):
        pass

    def handle_write(self):
        pass

    def handle_close(self):
        pass

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            koneksi_client, alamat_client = pair
            print 'Incoming connection from %s' % repr(alamat_client)
            ClientHandler(koneksi_client)
            # koneksi_client.send('haha')
            # koneksi_client.close()
            # s = threading.Thread(target=layani_client, args=(koneksi_client,alamat_client))
            # s.start()


server = WebServer('localhost', 13000)
# asyncore.loop()