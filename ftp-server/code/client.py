import socket
import sys
import time


# Inisialisasi Create a TCP/IP socket
client_socket  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Koneksi
server_address = ('localhost', 14000)
print >>sys.stderr, 'connecting to %s port %s' % server_address
client_socket.connect(server_address)
client_socket.setblocking(0)

usercmd = raw_input("")
cmd, src_path, dest_path = usercmd.split(" ")
client_socket.send(usercmd)
message = ""
if(cmd=="UPLOAD") :
	try:
		f = open(src_path, "rb")
		message = f.read(512)
		print message
		while (message):
			client_socket.send(message)
			message = f.read(512)
	finally:
		f.close()
		print >> sys.stderr, 'closing socket'
		client_socket.close()

elif(cmd=="DOWNLOAD") :
	try:
		f = open(dest_path, "wb")
		flag = 0
		while True:
			try :
				message = client_socket.recv(512)
				while(message):
					f.write(message)
					flag = 1
					message = client_socket.recv(512)
			except :
				time.sleep(0.5)
				if (len(message) < 512 and flag == 1):
						break
	finally:
		f.close()
		print >> sys.stderr, 'closing socket'
		client_socket.close()