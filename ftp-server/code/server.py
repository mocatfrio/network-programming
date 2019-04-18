import sys
import socket
from threading import Thread

def proses_upload(input) :
    try :
        cmd, src_path, dest_path = input.split(" ")
        f = open(dest_path, "wb")
        data = socket_si_client.recv(512)
        while (data):
           f.write(data)
           data = socket_si_client.recv(512)
        f.close()
        return 1
    except :
        return 0
    finally :
        f.close()

def proses_download(input) :
    try :
        cmd, src_path, dest_path = input.split(" ")
        f = open(src_path, "rb")
        data = f.read(512)
        print data
        while (data):
            socket_si_client.sendall(data)
            data = f.read(512)
        f.close()
        return 1
    except :
        return 0
    finally :
        f.close()

def status_check(hasil) :
    if (hasil == 1):
        print "Transfer successful\r\n"
    elif (hasil == 0):
        print "Transfer failed\r\n"
    else:
        print "Unknown error\r\n"


def handle_client(socket_si_client, client_address):
    print "Koneksi dari %s \r\n" % (str(client_address))
    pesan_dari_client = ""
    while True:
        data = socket_si_client.recv(128)
        if not data:
            print "socket diclose paksa\r\n"
            break
        pesan_dari_client = pesan_dari_client + data
        
        if pesan_dari_client.startswith("UPLOAD"):
            hasil = proses_upload(pesan_dari_client)
            status_check(hasil)
            pesan_dari_client = ''
        elif pesan_dari_client.startswith("DOWNLOAD"):
            hasil = proses_download(pesan_dari_client)
            status_check(hasil)
            pesan_dari_client = ''



# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 14000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)


#Wait for a connection
while True:
	print >>sys.stderr, 'waiting for a connection'
	socket_si_client, client_address = sock.accept()
	print >>sys.stderr, 'connection from', client_address
	client_process = Thread(target=handle_client,args=(socket_si_client,client_address,))
	client_process.start()