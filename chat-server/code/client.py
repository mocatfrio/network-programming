import socket
import select
import sys
from threading import *


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ("localhost", 14000)
client.connect(server_address)


thread_stopped = 0

def receive(client):
    while True:
        message = client.recv(2048)
        if not message:
            print("Disconnected from server\n")
            global thread_stopped
            thread_stopped = 1
            Thread.stop()
        message = message.decode("utf-8")
        try:
            sender, message = message.split("#>")
            print("<"+sender+"> " + message + "\n")
        except:
            print(message)

Thread(target=receive,args=(client,)).start()

while True:
    usercmd = input("")
    if thread_stopped == 1 or usercmd == "#KELUAR#":
        Thread.stop()
        break
    client.sendall(usercmd.encode('utf-8'))
    usercmd = ""


client.close()